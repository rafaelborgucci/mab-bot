#ADICIONE O TOKEN DENTRO DE sessao.txt
token = open('sessao.txt', 'r').read()
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import json
import re
import requests

#configs canais
instagram = 1552828499448963133
ranking_ch = 1550582459509252216
noticias_manga = 1553445800850235504

#MINHAS LIBS
from insta.insta import puxa_insta, faz_frame
from hentai.motorhentai import gera_rank,  capta_hentai

#DEFS
def extrai_user_insta(texto):
	texto = texto.strip()
	padrao = r'(?:https?://(?:www\.)?instagram\.com/|@)([a-zA-Z0-9_\.]+)'
	correspondencia = re.match(padrao, texto)
	if correspondencia:
		return correspondencia.group(1)
	return None




#BOT
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)

class BotaoLink(discord.ui.View):
    def __init__(self, url_noticia):
        super().__init__()
        self.add_item(discord.ui.Button(
            label="Ler Matéria Completa", 
            style=discord.ButtonStyle.link,
            url=url_noticia,
            emoji="📰"
        ))


@bot.event
async def on_ready():
	print(f'Logado como > {bot.user}')


#POST
@bot.command()
async def postar(ctx, link):
	if not ctx.message.author.guild_permissions.administrator:
		await ctx.send(f'**Você por acaso é admin? {ctx.author.display_name}**')
		return	
	if not link:
		await ctx.send("❌ **Por favor, forneça o link da notícia! Ex: `!blogbbm https://site.com`**")
		return
	msg1 = await ctx.send(f"*Acessando o link e preparando o jornal, só um minutinho...*")
	manga = await ctx.bot.fetch_channel(noticias_manga)
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)'}
		resposta = requests.get(link, headers=headers)
		soup = BeautifulSoup(resposta.text, 'html.parser')
		if resposta.status_code != 200:
			print (resposta.text)
			await msg1.edit(content="❌ Não consegui acessar o site. Verifique o link.")
			return
		titulo = soup.find("meta", property="og:title")["content"] if soup.find("meta", property="og:title") else "Sem Título"
		banner = soup.find("meta", property="og:image")["content"] if soup.find("meta", property="og:image") else ""
		og_desc = soup.find("meta", property="og:description")["content"] if soup.find("meta", property="og:description") else ""
		tag_thumb = soup.find("meta", property="og:image:secure_url")	
		autor = soup.find("meta", attrs={"name": "author"})["content"] if soup.find("meta", attrs={"name": "author"}) else False
		print (f'olha, tem autor! {autor}')
		conteudo_embed = f"# {titulo}\n\n{og_desc}"
		embed = discord.Embed(title='', description=conteudo_embed)
		embed.set_image(url=banner)  
		if autor:
			embed.set_footer(text=f"Escrito por: {autor}\n\nClique abaixo para abrir a matéria 👇")
		if tag_thumb:
			embed.set_thumbnail(url=tag_thumb)
		embed.set_author(name="MAB - JORNAL", icon_url="https://media.discordapp.net/attachments/1531116319204970496/1552767814056546324/image.png?ex=6ab6cf37&is=6ab57db7&hm=80400d3a363cc8537d8fbcf552ac94ce2dc7eb3cf0f5da762a5c1d677ca512d0&=&format=webp&quality=lossless")    
		 
		view_link = BotaoLink(url_noticia=link)
		await manga.send(embed=embed, view=view_link)
		await msg1.delete()
	except Exception as e:
		print(f"Erro ao processar URL: {e}")
		await msg1.edit(content="❌ Ocorreu um erro ao extrair as informações da URL.")

#RANKING HENTAIS
@bot.command()
async def ranking(ctx, link=None):
	if link is None:
		cmds = {'comandos':[
			{'comando': 'atualizahentai', 'explica': 'Atualiza o TOP de hentais no canal configurado'}
		]}
		comanditos = []
		for cmd in cmds['comandos']:
			comanditos.append(f'``!ranking {cmd["comando"]}`` {cmd["explica"]}')
		comandos_rnkg = '\n'.join(comanditos)

		await ctx.send(f'**Ei {ctx.author.display_name}, esses são os comandos disponíveis:**\n\n{comandos_rnkg}')
		return
	
	if 'atualizahentai' in link:
		if not ctx.message.author.guild_permissions.administrator:
			await ctx.send(f'**Você por acaso é admin? {ctx.author.display_name}**')
			return
		msg1 = await ctx.send(f"*Só um minutinho {ctx.author.display_name} ..*")
		ranque = await ctx.bot.fetch_channel(ranking_ch)
		await msg1.edit(content=f"**Estou limpando o canal {ranque.mention}...**")
		mensagens_apagadas = await ranque.purge(limit=None)
		rank = gera_rank()
		for hentai in rank['rank']:
			for chave, info in hentai.items():
				url = (hentai[chave]['url'])
				hentai_dados = capta_hentai(url)
				posicao_rank = (chave.replace('Hentai ', ''))
				generos = ' '.join(f'`{gênero}`' for gênero in hentai_dados['generos'])
				episodios = len(hentai_dados['episodios'])
				embed = discord.Embed(description=f"# {hentai_dados['titulo']} - TOP {posicao_rank}\n-# {hentai_dados['sinopse']}\n\n**Episódios:** ``{episodios}``\n\n{generos}", colour=0x00b0f4)

				embed.set_author(name="MAB", icon_url="https://media.discordapp.net/attachments/1531116319204970496/1552767814056546324/image.png?ex=6ab6cf37&is=6ab57db7&hm=80400d3a363cc8537d8fbcf552ac94ce2dc7eb3cf0f5da762a5c1d677ca512d0&=&format=webp&quality=lossless")
				embed.set_image(url=hentai_dados['poster'])
				embed.set_footer(text=hentai_dados['data'])
				await ranque.send(embed=embed)
		await msg1.edit(content=f"**✅ O {ranque.mention} foi atualizado com sucesso!**")
		return

