import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# --- server.py İLE AYNI BİLGİLER ---
CLIENT_ID = "c53e2005ca4146a891209c41df9878ed" 
CLIENT_SECRET = "d0ea3841b1394afc8e43b3e4d50fab77"
REDIRECT_URI = "http://127.0.0.1:8888"
SCOPE = "streaming user-modify-playback-state user-read-playback-state user-read-currently-playing"

# --- !!! BURAYI GÜNCELLE !!! ---
# Tarayıcıda (localhost:8888) gördüğün YENİ ID'yi buraya yapıştır:
YOUR_DEVICE_ID = "cfef2eddbd492d90f8224c0cdd4cedf6e1e02de0" 

# Test Şarkısı: Model - Değmesin Ellerimiz (Örnek)
TRACK_URI = "spotify:track:6wmcxlDsaaYpaHGBqF5n4b?si=eff02898ad944e93" 

try:
    # server.py hangi cache dosyasını kullanıyorsa aynısını kullanmalı
    # Eğer server.py'de cache_path=".cache-SON-DENEME" yaptıysak burada da öyle olmalı.
    # Emin değilsen klasörüne bak, .cache ile başlayan dosyanın tam adını yaz.
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".cache-SON-DENEME" # KLASÖRDEKİ CACHE DOSYASININ ADI NE?
    )
    
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print("Kumanda bağlandı.")

except Exception as e:
    print(f"Bağlantı hatası: {e}")
    exit()

# --- ŞARKIYI BAŞLAT ---
try:
    print(f"Cihaza bağlanılıyor: {YOUR_DEVICE_ID}")
    
    # Oynatmayı transfer et (sesi tarayıcıya ver)
    sp.transfer_playback(device_id=YOUR_DEVICE_ID, force_play=True)
    
    # Şarkıyı çal
    print(f"Şarkı çalınıyor... URI: {TRACK_URI}")
    sp.start_playback(device_id=YOUR_DEVICE_ID, uris=[TRACK_URI])
    
    print("BAŞARILI! Tarayıcıdan ses gelmesi lazım.")
    
    # 5 saniye sonra ses seviyesini %50 yap (Test amaçlı)
    time.sleep(5)
    sp.volume(50, device_id=YOUR_DEVICE_ID)
    print("Ses seviyesi %50 yapıldı.")

except Exception as e:
    print(f"HATA OLUŞTU: {e}")
    print("1. Tarayıcı açık mı?")
    print("2. Device ID doğru mu?")
    print("3. Spotify Premium hesabın aktif mi?")