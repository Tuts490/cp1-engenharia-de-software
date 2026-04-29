# app.py
import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'fiap-secret-key-2024'

# ==================== SEUS SERVICOS EXISTENTES ====================
# Copie ou importe suas classes: Usuario, Laboratorio, Reserva, 
# AuthService, LaboratorioService, ReservaService

# Exemplo simplificado (substitua pelas suas classes reais):
class AuthService:
    def __init__(self):
        self.usuarios = []
        self.logado = None
        self.carregar()
    
    def carregar(self):
        try:
            with open('data/usuarios.json', 'r') as f:
                dados = json.load(f)
                # Converter dados para objetos Usuario
        except:
            pass
    
    def cadastrar(self, rm, nome, email, senha):
        # Sua lógica de cadastro
        return True, "Cadastro realizado!"
    
    def login(self, rm, senha):
        # Sua lógica de login
        if rm == "123456" and senha == "123456":
            return True, "Login realizado!"
        return False, "RM ou senha incorretos"

auth_service = AuthService()

# ==================== ROTAS ====================

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logado'):
        return redirect(url_for('dashboard'))
    
    erro = None
    if request.method == 'POST':
        rm = request.form['rm']
        senha = request.form['senha']
        sucesso, mensagem = auth_service.login(rm, senha)
        if sucesso:
            session['logado'] = True
            session['rm'] = rm
            return redirect(url_for('dashboard'))
        else:
            erro = mensagem
    
    return render_template('login.html', erro=erro)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    erro = None
    sucesso = None
    
    if request.method == 'POST':
        rm = request.form['rm']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        sucesso, mensagem = auth_service.cadastrar(rm, nome, email, senha)
        if sucesso:
            return redirect(url_for('login'))
        else:
            erro = mensagem
    
    return render_template('cadastro.html', erro=erro, sucesso=sucesso)

@app.route('/dashboard')
def dashboard():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', nome_usuario=f"Usuário {session.get('rm')}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)