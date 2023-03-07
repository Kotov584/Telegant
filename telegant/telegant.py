import asyncio
import json
import re
import aiohttp 

class Telegant:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.message_handlers = {}
        self.command_handlers = {}
        self.callback_handlers = {}
        self.user_state = {}
        self.dialogues = {}

    def add_handler(self, handler_dict, key):
        def decorator(handler):
            handler_dict[key] = handler
            return handler
        return decorator

    def hears(self, pattern):
        return self.add_handler(self.message_handlers, pattern)

    def commands(self, commands_list):
        for command in commands_list:
            self.add_handler(self.command_handlers, command)

    def command(self, command_str):
        return self.add_handler(self.command_handlers, command_str)

    def callbacks(self, callbacks_list):
        for callback in callbacks_list:
            self.add_handler(self.callback_handlers, callback)

    def callback(self, callback_data):
        return self.add_handler(self.callback_handlers, callback_data)

    async def start_polling(self):
        last_update_id = 0
        async with aiohttp.ClientSession() as session:
            while True:
                response_json, last_update_id = await self.get_updates(session, last_update_id)
                if not response_json.get("ok"):
                    print("Error: Response is not OK")
                    continue

                for update in response_json["result"]:
                    await self.handle_update(update)

    async def get_updates(self, session, last_update_id):
        try:
            response = await session.get(f"{self.base_url}getUpdates", params={"offset": last_update_id})
            if response.status != 200:
                print(f"Error: {response.status}")
                return None, last_update_id

            response_json = await response.json()
            for update in response_json["result"]:
                last_update_id = max(last_update_id, update["update_id"] + 1)

            return response_json, last_update_id

        except Exception as e:
            print(f"Error polling for updates: {e}")
            return None, last_update_id

    async def handle_update(self, update):
        if "message" in update:
            await self.handle_message(update)
        elif "callback_query" in update:
            await self.handle_callback_query(update)

    async def handle_message(self, update):
        chat_id = update["message"]["chat"]["id"]
        message_text = update["message"]["text"]

        is_command = False
        if message_text.startswith('/'):
            command, *args = message_text[1:].split()
            handler = self.command_handlers.get(command)
            if handler is not None:
                is_command = True
                await handler(self, update, args)

        if not is_command:
            handled = False
            for pattern, handler in self.message_handlers.items(): 
                if re.fullmatch(pattern, message_text):
                    await handler(self, update)
                    handled = True
                    break

    async def handle_callback_query(self, update):
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        callback_data = update["callback_query"]["data"]
        
        callback_handler = self.callback_handlers.get(callback_data)
        if callback_handler is not None:
            await callback_handler(self, update, update["callback_query"]["message"])

        await self.answer_callback_query(update["callback_query"]["id"])

    async def answer_callback_query(self, callback_query_id):
        async with aiohttp.ClientSession() as session:
            try:
                await session.post(
                    f"{self.base_url}answerCallbackQuery",
                    params={"callback_query_id": callback_query_id}
                )
            except Exception as e:
                print(f"Error answering callback query: {e}")

    async def reply(self, chat_id, text, buttons=None):
        async with aiohttp.ClientSession() as session:
            params = {"chat_id": chat_id, "text": text}
            if buttons:
                inline_keyboard = [[{"text": b['text'], "callback_data": b['data']}] for b in buttons if 'data' in b]
                reply_keyboard = [[{"text": b['text']}] for b in buttons if 'data' not in b]
                params["reply_markup"] = json.dumps({"inline_keyboard": inline_keyboard, "keyboard": reply_keyboard, "one_time_keyboard": True})
            await session.post(f"{self.base_url}sendMessage", params=params)

    @staticmethod
    def with_args(keys):
        def decorator(handler_func):
            async def wrapper(bot, update, data):
                message = update.get("message")
                if message:
                    message_text = message.get("text", "")
                    args = message_text.split()[1:]
                    data = {k: args[i] if i < len(args) else "" for i, k in enumerate(keys)}
                    await handler_func(bot, update, data)
            return wrapper
        return decorator 
