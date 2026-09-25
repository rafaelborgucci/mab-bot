"""
===============================================================================
                       🚀 INSTALOGIN.PY - TUTORIAL & SCRIPT 🚀
===============================================================================
Este script serve para autenticar sua conta no Instagram usando apenas o seu 
'SESSION ID' do navegador, gerando o arquivo de sessão seguro para seus scripts.

⚠️ IMPORTANTE: O Session ID funciona como sua senha ativa. 
NUNCA compartilhe o arquivo 'session_saved.json' ou o código com esse token.
===============================================================================

📖 PASSO A PASSO PARA PEGAR O SEU SESSION ID:
1. Abra o navegador (Chrome, Firefox, Edge) e acesse: https://instagram.com
2. Certifique-se de que você está LOGADO na sua conta.
3. Pressione a tecla [ F12 ] no seu teclado para abrir as Ferramentas de Desenvolvedor.
4. Siga o caminho conforme o seu navegador:
   - CHROME / EDGE / BRAVE: 
     Vá na aba "Aplicativo" (Application) -> No menu esquerdo, abra "Cookies" 
     -> Clique em "https://instagram.com" -> Procure por "sessionid".
   - FIREFOX: 
     Vá na aba "Armazenamento" (Storage) -> No menu esquerdo, abra "Cookies" 
     -> Clique em "https://instagram.com" -> Procure por "sessionid".
5. Dê um duplo clique no valor longo (letras e números) da coluna "Valor" e COPIE-O.
6. Cole o valor na variável 'SESSION_ID' abaixo.
"""

import os
from instagrapi import Client

# ==========================================
# 🛠️ CONFIGURAÇÃO: COLE O SEU COOKIE AQUI
# ==========================================
SESSION_ID = "COLE_AQUI_O_SEU_SESSION_ID_DO_NAVEGADOR"
# ==========================================

# Nome do arquivo onde a estrutura completa de login será salva
NOME_ARQUIVO_SESSAO = "session_saved.json"

def gerar_sessao_instagram():
    # Verifica se o usuário esqueceu de colar o token real
    if "COLE_AQUI" in SESSION_ID or len(SESSION_ID) < 10:
        print("\n❌ ERRO: Você precisa colar o seu Session ID real na linha 32 do script!")
        print("Siga as instruções explicadas no topo do arquivo para encontrá-lo.")
        return

    print("🔄 Inicializando cliente da Instagrapi...")
    cl = Client()

    try:
        print("🌐 Tentando autenticar nos servidores do Instagram usando o Session ID...")
        # A própria biblioteca simula um dispositivo Android nativo e valida o ID de sessão
        cl.login_by_sessionid(SESSION_ID)
        
        # Se o login funcionar, salva as configurações de sessão estruturadas (com tokens adicionais)
        print(f"💾 Salvando arquivo de sessão estruturado em '{NOME_ARQUIVO_SESSAO}'...")
        cl.dump_settings(NOME_ARQUIVO_SESSAO)
        
        # Teste rápido obtendo o próprio nome de usuário logado para confirmar o sucesso
        username_logado = cl.username_info(cl.user_id).username
        
        print("\n" + "="*50)
        print(f"✅ SUCESSO ABSOLUTO! Você está logado como: @{username_logado}")
        print(f"📂 O arquivo '{NOME_ARQUIVO_SESSAO}' foi criado com êxito.")
        print("="*50)
        print("\n💡 O QUE FAZER AGORA?")
        print("Nos seus próximos scripts (ex: insta.py), você não precisa mais do Session ID!")
        print("Basta usar a linha abaixo para carregar o login instantaneamente:")
        print(f"👉 cl.load_settings('{NOME_ARQUIVO_SESSAO}')")
        print("="*50)

    except Exception as e:
        print("\n❌ FALHA NA AUTENTICAÇÃO")
        print(f"Detalhes do erro: {e}")
        print("\n💡 POSSÍVEIS CAUSAS:")
        print("1. O seu Session ID foi copiado incompleto ou já expirou.")
        print("2. O Instagram detectou atividade suspeita no seu IP. (Tente ligar uma VPN ou usar dados móveis).")
        
        # Remove arquivos residuais de sessões corrompidas para não quebrar tentativas futuras
        if os.path.exists(NOME_ARQUIVO_SESSAO):
            os.remove(NOME_ARQUIVO_SESSAO)

if __name__ == "__main__":
    gerar_sessao_instagram()

