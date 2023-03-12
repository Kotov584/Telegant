
<p align="center">
    <h1><code>Telegant</code></h1>
    <a href="https://t.me/telegant_group"><img src="https://img.shields.io/badge/Telegram-Group-blue.svg?logo=telegram"></a>
    <a href="https://t.me/telegant_official"><img src="https://img.shields.io/badge/Telegram%20channel-telegant_official-blue.svg?logo=telegram"></a>
</p>


# Telegant 
Telegant is an elegant modern bot framework for Python, designed to provide developers with simple and elegant access to the Telegram bot API.
The project is currently at the alpha testing stage and provides only the required basic features to prove the concept of simplicity.



# Installation 
To install the project, simply run:

```python 
pip install telegant
```

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

## On text 

If you need your bot to respond to defined text just use @bot.hears()

```python 
@bot.hears("hello")
async def say_hello(bot, update): 
    await bot.reply(update["message"]["chat"]["id"], "What's up?") 
```

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
        {"text": "Option 1 (reply)"},  
    ]

    await bot.reply(update["message"]["chat"]["id"], "What's up?", buttons) 
```

Bot always detects your buttons type automatically by data key. 
If you want to use inline buttons you have to write text and data values for each button.
As it is detects your inline button when you have "data" key in your button.
Otherwise, it will detect as reply keyboard.

## Commands

You can assign to one function one command or many commands as needed.
For single command use @bot.command() decorator.

```python 
@bot.command("start")
async def say_hello(bot, update):  
    await bot.reply(update["message"]["chat"]["id"], "Welcome, your bot works perfectly.", buttons) 
```
For several commands use @bot.commands() decorator.

```python 
@bot.commands(['help', 'ask'])
async def say_hello(bot, update):  
    await bot.reply(update["message"]["chat"]["id"], "Basic help information.", buttons) 
```

Export data after command by your keys

```python 
@bot.commands(['usernameandage'])
@bot.with_args(['username', 'age'])
async def handler(bot, update, data): 
    await bot.reply(update["message"]["chat"]["id"], f"Hello {data['username']}, you are {data['age']} years old.")
```

## Callbacks
Telegant also offers to you simply detect your callbacks where you able to assign many or one callback to your function

### Many callbacks example 

```python 
@bot.callbacks('option1', 'option2')
async def say_hello(bot, update):  
    await bot.reply(update["message"]["chat"]["id"], "Callback is detected", buttons) 
```

### Single callback example

```python 
@bot.callback('option1')
async def say_hello(bot, update):  
    await bot.reply(update["message"]["chat"]["id"], "Callback is detected", buttons) 
```
