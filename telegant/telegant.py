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

    def hears(self, pattern):
        def decorator(handler):
            self.message_handlers[pattern] = handler 
            return handler
        return decorator

    def commands(self, commands_list):
        def decorator(handler):
            for command in commands_list:
                self.command_handlers[command] = handler
            return handler
        return decorator

    def command(self, command_str):
        def decorator(handler):
            self.command_handlers[command_str] = handler
            return handler
        return decorator

    def callbacks(self, callbacks_list):
        def decorator(handler):
            for callback in callbacks_list:
                self.callback_handlers[callback] = handler
            return handler
        return decorator
    
    def callback(self, callback_data):
        def decorator(handler):
            self.callback_handlers[callback_data] = handler
            return handler
        return decorator

    async def start_polling(self):
        last_update_id = 0
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    response = await session.get(f"{self.base_url}getUpdates", params={"offset": last_update_id})
                    if response.status != 200:
                        print(f"Error: {response.status}")
                        continue

                    response_json = await response.json()
                    if not response_json.get("ok"):
                        print("Error: Response is not OK")
                        continue

                    for update in response_json["result"]:
                        if "message" in update:
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
                                for pattern, handler in self.message_handlers.items(): 
                                    if pattern == message_text:
                                        await handler(self, update)

                            last_update_id = update["update_id"] + 1

                        elif "callback_query" in update:
                            chat_id = update["callback_query"]["message"]["chat"]["id"]
                            callback_data = update["callback_query"]["data"]
                            
                            callback_handler = self.callback_handlers.get(callback_data)
                            if callback_handler is not None:
                                await callback_handler(self, update, update["callback_query"]["message"])

                            await self.answer_callback_query(update["callback_query"]["id"])
                            last_update_id = update["update_id"] + 1

                    await asyncio.sleep(0.1)

                except Exception as e:
                    print(f"Error polling for updates: {e}")

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
 
    async def answer_callback_query(self, callback_query_id):
        async with aiohttp.ClientSession() as session:
            try:
                await session.post(f"{self.base_url}answerCallbackQuery", params={"callback_query_id": callback_query_id})
            except Exception as e:
                print(f"Error answering callback query: {e}")

    async def reply(self, chat_id, text, buttons=None):
        async with aiohttp.ClientSession() as session:
            if buttons is None:
                params = {"chat_id": chat_id, "text": text}
                await session.post(f"{self.base_url}sendMessage", params=params)
                return None
            
            inline_keyboards = []
            reply_keyboards = []

            for button in buttons:
                (inline_keyboards.append(button) if "data" in button else reply_keyboards.append(button))

            inline_keyboard = []
            reply_keyboard = []

            if inline_keyboards:
                inline_keyboard = [[{"text": inline_keyboard['text'], "callback_data": inline_keyboard['data']}] for inline_keyboard in inline_keyboards]

            if reply_keyboards:
                reply_keyboard = [[{"text": reply_keyboard['text']}] for reply_keyboard in reply_keyboards]

            params = {"chat_id": chat_id, "text": text, "reply_markup": json.dumps({"inline_keyboard": inline_keyboard, "keyboard": reply_keyboard, "one_time_keyboard": True})}
            await session.post(f"{self.base_url}sendMessage", params=params)
