import requests
from requests.auth import HTTPBasicAuth

#questi devono essere uguali a quelli del server :-)
USR = "NOME_UTENTE"
PWD = "PASSWORD"

#questo oggetto va passato come parametro ad ogni chiamata
basicauth = HTTPBasicAuth(USR, PWD)


#per ogni chiamata stampo il body (che contiene i risultati in formato json)
#e lo status code (esito dell'operazione)
#200: ok
#404: non trovato
#500: errore lato server

#lettura
def callGET(key=None):
    print("***** GET *****")
    if (key == None):
        getUrl = url
    else:
        getUrl = url + "/" + key
    print("url: " + getUrl)
    response = requests.get(getUrl, auth=basicauth)
    print("status code: " + str(response.status_code))
    #print(response.content)
    json = response.json()
    print("response content:")
    print(json)
    print("***************")
    print("")
    print("")
    print("")


#inserimento
def callPOST(obj):
    print("***** POST *****")
    print("url: " + url)

    headers={
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    response = requests.post(
        url, 
        json=obj,
        headers=headers, 
        auth=basicauth
    )
    print("status code: " + str(response.status_code))
    #print("response content:")
    #print(response.content)
    print("***************")
    print("")
    print("")
    print("")


#modifica
def callPUT(obj):
    print("***** PUT *****")
    print("url: " + url)

    headers={
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    response = requests.put(
        url, 
        json=obj,
        headers=headers, 
        auth=basicauth
    )
    print("status code: " + str(response.status_code))
    #print("response content:")
    #print(response.content)
    print("***************")
    print("")
    print("")
    print("")


#eliminazione
def callDELETE(nome):
    print("***** DELETE *****")
    deleteUrl = url + "/" + str(nome)
    print("url: " + deleteUrl)
    response = requests.delete(deleteUrl, auth=basicauth)
    print("status code: " + str(response.status_code))
    #print(response.content)
    print("***************")
    print("")
    print("")
    print("")



#l'indirizzo della chiamata (dal client) dipende da come è stato configurato il server
url = 'http://127.0.0.1:8080'


#lettura di tutto il contenuto della collection
callGET()

#lettura di un singolo document
callGET("budino")

#eliminazione di un document
callDELETE("panzerotto")
#lettura per vedere se il document è stato effettivamente eliminato
callGET()

#creazione nuovo document
callPOST({"nome": "caffe", "stato": "liquido", "calorie": 1, "gusto": "amaro"})
#lettura per vedere se il document è stato effettivamente creato
callGET("caffe")


#modifica document esistente
callPUT({"nome": "pizza", "stato": "solido", "calorie": 600, "gusto": "salato"})
#lettura per vedere se il document è stato effettivamente modificato
callGET("pizza")
