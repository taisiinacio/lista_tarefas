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
        nome = request.form['nome']
        status = request.form['status']
        data = request.form ['data']
        tarefas.insert_one({'nome': nome, 'status': status, 'data': data})
        return redirect(url_for('index'))

    
    tarefas_todas = tarefas.find({'status': { '$ne': 'Concluída' }})
    tarefas_concluidas = tarefas.find({'status': { '$eq': 'Concluída' }})
    return render_template('index.html', tarefa = {}, tarefas = tarefas_todas, btn_submit= "Cadastrar tarefa", tarefas_concluidas = tarefas_concluidas)

#@app.app_template_filter('to_date')
#def format_datetime(value):
#  return value.strftime('%d/%m/%Y')


@app.route('/<id>/delete/', methods=('GET', 'POST'))
def delete(id):
    tarefas.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.route('/<id>/update/', methods=('GET', 'POST'))
def update(id):
    tarefas.update_one({"_id": ObjectId(id)},
    {'$set': {'status': 'Concluída' } } )
    
    tarefas_todas = tarefas.find({'status': { '$ne': 'Concluída' }})
    tarefas_concluidas = tarefas.find({'status': { '$eq': 'Concluída' }})
    return redirect(url_for('index', tarefas = tarefas_todas, tarefas_concluidas = tarefas_concluidas ))

   

@app.route('/<id>/edit/', methods=('GET', 'POST'))
def edit(id):

    if request.method=='GET':
        tarefa_selecionada = tarefas.find_one({"_id": ObjectId(id)})
        todas_tarefas = tarefas.find()

        return render_template('index.html', tarefa = tarefa_selecionada, tarefas=todas_tarefas, btn_submit= "Editar tarefa")
     
    if request.method=='POST':
        nome = request.form['nome']
        status = request.form['status']
        data = request.form ['data']
        tarefas.update_one({ "_id" : ObjectId(id)}, 
                {'$set': { 'nome': nome, 'status': status, 'data': data} } )
        return redirect(url_for('index'))