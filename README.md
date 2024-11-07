# Kazuma Meme Bot

Kazuma Meme Bot is a Discord bot that allows users to create memes using various templates. Users can input custom text and choose from a set of predefined templates to generate and share memes directly in Discord.

## Features

- **Meme Creation**: Create a meme by specifying the top and bottom text, along with the meme template name or ID.
- **Template Navigation**: Browse through available meme templates using a reaction-based menu.
- **Help Command**: Provides detailed instructions on how to use the bot's commands.

## Prerequisites

- Python 3.8+
- Required Python libraries: `discord.py`, `discord.ext.menus`, `requests`, `dotenv`
- A `.env` file with your bot token set as `token`
- A `cogs/meme_templates.txt` file containing meme template names, each on a new line
