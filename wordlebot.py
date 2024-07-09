from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

from wordle_solver import load_word_list, get_feedback, filter_words, solve_wordle

chromedriver_path = '/opt/homebrew/bin/chromedriver'
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service)
driver.get('https://www.nytimes.com/games/wordle/index.html')

wait = WebDriverWait(driver, 20)

try:
    # Click the play button
    play_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Play")]')))
    print("Play button found")
    play_button.click()
    time.sleep(2)

    # Click the 'X' button to close the pop-up
    close_ad_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]')))
    print("Close button found")
    close_ad_button.click()
    time.sleep(2)

    word_list = load_word_list('answers.txt')
    solve_wordle(word_list, driver)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()















