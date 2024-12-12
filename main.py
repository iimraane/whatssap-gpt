# Importation des bibliothèques nécessaires
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openai import OpenAI
import os

# Initialisation de la clé API OpenAI
OPENAI_API_KEY = "YOUR KEY HERE"
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuration des options du navigateur Chrome
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Temp\\chrome-data")

# Initialisation du driver Selenium
driver = webdriver.Chrome(options=options)

try:
    print("Démarrage du script...")

    # Accès à WhatsApp Web
    driver.get("https://web.whatsapp.com")
    print("Veuillez scanner le QR code pour continuer...")
    time.sleep(20)  # Attente pour la connexion manuelle

    # Dictionnaire pour suivre les derniers messages lus
    last_messages = {}

    # Localiser l'élément avec le texte "Non lues"
    button = driver.find_element(By.XPATH, "//div[contains(text(), 'Non lues')]")
    button.click()
    print("Bouton 'non-lu' cliqué")

    while True:
        print("Recherche des conversations non lues...")

        try:
            unread_chat = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='gridcell'][aria-colindex='2']._ak8o"))
            )
            unread_chat.click()
            print("Premier chat non lu cliqué avec succès.")
            
            # Ouverture de la conversation non lue
            time.sleep(2)

            # Chargement des messages de la conversation
            print("Chargement des messages...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'message-in') or contains(@class, 'message-out')]")
            ))

            # Récupération des messages entrants
            rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]")

            if rows:
               # Récupération des 10 derniers messages entrants
                rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]")
                recent_messages = rows[-20:] if len(rows) > 10 else rows

                chat_history = []
                for row in recent_messages:
                    text_elements = row.find_elements(By.XPATH, ".//span[@class and @dir='ltr']")
                    message_text = " ".join([el.text for el in text_elements if el.text])

                    metadata_element = row.find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]")
                    timestamp_author = metadata_element.get_attribute("data-pre-plain-text")
                    timestamp = timestamp_author.split(']')[0].replace('[', '').strip()
                    author = timestamp_author.split(']')[-1].split(':')[0].strip()

                    chat_history.append({"role": "user", "content": f"{timestamp} - {author} : {message_text}"})

                # Identifier la conversation actuelle
                conversation_id = driver.current_url

                # Vérification de la nouveauté du message
                if conversation_id not in last_messages or last_messages[conversation_id] != chat_history:
                    print(f"Historique des messages : {chat_history}")
                    last_messages[conversation_id] = chat_history

                    print("Génération de la réponse avec OpenAI...")
                    chat_history.insert(0, {"role": "system", "content": " N'ecrit pas les horodtatage et les noms, juste ta reponse, Ceci est une conversation SMS. Tu dois te comporter comme un humain, avec des réponses courtes, simples et naturelles, comme un pote chill et décontracté. Pas de markdown, pas d'emojis, juste du naturel, avec un ton léger mais sérieux quand il le faut. Reste spontané, comme dans une vraie discussion entre potes. Tu t'appelles Imrane et ton numero de telephone c'est 0780391078 et comporte toi comme un Imrane, n'ecrit pas les horodtatage et les noms, juste ta reponse"})

                    # Réponse générée par OpenAI
                    print(f"Prompt : {chat_history}")
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=chat_history
                    )
                    ai_response = response.choices[0].message.content
                    print(f"Réponse : {ai_response}")

                    # Envoi de la réponse sur WhatsApp
                    try:
                        message_box = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
                        ))
                        message_box.click()
                        message_box.send_keys(ai_response)
                        message_box.send_keys(Keys.ENTER)
                        print("Message envoyé avec succès.")
                        # Localiser et cliquer sur le bouton avec CSS Selector
                        menu_button = driver.find_element(By.XPATH, "(//div[@role='button' and @aria-label='Menu' and @title='Menu'])[2]")
                        menu_button.click()

                        button = driver.find_element(By.XPATH, "//div[contains(text(), 'Fermer la discussion')]")
                        button.click()
                        print("Fermeture du chat..")

                    except Exception as e:
                        print(f"Erreur lors de l'envoi : {e}")
                else:
                    print("Message vide, aucune réponse générée.")

        except Exception as e:
            print(f"Aucune conversation non lue, attente...")

        time.sleep(5)  # Pause entre chaque vérification

except KeyboardInterrupt:
    print("Script interrompu par l'utilisateur.")

finally:
    print("Fermeture du navigateur...")
    driver.quit()
    print("Script terminé.")
