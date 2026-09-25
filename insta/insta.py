from instagrapi import Client
import os
import time
import random

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import requests

def puxa_insta(user):
	cl = Client()
	session_file = "session_saved.json"
	SESSION_ID = open('sessionid.txt', 'r').read() #INSIRA SUA SESSION ID
	alvo = user
	dados_insta = {}
	try:
		if os.path.exists(session_file):
			cl.load_settings(session_file)
		else:
			cl.login_by_sessionid(SESSION_ID)
			cl.dump_settings(session_file)
		delay = random.randint(3, 6)
		time.sleep(delay)
		target = alvo
		user_info = cl.user_info_by_username(target)
		foto_url = getattr(user_info, "profile_pic_url_hd", user_info.profile_pic_url)
		dados_insta.update({'username': user_info.username, 'nome':user_info.full_name, 'biografia':user_info.biography, 'seguidores':user_info.follower_count, 'foto':foto_url})
		return dados_insta

	except Exception as e:
		print(f"\nErro na execução: {e}")
		if os.path.exists(session_file) and "login" in str(e).lower():
			os.remove(session_file)

def faz_frame(imagem_url, username):
	with requests.get(imagem_url, stream=True) as response:
		with open("pfp.jpg", 'wb') as file:
			for chunk in response.iter_content(chunk_size=8192):
				file.write(chunk)
				
	FONT_PATH = Path("DejaVuSans.ttf")
	img_cima = Image.open("insta/FRAME.png").convert("RGBA")
	fundo = Image.open("pfp.jpg").convert("RGBA")
	CAIXA_PFP = (221, 274, 1798, 1818)
	largura_pfp_caixa = CAIXA_PFP[2] - CAIXA_PFP[0]
	altura_pfp_caixa = CAIXA_PFP[3] - CAIXA_PFP[1]
	fundo_redimensionado = fundo.resize((largura_pfp_caixa, altura_pfp_caixa))

	imagem_final = Image.new("RGBA", img_cima.size, (0, 0, 0, 0))
	imagem_final.paste(fundo_redimensionado, (CAIXA_PFP[0], CAIXA_PFP[1]))
	imagem_final.paste(img_cima, (0, 0), mask=img_cima)

	draw_final = ImageDraw.Draw(imagem_final)

	CAIXA_TEXTO = (1589, 1953, 1859, 1994)
	texto = f"@{username}"
	fonte = ImageFont.truetype(str(FONT_PATH), 44)

	text_box = draw_final.textbbox((0, 0), texto, font=fonte)
	largura_texto = text_box[2] - text_box[0]
	altura_texto = text_box[3] - text_box[1]

	largura_caixa_texto = CAIXA_TEXTO[2] - CAIXA_TEXTO[0]
	altura_caixa_texto = CAIXA_TEXTO[3] - CAIXA_TEXTO[1]

	x = CAIXA_TEXTO[0] + (largura_caixa_texto - largura_texto) / 2
	y = CAIXA_TEXTO[1] + (altura_caixa_texto - altura_texto) / 2

	deslocamento_sombra = 2
	draw_final.text((x + deslocamento_sombra, y + deslocamento_sombra), texto, fill=(0, 0, 0, 180), font=fonte)
	draw_final.text((x, y), texto, fill=(7, 109, 242), font=fonte)

	imagem_final.convert("RGB").save("resultado.png")
	return Path("resultado.png")


