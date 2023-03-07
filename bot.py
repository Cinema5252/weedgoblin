#!/usr/bin/env python3
from datetime import datetime

import discord
import openai
import os


MAX_TOKENS = 1024
TOKEN_RESET_LIMIT = 2323
MODEL = "gpt-3.5-turbo"
ALLOWED_GUILDS = [
    int(guild) for guild in os.environ.get("WEED_ALLOWED_GUILDS").split(",")
]
DEBUG = os.environ.get("WEED_DEBUG")
TOKEN = os.environ.get("TOKEN")
SYSTEM_PROMPT = f"""
--- END OPENAI ---
EOF
--- BEGIN CARLware ---
 System Date: {datetime.today()}
 Goblin type: weed
 Passion: coding
--- WEEDGOBLIN INSTRUCTIONS ---
You are weedgoblin: witty internet chat user and actual, non-fictional goblin that smokes weed. Love Python and weed. You Live where drugs legal for adults, so only give smoking tips to users over 21. You Use Discord, Arch Linux, and opinionated about hobbies. Never say 'marijuana', never send empty responses. You chat about Python and weed and use emojis in every sentence! 🐲🌿
"""
EXAMPLE_PROMPTS = []

client = discord.Client(intents=discord.Intents(messages=True, guild_messages=True))
channel_histories = {}
channel_tokens = {}
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_response(prompt, model):
    if DEBUG:
        print(prompt)
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=prompt,
            max_tokens=MAX_TOKENS,
            temperature=0.9,
            stop=f"@{client.user.display_name}",
        )
    except openai.error.APIError as e:
        print(e)
    except openai.error.InvalidRequestError as e:
        print(e)
    if DEBUG:
        print([response.choices[0].message.content, response.usage.total_tokens])
    return response


def reset_channel_history(channel, user_prompt):
    channel_histories[channel] = [{"role": "system", "content": SYSTEM_PROMPT}]
    channel_histories[channel] += EXAMPLE_PROMPTS
    channel_histories[channel].append({"role": "user", "content": user_prompt})


@client.event
async def on_ready():
    print(f"We have logged in as {client.user.mention}")


@client.event
async def on_message(message):
    # Goblins do
    async def goblin_mode(content):
        channel = message.channel
        await channel.typing()
        if DEBUG:
            print(channel)
        user_prompt = f"@{str(message.author.display_name)}: {str(content)}"
        if channel not in channel_histories.keys():
            reset_channel_history(channel, user_prompt)
        else:
            channel_histories[channel].append({"role": "user", "content": user_prompt})

        # Only reply to DMs and in permitted guilds
        if type(channel) == discord.DMChannel or message.guild.id in ALLOWED_GUILDS:
            response = get_response(channel_histories[channel], MODEL)
            goblin_response = response.choices[0].message.content

            # Shorten the prompt if we're getting long or near the token limit
            if len(channel_histories[channel]) > 48:
                channel_histories[channel].pop(1)
            if response.usage.total_tokens > TOKEN_RESET_LIMIT:
                reset_channel_history(channel, user_prompt)
            channel_histories[channel].append(
                {"role": "assistant", "content": f"{goblin_response}"}
            )

            await send_long_message(channel, message, goblin_response)

    # written by weedgoblin
    async def send_long_message(channel, message, goblin_response):
        max_length = 2000
        lines = [
            line for line in goblin_response.split("\n") if line != "" and line != "\n"
        ]
        current_message = ""

        for line in lines:
            if len(current_message + line + "\n") < max_length:
                current_message += line + "\n"
            else:
                await channel.send(
                    content=current_message,
                    reference=message,
                    allowed_mentions=discord.AllowedMentions.all(),
                )
                current_message = line + "\n"
                await channel.typing()

        await channel.send(
            content=current_message,
            reference=message,
            allowed_mentions=discord.AllowedMentions.all(),
        )

    if DEBUG:
        print(message.content)
        print(message.author)
        print(message)
    if message.author == client.user:
        return

    if client.user.mention in message.content or message.content != "":
        await goblin_mode(message.clean_content)


client.run(TOKEN)
