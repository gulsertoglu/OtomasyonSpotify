import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json
import datetime

# --- AYARLAR ---
CLIENT_ID = "c53e2005ca4146a891209c41df9878ed"
CLIENT_SECRET = "d0ea3841b1394afc8e43b3e4d50fab77"
REDIRECT_URI = "http://127.0.0.1:8888"
SCOPE = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

TOTAL_SONGS_TO_TEST = 100
LISTEN_DURATION = 60  # saniye

# Dinletmek istediğin playlist (kendininkini yaz)
PLAYLIST_URI = "spotify:playlist:52Ul3jyC5OLFnOhx7MB6qd?si=ef4449f443f8475d"  # örnek

# --- FONKSİYON: AKTİF CİHAZ BUL ---
def get_active_device(sp):
    devices = sp.devices()
    devs = devices.get("devices", [])
    if not devs:
        raise RuntimeError("Hiç cihaz bulunamadı. Spotify uygulamasını aç ve bir şarkı çal / cihazı aktif et.")

    # Aktif cihaz varsa onu kullan, yoksa ilk cihaz
    for d in devs:
        if d.get("is_active"):
            return d["id"]
    return devs[0]["id"]

# --- BAĞLANTI ---
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=".cache-SON-DENEME"
)
sp = spotipy.Spotify(auth_manager=auth_manager)
print("✅ Robot hazır. Bağlantı kuruldu.")

# --- VERİ ---
collected_data = []

try:
    device_id = get_active_device(sp)
    print(f"🔊 Kullanılacak cihaz: {device_id}")

    # Cihazı aktif et ve playlist başlat
    sp.transfer_playback(device_id=device_id, force_play=True)
    sp.start_playback(device_id=device_id, context_uri=PLAYLIST_URI)
    sp.volume(50, device_id=device_id)

    print("⏳ Sistem ısınıyor (3 saniye)...")
    time.sleep(3)

    last_track_id = None

    for i in range(1, TOTAL_SONGS_TO_TEST + 1):
        print("\n--------------------------------")
        print(f"🎧 ŞARKI {i} / {TOTAL_SONGS_TO_TEST}")

        # Şu an çalanı 3 kereye kadar dene
        current_track = None
        for _ in range(3):
            current_track = sp.current_playback()
            if current_track and current_track.get("item"):
                break
            time.sleep(1)

        if not current_track or not current_track.get("item"):
            print("⚠️ Şu an bir şey çalmıyor, sıradakine geçiliyor...")
            sp.next_track(device_id=device_id)
            time.sleep(3)
            continue

        track = current_track["item"]
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        track_id = track["id"]
        popularity = track["popularity"]

        is_playing = current_track.get("is_playing", False)
        progress_ms = current_track.get("progress_ms", 0)

        print(f"🎵 Çalıyor: {track_name} - {artist_name}")
        print(f"▶️ is_playing={is_playing}, progress_ms={progress_ms}")
        print(f"⏱️ {LISTEN_DURATION} saniye dinleniyor...")

        # Eğer çalmıyorsa zorla başlat
        if not is_playing:
            sp.start_playback(device_id=device_id)
            time.sleep(1)

        time.sleep(LISTEN_DURATION)

        # Veriyi kaydet
        song_data = {
            "sira": i,
            "tarih": str(datetime.datetime.now()),
            "sarki_adi": track_name,
            "sanatci": artist_name,
            "spotify_id": track_id,
            "populerlik": popularity,
            "dinlenen_sure_sn": LISTEN_DURATION
        }
        collected_data.append(song_data)
        print("✅ Veri kaydedildi.")

        # Sıradaki şarkıya geç
        print("⏭️ Sıradaki şarkıya geçiliyor...")
        sp.next_track(device_id=device_id)

        # Gerçekten yeni şarkıya geçti mi diye 3 sn bekle + kontrol
        time.sleep(3)
        new_playback = sp.current_playback()
        if new_playback and new_playback.get("item"):
            new_id = new_playback["item"]["id"]
            print(f"ℹ️ Yeni şarkı id: {new_id}")
            if new_id == track_id:
                print("⚠️ Uyarı: Şarkı id aynı, next_track işe yaramamış olabilir.")

except Exception as e:
    print(f"\n❌ BİR HATA OLUŞTU: {e}")

finally:
    print("\n💾 Toplanan veriler 'sonuclar.json' dosyasına yazılıyor...")
    with open("sonuclar.json", "w", encoding="utf-8") as f:
        json.dump(collected_data, f, ensure_ascii=False, indent=4)
    print("🏁 İŞLEM TAMAMLANDI! 'sonuclar.json' dosyasını kontrol et.")
