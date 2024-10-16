import streamlit as st
import numpy as np

# Função para simular a fila com atendentes trabalhando simultaneamente
def simulate_queue(num_attendants, num_processes, central_type):
    # Definindo os tempos de atendimento baseados no tipo de central
    if central_type == "Central 1":
        service_times = np.full(num_processes, 40)  # Todos os processos demoram 40 dias
    else:
        service_times = np.full(num_processes, 60)  # Todos os processos demoram 60 dias

    # Ordena os tempos de atendimento (menores primeiros) para simular o atendimento mais eficiente
    service_times.sort()
    
    total_time = 0
    processes_remaining = num_processes
    busy_time = 0  # Tempo total ocupado dos atendentes

    # Simulação do atendimento simultâneo
    while processes_remaining > 0:
        # Pega até 'num_attendants' processos ao mesmo tempo
        current_batch_size = min(num_attendants, processes_remaining)
        # O tempo para concluir esta rodada é o tempo do processo mais longo na rodada atual
        round_time = service_times[-current_batch_size]
        total_time += round_time
        busy_time += round_time * current_batch_size  # Soma o tempo que os atendentes ficaram ocupados

        # Remove os processos atendidos nesta rodada
        service_times = service_times[:-current_batch_size]
        processes_remaining -= current_batch_size

    # Tempo total disponível dos atendentes durante o atendimento
    total_attendant_time = num_attendants * total_time
    
    # Cálculo da taxa de utilização
    utilization_rate = busy_time / total_attendant_time if total_attendant_time > 0 else 0

    return total_time, utilization_rate

# Função para exibir informações da central
def show_central_info(central_name, num_attendants, num_processes, utilization_rate):
    st.write(f"### Informações da {central_name}")
    st.write(f"**Número de processos ativos:** {num_processes}")
    st.write(f"**Número de atendentes:** {num_attendants}")
    st.write(f"**Taxa de utilização:** {utilization_rate:.2%}")

# Configurações do Streamlit
st.title("Simulação de Teoria das Filas com Atendentes Simultâneos")

# Simular duas centrais
centrais = {
    "Central Varejo (40 dias)": {"atendentes": 3, "processos": 10},
    "Central Grande (60 dias)": {"atendentes": 4, "processos": 8},
}

# Exibição das centrais
st.write("### Centrais Disponíveis")
for central_name, data in centrais.items():
    if st.button(central_name):
        total_time, utilization_rate = simulate_queue(data["atendentes"], data["processos"], central_name)
        show_central_info(central_name, data["atendentes"], data["processos"], utilization_rate)

# Seção de simulação personalizada
st.write("---")
st.write("### Simulação Personalizada")

# Opções de seleção para a central
central_type = st.selectbox("Escolha a central:", ["Central Pequena (40 dias)", "Central Média/Grande (60 dias)"])

num_attendants = st.number_input("Número de atendentes:", min_value=1, value=1)
num_processes = st.number_input("Número de processos:", min_value=1, value=1)

if st.button("Simular"):
    # Determina o tipo de central com base na seleção do usuário
    if central_type == "Central 1 (40 dias)":
        total_time, utilization_rate = simulate_queue(num_attendants, num_processes, "Central 1")
    else:
        total_time, utilization_rate = simulate_queue(num_attendants, num_processes, "Central 2")

    st.write(f"Tempo total para atender todos os processos: {total_time} dias.")
    st.write(f"Taxa de utilização do sistema: {utilization_rate:.2%}")

