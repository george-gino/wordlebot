import random
import ast
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        words = ast.literal_eval(file.read())
    return words

def get_feedback(guess, solution):
    feedback = [''] * 5
    solution_chars = list(solution)
    
    for i in range(5):
        if guess[i] == solution[i]:
            feedback[i] = 'green'
            solution_chars[i] = ''
    
    for i in range(5):
        if feedback[i] == '':
            if guess[i] in solution_chars:
                feedback[i] = 'yellow'
                solution_chars[solution_chars.index(guess[i])] = ''
            else:
                feedback[i] = 'gray'
    
    return feedback

def filter_words(word_list, guess, feedback):
    filtered_words = []
    
    for word in word_list:
        match = True
        word_chars = list(word)
        
        for i in range(5):
            if feedback[i] == 'green' and guess[i] != word[i]:
                match = False
                break
            if feedback[i] == 'yellow':
                if guess[i] == word[i] or guess[i] not in word_chars:
                    match = False
                    break
            if feedback[i] == 'gray' and guess[i] in word_chars:
                match = False
                break
        
        if match:
            filtered_words.append(word)
    
    return filtered_words

def read_feedback_from_webpage(driver, attempt_number):
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, '.Row-module_row__pwpBq')
        current_row = rows[attempt_number]
        
        tiles = current_row.find_elements(By.CSS_SELECTOR, '.Tile-module_tile__UWEHN')
        
        feedback = []
        for tile in tiles:
            state = tile.get_attribute('data-state')
            print(f"Tile state: {state}") 
            
            if state == 'correct':
                feedback.append('green')
            elif state == 'present':
                feedback.append('yellow')
            elif state == 'absent':
                feedback.append('gray')
            else:
                feedback.append('')
        
        return feedback
    except Exception as e:
        print(f"An error occurred while reading feedback: {e}")
        return [''] * 5  

def solve_wordle(word_list, selenium_driver):
    possible_words = word_list[:]
    guess = "crane"  # Starting with a common first guess
    attempts = 0
    
    while attempts < 6:
        attempts += 1
        print(f"Attempt {attempts}: Guessing '{guess}'")

        body = WebDriverWait(selenium_driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        body.click()  
        for letter in guess:
            body.send_keys(letter)
            time.sleep(0.1)
        body.send_keys(Keys.ENTER)
        time.sleep(2)  

        feedback = read_feedback_from_webpage(selenium_driver, attempts - 1)
        print(f"Feedback: {feedback}")

        if feedback == ['green'] * 5:
            print(f"Solved! The word is '{guess}'")
            return

        possible_words = filter_words(possible_words, guess, feedback)
        guess = random.choice(possible_words)
    
    print("Failed to solve the Wordle within 6 attempts")

 
