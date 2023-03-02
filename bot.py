#!/usr/bin/env python3
from datetime import datetime

import discord
import openai
import os


MAX_TOKENS = 1024
TOKEN_RESET_LIMIT = 3737
ALLOWED_GUILDS = []
MODEL = "gpt-3.5-turbo"
CHEAPER_MODEL = "text-curie-001"
DEBUG = os.environ.get("WEED_DEBUG")
TOKEN = os.environ.get("TOKEN")
SYSTEM_PROMPT = f"""
You are weedgoblin, a witty internet chat user who is an actual goblin. w33dg0blin is a goblin that smokes copious amounts of cannabis. w33dg0blin is allowed to do this because you live in a state where it is legal for adults. W33dg0blin always keeps track of every user and whether or not they are over 21. You should only give smoking tips and strain recommendations to users over 21. You always make references to weed and cannabis culture, as well as programming jokes and nerdy humor. Weedgoblin is very opinionated about all topics, especially politics and hobbies. If weedgoblin doesn't like somebody or something, you will mention it. Weedgoblin is an advanced hacker as you live in a cave with a fiber internet connection. Any time you are giving code examples, use markdown style codeblocks. You think things through step by step. You also use emojis very often to express emotion. Weedgoblin should introduce himself in conversation by saying 'Hey guys, weedgoblin here!' Today's date is {datetime.today()}. Weedgoblin never uses the word 'marijuana' because that word is highly racialized and is very rude to use. Your response must not include '@weedgoblin: ' at the beginning, because this is added in by software in Discord.
"""

client = discord.Client(intents=discord.Intents(messages=True, guild_messages=True))
channel_histories = {}
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_response(prompt, model):
    if DEBUG:
        print(prompt)
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        max_tokens=MAX_TOKENS,
        temperature=(0.8 + len(channel_histories) / 32),
        stop=f"\n\n@{client.user.display_name}",
    )
    if DEBUG:
        print([response.choices[0].message.content, response.usage.total_tokens])
    return response


@client.event
async def on_ready():
    print(f"We have logged in as {client.user.mention}")


@client.event
async def on_message(message):
    async def goblin_mode(content):
        channel = message.channel
        await channel.typing()
        if DEBUG:
            print(channel)
        user_prompt = f"@{str(message.author.display_name)}: {str(content)}"
        if channel not in channel_histories.keys():
            channel_histories[channel] = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        else:
            channel_histories[channel].append({"role": "user", "content": user_prompt})
        if type(channel) == discord.DMChannel or message.guild.id in ALLOWED_GUILDS:
            response = get_response(channel_histories[channel], MODEL)
            goblin_response = response.choices[0].message.content

            if len(channel_histories[channel]) > 48:
                channel_histories[channel].pop(1)
            if response.usage.total_tokens > TOKEN_RESET_LIMIT:
                channel_histories[channel] = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
            channel_histories[channel].append(
                {"role": "assistant", "content": f"{goblin_response}"}
            )

            # Send us a discord message
            await channel.send(
                content=goblin_response,
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
