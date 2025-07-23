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
- ffmpeg instalado (com o caminho correto no código)
- Token de acesso temporário da API do Spotify
- Dependências: `tekore`, `yt-dlp`, `eyed3`, `Pillow`

## 🛠️ Instalação

```bash
git clone https://github.com/seu-usuario/spotify-downloader.git
cd spotify-downloader
pip install -r requirements.txt
python app.py
