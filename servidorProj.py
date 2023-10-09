import flask
import socket
from flask import request, jsonify, render_template
import json
import BdProj as bd
import random
import time
import os
import _thread
import pygame as pg
from threading import Thread
  
sw=600

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print("Servidor %s em %s " % (hostname, local_ip))

app = flask.Flask(__name__)
app.config["DEBUG"]=True  
    
@app.route("/insere", methods=['POST'])     
def cadastrar():
    try:        
        nome = request.form['nome']
        data_hora = request.form['data_hora']       
        bd.inserir(nome, data_hora)
        return '{"cod": 1, "status": "inserido"}'
    
    except:      
        return '{"cod": 0, "status": "não inserido"}'  
    

@app.route("/getLista", methods=['GET'])
def listar():
    try:        
        return bd.listarPessoas() 
    
    except Error as e:   
        print(e)
        return '{"cod": 0, "status": "problemas com a lista"}' 

     
@app.route("/getDetalhe", methods=['GET'])
def buscarPorId():
    try:
        id = request.args.get("id", False)   
        return bd.buscarPorId(id)
    except:
        return "{\"cod\":0, \"status\":\"não existe esse id\"}"
    
@app.route("/apagaID", methods=['POST'])
def excluir(): 
    try:        
        id = request.form.get("id") 
        bd.excluir(id)
        return "{\"cod\": 1, \"status\": \"apagado\"}"
    except:
        return "{\"cod\": 0, \"status\": \"não apagado\"}"

@app.route("/animação", methods=['GET'])
def animacoes():
    try:        
        animacao = request.args.get("animacao")      
        
        if animacao == "Baby Yoda":
            bd.animacao1()
        elif animacao == "Sapo":
            bd.animacao2()   
        elif animacao == "Espirais":
            bd.animacao3() 
        elif animacao == "Galatica":
            bd.animacao4()         
    
        return "{ \"cod\":1, \"status\":\"ok\" }"
    
    except:
        return "{ \"cod\":0, \"status\":\"não ok\" }"
    
if __name__ == '__main__':
    app.run(host=local_ip, port=8080)        