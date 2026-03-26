# main.py - Versão sem Emojis
# Colocar este arquivo na PASTA PRINCIPAL do projeto

import json
import os
from datetime import datetime

# ==================== MODELOS ====================

class Usuario:
    def __init__(self, rm, nome, email, senha, tipo="aluno"):
        self.rm = rm
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
        recursos_str = ", ".join(self.recursos) if self.recursos else "Nenhum"
        return f"{self.nome} | Cap: {self.capacidade} | Recursos: {recursos_str} | Local: {self.predio} - {self.andar} andar"


class Reserva:
    def __init__(self, id, rm_aluno, id_laboratorio, data_inicio, data_fim, status="ativa"):
        self.id = id
        self.rm_aluno = rm_aluno
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
            with open(self.ARQUIVO, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.usuarios = [Usuario.from_dict(u) for u in dados]
        except:
            self.usuarios = []
            self.criar_iniciais()
    
    def salvar(self):
        os.makedirs("data", exist_ok=True)
        with open(self.ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=2, ensure_ascii=False)
    
    def criar_iniciais(self):
        self.usuarios = [
            Usuario("123456", "Ana Silva", "ana@fiap.com.br", "123456"),
            Usuario("789012", "Carlos Santos", "carlos@fiap.com.br", "789012"),
            Usuario("999888", "Coordenação", "coord@fiap.com.br", "admin123", "coordenador")
        ]
        self.salvar()
    
    def cadastrar(self, rm, nome, email, senha):
        for u in self.usuarios:
            if u.rm == rm:
                return False, "RM ja cadastrado!"
        
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
            with open(self.ARQUIVO, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.laboratorios = [Laboratorio(l["id"], l["nome"], l["capacidade"], l["recursos"], l["predio"], l["andar"]) for l in dados]
        except:
            self.criar_iniciais()
    
    def salvar(self):
        os.makedirs("data", exist_ok=True)
        with open(self.ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump([{"id": l.id, "nome": l.nome, "capacidade": l.capacidade, "recursos": l.recursos, "predio": l.predio, "andar": l.andar} for l in self.laboratorios], f, indent=2, ensure_ascii=False)
    
    def criar_iniciais(self):
        self.laboratorios = [
            Laboratorio(1, "Lab Informatica A", 30, ["computadores", "projetor"], "Paulista", 2),
            Laboratorio(2, "Lab Informatica B", 30, ["computadores"], "Paulista", 2),
            Laboratorio(3, "Lab Redes", 20, ["equipamentos rede"], "Paulista", 3),
            Laboratorio(4, "Lab IoT", 15, ["Arduinos"], "Vila Olimpia", 1),
            Laboratorio(5, "Sala Estudos", 40, ["quadro"], "Paulista", 1),
        ]
        self.salvar()
    
    def listar(self):
        if not self.laboratorios:
            print("Nenhum laboratorio cadastrado.")
            return
        
        print("\n" + "="*60)
        print("LABORATORIOS DISPONIVEIS")
        print("="*60)
        for lab in self.laboratorios:
            print(f"\n[{lab.id}] {lab}")
        print("\n" + "="*60)
    
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
            with open(self.ARQUIVO, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.reservas = [Reserva(r["id"], r["rm_aluno"], r["id_laboratorio"], r["data_inicio"], r["data_fim"], r.get("status", "ativa")) for r in dados]
        except:
            self.reservas = []
    
    def salvar(self):
        os.makedirs("data", exist_ok=True)
        with open(self.ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump([{"id": r.id, "rm_aluno": r.rm_aluno, "id_laboratorio": r.id_laboratorio, "data_inicio": r.data_inicio, "data_fim": r.data_fim, "status": r.status} for r in self.reservas], f, indent=2, ensure_ascii=False)
    
    def disponivel(self, lab_id, inicio, fim):
        for r in self.reservas:
            if r.id_laboratorio == lab_id and r.status == "ativa":
                if not (fim <= r.data_inicio or inicio >= r.data_fim):
                    return False, r
        return True, None
    
    def verificar_disponibilidade(self, lab_id, inicio, fim):
        lab = self.lab_service.buscar(lab_id)
        if not lab:
            return False, "Laboratorio nao encontrado!"
        
        disponivel, reserva_conflito = self.disponivel(lab_id, inicio, fim)
        
        if disponivel:
            return True, f"Laboratorio DISPONIVEL para o horario solicitado!\n   {inicio} ate {fim}"
        else:
            return False, f"Laboratorio INDISPONIVEL!\n   Conflito com reserva #{reserva_conflito.id}\n   Horario: {reserva_conflito.data_inicio} ate {reserva_conflito.data_fim}"
    
    def reservar(self, rm, lab_id, inicio, fim):
        lab = self.lab_service.buscar(lab_id)
        if not lab:
            return False, "Laboratorio nao encontrado!"
        
        disponivel, _ = self.disponivel(lab_id, inicio, fim)
        if not disponivel:
            return False, "Horario indisponivel! Laboratorio ja reservado neste periodo."
        
        if inicio >= fim:
            return False, "Data de inicio deve ser anterior ao fim!"
        
        if inicio < datetime.now().strftime("%Y-%m-%d %H:%M"):
            return False, "Nao pode reservar horario passado!"
        
        novo_id = max([r.id for r in self.reservas], default=0) + 1
        nova = Reserva(novo_id, rm, lab_id, inicio, fim)
        self.reservas.append(nova)
        self.salvar()
        return True, f"Reserva #{novo_id} confirmada!\n   Laboratorio: {lab.nome}\n   Horario: {inicio} ate {fim}"
    
    def cancelar(self, res_id, rm):
        for r in self.reservas:
            if r.id == res_id:
                if r.rm_aluno != rm:
                    return False, "Voce so pode cancelar suas reservas!"
                if r.status != "ativa":
                    return False, "Reserva ja cancelada!"
                r.status = "cancelada"
                self.salvar()
                return True, f"Reserva #{res_id} cancelada!"
        return False, "Reserva nao encontrada!"
    
    def minhas_reservas(self, rm):
        ativas = [r for r in self.reservas if r.rm_aluno == rm and r.status == "ativa"]
        if not ativas:
            print("\nNenhuma reserva ativa.")
            return
        
        print("\n" + "="*60)
        print("MINHAS RESERVAS ATIVAS")
        print("="*60)
        for r in ativas:
            lab = self.lab_service.buscar(r.id_laboratorio)
            print(f"\nReserva #{r.id}")
            print(f"   Laboratorio: {lab.nome}")
            print(f"   Inicio: {r.data_inicio}")
            print(f"   Fim: {r.data_fim}")
        print("\n" + "="*60)
    
    def todas_reservas(self):
        if not self.reservas:
            print("\nNenhuma reserva cadastrada.")
            return
        
        print("\n" + "="*60)
        print("TODAS AS RESERVAS")
        print("="*60)
        for r in self.reservas:
            lab = self.lab_service.buscar(r.id_laboratorio)
            print(f"\nReserva #{r.id} | Status: {r.status}")
            print(f"   RM: {r.rm_aluno}")
            print(f"   Laboratorio: {lab.nome if lab else 'N/A'}")
            print(f"   Inicio: {r.data_inicio}")
            print(f"   Fim: {r.data_fim}")
        print("\n" + "="*60)


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
        print("RESERVA DE LABORATORIOS - FIAP")
        print("="*50)
        
        if auth.get_usuario() is None:
            print("\n1 - Login")
            print("2 - Cadastrar")
            print("0 - Sair")
            op = input("\nEscolha: ")
            
            if op == "1":
                rm = input("RM: ")
                senha = input("Senha: ")
                ok, msg = auth.login(rm, senha)
                print(msg)
                input("\nPressione Enter...")
            elif op == "2":
                rm = input("RM: ")
                nome = input("Nome: ")
                email = input("Email: ")
                senha = input("Senha: ")
                ok, msg = auth.cadastrar(rm, nome, email, senha)
                print(msg)
                input("\nPressione Enter...")
            elif op == "0":
                print("Ate logo!")
                break
        else:
            user = auth.get_usuario()
            print(f"\nLogado: {user.nome} (RM: {user.rm})")
            
            if auth.is_coordenador():
                print("\n[1] Listar laboratorios")
                print("[2] Verificar disponibilidade")
                print("[3] Fazer reserva")
                print("[4] Minhas reservas")
                print("[5] Cancelar reserva")
                print("[6] Ver todas reservas")
                print("[0] Logout")
            else:
                print("\n[1] Listar laboratorios")
                print("[2] Verificar disponibilidade")
                print("[3] Fazer reserva")
                print("[4] Minhas reservas")
                print("[5] Cancelar reserva")
                print("[0] Logout")
            
            op = input("\nEscolha: ")
            
            if op == "1":
                lab_service.listar()
                input("\nPressione Enter...")
            
            elif op == "2":
                limpar()
                print("="*50)
                print("VERIFICAR DISPONIBILIDADE")
                print("="*50)
                lab_service.listar()
                try:
                    lab_id = int(input("\nDigite o ID do laboratorio: "))
                    print("\nDigite a data e hora no formato: AAAA-MM-DD HH:MM")
                    inicio = input("Data e hora de inicio: ")
                    fim = input("Data e hora de fim: ")
                    ok, msg = reserva_service.verificar_disponibilidade(lab_id, inicio, fim)
                    print("\n" + msg)
                except ValueError:
                    print("\nID do laboratorio deve ser um numero!")
                input("\nPressione Enter...")
            
            elif op == "3":
                limpar()
                print("="*50)
                print("FAZER RESERVA")
                print("="*50)
                lab_service.listar()
                try:
                    lab_id = int(input("\nDigite o ID do laboratorio: "))
                    print("\nDigite a data e hora no formato: AAAA-MM-DD HH:MM")
                    inicio = input("Data e hora de inicio: ")
                    fim = input("Data e hora de fim: ")
                    ok, msg = reserva_service.reservar(user.rm, lab_id, inicio, fim)
                    print("\n" + msg)
                except ValueError:
                    print("\nID do laboratorio deve ser um numero!")
                input("\nPressione Enter...")
            
            elif op == "4":
                reserva_service.minhas_reservas(user.rm)
                input("\nPressione Enter...")
            
            elif op == "5":
                limpar()
                print("="*50)
                print("CANCELAR RESERVA")
                print("="*50)
                reserva_service.minhas_reservas(user.rm)
                try:
                    res_id = int(input("\nDigite o ID da reserva para cancelar: "))
                    ok, msg = reserva_service.cancelar(res_id, user.rm)
                    print("\n" + msg)
                except ValueError:
                    print("\nID da reserva deve ser um numero!")
                input("\nPressione Enter...")
            
            elif op == "6" and auth.is_coordenador():
                reserva_service.todas_reservas()
                input("\nPressione Enter...")
            
            elif op == "0":
                auth.logout()


if __name__ == "__main__":
    main()