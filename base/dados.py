# dados.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#carrega os dados
def carregar_dados():
    df = pd.read_csv('base/dataset/steam_games.csv')
    # Configure as fontes para japonês e chinês
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'Noto Sans CJK SC']
    plt.rcParams['axes.unicode_minus'] = False
    return df
    
#verifica os tipos de dados das colunas
def verificar_tipos_de_dados(df, colunas):
    tipos_de_dados = df[colunas].dtypes
    return tipos_de_dados

def top_10_melhores_avaliados(df):
     # Ordenar o DataFrame pelo Metacritic score em ordem decrescente e, em caso de empate, pela Release date em ordem decrescente
    df_sorted = df.sort_values(by=['Metacritic score', 'Release date'], ascending=[False, False])
    
    # Filtrar os 10 jogos mais bem avaliados
    top_10 = df_sorted.head(10)
    
    return top_10

def tratamento_de_dados(df):
    df['Publishers'] = df['Publishers'].str.upper()
    df['Movies'].fillna('Sem Filme', inplace=True)  # Preencher com "Sem Filme"
    return df
    
def calcular_estatisticas_rpg(df):
    df_rpg = df[df['Genres'] == 'RPG'].copy()
    media_dlc = df_rpg['DLC count'].mean()
    max_dlc = df_rpg['DLC count'].max()

    media_positive = df_rpg['Positive'].mean()
    max_positive = df_rpg['Positive'].max()

    media_negative = df_rpg['Negative'].mean()
    max_negative = df_rpg['Negative'].max()

    df_rpg['Has_Movies'] = df_rpg['Movies'].notna().astype(int)  # Cria coluna de presença de Movies
    df_rpg['Has_Screenshots'] = df_rpg['Screenshots'].notna().astype(int)  # Cria coluna de presença de Screenshots

    total_movies_and_screenshots = df_rpg['Has_Movies'] + df_rpg['Has_Screenshots']  # Soma das colunas Has_Movies e Has_Screenshots

    return {
        'media_dlc': media_dlc, 'max_dlc': max_dlc,
        'media_positive': media_positive, 'max_positive': max_positive,
        'media_negative': media_negative, 'max_negative': max_negative,
        'total_movies_and_screenshots': total_movies_and_screenshots,  # Soma das colunas Has_Movies e Has_Screenshots
        'df_rpg': df_rpg
    }

def tratar_coluna_publishers(df):
    df['Publishers'].fillna('Desconhecido', inplace=True)
    return df

def calcular_mediana_media_avaliacoes_positivas_empresas(df, empresas):
    resultados = {}
    
    for empresa in empresas:
        df_empresa = df[(df['Publishers'] == empresa) & (df['Price'] > 0)].copy()  # Faz uma cópia do DataFrame
        
        media = df_empresa['Positive'].mean()
        mediana = df_empresa['Positive'].median()
        
        resultados[empresa] = {'media': media, 'mediana': mediana}
    
    return resultados


def calcular_top_empresas(df):
    top_empresas = df[df['Price'] > 0]['Publishers'].value_counts().head(5)
    return top_empresas

import pandas as pd

def verificar_crescimento_jogos_linux(df):
    # Converter a coluna 'Release date' para o tipo datetime
    df['Release date'] = pd.to_datetime(df['Release date'], errors='coerce')

    # Filtrar jogos Linux com datas válidas
    jogos_linux = df[(df['Linux'] == True) & (df['Release date'].notna())]

    # Filtrar jogos lançados entre 2018 e 2022
    jogos_filtrados = jogos_linux[(jogos_linux['Release date'].dt.year >= 2018) & (jogos_linux['Release date'].dt.year <= 2022)]

    # Verificar se houve crescimento entre 2018 e 2022
    houve_crescimento = len(jogos_filtrados) > 0

    # Contar o número de jogos em cada ano
    num_jogos_em_2018 = len(jogos_filtrados[jogos_filtrados['Release date'].dt.year == 2018])
    num_jogos_em_2019 = len(jogos_filtrados[jogos_filtrados['Release date'].dt.year == 2019])
    num_jogos_em_2020 = len(jogos_filtrados[jogos_filtrados['Release date'].dt.year == 2020])
    num_jogos_em_2021 = len(jogos_filtrados[jogos_filtrados['Release date'].dt.year == 2021])
    num_jogos_em_2022 = len(jogos_filtrados[jogos_filtrados['Release date'].dt.year == 2022])

    # Converter a resposta para 'Sim' em vez de True
    houve_crescimento_texto = 'Sim' if houve_crescimento else 'Não'

    return {
        'houve_crescimento': houve_crescimento_texto,
        'num_jogos_em_2018': num_jogos_em_2018,
        'num_jogos_em_2019': num_jogos_em_2019,
        'num_jogos_em_2020': num_jogos_em_2020,
        'num_jogos_em_2021': num_jogos_em_2021,
        'num_jogos_em_2022': num_jogos_em_2022
    }

