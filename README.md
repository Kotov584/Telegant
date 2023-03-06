# Telegant 
Telegant - An Elegant Modern Bot Framework for Python.
This project is designed to provide developers simple and elegant access to Telegram bot api.
Project is at the Alpha testing stage and provides only required basic features at the moment to proof concept of simplicity.

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

#Your code here (Recommended to write your functions in order)

asyncio.run(bot.start_polling())
```

# Usage 

## Sending bot with buttons

### Inline buttons example
```python 
@bot.hears("hello")
async def say_hello(bot, update): 
 
    buttons = [
        {"text": "Option 1 (inline)", "data": "option1"},  
    ]

    await bot.reply(update["message"]["chat"]["id"], "What's up?", buttons) 
```

### Reply buttons example

```python 
@bot.hears("hello")
async def say_hello(bot, update): 
 
    buttons = [
        {"text": "Option 1 (inline)"},  
    ]

    await bot.reply(update["message"]["chat"]["id"], "What's up?", buttons) 
```

Bot always detects your buttons type automatically by data key. 
If you want to use inline buttons you have to write text and data values for each button.
As it is detects your inline button when you have "data" key in your button.
Otherwise, it will detect as reply keyboard.

## Commands

You can assign to one function one command or many commands as needed
For single command use @bot.command decorator

```python 
@bot.command("start")
async def say_hello(bot, update): 
 
    buttons = [
        {"text": "Option 1 (inline)", "data": "option1"},  
    ]

    await bot.reply(update["message"]["chat"]["id"], "What's up?", buttons) 
```



