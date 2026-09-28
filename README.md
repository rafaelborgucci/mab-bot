# 🤖 MAB Bot — Discord

Bot para Discord desenvolvido em **Python 3**, com funções de ajuda, ranking de conteúdo, publicação de notícias e integração com Instagram.

---

## 📋 Comandos

| Comando                   | Descrição                                                                  |
| ------------------------- | -------------------------------------------------------------------------- |
| `!ajuda`                  | Exibe a lista de comandos disponíveis.                                     |
| `!ranking atualizahentai` | Atualiza os hentais do canal configurado.                                  |
| `!insta [link]`           | Publica o Instagram informado utilizando uma moldura no canal configurado. |
| `!instacl`                | Limpa o canal configurado para publicações de Instagram.                   |
| `!postar [link]`          | Publica uma notícia através do link informado no canal configurado.        |

---

## 📸 Instagram

### `!insta [link]`

O comando `!insta` permite publicar o Instagram de uma pessoa no canal configurado.

O bot recebe o link do perfil e gera a publicação utilizando a **moldura configurada para Instagram**.

### Exemplo:

```text
!insta https://www.instagram.com/exemplo/
```

Após executar o comando, o bot irá processar o Instagram informado e publicar o resultado no **canal configurado para Instagram**.

### Outro exemplo:

```text
!insta https://instagram.com/pessoa
```

> 💡 Basta enviar o link do perfil do Instagram após o comando `!insta`.

---

## 📰 Publicação de notícias

### `!postar [link]`

O comando `!postar` permite publicar uma notícia informando apenas o link da página.

### Exemplo:

```text
!postar https://exemplo.com/noticia
```

O bot irá processar o link informado e publicar a notícia automaticamente no **canal configurado para postagens**.

### Outro exemplo:

```text
!postar https://site.com.br/noticias/tecnologia/nova-noticia
```

> 💡 O canal de destino precisa estar configurado no código do bot antes da utilização do comando.

---

## 🧹 Limpar publicações do Instagram

### `!instacl`

O comando `!instacl` é utilizado para limpar o canal configurado para publicações de Instagram.

### Exemplo:

```text
!instacl
```

Ao executar o comando, o bot irá limpar as mensagens do **canal configurado para Instagram**.

> ⚠️ O bot precisa ter as permissões necessárias para gerenciar e excluir mensagens no canal.

---

## 🏆 Ranking

### `!ranking atualizahentai`

Atualiza o conteúdo relacionado ao ranking no canal configurado.

### Exemplo:

```text
!ranking atualizahentai
```

O bot executará a atualização e enviará o resultado para o **canal configurado para o ranking**.

---

## ❓ Ajuda

### `!ajuda`

Exibe no Discord a lista de comandos disponíveis no bot.

### Exemplo:

```text
!ajuda
```

O bot apresentará os comandos que podem ser utilizados pelos usuários.

---

# 🚀 Instalação e configuração

## 1. Requisitos

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
# ADICIONE O TOKEN DENTRO DE sessao.txt
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

> ⚠️ **Nunca compartilhe seu token do Discord ou publique o arquivo `sessao.txt` no GitHub.**

---

# ⚙️ Configuração dos canais

Algumas funções do MAB utilizam canais específicos para realizar suas publicações.

Por exemplo:

* 📸 Instagram → canal configurado para Instagram
* 📰 Notícias → canal configurado para postagens
* 🏆 Ranking → canal configurado para ranking

Os canais devem ser definidos na configuração do bot conforme a implementação presente no `mab_bot.py`.

---

# ▶️ Executando o bot

Após configurar o token e instalar as dependências, execute:

```bash
python3 mab_bot.py
```

Se tudo estiver configurado corretamente, o bot ficará online no Discord e poderá receber os comandos disponíveis.

---

# 📁 Estrutura básica

```text
MAB Bot/
├── mab_bot.py
├── sessao.txt
├── requirements.txt
└── README.md
```

> 🔒 Recomenda-se adicionar `sessao.txt` ao `.gitignore` para evitar que o token seja enviado acidentalmente para um repositório Git.

### `.gitignore`

```gitignore
sessao.txt
__pycache__/
*.pyc
.venv/
venv/
```

---

# 🛠️ Tecnologias

* **Python 3**
* **Discord.py**
* Integração com Instagram
* Processamento e publicação de notícias através de links
* Automação de publicações no Discord

