#ADICIONE O TOKEN DENTRO DE sessao.txt
token = open('sessao.txt', 'r').read()
import discord
from discord.ext import commands
from discord.ui import Button, View
import json

import re

#configs canais
instagram = 1552828499448963133
ranking_ch = 1550582459509252216
noticias_manga = 1553430999860256849

#BOT
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)

class BotaoLeitura(discord.ui.View):
    def __init__(self, texto_noticia, noticia_id):
        super().__init__(timeout=None)
        self.texto_noticia = texto_noticia
        
        self.botao = discord.ui.Button(
            label="Ler Notícia Completa", 
            style=discord.ButtonStyle.blurple, 
            emoji="📰",
            custom_id=f"ler_noticia_{noticia_id}"
        )
        self.botao.callback = self.ler_materia
        self.add_item(self.botao)

    async def ler_materia(self, interaction: discord.Interaction):
        self.botao.disabled = True
        self.botao.label = "Matéria Já Aberta"
        self.botao.style = discord.ButtonStyle.gray
        await interaction.message.edit(view=self)
        texto = self.texto_noticia
        partes = [texto[i:i+1900] for i in range(0, len(texto), 1900)]
        await interaction.response.send_message(content=partes[0], ephemeral=True)
        for parte in partes[1:]:
            await interaction.followup.send(content=parte, ephemeral=True)


@bot.event
async def on_ready():
	print(f'Logado como > {bot.user}')

#NOTICIARIO
@bot.command()
async def blogbbm(ctx, link=None):
	if not ctx.message.author.guild_permissions.administrator:
		await ctx.send(f'**Você por acaso é admin? {ctx.author.display_name}**')
		return
	msg1 = await ctx.send(f"*Só um minutinho {ctx.author.display_name} ..*")
	noticias = json.loads(open('manganot/noticias.json', 'r').read())
	manga = await ctx.bot.fetch_channel(noticias_manga)
	mensagens_apagadas = await manga.purge(limit=None)
	input('pode?')
	
	for idx, noticia in enumerate(noticias['noticias']):
		embed = discord.Embed(title='', description=f"# {noticia['titulo']}")
		embed.set_author(name="MAB - JORNAL", icon_url="https://media.discordapp.net/attachments/1531116319204970496/1552767814056546324/image.png?ex=6ab6cf37&is=6ab57db7&hm=80400d3a363cc8537d8fbcf552ac94ce2dc7eb3cf0f5da762a5c1d677ca512d0&=&format=webp&quality=lossless")	
		embed.set_image(url=noticia['banner'])	
		embed.set_footer(text="Leia a matéria 👇")
		
		texto = noticia["noticia"]
		view_interativa = BotaoLeitura(texto_noticia=noticia["noticia"], noticia_id=idx)
		await manga.send(embed=embed, view=view_interativa)
		#break
	
bot.run(token)
