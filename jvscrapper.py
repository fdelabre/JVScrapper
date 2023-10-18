import requests
from bs4 import BeautifulSoup
import webbrowser

# Codes d'échappement ANSI pour les couleurs
COLOR_RED = '\033[91m'
COLOR_END = '\033[0m'

# URL de la page à analyser
url = 'https://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm'

# Envoi de la requête HTTP GET
response = requests.get(url)

# Vérification du statut de la réponse
if response.status_code == 200:
    # Extraction du contenu HTML
    html = response.text

    # Création de l'objet BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Recherche de tous les éléments avec la classe "topic-subject"
    topic_subject_elements = soup.find_all(class_='topic-subject')

    # Suppression du premier élément
    if topic_subject_elements:
        topic_subject_elements.pop(0)

    print("\n")

    # Affichage des éléments restants avec leurs liens
    for i, element in enumerate(topic_subject_elements, 1):
        text = element.text.strip()
        if text:
            print(f"{i}. {text}")

        # Recherche des éléments <a> dans le <span> courant
        link_elements = element.find_all('a')

        # Affichage des liens avec une couleur différente
        for link_element in link_elements:
            link = link_element.get('href')

    print("\n")

    # Demande à l'utilisateur de choisir un sujet
    choice = input("Ouvrir un sujet [Numéro] : ")
    choice = int(choice)

    # Vérification de la validité du choix
    if 1 <= choice <= len(topic_subject_elements):
        chosen_element = topic_subject_elements[choice - 1]
        link_element = chosen_element.find('a')
        link = link_element.get('href')
        if link:
            print(f"Ouverture du lien : {link}")
            # webbrowser.open('https://www.jeuxvideo.com'+link)

            # Envoi de la requête HTTP GET sur le lien saisi par l'utilisateur
            response = requests.get('https://www.jeuxvideo.com'+link)

            # Vérification du statut de la réponse
            if response.status_code == 200:
                # Extraction du contenu HTML de la nouvelle page
                html = response.text

                # Création de l'objet BeautifulSoup pour la nouvelle page
                soup = BeautifulSoup(html, 'html.parser')

                # Recherche de tous les éléments avec la classe "bloc-contenu"
                bloc_contenu_elements = soup.find_all(class_='bloc-contenu')

                # Affichage des contenus des classes "bloc-contenu" (sauf ceux entre 'blockquote-jv')
                for element in bloc_contenu_elements:
                    # Suppression du contenu entre la classe "blockquote-jv"
                    for blockquote_jv in element.find_all(class_='blockquote-jv'):
                        blockquote_jv.decompose()
                    for blockquote_jv in element.find_all(class_='info-edition-msg'):
                        blockquote_jv.decompose()

                    content = element.text.strip()
                    if content:
                        colored_msg = f"{COLOR_RED}MESSAGE : {COLOR_END}\n"
                        print(f"   {colored_msg}")
                        print(content)
            else:
                print(f"Échec de la requête. Statut : {response.status_code}")
        else:
            print("Le sujet sélectionné n'a pas de lien associé.")
    else:
        print("Choix invalide.")
else:
    print(f"Échec de la requête. Statut : {response.status_code}")

# Demande à l'utilisateur s'il souhaite se rendre sur la page
choice = input("Voulez-vous vous rendre sur la page ? (Oui/Non) ")

if choice.lower() == "o":
    webbrowser.open('https://www.jeuxvideo.com'+link)