#NOTICIAS-CL
@bot.command()
async def clnoticias(ctx, link=None):
	if not ctx.message.author.guild_permissions.administrator:
		await ctx.send(f'**Você por acaso é admin? {ctx.author.display_name}**')
		return
	insta_ch = await ctx.bot.fetch_channel(noticias_manga)
	emoji_sim = "👍"
	emoji_nao = "👎"
	msg1 = await ctx.send(f"*Ei {ctx.author.display_name}, você realmente quer limpar o {insta_ch.mention}?*")
	await msg1.add_reaction(emoji_sim)
	await msg1.add_reaction(emoji_nao)
	def check(reaction, user):
		return (
			reaction.message.id == msg1.id
			and not user.bot 
			and user.guild_permissions.administrator 
			and str(reaction.emoji) in [emoji_sim, emoji_nao]
		)
	reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
	if str(reaction.emoji) == emoji_sim:
		await msg1.edit(content=f"**🧹Aguarde estou limpando {insta_ch.mention} ...**")
		await insta_ch.purge(limit=None)
		await msg1.edit(content=f"**🧹 O {insta_ch.mention} foi limpo com sucesso!**")
		return
	else:
		await msg1.edit(content=f"**OPERAÇÃO CANCELADA**")
	return



#INSTA-CL
@bot.command()
async def clinsta(ctx, link=None):
	if not ctx.message.author.guild_permissions.administrator:
		await ctx.send(f'**Você por acaso é admin? {ctx.author.display_name}**')
		return
	insta_ch = await ctx.bot.fetch_channel(instagram)
	emoji_sim = "👍"
	emoji_nao = "👎"
	msg1 = await ctx.send(f"*Ei {ctx.author.display_name}, você realmente quer limpar o {insta_ch.mention}?*")
	await msg1.add_reaction(emoji_sim)
	await msg1.add_reaction(emoji_nao)
	def check(reaction, user):
		return (
			reaction.message.id == msg1.id
			and not user.bot 
			and user.guild_permissions.administrator 
			and str(reaction.emoji) in [emoji_sim, emoji_nao]
		)
	reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
	if str(reaction.emoji) == emoji_sim:
		await msg1.edit(content=f"**🧹Aguarde estou limpando {insta_ch.mention} ...**")
		await insta_ch.purge(limit=None)
		await msg1.edit(content=f"**🧹 O {insta_ch.mention} foi limpo com sucesso!**")
		return
	else:
		await msg1.edit(content=f"**OPERAÇÃO CANCELADA**")
	return
		

#INSTA
@bot.command()
async def insta(ctx, link):
	insta_user = extrai_user_insta(link)
	if insta_user:
		mensagem1 = await ctx.send(f"*Só um minutinho {ctx.author.display_name} ..*")
		try:
			insta_dados = puxa_insta(insta_user)
		except:
			await ctx.send(f"**ERRO***")
			return
		insta_ch = await ctx.bot.fetch_channel(instagram)
		x = faz_frame(insta_dados['foto'], insta_user)
		embed = discord.Embed()
		embed.set_author(name="MAB", icon_url="https://media.discordapp.net/attachments/1531116319204970496/1552767814056546324/image.png?ex=6ab6cf37&is=6ab57db7&hm=80400d3a363cc8537d8fbcf552ac94ce2dc7eb3cf0f5da762a5c1d677ca512d0&=&format=webp&quality=lossless")
		foto_local = discord.File("resultado.png", filename="foto_perfil.jpg")			
		embed = discord.Embed()
		embed = discord.Embed(title=f"🍥 Ei, senpai!", url=f"https://instagram.com/{insta_user}", description=f"\n## \n*Que tal dar uma espiadinha nesse perfil? 👀✨*ㅤㅤㅤㅤㅤㅤㅤ\n \n**✨ Nome:** ``\"{insta_dados['nome']}\"``\n**🌙 Bio:** ``\"{insta_dados['biografia']}\"``\n**👥 Seguidores** ``{insta_dados['seguidores']} almas``\n### [🌸 Seguir](https://instagram.com/{insta_user})")
		embed.set_image(url="attachment://foto_perfil.jpg")
		await insta_ch.send(embed=embed, file=foto_local)
		await mensagem1.edit(content=f"**Acabei de postar no {insta_ch.mention}!**")
		return
	else:
		await ctx.send(f"**Ei {ctx.author.display_name}, você inseriu de forma inválida!!**\n### Exemplos:\n- ``!insta @username``\n- ``!insta https://instagram.com/username``")
		return

@bot.command()
async def ajuda(ctx):
	dados = json.loads(open('comandos.json', 'r').read())
	mensagem = []
	for comandor in dados['comandos']:
		for chave, info in comandor.items():
			if info['subcomandos'] and isinstance(info['subcomandos'], list):
				for sub_dict in info['subcomandos']:
					nome_sub = list(sub_dict.keys())[0]
				mensagem.append(f'``!{chave} {nome_sub}`` {sub_dict[nome_sub]}')
			else:
				mensagem.append(f'``!{chave}`` {info["help"]}')
	await ctx.send(f"### Meus comandos:\n{'\n'.join(mensagem)}")
	return


bot.run(token)
