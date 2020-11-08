import requests
from bs4 import BeautifulSoup

def cercaMaterie(nomeFile, link):
    soup = BeautifulSoup(requests.get(link).content, "html.parser")
    try:
        pulsanteSubjects = soup.find_all('div', attrs={'id': 'div1'})[0]
        bottone = pulsanteSubjects.find_all('a')[0]
        indirizzo = "https://www.upv.es/" + bottone["href"]
        scriviCSV(nomeFile, indirizzo)
    except:
        pass


def scriviCSV(file, link):
    # ---------Inizializzazione----
    site = requests.get(link).content
    soup = BeautifulSoup(site, "html.parser")
    body = soup.find_all('iframe', attrs={'id': 'marco'})[0]
    # -----------------------------
    indirizzo = "https://www.upv.es" + str(body["src"])
    f = open(file, 'a')
    nome = soup.find_all('div', attrs={'id': 'banner_nombre'})[0].text
    nome = str(nome).replace(",", " -")
    print(nome)
    f.write(nome + "," + "" + "," + "" + "," + "" + "\n")

    site = requests.get(indirizzo).content
    soup = BeautifulSoup(site, 'html.parser')
    tables = soup.find_all('table', attrs={'class': 'upv_listacolumnas'})

    for tabella in tables[1:-1]:
        righe = tabella.tbody.find_all('tr')
        for riga in righe:
            colonne = riga.find_all("td")
            if colonne[-5].text == "B":
                code = colonne[0].text
                nomeInsegnamento = colonne[1].text
                nomeInsegnamento = str(nomeInsegnamento).replace(",", " -")
                webPage = "https://www.upv.es/pls/oalu/" + \
                    colonne[1].find_all('a')[0]["href"]
                crediti = colonne[-2].text
                crediti = str(crediti).replace(",", ".")

                f.write(code + "," + nomeInsegnamento +
                        "," + webPage + "," + crediti + "\n")
    f.close()
