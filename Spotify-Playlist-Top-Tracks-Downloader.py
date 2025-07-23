import tekore as tek
import os
import yt_dlp as youtube_dl
import eyed3
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor
import queue

# Variável global para o objeto Spotify
spotify = None

# Opções do youtube-dl
ydl_opts = {
    'ffmpeg_location': r'C:\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe',  # Atualize para seu ffmpeg
    'format': 'bestaudio/best',
    'extractaudio': True,
    'outtmpl': '%(title)s.%(ext)s',
    'addmetadata': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'logger': None,
}

log_queue = queue.Queue()

def write_log_threadsafe(message):
    log_queue.put(message)

def process_log_queue():
    while not log_queue.empty():
        msg = log_queue.get_nowait()
        log_text.insert(tk.END, msg)
        log_text.see(tk.END)
    root.after(100, process_log_queue)

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " ._-()").rstrip()

def songs_downloader(folder, tracks):
    os.makedirs(folder, exist_ok=True)

    def download_track(track):
        song = sanitize_filename(track.name)
        artist = sanitize_filename(track.artists[0].name)
        album = sanitize_filename(track.album.name)

        write_log_threadsafe(f"Baixando: {song} - {artist}\n")

        filename_template = os.path.join(folder, f'{artist} - {song}.%(ext)s')
        ydl_opts_local = ydl_opts.copy()
        ydl_opts_local['outtmpl'] = filename_template

        full_destination = os.path.join(folder, f'{artist} - {song}.mp3')

        if os.path.exists(full_destination):
            write_log_threadsafe(f"{full_destination} já baixado\n")
            return

        try:
            with youtube_dl.YoutubeDL(ydl_opts_local) as ydl:
                ydl.download([f'ytsearch1:{song} {artist}'])

            if not os.path.exists(full_destination):
                write_log_threadsafe(f'Falha ao baixar {full_destination}\n')
                return

            audiofile = eyed3.load(full_destination)
            if audiofile.tag is None:
                audiofile.initTag()
            audiofile.tag.artist = artist
            audiofile.tag.title = song
            audiofile.tag.album = album
            audiofile.tag.album_artist = track.album.artists[0].name

            genres = spotify.artist(track.artists[0].id).genres
            if genres:
                audiofile.tag.genre = genres[-1]
            audiofile.tag.track_num = track.track_number

            try:
                image_url = track.album.images[0].url
                image_data = urllib.request.urlopen(image_url).read()
                image = Image.open(io.BytesIO(image_data)).convert("RGB")
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG")
                jpeg_data = buffer.getvalue()
                audiofile.tag.images.set(3, jpeg_data, 'image/jpeg')
            except Exception as e:
                write_log_threadsafe(f"Erro ao carregar imagem: {e}\n")

            audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

            write_log_threadsafe(f"Download e tag completos: {full_destination}\n")

        except Exception as e:
            write_log_threadsafe(f"Erro ao baixar '{song}': {e}\n")

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(download_track, tracks)

def get_playlists():
    playlists = spotify.playlists(spotify.current_user().id)
    return playlists.items

def get_playlist_tracks(playlist):
    playlist_id = playlist.id
    results = spotify.playlist_items(playlist_id)
    tracks = results.items
    while results.next:
        results = spotify.next(results)
        tracks.extend(results.items)
    return [item.track for item in tracks if item.track]

def main_app():
    global root, log_text, playlists

    root = tk.Tk()
    root.title("Spotify Downloader")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Playlists disponíveis:").pack(anchor=tk.W)

    playlists = get_playlists()
    playlist_names = [f"{p.name} ({p.tracks.total} faixas)" for p in playlists]
    playlist_box = ttk.Combobox(frame, values=playlist_names, state="readonly")
    playlist_box.pack(fill=tk.X)

    def on_download_playlist():
        selected_index = playlist_box.current()
        if selected_index < 0:
            messagebox.showwarning("Aviso", "Selecione uma playlist")
            return
        playlist = playlists[selected_index]
        write_log_threadsafe(f"Iniciando download da playlist: {playlist.name}\n")
        root.update()
        tracks = get_playlist_tracks(playlist)
        songs_downloader(playlist.name, tracks)
        messagebox.showinfo("Concluído", f"Download da playlist '{playlist.name}' finalizado")

    download_playlist_btn = ttk.Button(frame, text="Baixar Playlist Selecionada", command=on_download_playlist)
    download_playlist_btn.pack(fill=tk.X, pady=5)

    ttk.Label(frame, text="Baixar Top Tracks (quantidade):").pack(anchor=tk.W, pady=(10,0))
    top_tracks_entry = ttk.Entry(frame)
    top_tracks_entry.insert(0, "5")
    top_tracks_entry.pack(fill=tk.X)

    def on_download_top_tracks():
        try:
            limit = int(top_tracks_entry.get())
        except ValueError:
            limit = 5
        write_log_threadsafe(f"Iniciando download das top {limit} tracks\n")
        root.update()
        tracks = spotify.current_user_top_tracks(limit=limit).items
        songs_downloader("Top Tracks", tracks)
        messagebox.showinfo("Concluído", "Download das Top Tracks finalizado")

    download_top_tracks_btn = ttk.Button(frame, text="Baixar Top Tracks", command=on_download_top_tracks)
    download_top_tracks_btn.pack(fill=tk.X, pady=5)

    ttk.Label(frame, text="Logs:").pack(anchor=tk.W, pady=(10,0))
    log_text = tk.Text(frame, height=15)
    log_text.pack(fill=tk.BOTH, expand=True)

    root.after(100, process_log_queue)
    root.mainloop()

def ask_token():
    # Janela raiz temporária para diálogo de input
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    token = simpledialog.askstring("Token Spotify", "Cole seu token de acesso Spotify:", parent=root)

    root.destroy()  # Fecha a janela temporária

    return token

if __name__ == "__main__":
    token = ask_token()
    if not token:
        print("Token não informado. Encerrando.")
        exit(1)

    try:
        spotify = tek.Spotify(token)
        # Testa token requisitando usuário atual para validar
        spotify.current_user()
    except Exception as e:
        print(f"Token inválido ou erro na autenticação: {e}")
        exit(1)

    main_app()
