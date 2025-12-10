import json
import os
import re
from pathlib import Path
from datetime import datetime

import requests  # Ollama'ya HTTP istek atmak için


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"  # 'llama3' kullanmak istersen burayı değiştir


def ask_local_ai(prompt: str) -> str:
    """
    Ollama üzerinde çalışan yerel LLM'e (mistral) istek atar.
    Gerçek AI analizi burada üretiliyor.
    """
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["response"]


def analyze_session_json(json_path: str, out_dir: str = "data/analysis") -> str:
    # Oturum JSON'unu oku
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tracks = data["tracks"]
    if not tracks:
        raise ValueError("JSON içinde hiç parça yok.")

    seed = tracks[0]

    # LLM için prompt (TÜRKÇE)
    prompt = f"""
Sen bir müzik öneri sistemi analisti olarak çalışıyorsun.

Spotify'da otomatik çalma / radyo ile kaydedilmiş bir oturum veriyorum.
Şarkılar sırayla şöyle:

BAŞLANGIÇ (SEED) ŞARKI:
- {seed['name']} - {', '.join(seed['artists'])}
  Türler (artist_genres_main): {seed.get('artist_genres_main')}
  Popülerlik: {seed.get('popularity')}

DEVAMI GELEN ÖNERİLER:
"""

    for i, t in enumerate(tracks[1:], start=1):
        prompt += f"""
{i}. {t['name']} – {', '.join(t['artists'])}
   Türler (artist_genres_main): {t.get('artist_genres_main')}
   Popülerlik: {t.get('popularity')}
"""

    prompt += """
GÖREVİN:

1. Önerilerin seed şarkıyla ne kadar alakalı olduğunu analiz et.
   - Tür (genre) benzerliği
   - Sanatçı / sahne / dönem yakınlığı
   - Genel hava / ruh hali (mutsuz, enerjik, sakin vb.)
   - Popülerlik ve “mainstream” seviyesi

2. Genel öneri kalitesine 0 ile 100 arasında bir puan ver.
   - 0: Tamamen alakasız, saçma öneriler
   - 100: Seed şarkının ruhunu mükemmel yakalayan öneriler

3. Puan verirken kısaca ama net bir şekilde nedenlerini açıkla.
   - Güçlü yanlar
   - Zayıf yanlar

4. CEVABI TÜRKÇE YAZ.
   Sonda mutlaka şu formatta bir satır ekle:
   "GENEL PUAN: X/100"
"""

    # Yerel AI'dan analiz al
    analysis_text = ask_local_ai(prompt)

    # GENEL PUAN satırından sayıyı çek
    match = re.search(r"GENEL PUAN:\s*(\d+)\s*/\s*100", analysis_text)
    score = int(match.group(1)) if match else None

    # Kayıt klasörü
    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = Path(json_path).stem

    # 1) JSON çıktısı
    json_out_path = out_dir_path / f"analysis_{ts}_{base_name}.json"
    analysis_payload = {
        "session_file": json_path,
        "created_at": datetime.now().isoformat(),
        "model": f"ollama:{MODEL_NAME}",
        "score": score,
        "analysis_text": analysis_text,
    }
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(analysis_payload, f, ensure_ascii=False, indent=2)

    # 2) Okunabilir .md çıktısı
    md_out_path = out_dir_path / f"analysis_{ts}_{base_name}.md"
    with open(md_out_path, "w", encoding="utf-8") as f:
        f.write(analysis_text)

    return str(json_out_path)


if __name__ == "__main__":
    path = input("Analiz edilecek oturum JSON yolu: ").strip()
    out_file = analyze_session_json(path)
    print("\n--- YEREL LLM ANALİZİ KAYDEDİLDİ ---")
    print(out_file)
    print("(Aynı isimle bir de .md dosyası oluşturuldu)")
