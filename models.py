# models.py
# ============================================
# CLASSES DE MODELO - Baseado no CP1
# ============================================

import json
from datetime import datetime

class Usuario:
    """Representa um usuário do sistema"""
    
    def __init__(self, rm, nome, email, senha, tipo="aluno"):
        self.rm = rm
        self.nome = nome
        self.email = email
        self.senha = senha  # Será hash quando implementado
        self.tipo = tipo    # "aluno" ou "coordenador"
    
    def to_dict(self):
        """Converte para dicionário (salvar JSON)"""
        return {
            "rm": self.rm,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "tipo": self.tipo
        }
    
    @staticmethod
    def from_dict(dados):
        """Cria Usuario a partir de dicionário (carregar JSON)"""
        return Usuario(
            rm=dados["rm"],
            nome=dados["nome"],
            email=dados["email"],
            senha=dados["senha"],
            tipo=dados.get("tipo", "aluno")
        )
    
    def __repr__(self):
        return f"{self.nome} (RM: {self.rm})"


class Laboratorio:
    """Representa um laboratório disponível"""
    
    def __init__(self, id, nome, capacidade, recursos, predio, andar):
        self.id = id
        self.nome = nome
        self.capacidade = capacidade
        self.recursos = recursos  # lista de strings
        self.predio = predio
        self.andar = andar
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "capacidade": self.capacidade,
            "recursos": self.recursos,
            "predio": self.predio,
            "andar": self.andar
        }
    
    @staticmethod
    def from_dict(dados):
        return Laboratorio(
            id=dados["id"],
            nome=dados["nome"],
            capacidade=dados["capacidade"],
            recursos=dados["recursos"],
            predio=dados["predio"],
            andar=dados["andar"]
        )
    
    def __repr__(self):
        recursos_str = ", ".join(self.recursos) if self.recursos else "Nenhum"
        return f"{self.nome} | Cap: {self.capacidade} | Recursos: {recursos_str} | Local: {self.predio} - {self.andar}º"


class Reserva:
    """Representa uma reserva de laboratório"""
    
    def __init__(self, id, rm_aluno, id_laboratorio, data_inicio, data_fim, status="ativa"):
        self.id = id
        self.rm_aluno = rm_aluno
        self.id_laboratorio = id_laboratorio
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = status  # "ativa", "cancelada", "concluida"
    
    def to_dict(self):
        return {
            "id": self.id,
            "rm_aluno": self.rm_aluno,
            "id_laboratorio": self.id_laboratorio,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "status": self.status
        }
    
    @staticmethod
    def from_dict(dados):
        return Reserva(
            id=dados["id"],
            rm_aluno=dados["rm_aluno"],
            id_laboratorio=dados["id_laboratorio"],
            data_inicio=dados["data_inicio"],
            data_fim=dados["data_fim"],
            status=dados.get("status", "ativa")
        )
    
    def __repr__(self):
        return f"Reserva #{self.id} | Lab {self.id_laboratorio} | {self.data_inicio} até {self.data_fim}"