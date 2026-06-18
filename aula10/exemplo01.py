import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Preparação dos dados
try:
    print('\nObtendo os dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    # utf-8, iso-8859-1, latin1, co1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    
    # variáveis
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    
    # Totalizando os roubos pelos municípios
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    
    # Ordenando o df
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo', ascending=False)
    
    
    print(df_roubo_veiculo.head(10))
except Exception as e:
    print(f'\nErro ao obter dados: Erro de{e}')
#---------------------------------------------------------------------------------------------#


# Obtendo as medidas
try:
    print('\nCalculando as medidas...')    
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])
    
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100)
    
    
    print('\nMedidas de Tendência Central')
    print(30*'-')
    print(f'Média: {media_roubo_veiculo:.0f}')            
    print(f'Mediana: {mediana_roubo_veiculo:.0f}')          
    print(f'Distância da média para mediana: {distancia:.0f}%') 
    
    # 0 - 10% dados simétricos = tem a tendencia de seguir uma certa simetria
    # 10 - 25% dados assimetricos = tem a tendencia de ter uma assimetria moderada pode ser usada como uma medida de resumo
    # 25%+ não é padrão =
except Exception as e:
    print(f'Erro ao processar as medidas: {e}')


# Obtendo a distribuição
try:
    print('\nProcessando os quartis')
    
    q1 = np.quantile(array_roubo_veiculo, .25)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nQuartis')
    print(95*'-')
    print(f'25% dos municípios tiveram roubo com valores menores que {q1:.0f} durante o periodo de 2003 à 2026')
    print(f'50%: {mediana_roubo_veiculo:.0f}')
    print(f'25% dos municípios tiveram roubo com valores maiores que {q3:.0f} durante o periodo de 2003 à 2026')

# Municipios com menores números de roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]

