import discord
import openai
import asyncio

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

TOKEN = 'BOT_TOKEN'
OPENAI_API_KEY = 'KEY_CHATGPT'

openai.api_key = 'OPENAI_KEY'

@client.event
async def on_ready():
    print(f'Conectado como {client.user.name}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.gchatp'):
        await message.channel.send(f'{message.author.mention} Olá, em que posso te ajudar?')

        try:
            user_question = await client.wait_for('message', timeout=120, check=lambda m: m.author == message.author and m.channel == message.channel)
        except asyncio.TimeoutError:
            await message.channel.send(f'{message.author.mention} Tempo expirado. Se precisar de ajuda, use o comando novamente.')
            return

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente, muito feliz, que gosta muito de ajudar a todos."},
                    {"role": "user", "content": f"{user_question.content}"}
                ]
            )
            bot_answer = response['choices'][0]['message']['content'].strip()
            await message.channel.send(f'{message.author.mention} {bot_answer}')

            while True:
                try:
                    user_message = await client.wait_for('message', timeout=120, check=lambda m: m.author == message.author and m.channel == message.channel)
                except asyncio.TimeoutError:
                    await message.channel.send(f'{message.author.mention} Tempo expirado. Se precisar de ajuda, use o comando novamente.')
                    break

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um assistente, muito feliz, que gosta muito de ajudar a todos."},
                        {"role": "user", "content": f"{user_message.content}"}
                    ]
                )
                bot_answer = response['choices'][0]['message']['content'].strip()
                await message.channel.send(f'{message.author.mention} {bot_answer}')

        except Exception as e:
            print(f'Ocorreu um erro ao processar a pergunta: {e}')
            print(openai.__version__)
            await message.channel.send(f'Ocorreu um erro ao processar a pergunta. Por favor, tente novamente.')

client.run(TOKEN)