def gerar_grafico_distribuicao_jogos_so(df):
    # Filtrar apenas os jogos que suportam pelo menos um dos sistemas operacionais
    df_filtered = df[df[['Mac', 'Windows', 'Linux']].any(axis=1)]

    # Criar uma nova coluna 'TotalVotes' contendo a quantidade de votos (sistemas suportados)
    df_filtered['TotalVotes'] = df_filtered[['Mac', 'Windows', 'Linux']].sum(axis=1)

    # Calcular a contagem de votos para cada sistema operacional
    vote_counts = df_filtered[['Mac', 'Windows', 'Linux']].sum()

    # Se um jogo suporta todos os três sistemas, contar como um voto para cada SO
    all_three = df_filtered[(df_filtered['Mac'] & df_filtered['Windows'] & df_filtered['Linux'])]
    if not all_three.empty:
        vote_counts += len(all_three)

    # Calcular o percentual de jogos para cada SO
    percentages = (vote_counts / vote_counts.sum()) * 100

    # Rótulos para os sistemas operacionais
    labels = percentages.index

    # Cores para as fatias do gráfico
    colors = ['maroon', 'darkkhaki', 'darkslategrey']
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, pctdistance=0.85)

# Definir as cores do texto dentro das fatias
    for text, autotext in zip(texts, autotexts):
        text.set(size=10, color='black')
        autotext.set(size=10, color='snow')

    # Adicionar uma legenda
    plt.legend(labels, loc='upper right')

    plt.axis('equal')  # Garante que a pizza seja desenhada como um círculo.
    plt.title('Distribuição de Jogos por Sistema Operacional')

    # Exibir o gráfico
    plt.show()

def gerar_grafico_votos_por_so(df):
    # Crie novas colunas para contar os votos de suporte para cada sistema operacional
    df['Votos_Mac'] = df['Mac'].apply(lambda x: 1 if x else 0)
    df['Votos_Windows'] = df['Windows'].apply(lambda x: 1 if x else 0)
    df['Votos_Linux'] = df['Linux'].apply(lambda x: 1 if x else 0)

    # Some os votos para cada sistema operacional
    total_votos_mac = df['Votos_Mac'].sum()
    total_votos_windows = df['Votos_Windows'].sum()
    total_votos_linux = df['Votos_Linux'].sum()

    # Crie uma lista com os totais de votos para cada sistema operacional
    totais = [total_votos_mac, total_votos_windows, total_votos_linux]

    # Crie uma lista com os rótulos para cada sistema operacional
    sistemas = ['Mac', 'Windows', 'Linux']

    # Crie um gráfico de barras
    plt.bar(sistemas, totais, color=['maroon', 'darkkhaki', 'darkslategrey'])

    # Adicione rótulos aos eixos
    plt.xlabel('Sistema Operacional')
    plt.ylabel('Total de Votos')

    # Adicione um título
    plt.title('Total de Votos por Sistema Operacional')
    # Mostre o gráfico
    plt.show()


