# services.py
# ============================================
# SERVIÇOS - Baseado no CP1
# ============================================

import json
import os
from datetime import datetime
from models import Usuario, Laboratorio, Reserva

# ==================== AUTH SERVICE ====================

class AuthService:
    """Gerencia autenticação e usuários"""
    
    ARQUIVO = "data/usuarios.json"
    
    def __init__(self):
        self.usuarios = []
        self.logado = None
        self.carregar()
    
    def carregar(self):
        """Carrega usuários do arquivo JSON"""
        try:
            with open(self.ARQUIVO, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.usuarios = [Usuario.from_dict(u) for u in dados]
        except FileNotFoundError:
            self.usuarios = []
            self.criar_iniciais()
    
    def salvar(self):
        """Salva usuários no arquivo JSON"""
        os.makedirs("data", exist_ok=True)
        with open(self.ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=2, ensure_ascii=False)
    
    def criar_iniciais(self):
        """Cria usuários de exemplo"""
        self.usuarios = [
            Usuario("123456", "Ana Silva", "ana@fiap.com.br", "123456"),
            Usuario("789012", "Carlos Santos", "carlos@fiap.com.br", "789012"),
            Usuario("999888", "Coordenação", "coord@fiap.com.br", "admin123", "coordenador")
        ]
        self.salvar()
    
    def cadastrar(self, rm, nome, email, senha):
        """Cadastra um novo usuário"""
        # Verifica se RM já existe
        for u in self.usuarios:
            if u.rm == rm:
                return False, "RM já cadastrado!"
        
        # Cria novo usuário
        novo = Usuario(rm, nome, email, senha)
        self.usuarios.append(novo)
        self.salvar()
        return True, "Cadastro realizado com sucesso!"
    
    def login(self, rm, senha):
        """Realiza login do usuário"""
        for u in self.usuarios:
            if u.rm == rm and u.senha == senha:
                self.logado = u
                return True, f"Bem-vindo, {u.nome}!"
        return False, "RM ou senha incorretos!"
    
    def logout(self):
        """Desloga o usuário"""
        self.logado = None
    
    def get_usuario(self):
        """Retorna usuário logado"""
        return self.logado
    
    def is_coordenador(self):
        """Verifica se é coordenador"""
        return self.logado and self.logado.tipo == "coordenador"


# ==================== LABORATORIO SERVICE ====================

class LaboratorioService:
    """Gerencia laboratórios"""
    
    ARQUIVO = "data/laboratorios.json"
    
    def __init__(self):
        self.laboratorios = []
        self.carregar()
    
    def carregar(self):
        """Carrega laboratórios do JSON"""
        try:
            with open(self.ARQUIVO, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.laboratorios = [Laboratorio.from_dict(l) for l in dados]
        except FileNotFoundError:
            self.criar_iniciais()
    
    def salvar(self):
        """Salva laboratórios no JSON"""
        os.makedirs("data", exist_ok=True)
        with open(self.ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump([l.to_dict() for l in self.laboratorios], f, indent=2, ensure_ascii=False)
    
    def criar_iniciais(self):
        """Cria laboratórios de exemplo"""
        self.laboratorios = [
            Laboratorio(1, "Lab Informática A", 30, ["computadores", "projetor"], "Paulista", 2),
            Laboratorio(2, "Lab Informática B", 30, ["computadores"], "Paulista", 2),
            Laboratorio(3, "Lab Redes", 20, ["equipamentos rede"], "Paulista", 3),
            Laboratorio(4, "Lab IoT", 15, ["Arduinos"], "Vila Olímpia", 1),
            Laboratorio(5, "Sala Estudos", 40, ["quadro"], "Paulista", 1),
        ]
        self.salvar()
    
    def listar(self):
        """Retorna lista de laboratórios"""
        return self.laboratorios
    
    def buscar(self, id):
        """Busca laboratório por ID"""
        for lab in self.laboratorios:
            if lab.id == id:
                return lab
        return None


# ==================== RESERVA SERVICE ====================

class ReservaService:
    """Gerencia reservas de laboratórios"""
    
    ARQUIVO = "data/reservas.json"
    
    def __init__(self, lab_service):
        self.lab_service = lab_service
        self.reservas = []
        self.carregar()
    
    def carregar(self):
        """Carrega reservas do JSON"""
        try:
            with open(self.ARQUIVO, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.reservas = [Reserva.from_dict(r) for r in dados]
        except FileNotFoundError:
            self.reservas = []
    
    def salvar(self):
        """Salva reservas no JSON"""
        os.makedirs("data", exist_ok=True)
        with open(self.ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in self.reservas], f, indent=2, ensure_ascii=False)
    
    def disponivel(self, lab_id, inicio, fim):
        """Verifica se um laboratório está disponível no horário"""
        for r in self.reservas:
            if r.id_laboratorio == lab_id and r.status == "ativa":
                if not (fim <= r.data_inicio or inicio >= r.data_fim):
                    return False, r
        return True, None
    
    def verificar_disponibilidade(self, lab_id, inicio, fim):
        """Versão amigável para verificar disponibilidade"""
        lab = self.lab_service.buscar(lab_id)
        if not lab:
            return False, "Laboratório não encontrado!"
        
        disponivel, conflito = self.disponivel(lab_id, inicio, fim)
        
        if disponivel:
            return True, f"Laboratório disponível para {inicio} até {fim}"
        else:
            return False, f"Indisponível! Conflito com reserva #{conflito.id}"
    
    def reservar(self, rm, lab_id, inicio, fim):
        """Realiza uma nova reserva"""
        lab = self.lab_service.buscar(lab_id)
        if not lab:
            return False, "Laboratório não encontrado!"
        
        # Verifica disponibilidade
        disponivel, _ = self.disponivel(lab_id, inicio, fim)
        if not disponivel:
            return False, "Horário indisponível!"
        
        # Valida horários
        if inicio >= fim:
            return False, "Data de início deve ser anterior ao fim!"
        
        if inicio < datetime.now().strftime("%Y-%m-%d %H:%M"):
            return False, "Não pode reservar horário passado!"
        
        # Cria reserva
        novo_id = max([r.id for r in self.reservas], default=0) + 1
        nova = Reserva(novo_id, rm, lab_id, inicio, fim)
        self.reservas.append(nova)
        self.salvar()
        
        return True, f"Reserva #{novo_id} confirmada! Laboratório: {lab.nome}"
    
    def cancelar(self, res_id, rm):
        """Cancela uma reserva"""
        for r in self.reservas:
            if r.id == res_id:
                if r.rm_aluno != rm:
                    return False, "Você só pode cancelar suas reservas!"
                if r.status != "ativa":
                    return False, "Reserva já cancelada!"
                r.status = "cancelada"
                self.salvar()
                return True, f"Reserva #{res_id} cancelada!"
        return False, "Reserva não encontrada!"
    
    def minhas_reservas(self, rm):
        """Retorna reservas ativas de um aluno"""
        return [r for r in self.reservas if r.rm_aluno == rm and r.status == "ativa"]
    
    def todas_reservas(self):
        """Retorna todas as reservas (para coordenador)"""
        return self.reservas