from flask import Flask
from pymongo import MongoClient

#instancia a app Flask
app = Flask('_name_')

#cliente de conecção com o mongo
client = MongoClient('localhost', 27017)

#concecta no db lista_tarefas
db = client.lista_tarefas

#acessa a collection
tarefas = db.tarefas

#

todas_tarefas = tarefas.find()
for t1 in todas_tarefas:
    print(t1)
    
    
