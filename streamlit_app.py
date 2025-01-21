import streamlit as st

def calcular_media_diaria(x, y, z):
    dias_por_mes = 30  # Considerando 30 dias em um mês
    total_dias = z * dias_por_mes
    media_diaria_necessaria = (y + x * total_dias) / total_dias
    return media_diaria_necessaria

# Configuração da interface
st.title("Calculadora de Média de Sinistros Resolvidos por Dia")

st.write(
    "Insira os valores abaixo para calcular a média de sinistros que precisam ser resolvidos diariamente para alcançar a meta."
)

# Entrada de dados
x = st.number_input("Número médio de sinistros que entram por dia (x):", min_value=0.0, value=10.0, step=1.0)
y = st.number_input("Número atual de sinistros pendentes (y):", min_value=0.0, value=50.0, step=1.0)
z = st.number_input("Período desejado para reduzir os sinistros (em meses) (z):", min_value=0.1, value=6.0, step=0.1)

# Cálculo
if st.button("Calcular"):
    media_diaria = calcular_media_diaria(x, y, z)
    st.success(f"Para reduzir o número de sinistros pendentes em {z} meses, você precisará resolver, em média, {media_diaria:.2f} sinistros por dia.")
