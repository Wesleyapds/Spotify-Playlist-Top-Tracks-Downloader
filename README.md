# 🎵 Spotify Downloader com Interface Gráfica

Este projeto permite baixar músicas de playlists e faixas favoritas do Spotify em formato MP3 com qualidade 320kbps. Com uma interface gráfica (Tkinter), você pode baixar facilmente suas playlists ou Top Tracks diretamente do YouTube, com metadados completos e capas de álbuns.

## 🔧 Funcionalidades

- Baixar playlists da sua conta do Spotify
- Baixar faixas mais ouvidas (Top Tracks)
- Conversão automática para MP3
- Adiciona título, artista, álbum, gênero e capa da música
- Interface gráfica fácil de usar

## 📦 Requisitos

- Python 3.8 ou superior
- ffmpeg instalado (com o caminho correto configurado no código)
- Token de acesso temporário da API do Spotify
- Dependências Python: `tekore`, `yt-dlp`, `eyed3`, `Pillow`

## 🛠️ Instalação

```bash
git clone https://github.com/seu-usuario/spotify-downloader.git
cd spotify-downloader
pip install -r requirements.txt
python app.py
🔑 Como obter o Token de Acesso Spotify
Para que o aplicativo funcione corretamente, é necessário obter um token de acesso (access token) válido do Spotify, que autoriza o app a acessar suas playlists e músicas.

Passos para gerar o token manualmente
Acesse o site oficial para desenvolvedores do Spotify:
https://developer.spotify.com

<img width="935" height="888" alt="image" src="https://github.com/user-attachments/assets/c83ebc17-457c-439f-b949-5977663f7c70" />

clicar em Veja em ação 

pegue o token no codigo

<img width="955" height="906" alt="image" src="https://github.com/user-attachments/assets/fa7800b4-ed8b-4101-84a4-899aea1fc0ee" />

Observações
O token gerado manualmente é temporário e expira em aproximadamente 1 hora.
