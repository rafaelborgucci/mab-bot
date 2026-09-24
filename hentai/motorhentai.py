import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup as sp

def baixa_ep(url_h):
	session = requests.Session()
	pasta_destino = Path.home() / "Downloads"
	pasta_destino.mkdir(parents=True, exist_ok=True)
	headers_base = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1'
	}
	r = session.get(url_h, headers=headers_base)
	html = sp(r.text, 'html.parser')
	botoes = html.find('div', {'id':'playex'}).find('div', {'class':'control'}).find_all('a')
	titulo = (html.find('div', {'class':'sbox info_pad'}).find('h1').text.strip())
	for botao in botoes:
		try:
			if 'baixar' in botao.attrs['href']:
				url_botao = (f"https://www.muitohentai.com{botao.attrs['href']}")
				break
		except:
			pass

	if url_botao:
		headers_passo2 = headers_base.copy()
		headers_passo2['Referer'] = url_h
		r2 = session.get(url_botao, headers=headers_passo2)
		html2 = sp(r2.text, 'html.parser')
		link = None
		for btn in html2.find_all('a', {'class': 'button22'}):
			href_btn = btn.attrs.get('href', '')
			if 'www.muitohentai' in href_btn:
				link = href_btn
				break
		if link:
			headers_passo3 = headers_base.copy()
			headers_passo3['Referer'] = url_botao
			r3 = session.get(link, headers=headers_passo3, stream=True)
			if r3.status_code == 200:
				nome_arquivo = f"{titulo}.mp4"
				print(f"Iniciando o download de: {nome_arquivo}...")
				caminho_completo = pasta_destino / nome_arquivo
				with caminho_completo.open('wb') as f:
					for chunk in r3.iter_content(chunk_size=1024 * 1024):
						if chunk:
							 f.write(chunk)
							 print(".", end="", flush=True)
				print(f"\nDownload concluído!: [{caminho_completo}]")
	return caminho_completo


def capta_hentai(url_n):
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'none',
		'Sec-Fetch-User': '?1',
		'Priority': 'u=0, i',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache'
	}

	episodio = {}
	r = requests.get(url_n, headers=headers)
	html = sp(r.text, 'html.parser')
	dados_ep = html.find('div', {'id':'single'})
	episodio.update({'titulo':dados_ep.find('div', {'class':'data'}).find('h1').text})
	episodio.update({'sinopse':dados_ep.find('div', {'class':'data'}).find('div', {'id':'info1'}).find('p').text})
	episodio.update({'poster':dados_ep.find('div', {'class':'poster'}).find('img').attrs['src']})
	episodio.update({'data':dados_ep.find('div', {'class':'data'}).find('div', {'class':'extra'}).text})
	episodio.update({'generos':[]})
	episodio.update({'episodios':[]})

	for genero in dados_ep.find('div', {'class':'data'}).find('div', {'class':'sgeneros'}).find_all('a'):
		episodio['generos'].append(genero.text)

	for ep in html.find('div', {'id':'episodes'}).find('div', {'class':'module series'}).find('div', {'class':'content series'}).find('div', {'class':'items'}).find_all('article'):
		
		tit = (f"{ep.find('div', {'class':'data'}).find('h3').text.strip()} - {ep.find('div', {'class':'data'}).find('span').text.strip()}")
		link = (ep.find('a').attrs['href'])
		epesodeo = {'titulo':tit, 'link':f'https://www.muitohentai.com{link}'}
		episodio['episodios'].append(epesodeo)


	return_episodio = json.dumps(episodio, ensure_ascii=False, indent=2)
	return json.loads(return_episodio)


def gera_rank():
	url = 'https://www.muitohentai.com/ranking-hentais/'
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'none',
		'Sec-Fetch-User': '?1',
		'Priority': 'u=0, i',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache'
	}
	r = requests.get(url, headers=headers)
	html = sp(r.text, 'html.parser')
	ranking = {'rank':[]}
	for li in html.find('ul', {'class':'ul_sidebar'}).find_all('li'):
		link = 'https://www.muitohentai.com'+li.find('a').attrs['href']
		foto = li.find('img').attrs['src']
		posicao = int(li.find('i', {'style':'color: red;'}).text)
		for b in li.find_all('b'):
			if b.find('i') == None:
				if 'Nome do hentai' in b.text:
					titulo = (b.find('a').text)
					break
		json_hent = {f'Hentai {posicao}': {}}
		json_hent[f'Hentai {posicao}'].update({'url':link})
		json_hent[f'Hentai {posicao}'].update({'titulo':titulo})
		json_hent[f'Hentai {posicao}'].update({'poster':foto})
		ranking['rank'].append(json_hent)

	return_rank = json.loads(json.dumps(ranking, ensure_ascii=False, indent=2))
	return return_rank
