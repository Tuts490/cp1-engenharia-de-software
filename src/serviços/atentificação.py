import json
import os
from ..modelos.usuario import Usuario

class AuthService:
    """Gerencia cadastro, login e autenticação de usuários"""
    
    ARQUIVO_DADOS = "src/data/usuarios.json"
    
    def __init__(self):
        self.usuarios = []
        self.usuario_logado = None
        self.carregar_usuarios()
    
    def carregar_usuarios(self):
        """Carrega os usuários do arquivo JSON"""
        try:
            with open(self.ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.usuarios = [Usuario.from_dict(u) for u in dados]
        except FileNotFoundError:
            self.usuarios = []
            self.criar_usuarios_iniciais()
    
    def salvar_usuarios(self):
        """Salva os usuários no arquivo JSON"""
        with open(self.ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=2, ensure_ascii=False)
    
    def criar_usuarios_iniciais(self):
        """Cria usuários de exemplo para teste"""
        self.usuarios = [
            Usuario("123456", "Ana Silva", "ana@fiap.com.br", "123456"),
            Usuario("789012", "Carlos Santos", "carlos@fiap.com.br", "789012"),
            Usuario("999888", "Coordenação", "coordenacao@fiap.com.br", "admin123", "coordenador")
        ]
        self.salvar_usuarios()
    
    def cadastrar(self, ra, nome, email, senha):
        """Cadastra um novo usuário"""
        # Verifica se RA já existe
        for usuario in self.usuarios:
            if usuario.ra == ra:
                return False, "RA já cadastrado!"
        
        # Cria novo usuário
        novo_usuario = Usuario(ra, nome, email, senha)
        self.usuarios.append(novo_usuario)
        self.salvar_usuarios()
        return True, "Cadastro realizado com sucesso!"
    
    def login(self, ra, senha):
        """Realiza o login do usuário"""
        for usuario in self.usuarios:
            if usuario.ra == ra and usuario.senha == senha:
                self.usuario_logado = usuario
                return True, f"Bem-vindo, {usuario.nome}!"
        return False, "RA ou senha incorretos!"
    
    def logout(self):
        """Desloga o usuário atual"""
        self.usuario_logado = None
    
    def esta_logado(self):
        """Verifica se há um usuário logado"""
        return self.usuario_logado is not None
    
    def get_usuario_logado(self):
        return self.usuario_logado
    
    def is_coordenador(self):
        """Verifica se o usuário logado é coordenador"""
        return self.usuario_logado and self.usuario_logado.tipo == "coordenador"