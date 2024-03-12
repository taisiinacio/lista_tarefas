from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId



#instancia a app Flask
app = Flask('_name_')

#cliente de conecção com o mongo
client = MongoClient('localhost', 27017)

#concecta no db lista_tarefas
db = client.lista_tarefas

#acessa a collection
tarefas = db.tarefas

#

# todas_tarefas = tarefas.find()
# for t1 in todas_tarefas:
#     print(t1)

#método que renderiza a página principal da aplicação
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['degree']
        tarefas.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))

    all_tarefas = tarefas.find()
    return render_template('index.html', tarefas=all_tarefas)


@app.post('/<id>/delete/')
def delete(id):
    tarefas.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))
