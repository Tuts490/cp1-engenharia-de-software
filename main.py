# main.py - Versão Simplificada com RM
# Colocar este arquivo na PASTA PRINCIPAL do projeto

import json
import os
from datetime import datetime

# ==================== MODELOS ====================

class Usuario:
    def __init__(self, rm, nome, email, senha, tipo="aluno"):
        self.rm = rm                      # RM do aluno
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
    
    def to_dict(self):
        return {"rm": self.rm, "nome": self.nome, "email": self.email, "senha": self.senha, "tipo": self.tipo}
    
    @staticmethod
    def from_dict(dados):
        return Usuario(dados["rm"], dados["nome"], dados["email"], dados["senha"], dados.get("tipo", "aluno"))


class Laboratorio:
    def __init__(self, id, nome, capacidade, recursos, predio, andar):
        self.id = id
        self.nome = nome
        self.capacidade = capacidade
        self.recursos = recursos
        self.predio = predio
        self.andar = andar
    
    def __repr__(self):
        return f"{self.nome} | Cap: {self.capacidade} | Local: {self.predio} - {self.andar}º"


class Reserva:
    def __init__(self, id, rm_aluno, id_laboratorio, data_inicio, data_fim, status="ativa"):
        self.id = id
        self.rm_aluno = rm_aluno          # RM do aluno
        self.id_laboratorio = id_laboratorio
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = status


# ==================== SERVIÇOS ====================

class AuthService:
    ARQUIVO = "data/usuarios.json"
    
    def __init__(self):
        self.usuarios = []
        self.logado = None
        self.carregar()
    
    def carregar(self):
        try:
            with open(self.ARQUIVO, 'r') as f:
                dados = json.load(f)
                self.usuarios = [Usuario.from_dict(u) for u in dados]
        except:
            self.usuarios = []
            self.criar_iniciais()
    
    def salvar(self):
        os.makedirs("data", exist_ok=True)
        with open(self.ARQUIVO, 'w') as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=2)
    
    def criar_iniciais(self):
        self.usuarios = [
            Usuario("123456", "Ana Silva", "ana@fiap.com.br", "123456"),
            Usuario("789012", "Carlos Santos", "carlos@fiap.com.br", "789012"),
            Usuario("999888", "Coordenação", "coord@fiap.com.br", "admin123", "coordenador")
        ]
        self.salvar()
    
    def cadastrar(self, rm, nome, email, senha):
        # Verifica se RM já existe
        for u in self.usuarios:
            if u.rm == rm:
                return False, "RM já cadastrado!"
        
        novo = Usuario(rm, nome, email, senha)
        self.usuarios.append(novo)
        self.salvar()
        return True, "Cadastro realizado com sucesso!"
    
    def login(self, rm, senha):
        for u in self.usuarios:
            if u.rm == rm and u.senha == senha:
                self.logado = u
                return True, f"Bem-vindo, {u.nome}!"
        return False, "RM ou senha incorretos!"
    
    def logout(self):
        self.logado = None
    
    def get_usuario(self):
        return self.logado
    
    def is_coordenador(self):
        return self.logado and self.logado.tipo == "coordenador"


class LaboratorioService:
    ARQUIVO = "data/laboratorios.json"
    
    def __init__(self):
        self.laboratorios = []
        self.carregar()
    
    def carregar(self):
        try:
            with open(self.ARQUIVO, 'r') as f:
                dados = json.load(f)
                self.laboratorios = [Laboratorio(l["id"], l["nome"], l["capacidade"], l["recursos"], l["predio"], l["andar"]) for l in dados]
        except:
            self.criar_iniciais()
    
    def salvar(self):
        os.makedirs("data", exist_ok=True)
        with open(self.ARQUIVO, 'w') as f:
            json.dump([{"id": l.id, "nome": l.nome, "capacidade": l.capacidade, "recursos": l.recursos, "predio": l.predio, "andar": l.andar} for l in self.laboratorios], f, indent=2)
    
    def criar_iniciais(self):
        self.laboratorios = [
            Laboratorio(1, "Lab Informática A", 30, ["computadores", "projetor"], "Paulista", 2),
            Laboratorio(2, "Lab Informática B", 30, ["computadores"], "Paulista", 2),
            Laboratorio(3, "Lab Redes", 20, ["equipamentos rede"], "Paulista", 3),
            Laboratorio(4, "Lab IoT", 15, ["Arduinos"], "Vila Olímpia", 1),
            Laboratorio(5, "Sala Estudos", 40, ["quadro"], "Paulista", 1),
        ]
        self.salvar()
    
    def listar(self):
        for lab in self.laboratorios:
            print(f"[{lab.id}] {lab}")
    
    def buscar(self, id):
        for lab in self.laboratorios:
            if lab.id == id:
                return lab
        return None


