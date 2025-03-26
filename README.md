# HEADS UP

I am completely refactoring this TODAY!

26/03/2025 

I will be pushing updates within the next few hours please do not fork or use the code until I have done extentive testing and have temoved this notice

# ALSO! READ BELOW

If you want to use the bot for free I will be hosting this bot 24/7 in a server which i'll also add to this github somewhere.

# Enhanced Receipt Generator Bot

A powerful Discord bot for generating customized receipts for various popular stores. Perfect for dropshipping or for educational purposes.

## Features

- Generate professional-looking receipts for major retailers (Amazon, Walmart, Target, Best Buy, Apple)
- Customize product details, prices, quantities, and more
- Choose from multiple shipping and payment options
- Realistic order numbers and dates
- Easy-to-use slash commands

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   ```
4. Run the bot:
   ```
   python main.py
   ```

## Commands

- `/receipt` - Generate a receipt with customizable options
- `/stores` - View all available stores and their details
- `/help` - Show all available commands and usage
- `/about` - Information about the bot

## Usage Example

```
/receipt store:amazon product:"Apple AirPods Pro" price:249.99 quantity:1 shipping:Express payment:Visa
```

## Permissions

The bot requires the following permissions:
- Send Messages
- Embed Links
- Attach Files
- Use Slash Commands

## License
This bot is Licenced under Apache 2.0

This project is for educational purposes only.

## Disclaimer

This bot is intended for educational purposes only. The generated receipts should not be used for fraudulent activities. The developer is not responsible for any misuse of this tool.

Copyright 2025 CoinKong
