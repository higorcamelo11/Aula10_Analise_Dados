import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    #Preparação dos dados
    print('\nObtendo Dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    
    #Variáveis
    df_estelionato = df_ocorrencias[['mes_ano', 'estelionato']]
    total_geral = df_estelionato['estelionato'].sum()
    df_estelionato = df_estelionato.groupby('mes_ano', as_index=False)['estelionato'].sum()
    df_estelionato = df_estelionato.sort_values(by='estelionato', ascending=False)
    
    
    # Medidas
    array_estelionato = np.array(df_estelionato['estelionato'])
    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)
    distancia = abs((media_estelionato - mediana_estelionato) / mediana_estelionato * 100)
    
    # Distribuição
    q1 = np.quantile(array_estelionato, .25)
    q3 = np.quantile(array_estelionato, .75)
    
    # Maior e Menor
    df_estelionato_menores = df_estelionato[df_estelionato['estelionato'] < q1]
    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato'] > q3]
    # Mínima, Máxima e Amplitude
    maximo = np.max(array_estelionato)
    minimo = np.min(array_estelionato)
    amplitude = maximo - minimo

    
    print(f'\nMeses e anos com as menores quantidade de ocorrências, são aqueles que apresentaram a quantidade menor que {q1} casos')
    print(30*'-')
    print(df_estelionato_maiores.sort_values(by='estelionato', ascending=True).head(10))
    
    print(f'\nMeses e anos com as menores quantidade de ocorrências, são aqueles que apresentaram a quantidade maior que {q3} casos')
    print(30*'-')
    print(df_estelionato_maiores.head(10))
    
    print('\nPadrão das ocorrências')
    print(30*'-')
    print(f'''A média de ocorrências do estado do Rio de Janeiro é de{media_estelionato:.0f} casos de estelionato, e o valor central(mediana) é de{mediana_estelionato:.0f} casos, e a distância desses dados é de {distancia:.0f}%.
Isso indica uma alta dispersão dos dados, significa que há alguns valores muito altos puxando a média para cima, o que nos diz que não há um padrão.
          ''')
    
    # IQR
    iqr = q3 - q1
    # Outliers
    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)
    df_estelionato_outliers_inferiores = df_estelionato[df_estelionato['estelionato'] < limite_inferior]
    df_estelionato_outliers_superiores = df_estelionato[df_estelionato['estelionato'] > limite_superior]
    
    print(f'\nMeses e anos que apresentam casos abaixo do Limite Inferior({limite_inferior:.0f}).')
    print(30*'-')
    if len(df_estelionato_outliers_inferiores) == 0:
        print('Não há outliers inferiores.')
        
    else:
        print(df_estelionato_outliers_inferiores.sort_values(by='estelionato', ascending=True))
        
    print(f'\nMeses e anos que apresentam casos acima do Limite Superior({limite_superior:.0f}).')
    print(30*'-')
    if len(df_estelionato_outliers_superiores) == 0:
        print('Não existe outliers superiores.')
        
    else:
        print(df_estelionato_outliers_superiores.sort_values(by='estelionato', ascending=False))
    


except Exception as e:
    print(f'Erro de análise: {e}')
    exit()
    
    
try:
    df_estelionato_maiores = df_estelionato_maiores.sort_values(by='estelionato', ascending=False).head(10)
    # plt.figure(figsize=(18, 8))
    plt.subplots(2, 2, figsize=(18, 7))
    
    #POSIÇÃO 1 - BOXPLOT
    plt.subplot(2, 2, 1)
    # showfliers=False
    plt.boxplot(array_estelionato, vert=False, showmeans=True)
    plt.title('Boxplot da Distribuição')
    
    
    #POSIÇÃO 2 - MEDIDAS
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_estelionato:.0f}')
    plt.text(0.1, 0.8, f'Distância: {distancia:.0f}')
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior:.0f}')
    plt.text(0.1, 0.6, f'Mínimo: {minimo:.0f}')
    plt.text(0.1, 0.5, f'Q1: {q1:.0f}')
    plt.text(0.1, 0.4, f'Mediana: {mediana_estelionato:.0f}')
    plt.text(0.1, 0.3, f'Q3: {q3:.0f}')
    plt.text(0.1, 0.2, f'Máximo: {maximo:.0f}')
    plt.text(0.1, 0.1, f'Limite Superior: {limite_superior:.0f}')
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude:.0f}')
    
    plt.axis('off')
    plt.title('Resumo Estatístico') 
    
    # OUTLIERS SUPERIORES
    plt.subplot(2, 2, 3)
    df_estelionato_outliers_superiores = (
        df_estelionato_outliers_superiores
        .head(10)
        .sort_values(by='estelionato', ascending=False)
    )
    plt.bar(
        df_estelionato_outliers_superiores['mes_ano'],
        df_estelionato_outliers_superiores['estelionato']
    )
    plt.xticks(rotation=45, ha='right')
    plt.title('OUTLIERS SUPERIORES')
    
    deslocamento = max(df_estelionato_outliers_superiores['estelionato']) * 0.01
    
    for i, valor in enumerate(df_estelionato_outliers_superiores['estelionato']):
        plt.text(
            i, # posição X
            valor + deslocamento, # posição Y
            f'{valor:,}',
            ha='center'
        )
    
    plt.subplot(2, 2, 4)
    # OUTLIERS INFERIORES OU MENORES
    if len(df_estelionato_outliers_inferiores) > 0:
        df_estelionato_outliers_inferiores = (
            df_estelionato_outliers_inferiores
            .sort_values(by='estelionato', ascending=True)
        )
        plt.barh(
            df_estelionato_outliers_inferiores['mes_ano'],
            df_estelionato_outliers_inferiores['estelionato']
        )
        
    else:
        df_estelionato_menores = (
            df_estelionato_menores
            .sort_values(by='estelionato', ascending=True)
            .head(10)
        )
        
        plt.barh(
            df_estelionato_menores['mes_ano'],
            df_estelionato_menores['estelionato']
        )
        
        deslocamento = max(df_estelionato_menores['estelionato']) * 0.03
    
        for i, valor in enumerate(df_estelionato_menores['estelionato']):
            plt.text(
                valor + deslocamento,
                i,
                f'{valor:,}',
                ha='center'
            )
            
        plt.title('Meses c/ Menos Casos')
    
    plt.show()
    
    
    
except Exception as e:
    print(f'Erro de análise: {e}')
    exit()