def tendencia_jogos_singleplayer(df):
    # 1. Converter a coluna 'Release date' para datetime
    df['Release date'] = pd.to_datetime(df['Release date'])

    # 2. Filtrar os dados para jogos Indie e Estratégia
    df_indie = df[(df['Genres'].str.contains('Indie')) &
                  (df['Release date'].dt.year >= 2010) & (df['Release date'].dt.year <= 2020) &
                  (df['Categories'] == 'Single-player')]

    df_strategy = df[(df['Genres'].str.contains('Strategy')) &
                     (df['Release date'].dt.year >= 2010) & (df['Release date'].dt.year <= 2020) &
                     (df['Categories'] == 'Single-player')]

    # 3. Agrupar e contar o número de jogos para Indie
    grouped_indie = df_indie.groupby(df_indie['Release date'].dt.year)['Name'].count()

    # 4. Agrupar e contar o número de jogos para Estratégia
    grouped_strategy = df_strategy.groupby(df_strategy['Release date'].dt.year)['Name'].count()

    # 5. Plote os dados para Indie
    plt.figure(figsize=(12, 6))
    plt.plot(grouped_indie.index, grouped_indie.values, marker='o', label='Indie', color='darkcyan')
    for i, value in enumerate(grouped_indie.values):
        plt.text(grouped_indie.index[i], value, str(value), ha='right', va='bottom')

    # 6. Plote os dados para Estratégia
    plt.plot(grouped_strategy.index, grouped_strategy.values, marker='o', label='Estratégia', color='saddlebrown')
    for i, value in enumerate(grouped_strategy.values):
        plt.text(grouped_strategy.index[i], value, str(value), ha='right', va='bottom')

    plt.xlabel('Ano')
    plt.ylabel('Número de Jogos Single-Player')
    plt.title('Tendência de Jogos Single-Player nos Gêneros "Indie" e "Estratégia" (2010-2020)')
    plt.grid(True)
    plt.legend()

    return plt


def obter_top_10_jogos(df):
    """
    Obtém os 10 jogos com as maiores pontuações de usuário.
    
    Args:
    df (pd.DataFrame): O DataFrame contendo os dados dos jogos.

    Returns:
    pd.DataFrame: Um DataFrame com as informações dos 10 jogos com as maiores pontuações.
    """
    # Ordene o DataFrame pelo User Score em ordem decrescente e pegue os 10 primeiros jogos
    top_10_jogos = df.nlargest(10, 'User score')

    # Crie um novo DataFrame com as informações dos 10 jogos com as maiores pontuações
    top_10_df = top_10_jogos[['AppID', 'Name', 'User score']]

    return top_10_df

def calcular_tempo_medio_jogo(df):
    """
    Calcula o tempo médio de jogo a partir da coluna 'Average playtime forever'.

    Args:
    df (pd.DataFrame): O DataFrame contendo os dados dos jogos.

    Returns:
    pd.Series: Uma série com o tempo médio de jogo para cada jogo.
    """
    # Converte a coluna 'Average playtime forever' para o tipo numérico (pode ser necessário ajustar o formato)
    df['Average playtime forever'] = pd.to_numeric(df['Average playtime forever'], errors='coerce')

    # Calcula o tempo médio de jogo para cada jogo
    tempo_medio_por_jogo = df.groupby('Name')['Average playtime forever'].mean()

    return tempo_medio_por_jogo

def plotar_grafico_tempo_medio(tempo_medio_por_jogo):
    """
    Plota um gráfico de barras com o tempo médio de jogo para cada jogo.

    Args:
    tempo_medio_por_jogo (pd.Series): Uma série com o tempo médio de jogo para cada jogo.
    """
    # Ordena os dados em ordem decrescente
    tempo_medio_por_jogo = tempo_medio_por_jogo.sort_values(ascending=False)

    # Plota o gráfico de barras
    plt.figure(figsize=(10, 6))
    tempo_medio_por_jogo.plot(kind='bar', color='skyblue')
    plt.xlabel('Jogo')
    plt.ylabel('Tempo Médio de Jogo (minutos)')
    plt.title('Tempo Médio de Jogo por Jogo')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Exibe o gráfico
    plt.show()

def gerar_histograma_top_10_jogos(df):
    # Ordene o DataFrame pelos maiores valores de 'Average playtime forever' e pegue os 10 primeiros
    top_10_games = df.nlargest(10, 'Average playtime forever')

    # Configure a paleta de cores (você pode escolher uma paleta de cores diferente aqui)
    sns.set_palette("deep")

    # Crie o gráfico de histograma
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Average playtime forever', y='Name', data=top_10_games)

    # Adicione rótulos aos eixos
    plt.xlabel('Tempo Médio de Jogo (horas)')
    plt.ylabel('Nome do Jogo')

    # Adicione um título
    plt.title('Top 10 Jogos com Maior Tempo Médio de Jogo')

    # Mostre o gráfico
    plt.tight_layout()
    plt.show()
