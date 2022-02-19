import discord

from discord.ext import commands

TOKEN = 'não falamos do token não não não'

client = commands.Bot(command_prefix='r!') # Aqui dá pra alterar o prefixo que o bot usa. Escolhi o r! porque é hype.


#Dicionário contendo os dados do evento.
EVENT_DATA = {
    "name":'',
    "description":'',
    "author":'',
    "days":'',
    "time":'',
    "name_set":False,
    "description_set":False,
    "image_set":False,
    "image_url":'https://picsum.photos/477/307/?blur', #Enquanto o usuário não escolher uma imagem específica usa uma imagem aleatória.
    "icon_url":'',
    "all_participants":[], 
    "present_participants":[],
}

#O help_embed é aqui definido para posterior utilização na hora da chamada do r!schedule. Esse é um modelo "puro", sem alterações, mas que está sujeito a sofrer modificações a medida que
#as alterações ocorrem em tempo real.


help_embed=discord.Embed(title="Vamos configurar sua sessão!", description="Os seguintes comandos podem ser utilizados para configurar o evento da sua sessão", color=0xd7c237)
help_embed.set_thumbnail(url="https://i.imgur.com/MFjFlz9.png")
help_embed.add_field(name="Nome ❌", value="r!setname *Nome*", inline=False)
help_embed.add_field(name="Descrição ❌", value="r!setdescription *Descrição*", inline=False)
help_embed.add_field(name="Imagem de Fundo ❌", value="r!setimage *Url da imagem*", inline=False)

HELP_EMBED_REFERENCE = '' #A variável HELP_EMBED_REFERENCE serve para manter uma referência à mensagem contendo o help_embed criado. Com isso é possível alterar esse embed criado primeiro em tempo real
                          # a medida que as etapas de configuração vão sendo concluídas.

#Verifica se o bot conseguiu se conectar. Caso algo dê errado provavelmente o token tá errado.
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

#O comando schedule é utilizado para postar um evento no canal em que foi chamado. Esse evento pode ser configurado com as informações específicas da sessão.
#Postriormente o schedule deverá surgir em um momento próximo ao início da sessão, marcando todos os jogadores. Ele também contará com uma lista de presentes e restantes atualizada em tempo real
#conforme os jogadores reagirem a mensagem. O dono do evento poderá reagir com um emote para iniciar o evento, iniciando assim um contador marcando o tempo total de sessão.
@client.command()
async def schedule(ctx):
    global EVENT_DATA # Em todos os comandos que precisam das informações definidas do evento eu preciso chamar essa variável global.
    global HELP_EMBED_REFERENCE
    if not HELP_EMBED_REFERENCE: #Caso não haja uma referência à mensagem de ajuda significa que a configuração nunca foi iniciada e portanto ela não existe. Nesse caso ela será criada agora.
        await ctx.send('Certo, vamos começar a configuração da sua sessão.')
        HELP_EMBED_REFERENCE = await ctx.send(embed=help_embed)

        if not EVENT_DATA["name_set"]:
            await ctx.send('Para começar, defina o nome da sessão usando o comando r!setname *nome*.')
            return
    #Definição do embed principal do evento onde os detalhes deverão ser atualizados em tempo real futuramente.
    embed=discord.Embed(title = EVENT_DATA["name"], description = EVENT_DATA["description"])
    embed.add_field(name='Presentes:', value="Nome 1, Nome 2, Nome 3  ✅", inline=False)
    embed.add_field(name='Restantes:', value="Nome 1, Nome 2, Nome 3  ❌", inline=False)
    embed.set_image(url=EVENT_DATA["image_url"])
    await ctx.send(embed=embed)

#Define o nome do evento caso não exista ou atualiza o nome existente.
@client.command()
async def setname(ctx, *, name):
    global EVENT_DATA
    EVENT_DATA["name"] = name
    EVENT_DATA["name_set"] = True
    help_embed.set_field_at(index = 0,name ="Nome ✅",value = 'r!setname *Nome*', inline = False)
    await HELP_EMBED_REFERENCE.edit(embed = help_embed)

    await ctx.send(f'Nome da sessão definido como: {EVENT_DATA["name"]}')

#Define a descrição do evento caso não exista ou atualiza a descrição existente.
@client.command()
async def setdescription(ctx, *, description):
    global EVENT_DATA
    EVENT_DATA["description"] = description
    EVENT_DATA["description_set"] = True
    help_embed.set_field_at(index = 1,name ="Descrição ✅",value = 'r!setdescription *Descrição*', inline = False)
    await HELP_EMBED_REFERENCE.edit(embed = help_embed)
    await ctx.send(f'Descrição da sessão definida como: {EVENT_DATA["description"]}')
    
#Define a imagem do evento caso não exista ou atualiza a imagem existente.
@client.command()
async def setimage(ctx, *, image_url):
    global EVENT_DATA
    EVENT_DATA["image_url"] = image_url
    EVENT_DATA["image_set"] = True
    help_embed.set_field_at(index = 2,name ="Imagem de Fundo ✅",value = 'r!setimage *Url da imagem*', inline = False)
    await HELP_EMBED_REFERENCE.edit(embed = help_embed)
    await ctx.send(f'Imagem de fundo definida como: {EVENT_DATA["image_url"]}')
    
#Mostra o nome definido para o evento caso exista. Caso contrário avisa que o nome ainda não foi definido.
@client.command()
async def name(ctx):
    if not EVENT_DATA["name"]:
        await ctx.send('Nome ainda não definido. Defina o nome da sessão usando o comando r!setname *nome*.')
        return
    else:
        await ctx.send(f'Nome da sessão definido como: {EVENT_DATA["name"]}')

#Mostra o menu de auxílio às configurações do schedule. É chamado automaticamente ao tentar um schedule caso nunca tenha sido utilizado.
@client.command()
async def setuphelp(ctx):
    global HELP_EMBED_REFERENCE
    HELP_EMBED_REFERENCE = await ctx.send(embed=help_embed)


client.run(TOKEN)

