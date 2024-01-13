import discord
import openai
import asyncio
import requests

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

TOKEN = 'MTE5NDc1MDI2Njg4NTU1NDMyNw.G5aGaJ.kF_aMXxuPG42MAuDyVCNSeFrQsaK6I-rtYpHNw'
OPENAI_API_KEY = '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'

PASTEBIN_URL = 'https://pastebin.com/raw/yVKL98EP'

openai.api_key = OPENAI_API_KEY

def check_license(license_key):
    try:
        response = requests.get(PASTEBIN_URL)
        response.raise_for_status()

        licenses = response.text.split('\n') 
        return license_key.strip() in licenses
    except Exception as e:
        print(f"Erro ao verificar a licença: {e}")
        return False

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

        await message.channel.send(f'{message.author.mention} Por favor, insira sua licença:')
        try:
            license_message = await client.wait_for('message', timeout=120, check=lambda m: m.author == message.author and m.channel == message.channel)
        except asyncio.TimeoutError:
            await message.channel.send(f'{message.author.mention} Tempo expirado. Se precisar de ajuda, use o comando novamente.')
            return

        valid_license = check_license(license_message.content.strip())

        if valid_license:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um assistente de linguagem."},
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
                            {"role": "system", "content": "Você é um assistente de linguagem."},
                            {"role": "user", "content": f"{user_message.content}"}
                        ]
                    )
                    bot_answer = response['choices'][0]['message']['content'].strip()
                    await message.channel.send(f'{message.author.mention} {bot_answer}')

            except Exception as e:
                print(f'Ocorreu um erro ao processar a pergunta: {e}')
                print(openai.__version__)
                await message.channel.send(f'Ocorreu um erro ao processar a pergunta. Por favor, tente novamente.')
        else:
            await message.channel.send(f'{message.author.mention} Licença inválida. Se precisar de ajuda, entre em contato com o suporte.')

client.run(TOKEN)
