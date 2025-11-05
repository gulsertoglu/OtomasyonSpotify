from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


SPOTIFY_URL = "https://www.spotify.com/"

CEREZ_KABUL_XPATH = "//button[contains(text(), 'Kabul ediyorum') or contains(text(), 'Accept') or contains(@title, 'Accept')]"
BEKLEME_SURESI = 10 


try:
    
    driver = webdriver.Chrome()
    
    driver.maximize_window()
    
    print(f" {SPOTIFY_URL} adresine gidiliyor")
    driver.get(SPOTIFY_URL)
    

    
    print("Çerez butonunun yüklenmesi bekleniyor")
    
    
    cerez_butonu = WebDriverWait(driver, BEKLEME_SURESI).until(
        EC.element_to_be_clickable((By.XPATH, CEREZ_KABUL_XPATH))
    )
    
    
    cerez_butonu.click()
    print(" Çerezler başarıyla kabul edildi/kapatıldı.")
    
    
    time.sleep(2) 
    
    
    print("\n Siteye Giriş ve Çerezler tamamlandı.")
    
except Exception as e:
    print("\n HATA OLUŞTU:")
    
    if "TimeoutException" in str(e):
        print("Çerez butonu belirlenen süre içinde bulunamadı.")
    else:
        print(f"Beklenmeyen bir hata oluştu: {e}")

finally:
     time.sleep(5) 
     #driver.quit()
    
