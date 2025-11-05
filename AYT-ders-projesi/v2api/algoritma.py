# ANA PROJE KODUNUZDA KULLANIM (Artık her seferinde bunu yapacaksınız)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Bilgileriniz
YOUR_CLIENT_ID = "b751a8a9b2634be0bec840ce8fd6c048"
YOUR_CLIENT_SECRET = "d61c7100768f413fadee56dcafd91377"
YOUR_REDIRECT_URI = "http://127.0.0.1:8888"
scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

# Bu kod, otomatik olarak .cache dosyasını kontrol edecek.
# Geçerli bir token varsa onu kullanacak.
# Token'ın süresi dolmuşsa, 'refresh_token' kullanarak arka planda yenisini alacak.
# Sizin bir daha ASLA tarayıcı açıp giriş yapmanız gerekmeyecek.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=YOUR_CLIENT_ID,
    client_secret=YOUR_CLIENT_SECRET,
    redirect_uri=YOUR_REDIRECT_URI,
    scope=scope
))

# ARTIK HAZIRSINIZ!
# sp nesnesi ile tüm komutları gönderebilirsiniz.
# Örn: O an çalan şarkıyı getir
track = sp.current_user_playing_track()
if track:
    print(f"Şu an çalan şarkı: {track['item']['name']}")
else:
    print("Şu an bir şey çalmıyor.")