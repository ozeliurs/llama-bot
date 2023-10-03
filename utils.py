import time

import discord
from llama_cpp import Llama

from params import bot_name, bot_prompt, discord_message_history_count


async def generate_prompt(
        message: discord.Message,
        client: discord.Client,
):
    """
    Generates a prompt for a model to continue.
    """
    # Create the prompt

    message_prompt = []

    # Print message history in order
    async for message in message.channel.history(limit=discord_message_history_count):
        message_prompt.append(f"{message.author.name}: {message.content}")

    # Make the prompt a single string
    message_prompt = "\n".join(message_prompt)

    # Replace the bot's uid with its name
    message_prompt = message_prompt.replace(f"<@{client.user.id}>", f"@{bot_name}")

    prompt = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.
    
    ### Instruction:
    {bot_prompt}
    {message_prompt}
    
    ### Response:
    {bot_name}: """

    return prompt


async def generate_answer(message: discord.Message, client: discord.Client, llama: Llama):
    """
    Generates a response to a message.
    """
    # Generate a prompt
    prompt = await generate_prompt(message, client)

    # Generate a response and make the bot type
    async with message.channel.typing():
        start = time.perf_counter()
        response = llama(prompt)["choices"][0]["text"]
        await record_time(start)

    return response


async def record_time(start: float, path="timings.csv"):
    """
    Records a time to a CSV file.
    """
    timing = str(time.perf_counter() - start)

    with open(path, "a") as f:
        f.write(f"{timing}\n")