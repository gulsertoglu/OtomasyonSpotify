from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

try:
    # Chrome Sürücüsünü otomatik olarak indirip ayarlıyoruz.
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Gitmek istediğin web sitesi
    driver.get("https://www.google.com")
    print(f"Başlık: {driver.title}")

    # 5 saniye bekleyip tarayıcıyı kapat
    time.sleep(5)

except Exception as e:
    print(f"Bir hata oluştu: {e}")

finally:
    if 'driver' in locals() and driver:
        driver.quit()