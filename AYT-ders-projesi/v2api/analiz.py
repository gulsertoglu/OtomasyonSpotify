import google.generativeai as genai
import json
import os

# --- 1. AYARLAR ---
# Google AI Studio'dan aldığın anahtarı buraya yapıştır
GOOGLE_API_KEY = "AIzaSyAzqQkulrRnMaUUMihCxxzIEziERHaFX_U"

# Ayarları yap
genai.configure(api_key=GOOGLE_API_KEY)

# Modeli seç (Gemini 1.5 Flash hızlı ve bedavadır)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 2. JSON DOSYASINI OKU ---
try:
    with open('sonuclar.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"{len(data)} adet şarkı verisi yüklendi.")
except FileNotFoundError:
    print("'sonuclar.json' bulunamadı! Önce algoritma.py'yi çalıştırıp veri topla.")
    exit()

# --- 3. GEMINI İÇİN MESAJI HAZIRLA (PROMPT) ---
# Gemini'ye şarkı listesini metin olarak vereceğiz.
sarki_listesi_str = ""
for item in data:
    sarki_listesi_str += f"{item['sira']}. {item['sarki_adi']} - {item['sanatci']} (Popülerlik: {item['populerlik']})\n"

prompt = f"""
Sen uzman bir müzikoloğsun ve algoritmaları denetliyorsun.
Aşağıda bir kullanıcının Spotify'da dinlediği şarkıların sırası var.
İlk şarkı kullanıcı tarafından seçildi, geri kalanlar Spotify'ın otomatik önerisiyle (Autoplay/Radio) geldi.

LÜTFEN ŞUNLARI ANALİZ ET:
1. Tür Uyumu: Şarkılar birbiriyle aynı veya uyumlu türlerde mi?
2. Akış (Vibe): Şarkıların modu (hüzünlü, hareketli, sert vb.) birbiriyle tutarlı mı?
3. Kopukluklar: Listede "Ne alaka?" dedirten çok saçma bir geçiş var mı?

İŞTE LİSTE:
{sarki_listesi_str}

ÇIKTI OLARAK BANA SADECE ŞUNU VER (JSON FORMATINDA):
{{
  "dogruluk_puani": (0 ile 100 arası bir sayı),
  "analiz_ozeti": "(Kısa bir paragraf yorum)",
  "uyumsuz_sarkilar": ["(Varsa uyumsuz şarkı adları)"]
}}
"""

# --- 4. GEMINI'YE GÖNDER VE SONUCU AL ---
print("Gemini şarkıları analiz ediyor... Lütfen bekle...")

try:
    response = model.generate_content(prompt)
    
    # Gelen cevabı temizle (Bazen markdown ```json falan ekliyor)
    cevap_text = response.text.replace("```json", "").replace("```", "").strip()
    
    # Sonucu ekrana bas
    print("\n" + "="*40)
    print("ANALİZ SONUCU")
    print("="*40)
    print(cevap_text)
    print("="*40)
    
    # İstersen bunu da bir dosyaya kaydet
    with open('analiz_sonucu.json', 'w', encoding='utf-8') as f:
        f.write(cevap_text)
        
except Exception as e:
    print(f"Gemini Hatası: {e}")