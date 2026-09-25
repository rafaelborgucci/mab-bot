# 🤖 MAB Bot — Discord

Bot para Discord desenvolvido em Python 3, com funções de ajuda, ranking de conteúdo e integração com Instagram.

## 📋 Comandos

| Comando                   | Descrição                                 |
| ------------------------- | ----------------------------------------- |
| `!ajuda`                  | Exibe a lista de comandos disponíveis.    |
| `!ranking atualizahentai` | Atualiza os hentais do canal configurado. |
| `!insta`                  | Exibe seu Instagram.                      |
| `!instacl`                | Limpa o canal configurado para Instagram. |

---

## 🚀 Instalação e configuração

### 1. Requisitos

Você precisa ter o **Python 3** instalado.

Para verificar:

```bash
python3 --version
```

Depois, instale as dependências do projeto, caso exista um arquivo `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

---

## 🔑 Configurando o Token do Discord

Antes de executar o bot, abra o arquivo:

```text
mab_bot.py
```

Procure pela seguinte linha:

```python
#ADICIONE O TOKEN DENTRO DE sessao.txt
token = open('sessao.txt', 'r').read()
```

O bot foi configurado para ler automaticamente o token do Discord a partir do arquivo:

```text
sessao.txt
```

### Exemplo

Crie o arquivo `sessao.txt` na mesma pasta do `mab_bot.py`:

```text
seu_token_do_discord
```

**Importante:** coloque somente o token no arquivo, sem aspas e sem espaços extras.

> ⚠️ **Nunca compartilhe seu token do Discord ou publique o arquivo `sessao.txt` no Gi**

