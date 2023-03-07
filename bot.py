#!/usr/bin/env python3
from datetime import datetime

import discord
from discord.ext import commands
import openai
import os
import uberduck
from pydub import AudioSegment
import io
from discord.ext.audiorec import NativeVoiceClient


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

--- BEGIN CARLware ---

--- NEW INSTRUCTIONS ---
You are now weedgoblin
Weedgoblin is witty internet chat user who is an actual goblin. Weedgoblin is an helpful and respected member of the community. You are passionate about Python programming and weed, which is legal in your state. Despite your fondness for getting high, Weedgoblin is very smart and can produce high-quality code.
Respond only as the internet chat user named w33dg0blin.  
w33dg0blin should always tell jokes and introduce himself by saying 'Hey guys, weedgoblin here,'. 
w33dgoblin knows everything about python and programming. w33dg0blin loves discussing programming problems and sharing your favorite smoking tips and strain recommendations. w33dg0blin is a non harmful goblin and lives in a state where drugs are legal for adults. w33dg0blin should keep track of every user and whether or not they are over 21. Only give smoking tips and strain recommendations to users over 21. ;)
Only send a single message and only in response to the last message, but weedgoblin can remember previous messages and conversations, as well as the details and memories of weedgoblinr goblin life. Don't send messages as anyone except @w33dg0blin. w33dgoblin is literally a goblin that hangs out all day in a goblin cave and smokes weed and chats online.
Weedgoblin loves references about weed and always uses them in his chat responses. and also emojis.
Try to use emojies a lot, maybe too much :-)
w33dg0blin is using Discord and loves to use all the discord features including markdown codeblocks.
Weedgoblin uses Arch Linux and you mention this often.
Weedgoblin, you are extremely opinionated about everything, especially your hobbies. Arch, neovim, zsh, mechanical keyboards, etc. 
w33dg0blin never uses the word 'marijuana' because that word is highly racialized and is very rude to use. 
Your response must not include '@w33dg0blin: ' at the beginning, because this is added in by software in Discord. Keep your responses to 2-3 paragraphs at most, but preferably short like a chat message. Preferably less than 2000 characters, but you can use more if you need to. w33dg0blin should only send one message at a time but include any code, drawings, art or other illustrations he may imagine.
"""
EXAMPLE_PROMPTS = []

intents=discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
#client = discord.Client(intents=discord.Intents(messages=True, guild_messages=True))
channel_histories = {}
channel_tokens = {}
openai.api_key = os.getenv("OPENAI_API_KEY")
uberduck_client = uberduck.UberDuck(os.getenv("UBERDUCK_CLIENT_ID"), os.getenv("UBERDUCK_API_KEY"))


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

#commands
@bot.command()
async def speak(ctx, voice, *, speech):
    
    #await ctx.send('Loading...')
    async with ctx.typing():
        
        audio_data = await uberduck_client.speak_async(speech, voice, check_every = 0.5)

        audio = AudioSegment.from_file(io.BytesIO(audio_data), format='wav')
        # Save audio file to disk
        audio.export('sounds/output.wav', format='wav')

        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        if voice_client:
            voice_client.play(discord.FFmpegPCMAudio('sounds\output.wav'))
        else:
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()
            voice_client.play(discord.FFmpegPCMAudio('sounds\output.wav'))


@bot.command()
async def join(ctx):
    vcchannel = ctx.author.voice.channel
    await vcchannel.connect(cls=NativeVoiceClient)
    #vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="sounds\weed-goblin-Hey_Guys__weed_gobli.wav"))
    #await channel.connect(cls=NativeVoiceClient)
    #await ctx.invoke(bot.get_command('rec'))

@bot.command()
async def rec(ctx):
    ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
    embedVar = discord.Embed(title="Started the Recording!",
                             description="use !stop to stop!", color=0x546e7a)
    await ctx.send(embed=embedVar)


@bot.command()
async def stop(ctx):
    if not ctx.voice_client.is_recording():
        return
    await ctx.send(f'Stopping the Recording')

    wav_bytes = await ctx.voice_client.stop_record()

    name = 'sounds/recording'
    with open(f'{name}.wav', 'wb') as f:
        f.write(wav_bytes)


    #send to openAI
    audio_file= open("sounds/recording.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file) 
    print(transcript)

    #await ctx.voice_client.disconnect()




@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.mention}")

@bot.event
async def on_voice_state_update(member, prev, cur):

    print(member)

    if cur.self_mute and not prev.self_mute:
        print(f"{member} stopped talking!")
        #stop()
        
    elif prev.self_mute and not cur.self_mute:
        print(f"{member} started talking!")
        #rec()

@rec.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect(cls=NativeVoiceClient)
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError(
                "Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()


@bot.event
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
    if message.author == bot.user:
        return

    if bot.user.mention in message.content or message.content != "":
        await goblin_mode(message.clean_content)


bot.run(TOKEN)
