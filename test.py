from datetime import datetime

import discord
from discord.ext import commands
import openai
import os
import uberduck
from pydub import AudioSegment
import io

DEBUG = True
TOKEN = "MTA3OTgxODkyOTQzNTg1Mjk3MA.GKKdpX.kwvSZJqkQFIpYHYo5WOyVwCKiKw7P7tAbWg84s"

uberduck_client = uberduck.UberDuck('pub_dselihpqtypbbwkxhj', 'pk_7a26317f-d500-4abd-87d8-83fb6721cc8c')

intents=discord.Intents.default()
intents.guilds = True
intents.members = True
    
bot = commands.Bot(command_prefix='!', intents=intents)
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
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="sounds\weed-goblin-Hey_Guys__weed_gobli.wav"))


@bot.event
async def on_message(message):
    guild = message.guild

    if DEBUG:
        print(message.content)
        print(message.author)
        print(message)
    if message.author == bot.user:
        #send to uberduck
        
        return

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.mention}")       

bot.run(TOKEN)