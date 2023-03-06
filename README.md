# Telegant 
Telegant - An Elegant Modern Bot Framework for Python.
This project is designed to provide developers simple and elegant access to Telegram bot api.

## Installation 
To install the project, simply run:
pip install telegant

# Example 
```python
from telegant import Telegant
import asyncio

bot = Telegant("YOUR_BOT_TOKEN_HERE")

@bot.hears("hello")
async def say_hello(bot, update): 
    await bot.reply(update["message"]["chat"]["id"], "What's up?") 
```


