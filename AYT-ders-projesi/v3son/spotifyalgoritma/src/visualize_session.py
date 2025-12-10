import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def load_session(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



# TÜR DAĞILIMI


def plot_genre_distribution(tracks):
    all_genres = []
    for t in tracks:
        genres = t.get("artist_genres_main", [])
        if genres:
            all_genres.extend(genres)

    if not all_genres:
        print("Bu session'da genre datası yok.")
        return

    counter = Counter(all_genres)
    labels = list(counter.keys())
    values = list(counter.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.title("Tür Dağılımı (Genre Distribution)")
    plt.xlabel("Tür")
    plt.ylabel("Frekans")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()



# POPÜLARİTE ÇİZGİSİ


def plot_popularity_trend(tracks):
    popularity = [t.get("popularity", 0) for t in tracks]
    names = [t["name"] for t in tracks]

    plt.figure(figsize=(10, 5))
    plt.plot(range(len(tracks)), popularity, marker="o")
    plt.title("Popularity Trend")
    plt.xlabel("Şarkı Sırası")
    plt.ylabel("Popularity")
    plt.xticks(range(len(tracks)), names, rotation=45, ha="right")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



# 3) ISI HARİTASI

def jaccard(set1, set2):
    if not set1 and not set2:
        return 1.0
    return len(set(set1) & set(set2)) / len(set(set1) | set(set2))


def plot_genre_similarity(tracks):
    names = [t["name"] for t in tracks]
    genres = [t.get("artist_genres_main", []) for t in tracks]

    n = len(tracks)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            matrix[i][j] = jaccard(genres[i], genres[j])

    plt.figure(figsize=(8, 7))
    plt.imshow(matrix, cmap="viridis")
    plt.colorbar(label="Genre Similarity (Jaccard)")
    plt.xticks(range(n), names, rotation=45, ha="right")
    plt.yticks(range(n), names)
    plt.title("Genre Similarity Heatmap")
    plt.tight_layout()
    plt.show()


# Komut

if __name__ == "__main__":
    path = input("Session JSON gir (data/sessions/...): ").strip()

    session = load_session(path)
    tracks = session["tracks"]

    print("Grafikler oluşturuluyor...\n")

    plot_genre_distribution(tracks)
    plot_popularity_trend(tracks)
    plot_genre_similarity(tracks)

    print("\nSon")
