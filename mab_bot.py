#ADICIONE O TOKEN DENTRO DE sessao.txt
token = open('sessao.txt', 'r').read()


#SERVER
ranking = 1550582459509252216

import discord
import json

#LIBS MADE BY ME
from hentai.motorhentai import gera_rank,  capta_hentai

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'Logado como > {client.user}')

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	#RANKING HENTAIS!
	if message.content.startswith('!ranking'):
		if not message.author.guild_permissions.administrator:
			await message.channel.send(f'**Você por acaso é admin? {message.author.display_name}**')
			return
		if 'atualiza' in message.content:
			ranque = await client.fetch_channel(ranking)
			a = await message.channel.send(f'*Ei **{message.author.display_name}** espera só um pouquinho que eu já atualizo os rankings em* {ranque.mention}, *ok ?*')
			try:
				mensagens_apagadas = await ranque.purge(limit=None)
				rank = gera_rank()
				for hentai in rank['rank']:
					for chave, info in hentai.items():
						url = (hentai[chave]['url'])
						hentai_dados = capta_hentai(url)
						posicao_rank = (chave.replace('Hentai ', ''))
						generos = ' '.join(f'`{gênero}`' for gênero in hentai_dados['generos'])
						embed = discord.Embed(description=f"# {hentai_dados['titulo']} - TOP {posicao_rank}\n-# {hentai_dados['sinopse']}\n\n{generos}", colour=0x00b0f4)

						embed.set_author(name="MAB", icon_url="https://media.discordapp.net/attachments/1531116319204970496/1552767814056546324/image.png?ex=6ab6cf37&is=6ab57db7&hm=80400d3a363cc8537d8fbcf552ac94ce2dc7eb3cf0f5da762a5c1d677ca512d0&=&format=webp&quality=lossless")
						embed.set_image(url=hentai_dados['poster'])
						embed.set_footer(text=hentai_dados['data'])
						await ranque.send(embed=embed)
				await a.edit(content=f"**✅ O {ranque.mention} foi atualizado com sucesso!**")
				return
			except ValueError:
				print (f'ERRO []')
			return

client.run(token)
