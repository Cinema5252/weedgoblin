# WeedGoblin

Welcome to the WeedGoblin project. This application is a Python program built to interact with users in a chatroom. The main purpose is to provide a helpful and friendly presence in the chatroom who can help to provide advice and answer questions. WeedGoblin is highly opinionated and loves discussing his hobbies, which include Python, weed, Arch Linux, and extreme hobbies.

## Getting Started

To get the WeedGoblin up and running, you will need the following installed on your computer:

- [Python 3.7+](https://www.python.org/downloads/)
- [OpenAI client](https://github.com/openai/openai-client)
- [discord.py](https://github.com/Rapptz/discord.py)

The next step will be to get your OpenAI API key and set up your environment variables. You also need to create an account on your respective chatroom or platform (e.g. Discord).
To get started creating a Discord bot account you'll need to check out the [Discord Developer Portal](https://discordapp.com/developers/applications/). Here you can find all the information you need to get started creating your own Discord application so you can use it to manage your bot.

The environment variables you'll need to set in order to get the WeedGoblin bot up and running are the following:

- WEED_DEBUG - Enable debugging and logging while the bot is running.
- TOKEN - Your application's Discord bot's access token
- OPENAI_API_KEY - Your OpenAI API key
- WEED_ALLOWED_GUILDS - Comma-separated list of guild IDs that the bot is allowed to operate in
  Once you have the dependencies and environment variables set up, clone this repository. Inside the root directory of the repository, run the following command to start the program:

```
$ python3 bot.py
```

That's it, now the bot is up and listening for your commands and questions.

## Features

Here's a full list of all the features and abilities that this bot can do:

- Speak with us- Answer general questions about Python programming
- Keep and remember users and conversations
- Give programming tips and advice
- Produce codeblocks with Markdown when giving LeetCode examples
- Add emojis to express emotions
- Utilize Arch Linux
- Highly opinionated and loves discussing his hobbies, including Python and weed
- Mention weed-related references and provide advice (for users over 21 years old in states where weeds are legal for adults)

## Conclusion

WeedGoblin is designed to be a helpful addition to your chatroom. With his sharp wit and excellent knowledge of programming, he will be a great asset to your community. Thanks for adding him in!
