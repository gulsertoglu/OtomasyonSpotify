import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template
import sys

# --- Kullanıcı Bilgileri ---
CLIENT_ID = "c53e2005ca4146a891209c41df9878ed"
CLIENT_SECRET = "d0ea3841b1394afc8e43b3e4d50fab77"
REDIRECT_URI = "http://127.0.0.1:8888"
SCOPE = "streaming user-read-email user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing"

# --- Değişkenler ---
app = Flask(__name__)
auth_manager = None  # Bunu aşağıda dolduracağız

# --- Kimlik Doğrulama ---
def setup_spotify_auth():
    global auth_manager # Dışarıdaki auth_manager'ı kullan
    try:
        print("Kimlik doğrulama yöneticisi (Auth Manager) kuruluyor...")
        auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        open_browser=True,
        cache_path=".cache-yeni",  # Bu kalmalı
        show_dialog=True            # Bu kalmalı
        )
        
        # .cache'i kontrol et. Yoksa veya geçersizse, tarayıcıyı aç.
        print("Token kontrol ediliyor (.cache dosyası aranıyor)...")
        token_info = auth_manager.get_access_token(check_cache=True)
        
        if token_info:
            print("BAŞARILI! Geçerli .cache dosyası bulundu ve token alındı.")
            return True # Her şey yolunda
        else:
            # Bu normalde olmamalı çünkü open_browser=True
            print("HATA: Token alınamadı. Tarayıcı açılması gerekiyordu.")
            return False

    except Exception as e:
        print(f"!!! KİMLİK DOĞRULAMA HATASI: {e}")
        print("Spotify Dashboard ayarlarını (ID, Secret, Redirect URI) kontrol et.")
        return False

# --- Flask ---

def get_token_from_cache():
    """Sadece cache'den token'ı okur, yenileme yapmaz (SDK için)"""
    try:
        token_info = auth_manager.get_cached_token()
        if token_info:
            return token_info['access_token']
        else:
            print("get_token_from_cache: Cache'de token bulunamadı.")
            return None
    except Exception as e:
        print(f"get_token_from_cache HATA: {e}")
        return None

@app.route('/')
def index():
    print("Tarayıcı '/' adresini istedi, index.html hazırlanıyor...")
    
    # Token'i al
    access_token = get_token_from_cache()
    
    if not access_token:
        print("!!! HATA: index() fonksiyonu token alamadı.")
        return "TOKEN ALINAMADI! Lütfen terminali kontrol et ve server.py'yi yeniden başlat."
        
    print("index.html'e token başarıyla gönderildi.")
    # index.html dosyasını render et ve 'token' değişkenini ona yolla
    return render_template('index.html', access_token=access_token)


# --- Başlangıç ---
print("Script başlatıldı.")
print("Adım 1: Spotify kimlik doğrulaması deneniyor...")

if setup_spotify_auth():
    # Kimlik doğrulama başarılıysa sunucuyu başlat
    print("\nAdım 2: Web sunucusu (Flask) başlatılıyor...")
    print(f"Lütfen tarayıcınızda http://127.0.0.1:8888 adresini AÇIK TUTUN.")
    
    # Sunucuyu başlat 
    app.run(host='127.0.0.1', port=8888, debug=True)
    
else:
    print("Kimlik doğrulama BAŞARISIZ. Sunucu başlatılamıyor. Terminali kapat.")
    sys.exit(1) # Hata varsa çık