import json
from datetime import datetime
from ..modelos.reserva import Reserva

class ReservaService:
    """Gerencia as reservas de laboratórios"""
    
    ARQUIVO_DADOS = "src/data/reservas.json"
    
    def __init__(self, laboratorio_service):
        self.laboratorio_service = laboratorio_service
        self.reservas = []
        self.carregar_reservas()
    
    def carregar_reservas(self):
        """Carrega as reservas do arquivo JSON"""
        try:
            with open(self.ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.reservas = [Reserva.from_dict(r) for r in dados]
        except FileNotFoundError:
            self.reservas = []
    
    def salvar_reservas(self):
        """Salva as reservas no arquivo JSON"""
        with open(self.ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in self.reservas], f, indent=2, ensure_ascii=False)
    
    def verificar_disponibilidade(self, id_laboratorio, data_inicio, data_fim):
        """
        Verifica se um laboratório está disponível no horário solicitado.
        <<include>> do caso de uso Fazer Reserva
        """
        for reserva in self.reservas:
            if reserva.id_laboratorio == id_laboratorio and reserva.status == "ativa":
                # Verifica conflito de horário
                if not (data_fim <= reserva.data_inicio or data_inicio >= reserva.data_fim):
                    return False, reserva
        return True, None
    
    def fazer_reserva(self, ra_aluno, id_laboratorio, data_inicio, data_fim):
        """
        Realiza uma nova reserva.
        Caso de uso: Fazer Reserva
        """
        # Verifica se o laboratório existe
        laboratorio = self.laboratorio_service.buscar_por_id(id_laboratorio)
        if not laboratorio:
            return False, "Laboratório não encontrado!"
        
        # Verifica disponibilidade (<<include>>)
        disponivel, reserva_conflito = self.verificar_disponibilidade(id_laboratorio, data_inicio, data_fim)
        if not disponivel:
            return False, f"Laborátorio já reservado neste horário! (Reserva #{reserva_conflito.id})"
        
        # Valida horários
        if data_inicio >= data_fim:
            return False, "Data de início deve ser anterior à data de fim!"
        
        if data_inicio < datetime.now().strftime("%Y-%m-%d %H:%M"):
            return False, "Não é possível reservar em horário passado!"
        
        # Cria a reserva
        novo_id = max([r.id for r in self.reservas], default=0) + 1
        nova_reserva = Reserva(
            id=novo_id,
            ra_aluno=ra_aluno,
            id_laboratorio=id_laboratorio,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        self.reservas.append(nova_reserva)
        self.salvar_reservas()
        
        return True, f"✅ Reserva #{novo_id} confirmada com sucesso!\n   Laboratório: {laboratorio.nome}\n   Horário: {data_inicio} até {data_fim}"
    
    def cancelar_reserva(self, id_reserva, ra_aluno):
        """
        Cancela uma reserva existente.
        Caso de uso: Cancelar Reserva
        """
        for reserva in self.reservas:
            if reserva.id == id_reserva:
                if reserva.ra_aluno != ra_aluno:
                    return False, "Você só pode cancelar suas próprias reservas!"
                
                if reserva.status != "ativa":
                    return False, "Esta reserva já foi cancelada ou concluída!"
                
                reserva.status = "cancelada"
                self.salvar_reservas()
                return True, f"✅ Reserva #{id_reserva} cancelada com sucesso!"
        
        return False, f"Reserva #{id_reserva} não encontrada!"
    
    def listar_reservas_por_aluno(self, ra_aluno):
        """Lista todas as reservas de um aluno específico"""
        reservas_aluno = [r for r in self.reservas if r.ra_aluno == ra_aluno]
        return reservas_aluno
    
    def listar_reservas_ativas_por_aluno(self, ra_aluno):
        """Lista reservas ativas de um aluno"""
        return [r for r in self.reservas if r.ra_aluno == ra_aluno and r.status == "ativa"]
    
    def exibir_minhas_reservas(self, ra_aluno):
        """Exibe as reservas do aluno formatadas"""
        reservas = self.listar_reservas_ativas_por_aluno(ra_aluno)
        
        if not reservas:
            print("\n📭 Você não possui reservas ativas.")
            return
        
        print("\n" + "="*60)
        print("📌 MINHAS RESERVAS ATIVAS")
        print("="*60)
        for r in reservas:
            lab = self.laboratorio_service.buscar_por_id(r.id_laboratorio)
            nome_lab = lab.nome if lab else "Laboratório não encontrado"
            print(f"\n🔹 Reserva #{r.id}")
            print(f"   Laboratório: {nome_lab}")
            print(f"   Início: {r.data_inicio}")
            print(f"   Fim: {r.data_fim}")
            print(f"   Status: {r.status}")
        print("\n" + "="*60)
    
    def exibir_todas_reservas(self):
        """Exibe todas as reservas (apenas coordenador)"""
        if not self.reservas:
            print("\n📭 Nenhuma reserva cadastrada.")
            return
        
        print("\n" + "="*60)
        print("📋 TODAS AS RESERVAS")
        print("="*60)
        for r in self.reservas:
            lab = self.laboratorio_service.buscar_por_id(r.id_laboratorio)
            nome_lab = lab.nome if lab else "N/A"
            print(f"\n🔹 Reserva #{r.id} | Status: {r.status}")
            print(f"   Aluno RA: {r.ra_aluno}")
            print(f"   Laboratório: {nome_lab}")
            print(f"   Início: {r.data_inicio}")
            print(f"   Fim: {r.data_fim}")
        print("\n" + "="*60)