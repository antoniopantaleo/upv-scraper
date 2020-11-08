from bs4 import BeautifulSoup
import requests
import os
from functions import *

# ------------------------------------------------------------------------------------------------------------------
# Questo script salva sul disco files csv, uno per ogni BRANCA DI STUDI dell'Università
# Politecnica di Valencia, contenenti il nome degli insegnamenti, i codici, i link ed i
# CFU dei corsi di studio sostenuti nel secondo semestre (Anno accademico 2018/2019)
# Author: Antonio Pantaleo
# ------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    indirizzo = 'https://www.upv.es/estudios/posgrado/masteres-por-ramas-en.html'
    soup = BeautifulSoup(requests.get(indirizzo).content, 'html.parser')
    body = soup.find_all('div', attrs={'id': 'bqpr-grados'})[0].ul
    if "Results" not in os.listdir("."):
        os.mkdir("Results")
    os.chdir("Results")
    print("Attendere, mentre i files vengono scaricati.......")
    for li in body:
        try:
            nomeBranch = li.div.span.text.replace("Branch: ", "") + ".csv"
            with open(nomeBranch, 'w') as f:
                f.write("Code, Nome, Link, Crediti\n")
            listaInsegnamenti = li.ul
            for insegnamento in listaInsegnamenti:
                try:
                    link = "https://www.upv.es/" + insegnamento.a["href"]
                    cercaMaterie(nomeBranch, link)
                except:
                    continue
        except:
            continue
