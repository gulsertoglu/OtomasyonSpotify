from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
import time
from dotenv import load_dotenv
import os
import random
import pickle

SPOTIFY_URL = "https://www.spotify.com/"
CEREZ_KABUL_XPATH = "//button[contains(text(), 'Kabul ediyorum') or contains(text(), 'Accept') or contains(@title, 'Accept')]"
BEKLEME_SURESI = 10 
COOKIE_FILE = "spotify_cookies.pkl"

def type_like_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

driver = None
try:
    driver = webdriver.Chrome()
    driver.maximize_window()
    print(f" {SPOTIFY_URL} adresine gidiliyor")
    driver.get(SPOTIFY_URL)
    
    try:
        print("Çerez butonunun yüklenmesi bekleniyor")
        cerez_butonu = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, CEREZ_KABUL_XPATH))
        )
        time.sleep(random.uniform(0.5, 1.0))
        cerez_butonu.click()
        print(" Çerezler başarıyla kabul edildi/kapatıldı.")
    except TimeoutException:
        print("Çerez butonu bulunamadı (Muhtemelen daha önce kabul edilmiş).")
    except Exception as e:
        print(f"Çerez hatası: {e}")

    if os.path.exists(COOKIE_FILE):
        print("\nOturum çerez dosyası bulundu, yükleniyor...")
        cookies = pickle.load(open(COOKIE_FILE, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        print("Çerezler yüklendi, giriş yapılmış olmalı.")
        time.sleep(random.uniform(2.5, 3.5))
    else:
        print("\n--- OTURUM ÇEREZİ BULUNAMADI, OTOMATİK GİRİŞ BAŞLATILIYOR ---")
        load_dotenv()
        KULLANICI_ADI = os.environ.get("SPOTIFY_USERNAME")
        SIFRE = os.environ.get("SPOTIFY_PASSWORD")
        
        GIRIS_LOCATOR = (By.XPATH, "//*[text()='Oturum aç' or text()='Log in']") 
        KULLANICI_LOCATOR = (By.XPATH, "//*[@id='username']") 
        SIFRE_LOCATOR = (By.XPATH, "//*[@id='password']")
        DEVAM_BUTONU_LOCATOR = (By.XPATH, "//button[@data-testid='login-button' or @data-testid='main-login-button']")
        KOD_ATLAMA_LOCATOR = (By.XPATH, "//*[text()='Parola ile oturum aç']")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(GIRIS_LOCATOR)).click()
        time.sleep(random.uniform(1.0, 1.5))

        kullanici_alan_elementi = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(KULLANICI_LOCATOR) 
        )
        type_like_human(kullanici_alan_elementi, KULLANICI_ADI)
        time.sleep(random.uniform(0.5, 1.0)) 

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(DEVAM_BUTONU_LOCATOR)).click()
        time.sleep(random.uniform(1.0, 1.5))

        try:
            print("'Parola ile oturum aç' linki aranıyor...")
            kod_atlama_elementi = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(KOD_ATLAMA_LOCATOR))
            time.sleep(random.uniform(0.5, 1.0))
            kod_atlama_elementi.click()
            print("'Parola ile oturum aç' linkine tıklandı.")
        except TimeoutException:
            print("Mail doğrulama ekranı çıkmadı, parola ekranı bekleniyor.")
            pass

        time.sleep(random.uniform(0.5, 1.0))
        sifre_alan_elementi = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(SIFRE_LOCATOR) 
        )
        type_like_human(sifre_alan_elementi, SIFRE)
        time.sleep(random.uniform(0.5, 1.0))

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(DEVAM_BUTONU_LOCATOR)).click()
        print("Başarıyla giriş yapıldı.")
        time.sleep(random.uniform(3.0, 4.0))
        
        print("Giriş çerezleri 'spotify_cookies.pkl' dosyasına kaydediliyor...")
        pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))
        print("Çerezler kaydedildi.")

    print("\n--- ARAMA VE ÇALMA İŞLEMİ BAŞLADI ---")
    SEARCH_BUTTON_LOCATOR = (By.XPATH, "//a[@href='/search']") 
    SEARCH_INPUT_LOCATOR = (By.XPATH, "//input[@data-testid='search-input']")
    SARKI_ADI = "Ne Farkeder?"
    SANATCI_ADI = "Pickpocket"
    satir_LOCATOR = "//div[@data-testid='tracklist-row']"

    def tam_eslesen_sarki_xpath(sarki_adi):
        return f"{satir_LOCATOR}//div/a[text()='{SARKI_ADI}']"

    print("Arama butonuna tıklanıyor...")
    arama_butonu = WebDriverWait(driver, BEKLEME_SURESI).until(
        EC.element_to_be_clickable(SEARCH_BUTTON_LOCATOR)
    )
    time.sleep(random.uniform(0.5, 1.0))
    arama_butonu.click()
    print("Arama sayfasına geçildi.")
    time.sleep(random.uniform(1.0, 1.5)) 
    
    print(f" '{SARKI_ADI}' aratılıyor...")
    arama_cubugu = WebDriverWait(driver, BEKLEME_SURESI).until(
        EC.presence_of_element_located(SEARCH_INPUT_LOCATOR)
    )
    arama_cubugu.clear()
    type_like_human(arama_cubugu, SARKI_ADI + Keys.ENTER)
    print("Arama tamamlandı.")
    
    time.sleep(random.uniform(2.0, 3.0))
    sarki_adi_elementi = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, tam_eslesen_sarki_xpath(SARKI_ADI)))
    )
    print(f" '{SARKI_ADI}' şarkısı arama sonuçlarında bulundu.")

    sarki_satiri = sarki_adi_elementi.find_element(By.XPATH, f"ancestor::{satir_LOCATOR[2:]}")
    oynat_dugmesi = sarki_satiri.find_element(By.XPATH, ".//button[@data-testid='play-button']")
    
    print(f"Tam eşleşen '{SARKI_ADI}' şarkısındaki oynat düğmesine tıklanıyor...")
    time.sleep(random.uniform(0.5, 1.0))
    oynat_dugmesi.click()
    print(f" Şarkı '{SARKI_ADI}' oynatılıyor.")

except Exception as e:
    print(f"\nBeklenmeyen bir ana hata oluştu: {e}")

finally:
    print("\n--- İşlem Bitti ---")
    print("Script 1 saat açık kalacak...")
    time.sleep(3600)
    if driver:
        driver.quit()