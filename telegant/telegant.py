from telegant.api import Api
from telegant.handler import Handler
from telegant.helper import Helper
import aiohttp   

class Bot(Handler, Api, Helper): 
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.message_handlers = {}
        self.command_handlers = {}
        self.callback_handlers = {} 
        self.chat_id = 0
        self.user_dialogues = {}

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

    def add_handler(self, handler_dict, key):
        def decorator(handler):
            handler_dict[key] = handler
            return handler
        return decorator

    def hears(self, pattern):
        return self.add_handler(self.message_handlers, pattern) 

    def command(self, command_str):
        return self.add_handler(self.command_handlers, command_str) 

    def commands(self, commands_list):
        def decorator(handler_func):
            for command in commands_list:
                self.add_handler(self.command_handlers, command)(handler_func)
            def wrapper(*args, **kwargs):
                return handler_func(*args, **kwargs)
            return wrapper
        return decorator 

    def callbacks(self, callbacks_list):
        def decorator(handler_func):
            for callback in callbacks_list:
                self.add_handler(self.callback_handlers, callback)(handler_func)
            def wrapper(*args, **kwargs):
                return handler_func(*args, **kwargs)
            return wrapper
        return decorator 

    def callback(self, callback_data):
        return self.add_handler(self.callback_handlers, callback_data)
'''
class Bot(Decorator): 
    api: Api, 
    helper: Helper, 
    handler: Handler
'''