# Municipios com maiores números de roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]
    
    print('\nMunicípios')
    print('\nOs municípios com as menores quantidades de roubos')
    print(50*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    print('\nOs municípios com as maiores quantidades de roubos')
    print(50*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    # #IQR  = Amplitude
    # iqr = q3 - q1
    # print('Outliers')
    # print(30*'-')
except Exception as e:
    print(f'Erro ao distribuir: {e}')
    
# Obtendo Medidas de dispersão

try:
    #Amplitude total
    #amplitude = máximo - mínimo
    #Resultado: mais próximo do mínimo, baixa dispersão. Maior homogeneidade dos dados.
    #Se for 0, quer dizer que todos os dados são iguais.
    #mais próximo do maior valor, alta variabilidade. Menos homogeneidade.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo
    
    
    print('\nMedidas de dispersão')
    print(20*'-')
    print(f'Maior valor: {maximo}')
    print(f'Menor valor: {minimo}')
    print(f'Amplitude Total: {amplitude}')
    
except Exception as e:
    print(f'Erro ao calcular medidas de dispersão: {e}')
    
#Calculando Outliers

try:
    # IQR (Intervalo Interquartil) == Amplitude dos 50% dos dados mais centrais.
    # iqr = q3 - q1
    # Ele ignora os valores extremos. Max e Min estão fora do intervalo interquartil.
    # Não sofre interferência dos valores extremos.
    # Quanto mais próximo do Zero, mais homogêneos são os dados.
    # Quanto mais próximo do Q3, menos homogêneos são os dados.
    iqr = q3 - q1
    
    # limite inferior
    # Identifica como outliers, os valores abaixo dele
    limite_inferior = q1 - (1.5 * iqr)
    
    # limite superior
    # Identifica como outliers, os valores acima dele
    limite_superior = q3 + (1.5 * iqr)
    
    
    print('\nMedidas')
    print(30*'-')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Mediada: {mediana_roubo_veiculo}') # Q2
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')
     
except Exception as e:
    print(f'Erro ao calcular os limites')
    
    
try:
    # Outliers Superior
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    # Outliers Inferiores
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    
    
    print('\nMunicípios c/ Outliers Inferiores')
    print(33*'-')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existe outliers inferiores')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=True))
    
    
    
    print('\nMunicípios c/ Outliers Superiores')
    print(33*'-')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers inferiores')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))
    
    
    
except Exception as e:
    print(f'Erro ao calcular os Outliers: {e}')
    
    
    
    
# Visualizando os dados

try:
    # df_roubo_veiculo_maiores = df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False).head(10)
    # # Plotando o Gráfico Colunas
    # plt.bar(df_roubo_veiculo_maiores['munic'], df_roubo_veiculo_maiores['roubo_veiculo'])
    plt.subplots(2, 2, figsize=(18, 8))
    
    # BOXPLOT
    plt.subplot(2, 2, 1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title('Boxplot da Distribuição')
    
    # MEDIDAS
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo:.0f}')
    plt.text(0.1, 0.8, f'Distância: {distancia:.0f}%')
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior:.0f}')
    plt.text(0.1, 0.6, f'Mínimo: {minimo:.0f}')
    plt.text(0.1, 0.5, f'Q1: {q1:.0f}')
    plt.text(0.1, 0.4, f'Mediana: {mediana_roubo_veiculo:.0f}')
    plt.text(0.1, 0.3, f'Q3: {q3:.0f}')
    plt.text(0.1, 0.2, f'Máximo: {maximo:.0f}')
    plt.text(0.1, 0.1, f'Limite Superior: {limite_superior:.0f}')
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude:.0f}')
    
    plt.axis('off')
    plt.title('Medidas')
    
    
    # OUTLIERS SUPERIORES
    plt.subplot(2, 2, 3)
    df_roubo_veiculo_outliers_superiores = (
        df_roubo_veiculo_outliers_superiores
        .head(10)
        .sort_values(by='roubo_veiculo', ascending=False)
    )
    
    plt.bar(
        # .str.slice(0, 10) - Corta as palavras
        df_roubo_veiculo_outliers_superiores['munic'], 
        df_roubo_veiculo_outliers_superiores['roubo_veiculo']
    )
    
    deslocamento = max(df_roubo_veiculo_outliers_superiores['roubo_veiculo']) * 0.01
    
    for i, valor in enumerate(df_roubo_veiculo_outliers_superiores['roubo_veiculo']):
        plt.text(
            i, # posição X
            valor + deslocamento, # posição Y
            f'{valor:,}',
            ha='center'
        )
    
    
    
    
    plt.xticks(rotation=45, ha='right') # Rotaciona o texto do eixo x
    plt.title('Municípios c/ Outliers Superiores')
    
    # OUTLIERS INFERIORES OU MENORES ROUBOS
    plt.subplot(2, 2, 4)
    
    if len(df_roubo_veiculo_outliers_inferiores) > 0:
        df_roubo_veiculo_outliers_inferiores = (
            df_roubo_veiculo_outliers_inferiores
            .sort_values(by='roubo_veiculo', ascending=True)
        )
        
        plt.barh(
            df_roubo_veiculo_outliers_inferiores['munic'],
            df_roubo_veiculo_outliers_inferiores['roubo_veiculo']
        )
    
        plt.title('Municípios c/ Outliers Inferiores')
    
    else:
        df_roubo_veiculo_menores = (
            df_roubo_veiculo_menores
            .sort_values(by='roubo_veiculo', ascending=True)
            .head(10)
            # .sort_values(by='roubo_veiculo', ascending=False)
        )
        
        plt.barh(
            df_roubo_veiculo_menores['munic'].str.slice(0, 10),
            df_roubo_veiculo_menores['roubo_veiculo']
        )
        
        deslocamento = max(df_roubo_veiculo_menores['roubo_veiculo']) * 0.01
        
        # Rótulo dos dados:
        for i, valor in enumerate(df_roubo_veiculo_menores['roubo_veiculo']):
            plt.text(
                valor + deslocamento, # posição X
                i, # posição Y
                f'{valor:,}',
                ha='center'
            )
        
        plt.title('Municípios com Menores Roubos')
    
    plt.show()
    
except Exception as e:
    print(f'Erro ao pplotar o gráfico: {e}')