import os
import sys
from serviços.atentificação import AuthService
from serviços.laboratorio_serviços import LaboratorioService
from serviços.reserva_serviços import ReservaService

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa a execução até o usuário pressionar Enter"""
    input("\n⏎ Pressione Enter para continuar...")

def exibir_cabecalho(titulo):
    """Exibe um cabeçalho formatado"""
    limpar_tela()
    print("="*60)
    print(f"🏫 LABRESERVE FIAP - {titulo}")
    print("="*60)

def menu_principal():
    """Exibe o menu principal não logado"""
    print("\n1️⃣  Login")
    print("2️⃣  Cadastrar")
    print("0️⃣  Sair")
    return input("\n👉 Escolha uma opção: ")

def menu_aluno():
    """Exibe o menu do aluno logado"""
    print("\n📱 MENU ALUNO")
    print("-" * 40)
    print("1️⃣  Listar laboratórios")
    print("2️⃣  Verificar disponibilidade")
    print("3️⃣  Fazer reserva")
    print("4️⃣  Minhas reservas")
    print("5️⃣  Cancelar reserva")
    print("0️⃣  Logout")
    return input("\n👉 Escolha uma opção: ")

def menu_coordenador():
    """Exibe o menu do coordenador logado"""
    print("\n👔 MENU COORDENADOR")
    print("-" * 40)
    print("1️⃣  Listar laboratórios")
    print("2️⃣  Verificar disponibilidade")
    print("3️⃣  Fazer reserva (como aluno)")
    print("4️⃣  Minhas reservas")
    print("5️⃣  Cancelar reserva")
    print("6️⃣  📊 Ver todas as reservas")
    print("0️⃣  Logout")
    return input("\n👉 Escolha uma opção: ")

def fazer_reserva_flow(reserva_service, auth_service):
    """Fluxo para fazer uma reserva"""
    exibir_cabecalho("FAZER RESERVA")
    
    usuario = auth_service.get_usuario_logado()
    
    # Lista laboratórios disponíveis
    reserva_service.laboratorio_service.exibir_todos()
    
    try:
        id_lab = int(input("\n📌 Digite o ID do laboratório: "))
        
        print("\n📅 Digite a data e hora no formato: AAAA-MM-DD HH:MM")
        data_inicio = input("⏰ Data e hora de início: ")
        data_fim = input("⏰ Data e hora de fim: ")
        
        sucesso, mensagem = reserva_service.fazer_reserva(
            usuario.ra, id_lab, data_inicio, data_fim
        )
        
        print("\n" + "="*60)
        print(mensagem)
        print("="*60)
        
    except ValueError:
        print("\n❌ ID do laboratório deve ser um número!")
    
    pausar()

def cancelar_reserva_flow(reserva_service, auth_service):
    """Fluxo para cancelar uma reserva"""
    exibir_cabecalho("CANCELAR RESERVA")
    
    usuario = auth_service.get_usuario_logado()
    
    # Mostra reservas ativas do usuário
    reservas = reserva_service.listar_reservas_ativas_por_aluno(usuario.ra)
    
    if not reservas:
        print("\n📭 Você não possui reservas ativas para cancelar.")
        pausar()
        return
    
    print("\n📌 SUAS RESERVAS ATIVAS:")
    for r in reservas:
        lab = reserva_service.laboratorio_service.buscar_por_id(r.id_laboratorio)
        print(f"   #{r.id} - {lab.nome} - {r.data_inicio} até {r.data_fim}")
    
    try:
        id_reserva = int(input("\n❌ Digite o ID da reserva que deseja cancelar: "))
        
        sucesso, mensagem = reserva_service.cancelar_reserva(id_reserva, usuario.ra)
        
        print("\n" + "="*60)
        print(mensagem)
        print("="*60)
        
    except ValueError:
        print("\n❌ ID da reserva deve ser um número!")
    
    pausar()

def verificar_disponibilidade_flow(reserva_service, laboratorio_service):
    """Fluxo para verificar disponibilidade de um laboratório"""
    exibir_cabecalho("VERIFICAR DISPONIBILIDADE")
    
    laboratorio_service.exibir_todos()
    
    try:
        id_lab = int(input("\n📌 Digite o ID do laboratório: "))
        
        print("\n📅 Digite a data e hora no formato: AAAA-MM-DD HH:MM")
        data_inicio = input("⏰ Data e hora de início: ")
        data_fim = input("⏰ Data e hora de fim: ")
        
        disponivel, reserva_conflito = reserva_service.verificar_disponibilidade(
            id_lab, data_inicio, data_fim
        )
        
        print("\n" + "="*60)
        if disponivel:
            print("✅ Laboratório DISPONÍVEL para este horário!")
        else:
            print("❌ Laboratório INDISPONÍVEL para este horário!")
            print(f"   Conflito com reserva #{reserva_conflito.id}")
        print("="*60)
        
    except ValueError:
        print("\n❌ ID do laboratório deve ser um número!")
    
    pausar()

def main():
    """Função principal do sistema"""
    
    # Inicializa os serviços
    auth_service = AuthService()
    laboratorio_service = LaboratorioService()
    reserva_service = ReservaService(laboratorio_service)
    
    while True:
        if not auth_service.esta_logado():
            # Menu de login/cadastro
            exibir_cabecalho("BEM-VINDO")
            opcao = menu_principal()
            
            if opcao == "1":
                # Login
                exibir_cabecalho("LOGIN")
                ra = input("📌 Digite seu RA: ")
                senha = input("🔒 Digite sua senha: ")
                
                sucesso, mensagem = auth_service.login(ra, senha)
                print("\n" + mensagem)
                
                if not sucesso:
                    pausar()
                else:
                    # Login bem sucedido
                    print("\n✅ Redirecionando para o menu...")
                    pausar()
                    
            elif opcao == "2":
                # Cadastro
                exibir_cabecalho("CADASTRO")
                ra = input("📌 Digite seu RA: ")
                nome = input("📌 Digite seu nome completo: ")
                email = input("📌 Digite seu e-mail: ")
                senha = input("🔒 Digite sua senha: ")
                
                sucesso, mensagem = auth_service.cadastrar(ra, nome, email, senha)
                print("\n" + mensagem)
                pausar()
                
            elif opcao == "0":
                print("\n👋 Até logo!")
                sys.exit(0)
            else:
                print("\n❌ Opção inválida!")
                pausar()
        else:
            # Usuário logado
            usuario = auth_service.get_usuario_logado()
            
            if auth_service.is_coordenador():
                exibir_cabecalho(f"MENU COORDENADOR - {usuario.nome}")
                opcao = menu_coordenador()
                
                if opcao == "1":
                    laboratorio_service.exibir_todos()
                    pausar()
                    
                elif opcao == "2":
                    verificar_disponibilidade_flow(reserva_service, laboratorio_service)
                    
                elif opcao == "3":
                    fazer_reserva_flow(reserva_service, auth_service)
                    
                elif opcao == "4":
                    reserva_service.exibir_minhas_reservas(usuario.ra)
                    pausar()
                    
                elif opcao == "5":
                    cancelar_reserva_flow(reserva_service, auth_service)
                    
                elif opcao == "6":
                    reserva_service.exibir_todas_reservas()
                    pausar()
                    
                elif opcao == "0":
                    auth_service.logout()
                    print("\n👋 Logout realizado com sucesso!")
                    pausar()
                else:
                    print("\n❌ Opção inválida!")
                    pausar()
            else:
                exibir_cabecalho(f"MENU ALUNO - {usuario.nome}")
                opcao = menu_aluno()
                
                if opcao == "1":
                    laboratorio_service.exibir_todos()
                    pausar()
                    
                elif opcao == "2":
                    verificar_disponibilidade_flow(reserva_service, laboratorio_service)
                    
                elif opcao == "3":
                    fazer_reserva_flow(reserva_service, auth_service)
                    
                elif opcao == "4":
                    reserva_service.exibir_minhas_reservas(usuario.ra)
                    pausar()
                    
                elif opcao == "5":
                    cancelar_reserva_flow(reserva_service, auth_service)
                    
                elif opcao == "0":
                    auth_service.logout()
                    print("\n👋 Logout realizado com sucesso!")
                    pausar()
                else:
                    print("\n❌ Opção inválida!")
                    pausar()

if __name__ == "__main__":
    main()