import cherrypy
import json
from pymongo import MongoClient

@cherrypy.expose
class MyController(object):
    records = [{"nome": "panzerotto", "stato": "solido", "calorie": 278, "gusto": "salato"},
               {"nome": "pizza", "stato": "solido", "calorie": 400, "gusto": "salato"},
                {"nome": "acqua", "stato": "liquido", "calorie": 0, "gusto": "neutro"},
                {"nome": "budino", "stato": "gelatinoso", "calorie": 150, "gusto": "dolce"}] #array che contiene i dati


    USR = "NOME_UTENTE"
    PWD = "PASSWORD"
    RLM = "NOME_APPLICAZIONE"

    #funzione di validazione delle credenziali inserite
    def validate_password(self, username, password):
        if (username == MyController.USR and password == MyController.PWD):
            return True
        else:
            return False

    #costruttore
    def __init__(self, url="mongodb://localhost:27017", db="MyDB", collection="Cibi"):
        #definisco delle variabili di istanza
        self.client = MongoClient(url)
        self.db = self.client[db]
        self.collection = self.db[collection]
        self.projection = {"_id": 0}
        #inizializzo i dati
        #cancello tutto
        self.collection.delete_many({})
        #inserimento
        self.collection.insert_many(MyController.records)

    #metodo per la lettura dei dati
    @cherrypy.tools.json_out() #NOTA: ricordarsi di aggiungere questo decoratore se vogliamo l'output in formato json!!!
    def GET(self, nome=""):
        #questa sarà la variabile che restituirà il metodo (contiene i dati selezionati)
        res = None
        try:
            filter = {}
            if nome != "":
                #caso della chiamata con parametro (singolo document)
                filter={ "nome": nome }
            res = list(self.collection.find(filter=filter, projection = self.projection))
            if len(res) == 1:
                res = res[0]
            #se passo il parametro e non viene trovato nulla devo cambiare lo status code della risposta 
            #(di default è 200)
            if nome!="" and len(res) == 0:
                cherrypy.response.status = 404
        except Exception as e:
            print(e)
        return res

    #metodo per l'inserimento un nuovo document
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        #data rappresenta l'oggetto che passo nel body della request
        data = cherrypy.request.json
        self.collection.insert_one(data)
        return 0


    #metodo per la modifica di un document
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    #@cherrypy.tools.accept(media='text/plain')
    def PUT(self):
        data = cherrypy.request.json #data è un dictionary -> per accedere alle sue proprietà utilizzo data["nome_proprietà"]
        #il primo parametro del metodo <collection>.update_one rappresenta il criterio (quali dati aggiornare)
        #il secondo contiene i campi da aggiornare con i relativi valori -> viene utilizzato il $set
        res = self.collection.update_one({ "nome": data["nome"] }, { "$set": { "stato": data["stato"], "calorie": data["calorie"], "gusto": data["gusto"] }})
        #come nella GET anche qui restituisco 404 se viene inserito un codice (nome) che non esiste
        if res.modified_count == 0:
            cherrypy.response.status = 404
        return data["nome"]


    #metodo per l'eliminazione di un document
    @cherrypy.tools.json_out()
    def DELETE(self, nome=""):
        #scrivi qui le istruzioni per eliminare un document
        res = self.collection.delete_one({"nome":nome})
        #come nella GET anche qui restituisco 404 se viene inserito un codice (nome) che non esiste
        if res.deleted_count == 0:
            cherrypy.response.status = 404
        return 0


#if __name__ == '__main__':
conf = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')],
        'tools.auth_basic.on': True,
        'tools.auth_basic.realm': MyController.RLM,
        'tools.auth_basic.checkpassword': MyController.validate_password
    }
}  

cherrypy.quickstart(MyController(), '/', conf)