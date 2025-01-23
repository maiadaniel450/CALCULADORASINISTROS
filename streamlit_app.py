import streamlit as st
import pandas as pd
from io import BytesIO

# Função de cálculo da média diária de sinistros
def calcular_media_diaria(x, y, z):
    dias_por_mes = 30  # Considerando 30 dias em um mês
    total_dias = z * dias_por_mes
    media_diaria_necessaria = (y + x * total_dias) / total_dias
    return media_diaria_necessaria

# Função para concatenar relatórios com verificação de colunas
def concatenar_relatorios(relatorios):
    # Lê o primeiro relatório para base
    relatorio_base = relatorios[0]

    for relatorio in relatorios[1:]:
        # Verifica se as colunas são compatíveis
        if list(relatorio.columns) != list(relatorio_base.columns):
            raise ValueError("Os relatórios possuem colunas incompatíveis!")

        # Concatena os relatórios
        relatorio_base = pd.concat([relatorio_base, relatorio], ignore_index=True)

    return relatorio_base

# Função para processar planilha de seguradoras
def processar_planilha(file, seguradoras_permitidas):
    # Lê a planilha enviada
    df = pd.read_excel(file)

    # Identifica a coluna da seguradora com base em possíveis variações de nome
    colunas_seguradora = [col for col in df.columns if col.upper() in ["SEG", "SEGURADORA"]]
    
    if not colunas_seguradora:
        st.error("Nenhuma coluna correspondente a 'Seguradora' foi encontrada.")
        return None

    coluna_alvo = colunas_seguradora[0]

    # Substitui seguradoras não permitidas por "CONGÊNERE 1", "CONGÊNERE 2", etc.
    df[coluna_alvo] = df[coluna_alvo].apply(lambda x: x if x in seguradoras_permitidas else None)
    df[coluna_alvo] = df[coluna_alvo].fillna(pd.Series([f"CONGÊNERE {i+1}" for i in range(len(df))]))

    return df

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
st.title("Sistema de Gestão de Sinistros e Seguradoras")

# Criação do menu de navegação
pagina = st.selectbox("Escolha a opção", ("Calculadora de Sinistros", "Concatenar Relatório", "Processar Seguradoras"))

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
    st.write("Aqui você pode concatenar até 20 relatórios com colunas de títulos semelhantes.")

    # Upload de múltiplos relatórios
    arquivos = st.file_uploader("Carregar relatórios (XLSX), até 20 arquivos:", type=["xlsx"], accept_multiple_files=True)

    if arquivos:
        # Inicializar lista para armazenar DataFrames
        relatorios = []
        
        # Processar cada arquivo
        for arquivo in arquivos:
            try:
                # Carregar o relatório
                relatorio = pd.read_excel(arquivo)
                
                # Adicionar à lista
                relatorios.append(relatorio)

                # Exibir uma amostra do relatório carregado
                st.write(f"Relatório {arquivo.name} carregado com sucesso:")
                st.dataframe(relatorio.head())

            except Exception as e:
                st.error(f"Erro ao carregar o arquivo {arquivo.name}: {e}")

        # Concatenar os relatórios
        if len(relatorios) > 0 and st.button("Concatenar Relatórios"):
            try:
                # Concatenar todos os relatórios carregados
                relatorio_concatenado = concatenar_relatorios(relatorios)
                st.success("Relatórios concatenados com sucesso!")
                st.write("Relatório Concatenado (Amostra):")
                st.dataframe(relatorio_concatenado.head())

                # Download do relatório concatenado
                output = BytesIO()
                relatorio_concatenado.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)

                st.download_button(
                    label="Baixar Relatório Completo",
                    data=output,
                    file_name="relatorio_concatenado_completo.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            except Exception as e:
                st.error(f"Erro ao concatenar os relatórios: {e}")

elif pagina == "Processar Seguradoras":
    st.write("Substitua seguradoras na planilha conforme critérios definidos.")

    # Upload de arquivo
    uploaded_file = st.file_uploader("Envie sua planilha", type=["xlsx", "xls"])
    seguradoras_permitidas = st.text_area("Digite as seguradoras permitidas separadas por vírgulas", "")

    if uploaded_file and seguradoras_permitidas:
        seguradoras_lista = [seg.strip() for seg in seguradoras_permitidas.split(",")]

        planilha_processada = processar_planilha(uploaded_file, seguradoras_lista)

        if planilha_processada is not None:
            st.success("Processamento concluído! Faça o download da planilha alterada abaixo.")
            output = BytesIO()
            planilha_processada.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="Baixar planilha",
                data=output,
                file_name="planilha_processada.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


