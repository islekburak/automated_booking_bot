import schedule
import time
from selenium import webdriver
import requests
from pydub import AudioSegment
import speech_recognition as sr
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DriverPath = "drivers/chrome/117.0.5938.88/chromedriver"
url = "http://online.spor.istanbul/uyegiris"
txtTCPasaport = "xxx"
txtSifre = "yyy"

def online_randevu():
    options = Options()
    options.add_experimental_option("detach", True)
    service = Service (DriverPath)
    driver = webdriver.Chrome(service=service, options= options)

    driver.get(url)
    driver.set_window_size(1024, 600)
    driver.maximize_window()

    #site = driver.current_url
    #print(site)
    #driver.close()
    #driver.quit()

    driver.find_element(by="id",value="txtTCPasaport" ).send_keys(txtTCPasaport)
    driver.find_element(by="id",value="txtSifre" ).send_keys(txtSifre)
    driver.find_element(by="name",value="btnGirisYap" ).click()
    driver.find_element(by="xpath",value="/html/body/form/div[3]/div[2]/div/div/ul/li[1]").click()


    #fitness
    driver.find_element(by="id",value="pageContent_rptListe_lbtnSeansSecim_1" ).click()

    #yüzme
    #driver.find_element(by="id",value="pageContent_rptListe_lbtnSeansSecim_0" ).click()

    # Salı = pageContent_rptList_ChildRepeater_1_cboxSeans_0
    # Perşembe = pageContent_rptList_ChildRepeater_3_cboxSeans_0
    # Cumartesi = pageContent_rptList_ChildRepeater_5_cboxSeans_0

    # scroll down 1000 pixels
    driver.execute_script('window.scrollBy(0, 300)')
    # wait for page to load
    time.sleep(2)

    driver.find_element(by="id", value="pageContent_rptList_ChildRepeater_1_cboxSeans_0").click()
    time.sleep(5)
    driver.find_element(by="id", value="pageContent_cboxOnay").click()
    time.sleep(2)


    # Switch to the iframe containing reCAPTCHA
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    time.sleep(2)
    # Now locate the reCAPTCHA checkbox or element
    recaptcha_checkbox = driver.find_element(By.CSS_SELECTOR ,"[id^='recaptcha-anchor']")
    recaptcha_checkbox.click()
    time.sleep(20)
    driver.switch_to.default_content()
    time.sleep(2)


    recaptcha_content_iframe = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/iframe")
    driver.switch_to.frame(recaptcha_content_iframe)

    driver.find_element(By.XPATH, '//*[@id="recaptcha-audio-button"]').click()
    time.sleep(2)


    recaptcha_link = driver.find_element(By.XPATH, '//*[@id="rc-audio"]/div[7]/a').get_attribute("href")

    r=requests.get(f"{recaptcha_link}")
    with open("sound.mp3","wb") as f:
        f.write(r.content)

    sound= AudioSegment.from_mp3("sound.mp3")
    sound.export("sound.wav",format="wav")
    time.sleep(2)

    data = sr.Recognizer()
    captcha_audio = sr.AudioFile("sound.wav")
    with captcha_audio as source:
        audio = data.record(captcha_audio)
        captcha_text = data.recognize_google(audio, language="en-US")
    driver.find_element(By.XPATH, '//*[@id="audio-response"]').send_keys(captcha_text)
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="recaptcha-verify-button"]').click()

    driver.switch_to.default_content()
    time.sleep(3)
    driver.find_element(by="id", value="lbtnKaydet").click()
    time.sleep(3)
    driver.quit()

# Pazartesi, Perşembe ve Cumartesi günleri saat 07:00'da çalıştırın
#schedule.every(3).days.at("10:00").do(online_randevu)
#schedule.every().monday.at("07:00").do(online_randevu)
#schedule.every().thursday.at("14:19").do(online_randevu)
schedule.every().saturday.at("11:48").do(online_randevu)

while True:
    schedule.run_pending()
    time.sleep(60)  # Her 30 dakikada bir kontrol et
    time.sleep(1)