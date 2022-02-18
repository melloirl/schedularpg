import discord

from discord.ext import commands

TOKEN = 'nota da direção: não comitar o token'

client = commands.Bot(command_prefix='r!')


#Dicionário contendo os dados do evento.
event_data = {
    "name":'',
    "author":'',
    "days":'',
    "time":'',
    "event_set":False,
    "image_url":'https://picsum.photos/477/307/?blur',
    "icon_url":'',
}

#Verifica se o bot conseguiu se conectar. Caso algo dê errado provavelmente o token tá errado.
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.command()
async def schedule(ctx):
    await ctx.send('Certo, vamos começar a configuração da sua sessão.')
    if not event_data["name"]:
        await ctx.send('Para começar, defina o nome da sessão usando o comando r!setname *nome*.')
        return
    
    embed=discord.Embed(title = event_data["name"])
    embed.add_field(name='Presentes:', value="Nome 1, Nome 2, Nome 3  ✅", inline=False)
    embed.add_field(name='Restantes:', value="Nome 1, Nome 2, Nome 3  ❌", inline=False)
    embed.set_image(url=event_data["image_url"])
    await ctx.send(embed=embed)

@client.command()
async def setname(ctx, *, name):
    global event_data
    event_data["name"] = name
    await ctx.send(f'Nome da sessão definido como: {event_data["name"]}')

@client.command()
async def name(ctx):
    if not event_data["name"]:
        await ctx.send('Nome ainda não definido. Defina o nome da sessão usando o comando r!setname *nome*.')
        return
    else:
        await ctx.send(f'Nome da sessão definido como: {event_data["name"]}')




client.run(TOKEN)

