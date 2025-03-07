import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
import customtkinter as ctk
from tkinter import messagebox
import logging
import threading
import time

# Configurações da API Last.fm
LASTFM_API_KEY = "37f8ca4bd996f18da37b3cfea46e3b41"
LASTFM_USERNAME = "esfaqueado"

# Configurações da API Spotify
SPOTIFY_CLIENT_ID = "6e3af70156354591952f0fcb31a6b429"
SPOTIFY_CLIENT_SECRET = "e86e6f9b6b0645d5b02497c51849c70e"
SPOTIFY_REDIRECT_URI = "http://localhost:3000/callback"  # URI de redirecionamento

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variável global para armazenar as músicas encontradas
tracks = []

# Configuração do CustomTkinter
ctk.set_appearance_mode("dark")  # Modo escuro
ctk.set_default_color_theme("blue")  # Tema azul

# Função para obter a música atual do Spotify
def get_current_track(sp):
    try:
        current_track = sp.current_user_playing_track()
        if current_track and current_track["is_playing"]:
            track_name = current_track["item"]["name"]
            artist_name = current_track["item"]["artists"][0]["name"]
            return f"{artist_name} - {track_name}"
        else:
            return "Nenhuma música tocando no momento."
    except Exception as e:
        logger.error(f"Erro ao obter a música atual: {e}")
        return "Erro ao obter a música atual."

# Função para atualizar a música atual na interface
def update_current_track(sp, label):
    while True:
        current_track = get_current_track(sp)
        label.configure(text=f"🎵 Tocando agora: {current_track}")
        time.sleep(5)  # Atualiza a cada 5 segundos

# Função para pegar as músicas escutadas no período especificado
def get_tracks(period, limit):
    global tracks
    try:
        end_date = datetime.now()
        if period == "last_day":
            start_date = end_date - timedelta(days=1)
        elif period == "last_week":
            start_date = end_date - timedelta(weeks=1)
        elif period == "last_4_weeks":
            start_date = end_date - timedelta(weeks=4)
        elif period == "last_year":
            start_date = end_date - timedelta(days=365)
        else:
            tracks = []
            return

        # Faz a requisição à API do Last.fm
        url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&from={int(start_date.timestamp())}&to={int(end_date.timestamp())}&limit={limit}"
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erro na requisição
        data = response.json()

        # Extrai as músicas escutadas
        tracks = []
        for track in data["recenttracks"]["track"]:
            track_name = track["name"]
            artist_name = track["artist"]["#text"]
            tracks.append(f"{artist_name} - {track_name}")

        messagebox.showinfo("Sucesso", f"{len(tracks)} músicas encontradas para o período selecionado.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar a API do Last.fm: {e}")
        messagebox.showerror("Erro", f"Erro ao acessar o Last.fm: {e}")

# Função para criar uma playlist no Spotify
def create_spotify_playlist(sp):
    global tracks
    if not tracks:
        messagebox.showwarning("Aviso", "Nenhuma música encontrada. Selecione um período primeiro.")
        return

    try:
        # Cria a playlist
        user_id = sp.current_user()["id"]
        playlist_name = f"Skiley Playlist - {datetime.now().strftime('%Y-%m-%d')}"
        playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
        logger.info(f"Playlist '{playlist_name}' criada com sucesso no Spotify!")

        # Procura as músicas no Spotify e adiciona à playlist
        track_uris = []
        for track in tracks:
            result = sp.search(q=track, type="track", limit=1)
            if result["tracks"]["items"]:
                track_uris.append(result["tracks"]["items"][0]["uri"])
                logger.info(f"Adicionada: {track}")

        # Limita o número de músicas para evitar problemas com playlists muito grandes
        if len(track_uris) > 100:
            track_uris = track_uris[:100]
            logger.warning("A playlist foi limitada a 100 músicas.")

        sp.playlist_add_items(playlist["id"], track_uris)
        logger.info(f"{len(track_uris)} músicas adicionadas à playlist.")
        messagebox.showinfo("Sucesso", f"Playlist criada com {len(track_uris)} músicas!")
    except spotipy.exceptions.SpotifyException as e:
        logger.error(f"Erro ao interagir com a API do Spotify: {e}")
        messagebox.showerror("Erro", f"Erro ao criar a playlist: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Função para lidar com a seleção do período
def on_period_select(sp):
    period = period_var.get()
    limit = int(limit_entry.get())
    if period and limit > 0:
        get_tracks(period, limit)
    else:
        messagebox.showwarning("Aviso", "Selecione um período válido e insira um limite de músicas.")

# Interface gráfica com CustomTkinter
root = ctk.CTk()
root.title("Skiley Playlist Creator")
root.geometry("500x400")

# Título
title_label = ctk.CTkLabel(root, text="🎶 Skiley Playlist Creator", font=("Arial", 20))
title_label.pack(pady=10)

# Frame para seleção de período
period_frame = ctk.CTkFrame(root)
period_frame.pack(pady=10)

# Variável para armazenar a seleção do período
period_var = ctk.StringVar(value="last_week")

# Opções de período
periods = [
    ("Último dia", "last_day"),
    ("Última semana", "last_week"),
    ("Últimas 4 semanas", "last_4_weeks"),
    ("Último ano", "last_year")
]

for text, value in periods:
    ctk.CTkRadioButton(period_frame, text=text, variable=period_var, value=value).pack(anchor="w", padx=20, pady=5)

# Frame para limite de músicas
limit_frame = ctk.CTkFrame(root)
limit_frame.pack(pady=10)

limit_label = ctk.CTkLabel(limit_frame, text="Limite de músicas:", font=("Arial", 14))
limit_label.pack(side="left", padx=10)

limit_entry = ctk.CTkEntry(limit_frame, width=100)
limit_entry.insert(0, "50")  # Valor padrão
limit_entry.pack(side="left")

# Botão para buscar as músicas
search_button = ctk.CTkButton(root, text="🔍 Buscar Músicas", command=lambda: on_period_select(sp), font=("Arial", 14))
search_button.pack(pady=10)

# Botão para criar a playlist
create_button = ctk.CTkButton(root, text="➕ Criar Playlist", command=lambda: create_spotify_playlist(sp), font=("Arial", 14))
create_button.pack(pady=10)

# Label para exibir a música atual
current_track_label = ctk.CTkLabel(root, text="🎵 Tocando agora: Nenhuma música tocando no momento.", font=("Arial", 12))
current_track_label.pack(pady=20)

# Autenticação no Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-currently-playing playlist-modify-public",
    cache_path=".cache"
))

# Inicia uma thread para atualizar a música atual
threading.Thread(target=update_current_track, args=(sp, current_track_label), daemon=True).start()

# Inicia a interface gráfica
root.mainloop()