# src/scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_EMAIL =os.getenv("DISCORD_EMAIL")
DISCORD_PASSWORD=os.getenv("DISCORD_PASSWORD")
DISCORD_CHANNEL_URL =os.getenv("DISCORD_CHANNEL_URL")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
CSV_PATH =os.getenv("CSV_PATH")


def run_scraper():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("https://discord.com/login")
        wait = WebDriverWait(driver, 20)
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys(DISCORD_EMAIL)
        password_field.send_keys(DISCORD_PASSWORD)
        password_field.send_keys(Keys.RETURN)

        time.sleep(10)
        driver.get(DISCORD_CHANNEL_URL)
        time.sleep(10)
        wait = WebDriverWait(driver, 15)

        message_area = driver.find_element(By.CLASS_NAME, "scrollerInner__36d07")
        wait = WebDriverWait(driver, 15)

        previous_count = 0
        same_count_times = 0
        all_data = []

        while same_count_times < 5:
            message_area.send_keys(Keys.HOME)
            time.sleep(3)

            messages_blocks = driver.find_elements(By.XPATH, "//li[contains(@class, 'messageListItem')]")
            current_count = len(messages_blocks)

            for block in messages_blocks:
                try:
                    auteur = block.find_element(By.XPATH, ".//span[contains(@class, 'username')]").text
                except:
                    auteur = "Inconnu"

                try:
                    texte = block.find_element(By.XPATH, ".//div[contains(@class, 'messageContent')]").text
                except:
                    texte = ""

                try:
                    emoji_img = block.find_element(By.XPATH, ".//img[contains(@class, 'emoji')]")
                    emoji = emoji_img.get_attribute("aria-label") or emoji_img.get_attribute("alt")
                except:
                    emoji = ""

                try:
                    date = block.find_element(By.XPATH, ".//span[contains(@class, 'timestamp')]//time").get_attribute("aria-label")
                except:
                    date = "Inconnu"

                all_data.append((auteur, texte, emoji, date))

            print(f"🔄 Scroll... {current_count} visibles, {len(all_data)} totaux")

            if current_count == previous_count:
                same_count_times += 1
            else:
                same_count_times = 0
                previous_count = current_count

            with open(CSV_PATH, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Auteur", "Message", "Emoji", "Date"])
                writer.writerows(all_data)

            print("\n✅ Messages sauvegardés dans :", CSV_PATH)

    except TimeoutException:
        print("⛔ Timeout — Zone de messages introuvable.")

    finally:
        driver.quit()