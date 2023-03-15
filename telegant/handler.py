import re
import aiohttp

class Handler:
    async def handle_update(self, update):
        handlers = {
            "message": self.handle_message,
            "callback_query": self.handle_callback_query,
        }
        
        for key in update:
            if key in handlers:
                await handlers[key](update)

    async def handle_message(self, update):
        self.chat_id = update["message"]["from"]["id"]
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
        self.chat_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]
        
        callback_handler = self.callback_handlers.get(callback_data)
        if callback_handler is not None:    
            await callback_handler(self, update, update["callback_query"]["message"])

        await self.answer_callback_query(update["callback_query"]["id"])

    async def answer_callback_query(self, callback_query_id): 
        return await self.request("answerCallbackQuery", {"callback_query_id": callback_query_id})