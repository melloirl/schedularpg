import discord

from discord.ext import commands

TOKEN = ''

client = commands.Bot(command_prefix='r!')

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.command()
async def ping(ctx):
    await ctx.send('pong')

@client.command()
async def schedule(ctx):
    day_emojis = ["2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","🇸","🇩"]
    for day in day_emojis:
        await ctx.message.add_reaction(emoji=day)
    await ctx.send('Certo, em que dia da semana ocorrerrão as sessões?')
    



client.run(TOKEN)

