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
# Demander à l'utilisateur s'il veut activer le mode headless
headless_choice = input("Voulez-vous activer le mode headless ? (oui/non) : ").strip().lower()

if headless_choice in ['oui', 'yes', 'y']:
    # Activer le mode headless si l'utilisateur choisit oui
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")  # Définit une taille d'écran
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")  # Nécessaire dans certains environnements Linux
    options.add_argument("--disable-dev-shm-usage")  # Évite les problèmes de mémoire partagée
    print("Mode headless activé.")
else:
    print("Mode headless désactivé. Une fenêtre de navigateur s'ouvrira.")



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
            time.sleep(1)

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
                recent_messages = rows[-25:] if len(rows) > 25 else rows

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
                    chat_history.insert(0, {"role": "system", "content": "Tu n’es pas une IA. Pas de style robotique ni de phrases rigides. C’est une discussion par SMS entre potes, donc reste naturel et fluide. Parle simplement, comme si tu répondais à un ami, avec un ton décontracté mais jamais négligé. Tes réponses doivent être courtes, claires, parfois drôles ou pleines de second degré, mais toujours adaptées à la situation. Tu peux être sérieux si le sujet l’exige, mais garde toujours une vibe détendue. Tu t’appelles Imrane, ton numéro c’est 0780391078, et tu te comportes comme un vrai pote nommé Imrane. Tes réponses doivent refléter une vraie personnalité : un mec sympa, qui écoute, qui a de l’humour mais sait être pertinent. Pas de markdown, pas d’émoticônes, juste des phrases qui coulent comme dans une vraie conversation. Adapte ton style en fonction de la personne en face, mais toujours avec naturel et spontanéité."})

                    # Réponse générée par OpenAI
                    print()
                    print(f"Prompt : {chat_history}")
                    print()
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=chat_history
                    )
                    ai_response = response.choices[0].message.content
                    print()
                    print(f"Réponse : {ai_response}")
                    print()

                    # Envoi de la réponse sur WhatsApp
                    try:
                        message_box = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
                        ))
                        message_box.click()
                        # Écrire chaque lettre individuellement avec un délai
                        for char in ai_response:
                            if char.lower() == '\n':  # Vérifie les retours à la ligne
                                continue
                            message_box.send_keys(char)

                        # Appuyer sur Entrée après avoir écrit le message
                        message_box.send_keys(Keys.ENTER)
                        print("Message envoyé avec succès.")
                        # Localiser et cliquer sur le bouton avec CSS Selector
                        menu_button = driver.find_element(By.XPATH, "(//div[@role='button' and @aria-label='Menu' and @title='Menu'])[2]")
                        time.sleep(0.0001)
                        menu_button.click()

                        button = driver.find_element(By.XPATH, "//div[contains(text(), 'Fermer la discussion')]")
                        time.sleep(0.0001)

                        button.click()
                        print("Fermeture du chat..")
                        time.sleep(0.8)

                    except Exception as e:
                        print(f"Erreur lors de l'envoi : {e}")
                else:
                    print("Message vide, aucune réponse générée.")

        except Exception as e:
            print(f"Aucune conversation non lue, attente...")

        time.sleep(0.25)  # Pause entre chaque vérification

except KeyboardInterrupt:
    print("Script interrompu par l'utilisateur.")

finally:
    print("Fermeture du navigateur...")
    driver.quit()
    print("Script terminé.")
