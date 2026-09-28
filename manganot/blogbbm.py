import json
import requests
import re
from bs4 import BeautifulSoup as sp
from bs4 import NavigableString, Tag
from datetime import datetime


#DEFS
def html_para_discord(node):
	def converter(elemento):
		
		if isinstance(elemento, NavigableString):
			return str(elemento)
		
		if not isinstance(elemento, Tag):
			return ""
		
		tag = elemento.name.lower()
		conteudo = "".join( converter(filho) for filho in elemento.children )
		
		if tag in ("strong", "b"):
			return f"**{conteudo}**" 
		
		if tag in ("em", "i"):
			return f"*{conteudo}*"
		
		if tag == "a":
			href = elemento.get("href")
			if href:
				return f"[{conteudo}]({href})"
			return conteudo
		
		if tag == "br":
			return "\n\n"
		
		if tag == "p":
			return conteudo.strip()		
		return conteudo 
	
	return converter(node).strip()


agora = datetime.now()
dia_ano = agora.strftime("%d/%Y")

notica_dados = {'noticias':[]}


def gera_notcs():
	for num_page in range(440-1):
		r = requests.get(f'https://blogbbm.com/blog/page/{num_page+1}/')
		html = sp(r.text, 'html.parser')

		noticias = []
		for noticia in html.find_all('div', {'class':"entry-readmore"}):
			noticias.append(noticia.find('a').attrs['href'])
		return noticias
		
def capta_noticia(noti):
	dados_um = {}
	r = requests.get(noti)
	html = sp(r.text, "html.parser")

	dados_um.update({"titulo": html.find("h1", {"class": "entry-title"}).text})
	dados_um.update({"data": html.find("span", {"class": "entry-post-date"}).text})
	dados_um.update({"banner": html.find("div", {"class": "entry-banner"}).attrs["style"].split("'")[1]})

	mensagem = []
	base = html.find("div", {"class": "entry-content"})
	paragrafos = base.find_all("p", style="text-align: justify;")
	
	for p in paragrafos:
		html_p = str(p)
		texto_convertido = html_para_discord(p)
		if texto_convertido:
			mensagem.append(texto_convertido)
	dados_um.update({"noticia":'\n'.join(mensagem)})
	
	return dados_um


for n in gera_notcs():
	x = capta_noticia(n)
	notica_dados['noticias'].append(x)

with open("manganot/noticias.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(notica_dados, indent=1, ensure_ascii=False))
