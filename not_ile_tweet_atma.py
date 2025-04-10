import os
import time
from datetime import datetime
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By

DOSYA_ADI = "notlar.txt"
CHROMEDRIVER_PATH = "chromedriver.exe"  # ChromeDriver yolunu burada ayarla

def not_ekle():
    not_metni = input("Yeni notunuzu yazın: ")
    with open(DOSYA_ADI, "a", encoding="utf-8") as dosya:
        dosya.write(not_metni + "\n")
    print("✅ Not kaydedildi.\n")

def notlari_goster():
    if not os.path.exists(DOSYA_ADI):
        print("📂 Henüz hiç not eklenmemiş.\n")
        return
    print("\n📓 Kayıtlı Notlar:")
    with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
        for i, satir in enumerate(dosya, start=1):
            print(f"{i}. {satir.strip()}")
    print()

def tweet_at(not_metni):
    print(f"📤 Tweet atma işlemi başlatılıyor: '{not_metni}'")

    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=C:\\Users\\xx\\AppData\\Local\\Google\\Chrome\\User Data")  # Profil yolunu kendi bilgisayarına göre düzenlemen gerekli
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

    try:
        driver.get("https://twitter.com/home")
        time.sleep(5)

        tweet_kutusu = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Tweet metni']")
        tweet_kutusu.send_keys(not_metni)

        tweetle_butonu = driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']")
        tweetle_butonu.click()

        print("✅ Tweet başarıyla atıldı.")
    except Exception as e:
        print("❌ Tweet atılamadı:", e)
    finally:
        time.sleep(3)
        driver.quit()

def zamanli_tweet_ayarla():
    if not os.path.exists(DOSYA_ADI):
        print("⚠️ Önce bir not eklemelisin.\n")
        return

    with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
        ilk_satir = dosya.readline().strip()

    if not ilk_satir:
        print("⚠️ 1. satır boş, tweet atılamaz.\n")
        return

    saat = input("Tweet atılacak saati gir (örn: 14:30): ").strip()

    def gorev():
        tweet_at(ilk_satir)

    schedule.every().day.at(saat).do(gorev)
    print(f"⏰ {saat} saatinde tweet atılmak üzere zamanlandı: '{ilk_satir}'\n")

    print("🕒 Zamanlayıcı çalışıyor. Ctrl + C ile iptal edebilirsin.\n")
    while True:
        schedule.run_pending()
        time.sleep(1)

def uygulamayi_baslat():
    print("📝 Not Defteri Uygulamasına Hoş Geldin!\n")

    while True:
        print("Seçenekler:")
        print("1 - Not Ekle")
        print("2 - Notları Göster")
        print("3 - 1. satırı belirli saatte tweet at")
        print("4 - Çıkış\n")
        secim = input("Seçiminiz (1/2/3/4): ").strip()

        if secim == "1":
            not_ekle()
        elif secim == "2":
            notlari_goster()
        elif secim == "3":
            zamanli_tweet_ayarla()
        elif secim == "4":
            print("👋 Güle güle!")
            break
        else:
            print("⚠️ Geçersiz seçim, lütfen 1-4 arasında bir sayı girin.\n")

if __name__ == "__main__":
    uygulamayi_baslat()
