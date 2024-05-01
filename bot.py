import discord
import openai
import asyncio

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

TOKEN = 'BOT-TOKEN'
OPENAI_API_KEY = 'OPENAI-KEY'

openai.api_key = OPENAI_API_KEY

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.gchatp'):
        await message.channel.send(f'{message.author.mention} Hello, how can I assist you?')

        try:
            user_question = await client.wait_for('message', timeout=120, check=lambda m: m.author == message.author and m.channel == message.channel)
        except asyncio.TimeoutError:
            await message.channel.send(f'{message.author.mention} Time expired. If you need help, use the command again.')
            return

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant, very happy, who loves to help everyone."},
                    {"role": "user", "content": f"{user_question.content}"}
                ]
            )
            bot_answer = response['choices'][0]['message']['content'].strip()
            await message.channel.send(f'{message.author.mention} {bot_answer}')

            while True:
                try:
                    user_message = await client.wait_for('message', timeout=120, check=lambda m: m.author == message.author and m.channel == message.channel)
                except asyncio.TimeoutError:
                    await message.channel.send(f'{message.author.mention} Time expired. If you need help, use the command again.')
                    break

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an assistant, very happy, who loves to help everyone."},
                        {"role": "user", "content": f"{user_message.content}"}
                    ]
                )
                bot_answer = response['choices'][0]['message']['content'].strip()
                await message.channel.send(f'{message.author.mention} {bot_answer}')

        except Exception as e:
            print(f'An error occurred while processing the question: {e}')
            print(openai.__version__)
            await message.channel.send(f'An error occurred while processing the question. Please try again.')

client.run(TOKEN)
