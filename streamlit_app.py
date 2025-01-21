import streamlit as st
import pandas as pd

# Função de cálculo da média diária de sinistros
def calcular_media_diaria(x, y, z):
    dias_por_mes = 30  # Considerando 30 dias em um mês
    total_dias = z * dias_por_mes
    media_diaria_necessaria = (y + x * total_dias) / total_dias
    return media_diaria_necessaria

# Função para concatenar relatórios
def concatenar_relatorios(relatorio_1, relatorio_2):
    # Garantir que ambos os relatórios têm colunas com os mesmos títulos
    relatorio_concatenado = pd.concat([relatorio_1, relatorio_2], ignore_index=True)
    return relatorio_concatenado

# Estilo personalizado para o tema dark com cores agressivas
st.markdown("""
    <style>
        /* Fundo escuro */
        .main {
            background-color: #181818;
        }

        /* Estilo dos títulos */
        h1 {
            color: #e60000;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
        }

        h2, h3, .css-1xarl3v {
            color: #c299ff;
        }

        /* Tamanho e cor dos textos */
        .css-1v3fvcr {
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }

        /* Cores dos botões */
        .stButton>button {
            background-color: #c299ff;
            color: #ffffff;
            font-weight: bold;
            border-radius: 5px;
        }
        
        .stButton>button:hover {
            background-color: #e60000;
            color: #fff;
        }

        /* Estilo do input box */
        .stNumberInput>div>label {
            color: #e60000;
        }
        .stNumberInput>div>input {
            background-color: #333;
            color: #fff;
            border: 1px solid #c299ff;
            border-radius: 5px;
            padding: 5px;
        }

        /* Estilo dos DataFrames */
        .stDataFrame {
            background-color: #222;
            color: #fff;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Configuração da interface
st.title("Sistema de Gestão de Sinistros")

# Criação do menu de navegação
pagina = st.selectbox("Escolha a opção", ("Calculadora de Sinistros", "Concatenar Relatório"))

if pagina == "Calculadora de Sinistros":
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

elif pagina == "Concatenar Relatório":
    st.write("Aqui você pode concatenar dois relatórios com colunas de títulos semelhantes.")

    # Upload dos relatórios
    arquivo_1 = st.file_uploader("Carregar o primeiro relatório (CSV):", type=["csv"])
    arquivo_2 = st.file_uploader("Carregar o segundo relatório (CSV):", type=["csv"])

    if arquivo_1 and arquivo_2:
        # Carregar os dados dos arquivos CSV
        relatorio_1 = pd.read_csv(arquivo_1)
        relatorio_2 = pd.read_csv(arquivo_2)

        # Exibir uma amostra dos dados
        st.write("Primeiro Relatório:")
        st.dataframe(relatorio_1.head())
        st.write("Segundo Relatório:")
        st.dataframe(relatorio_2.head())

        # Concatenar os relatórios
        if st.button("Concatenar Relatórios"):
            try:
                relatorio_concatenado = concatenar_relatorios(relatorio_1, relatorio_2)
                st.success("Relatórios concatenados com sucesso!")
                st.write("Relatório Concatenado:")
                st.dataframe(relatorio_concatenado.head())
            except Exception as e:
                st.error(f"Erro ao concatenar os relatórios: {e}")