class ReservaService:
    ARQUIVO = "data/reservas.json"
    
    def __init__(self, lab_service):
        self.lab_service = lab_service
        self.reservas = []
        self.carregar()
    
    def carregar(self):
        try:
            with open(self.ARQUIVO, 'r') as f:
                dados = json.load(f)
                self.reservas = [Reserva(r["id"], r["rm_aluno"], r["id_laboratorio"], r["data_inicio"], r["data_fim"], r.get("status", "ativa")) for r in dados]
        except:
            self.reservas = []
    
    def salvar(self):
        os.makedirs("data", exist_ok=True)
        with open(self.ARQUIVO, 'w') as f:
            json.dump([{"id": r.id, "rm_aluno": r.rm_aluno, "id_laboratorio": r.id_laboratorio, "data_inicio": r.data_inicio, "data_fim": r.data_fim, "status": r.status} for r in self.reservas], f, indent=2)
    
    def disponivel(self, lab_id, inicio, fim):
        for r in self.reservas:
            if r.id_laboratorio == lab_id and r.status == "ativa":
                if not (fim <= r.data_inicio or inicio >= r.data_fim):
                    return False
        return True
    
    def reservar(self, rm, lab_id, inicio, fim):
        lab = self.lab_service.buscar(lab_id)
        if not lab:
            return False, "Laboratório não encontrado!"
        
        if not self.disponivel(lab_id, inicio, fim):
            return False, "Horário indisponível!"
        
        if inicio >= fim:
            return False, "Data de início deve ser anterior ao fim!"
        
        if inicio < datetime.now().strftime("%Y-%m-%d %H:%M"):
            return False, "Não pode reservar horário passado!"
        
        novo_id = max([r.id for r in self.reservas], default=0) + 1
        nova = Reserva(novo_id, rm, lab_id, inicio, fim)
        self.reservas.append(nova)
        self.salvar()
        return True, f"✅ Reserva #{novo_id} confirmada!"
    
    def cancelar(self, res_id, rm):
        for r in self.reservas:
            if r.id == res_id:
                if r.rm_aluno != rm:
                    return False, "Você só pode cancelar suas reservas!"
                if r.status != "ativa":
                    return False, "Reserva já cancelada!"
                r.status = "cancelada"
                self.salvar()
                return True, f"✅ Reserva #{res_id} cancelada!"
        return False, "Reserva não encontrada!"
    
    def minhas_reservas(self, rm):
        ativas = [r for r in self.reservas if r.rm_aluno == rm and r.status == "ativa"]
        if not ativas:
            print("📭 Nenhuma reserva ativa.")
        for r in ativas:
            lab = self.lab_service.buscar(r.id_laboratorio)
            print(f"#{r.id} - {lab.nome} - {r.data_inicio} até {r.data_fim}")


# ==================== MENU ====================

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    auth = AuthService()
    lab_service = LaboratorioService()
    reserva_service = ReservaService(lab_service)
    
    while True:
        limpar()
        print("="*50)
        print("🏫 RESERVA DE LABORATÓRIOS - FIAP")
        print("="*50)
        
        if auth.get_usuario() is None:
            print("\n1 - Login")
            print("2 - Cadastrar")
            print("0 - Sair")
            op = input("\n👉 Escolha: ")
            
            if op == "1":
                rm = input("RM: ")
                senha = input("Senha: ")
                ok, msg = auth.login(rm, senha)
                print(msg)
                input("Pressione Enter...")
            elif op == "2":
                rm = input("RM: ")
                nome = input("Nome: ")
                email = input("Email: ")
                senha = input("Senha: ")
                ok, msg = auth.cadastrar(rm, nome, email, senha)
                print(msg)
                input("Pressione Enter...")
            elif op == "0":
                print("Até logo!")
                break
        else:
            user = auth.get_usuario()
            print(f"\n👤 Logado: {user.nome} (RM: {user.rm})")
            
            if auth.is_coordenador():
                print("\n[1] Listar laboratórios")
                print("[2] Fazer reserva")
                print("[3] Minhas reservas")
                print("[4] Cancelar reserva")
                print("[5] Ver todas reservas")
                print("[0] Logout")
            else:
                print("\n[1] Listar laboratórios")
                print("[2] Fazer reserva")
                print("[3] Minhas reservas")
                print("[4] Cancelar reserva")
                print("[0] Logout")
            
            op = input("\n👉 Escolha: ")
            
            if op == "1":
                lab_service.listar()
                input("\nPressione Enter...")
            elif op == "2":
                lab_service.listar()
                try:
                    lab_id = int(input("\nID do laboratório: "))
                    inicio = input("Data início (AAAA-MM-DD HH:MM): ")
                    fim = input("Data fim (AAAA-MM-DD HH:MM): ")
                    ok, msg = reserva_service.reservar(user.rm, lab_id, inicio, fim)
                    print(msg)
                except:
                    print("ID inválido!")
                input("Pressione Enter...")
            elif op == "3":
                reserva_service.minhas_reservas(user.rm)
                input("\nPressione Enter...")
            elif op == "4":
                reserva_service.minhas_reservas(user.rm)
                try:
                    res_id = int(input("\nID da reserva para cancelar: "))
                    ok, msg = reserva_service.cancelar(res_id, user.rm)
                    print(msg)
                except:
                    print("ID inválido!")
                input("Pressione Enter...")
            elif op == "5" and auth.is_coordenador():
                for r in reserva_service.reservas:
                    lab = lab_service.buscar(r.id_laboratorio)
                    print(f"#{r.id} | RM: {r.rm_aluno} | {lab.nome} | {r.data_inicio} | Status: {r.status}")
                input("\nPressione Enter...")
            elif op == "0":
                auth.logout()


if __name__ == "__main__":
    main()