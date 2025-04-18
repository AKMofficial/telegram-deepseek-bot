# Telegram DeepSeek Bot

This project implements a Telegram bot for DeepSeek API using the OpenAI client library. The bot allows authorized users to start a conversation, display the current model, and clear conversation history. It also maintains context for ongoing conversations and handles too-long responses by sending them as a txt file.

## Features

* **DeepSeek Integration:** Connects to the DeepSeek API (`https://api.deepseek.com`).
* **Model:** Uses the `deepseek-reasoner` model by default (can be changed in the script to V3).
* **Conversation History:** Remembers the context of the current conversation.
* **Authorization:** Only allows users in the `AUTHORIZED_ACCOUNTS` environment variable to interact with the bot.
* **Custom System Prompt:** Reads a `prompt.txt` file to set a custom system message for the AI. 
* **Telegram Bot Commands:**
    * `/start`: Initializes the bot for the user, clears previous history, and shows a welcome message.
    * `/help`: Displays a list of the commands.
    * `/model`: Shows the name of the DeepSeek model currently in use.
    * `/clear`: Clears the conversation history for the current user.
* **Long Text Handling:** Sends responses exceeding Telegram's message length limit (4096 characters) as a `.txt` file.
* **Asynchronous:** Built using `asyncio` and the `python-telegram-bot` library for efficient operation.
* **Environment Variable Configuration:** Uses a `.env` file to easily manage API keys and settings.
* **Basic Logging:** Logs key events like bot startup, user interactions, and errors.

## Need & Purpose

This bot is programmed to interact with DeepSeek's API by a single system prompt loaded from a file (`prompt.txt`). Instead of sending the same prompt with every request, the system prompt is included only once at the beginning of each conversation. Also, interacting via the API may offer a more consistent experience compared to potential high-traffic periods on web interfaces.

## Requirements

* Python 3.7 or higher
* A Telegram Bot Token. Create a new bot using [BotFather](https://t.me/BotFather).
* A DeepSeek API. Obtain it from the [DeepSeek platform](https://platform.deepseek.com/)

## Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/akmofficial/telegram-deepseek-bot.git
    cd telegram-deepseek-bot
    ```

2.  **Install Dependencies:**
    ```bash
    pip install python-telegram-bot openai python-dotenv
    ```

3.  **Create Configuration File:**
    Create a file named `.env` in the same folder as the Python script. Add the following lines and replace the placeholders with your credentials:
    ```dotenv
    #
    BOT_TOKEN= <Your Telegram Bot Token>
    DEEPSEEK_API_KEY= <Your DeepSeek API Key>

    AUTHORIZED_ACCOUNTS= <UserID1>
    ```
* You can get the user ID from Telegram bots like @userinfobot.
* Optional: Comma-separated (,) list of Telegram User IDs allowed to use the bot.
* (Remember to remove the < and > brackets when adding your actual token and ID).

4.  **Create Custom System Prompt (Optional):**
    Create a file named `prompt.txt` in the same folder. Write the text you want to use as the system prompt (e.g., "You are a programming instructor, provide your answers with explanation and examples."). If this file is not present, the default prompt "You are a helpful assistant." will be used.

## Running the Bot

```bash
main.py
```

The bot is ready! You should see logging output in your terminal.

## Usage

1.  Find your bot on Telegram using the username you set up with BotFather.
2.  Send `/start`. 
3.  Send text messages.
4.  Use the commands `/help`, `/model`, and `/clear` as needed.

## Development Note

This project was developed with assistance from AI models.
