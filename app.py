import os
from pathlib import Path

import discord
from dotenv import load_dotenv
from llama_cpp import Llama

from utils import generate_answer, bot_prompt

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())
llm = Llama(model_path="nous-hermes-llama2-13b.Q2_K.gguf")

timings = Path("timings.csv")

if not timings.exists():
    timings.write_text("response_time\n")


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!timings"):
        times = timings.read_text().split("\n")[1:-1]
        times = [float(t) for t in times]
        if len(times) == 0:
            await message.reply("No timings recorded.")
            return
        await message.reply(f"Average response time: {sum(times) / len(times)}")
        return

    if message.content.startswith("!prompt"):
        await message.reply(bot_prompt)
        return

    # Ignore messages that don't contain the bot's name
    if f"<@{client.user.id}>" in message.content.lower():
        await message.reply(generate_answer(message, client, llm))

client.run(TOKEN)