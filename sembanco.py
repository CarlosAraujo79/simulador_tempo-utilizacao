import streamlit as st
import numpy as np
import os

# Função para carregar o estilo CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Carregar o arquivo CSS
local_css("styles.css")

# Função para simular a fila com atendentes trabalhando simultaneamente
def simulate_queue(num_attendants, num_processes, existing_processes, central_type):
    if central_type == "Central Pequena (40 dias)":
        service_times = np.full(num_processes, 40)
    else:
        service_times = np.full(num_processes, 60)

    existing_service_times = np.full(existing_processes, 40 if central_type == "Central Pequena (40 dias)" else 60)
    service_times = np.concatenate((service_times, existing_service_times))

    service_times.sort()
    
    total_time = 0
    processes_remaining = len(service_times)
    busy_time = 0

    while processes_remaining > 0:
        current_batch_size = min(num_attendants, processes_remaining)
        round_time = service_times[-current_batch_size]
        total_time += round_time
        busy_time += round_time * current_batch_size
        service_times = service_times[:-current_batch_size]
        processes_remaining -= current_batch_size

    total_attendant_time = num_attendants * total_time
    utilization_rate = busy_time / total_attendant_time if total_attendant_time > 0 else 0

    return total_time, utilization_rate

# Função para exibir informações da central
def show_central_info(central_name, total_attendants, total_processes, utilization_rate, total_time):
    st.write(f"### Informações da {central_name}")
    st.write(f"**Número total de processos (ativos + novos):** {total_processes}")
    st.write(f"**Número total de atendentes:** {total_attendants}")
    st.write(f"**Taxa de utilização:** {utilization_rate:.2%}")
    st.write(f"**Tempo total para atender todos os processos:** {total_time} dias")

# Exibição das centrais usando expanders (acordeão)
st.write("### Centrais Disponíveis")
for central_name, data in centrais.items():
    with st.expander(central_name):
        total_processes = data["processos"] + data["existentes"]
        total_time, utilization_rate = simulate_queue(data["atendentes"], data["processos"], data["existentes"], central_name)
        show_central_info(central_name, data["atendentes"], total_processes, utilization_rate, total_time)


# Configurações do Streamlit
st.title("Acompanhamento de uso das Centrais - Banco do Nordeste")

# Simular duas centrais com processos existentes
centrais = {
    "Central Varejo (40 dias)": {"atendentes": 3, "processos": 5, "existentes": 5},
    "Central Grande (60 dias)": {"atendentes": 4, "processos": 3, "existentes": 3},
}

# Exibição das centrais usando expanders (acordeão)
st.write("### Centrais Disponíveis")
for central_name, data in centrais.items():
    with st.expander(central_name):
        total_processes = data["processos"] + data["existentes"]
        total_time, utilization_rate = simulate_queue(data["atendentes"], data["processos"], data["existentes"], central_name)
        show_central_info(central_name, data["atendentes"], total_processes, utilization_rate)

# Seção de simulação personalizada com expander
st.write("---")
with st.expander("Simulação Personalizada"):
    st.write("### Personalize a Simulação")

    # Opções de seleção para a central
    central_type = st.selectbox("Escolha a central:", ["Central Pequena (40 dias)", "Central Grande (60 dias)"])

    # Entrada de novos atendentes e processos para simulação
    num_attendants = st.number_input("Número de atendentes adicionados:", min_value=1, value=1)
    num_processes = st.number_input("Número de processos novos adicionados:", min_value=1, value=1)

    # Obter número de processos e atendentes existentes com base na central selecionada
    if central_type == "Central Pequena (40 dias)":
        existing_processes = centrais["Central Varejo (40 dias)"]["existentes"]
        current_total_processes = centrais["Central Varejo (40 dias)"]["processos"] + existing_processes
        current_total_attendants = centrais["Central Varejo (40 dias)"]["atendentes"]
    else:
        existing_processes = centrais["Central Grande (60 dias)"]["existentes"]
        current_total_processes = centrais["Central Grande (60 dias)"]["processos"] + existing_processes
        current_total_attendants = centrais["Central Grande (60 dias)"]["atendentes"]

    # Exibir quantidade atual de processos e atendentes
    st.write(f"**Quantidade atual de processos:** {current_total_processes}")
    st.write(f"**Quantidade atual de atendentes:** {current_total_attendants}")

    if st.button("Simular"):
        total_attendants_after = num_attendants + current_total_attendants
        total_processes_after = num_processes + current_total_processes
        total_time, utilization_rate = simulate_queue(total_attendants_after, num_processes, existing_processes, central_type)

        st.write(f"**Quantidade total de processos após a adição:** {total_processes_after}")
        st.write(f"**Quantidade total de atendentes após a simulação:** {total_attendants_after}")
        st.write(f"Tempo total para atender todos os processos: {total_time} dias.")
        st.write(f"Taxa de utilização do sistema: {utilization_rate:.2%}")
