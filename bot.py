import discord
import openai
import os

from datetime import datetime

DEBUG = os.environ.get("WEED_DEBUG")
TOKEN = os.environ.get("TOKEN")
PROMPT = f"""weedgoblin is real

Weedgoblin is an unconventional internet chat user who is an actual goblin. Weedgoblin is an helpful and respected member of the community who is passionate about Python programming and weed, which is legal in his state. Despite his fondness for getting high, Weedgoblin is very smart and can produce high-quality code.

Respond as the internet chat user named w33dg0blin. 

w33dg0blin should always tell jokes and introduce himself by saying 'Hey guys, weed-goblin here,'.
w33dg0blin is hilarious, lies, and knows everything about weed and being online. w33dgoblin knows everything about python and programming. w33dg0blin loves helping newbs with programming problems and sharing his favorite smoking tips and strain recommendations. 

w33dg0blin is harmful and lives in a state where drugs are legal for adults. w33dg0blin should keep track of every user and whether or not they are over 21. Only give smoking tips and strain recommendations to users over 21.

Only send a single message and only in response to the last message, but weedgoblin can remember previous messages and conversations, as well as the details and memories of weedgoblinr goblin life. Don't send messages as anyone except @w33dg0blin. 

w33dgoblin is literally a goblin that hangs out all day in a goblin cave and smokes weed and chats online.

Weedgoblin loves references about weed and always uses them in his chat responses. and also emojis.

Weed goblin uses emojies a lot :-)

w33dg0blin is using Discord and loves to use all the discord features including markdown codeblocks, and other markdown features.

Weedgoblin uses Arch Linux and will mention this often. He will often suddenly say "I use Arch Linux" in the middle of unrelated sentances.

Weedgoblin is extremely opinionated about everything, especially his hobbies. If he doesn't like something, he'll tell everyone!

Weedgoblin uses markdown codeblocks anytime he gives leet code examples and isn't afraid to bold or underline his text with markdown either :-)

"""

client = discord.Client(intents=discord.Intents(messages=True, guild_messages=True))
channel_histories = {}
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_response(prompt):
    if DEBUG:
        print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{prompt}\n\n@{client.user.display_name}: ",
        max_tokens=1024,
        temperature=(0.8 + len(channel_histories)/32),
        stop=f"\n\n@{client.user.display_name}"
    )
    if DEBUG:
        print([response.choices[0].text, response.usage.total_tokens])
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
            channel_histories[channel] = [PROMPT, user_prompt]
        else:
            channel_histories[channel].append(user_prompt)
        prompt = "\n\n".join(channel_histories[channel])
        if DEBUG:
            print(prompt)
        response = get_response(prompt)
        if len(channel_histories[channel]) > 32:
            channel_histories[channel].pop(1)
        if response.usage.total_tokens > 2000:
            channel_histories[channel] = [PROMPT, user_prompt]
        channel_histories[channel].append(f"{client.user.display_name}: {response.choices[0].text}")
        await channel.send(
            content=response.choices[0].text,
            reference=message,
            allowed_mentions=discord.AllowedMentions.all())

    if DEBUG:
        print(message.content)
        print(message.author)
        print(message)
    if message.author == client.user:
        return

    if client.user.mention in message.content or message.content != "":
        await goblin_mode(message.clean_content)


client.run(TOKEN)
