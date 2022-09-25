import pandas as pd
import matplotlib.pyplot as plt
import excessoes as ex
import manipulacoes_pandas as ManP
from datetime import date
from calendar import monthrange


# === PLOTAGEM GRAFICA DOS DADOS DE RESULTADO DO EXERCÍCIO E DO BALANCO PATRIMONIAL === #

# Gráfico de barras do confronto de Receitas e Despesas do período para as contas de resultado com início 8.
def demonstracao_do_resultado_barras(de_mes, de_ano, ate_mes, ate_ano):
    if '' == str(de_mes).strip() or \
            '' == str(de_ano).strip() or \
            '' == str(ate_mes).strip() or \
            '' == str(ate_ano).strip():
        raise ex.CamposEmBranco('Existem campos em branco que deveriam ter sido preenchidos.')

    demes = int(de_mes)
    deano = int(de_ano)
    atemes = int(ate_mes)
    ateano = int(ate_ano)

    # Ultimo dia da data de partida (de) e da data limite (ate) para obter o resultado da condição de verdadeiro
    # ou falso.
    ultimo_de = monthrange(deano, demes)[1]
    ultimo_ate = monthrange(ateano, atemes)[1]
    de_data = date(deano, demes, ultimo_de)
    ate_data = date(ateano, atemes, ultimo_ate)

    # Condição para seleção de uma data limite (Até) ser menor que a data de partida (De).
    if de_data > ate_data:
        raise ex.DataPosteriorMenor('A data posterior (Até) é menor que a data de partida (De).')

    # Condição para o caso de não existir dados no arquivo que correspondam ao ponto de partida (De).
    if ManP.verificar_ponto_de_partida_balancete(demes, deano) is False:
        raise ex.PontoDePartidaInexistente('Não existem dados para o ponto de partida inicial.')

    # Data limite que consta no arquivo.
    limite = ManP.verificar_limite_balancete()

    # No caso da data limite (Até) ser maior do que a data limite do arquivo, os nossos parâmetros recebem o ano
    # e o mês da data limite do arquivo.
    if ate_data > limite:
        atemes = limite.month
        ateano = limite.year

    # Leitura do arquivo csv que guarda as informações do balancete.
    df_dre = pd.read_csv('BALANCETE.csv')

    df_dre = df_dre.loc[df_dre['TIPO'] == 'NORMAL', :]

    # Transformação do tipo de dado para float64.
    df_dre['SALDOFINAL'] = df_dre['SALDOFINAL'].replace({',': '.'}, regex=True).astype({'SALDOFINAL': 'float64'})

    # Filtro por tipo de conta, neste caso, estamos utilizando somente contas de resultado (com início 8)
    # Para a análise que iremos fazer. Além disso, é definida a extensão do período (de data, até data) e
    # também as contas que possuem saldo final maior do que 0.
    df_dre = df_dre.loc[(df_dre['NUMERO DA CONTA'].str.startswith('8')) &
                        ((df_dre['MES'] >= demes) & (df_dre['MES'] <= atemes)) &
                        ((df_dre['ANO'] >= deano) & (df_dre['ANO'] <= ateano)) &
                        (df_dre['SALDOFINAL'] > 0), :]

    # Indice contendo o número inicial de cada conta para posterior separação entre contas de receita e despesa.
    indice = df_dre['NUMERO DA CONTA'].str.replace('.', '', regex=False).str.extract(r'(\S{2})').astype('int64')

    # Atribuição do número inicial das contas de receita e despesa para o número da conta do df_dre.
    df_dre['NUMERO DA CONTA'] = indice[0]

    # Aplicação de transformação em um tipo datetime com a junção das colunas ['MES'] e ['ANO'] para que
    # seja possível transformar em um formato desejado de 'MES/ANO' (ex: '07/2022').
    df_dre['DATA'] = pd.to_datetime(df_dre['MES'].astype('str').str.cat(df_dre['ANO'].astype('str')),
                                    format='%m%Y').dt.strftime('%m/%Y')

    # Agrupamento e seleção de colunas e soma da coluna de saldo final.
    df_grupo = df_dre[['DATA', 'NUMERO DA CONTA', 'SALDOFINAL']].groupby(['DATA', 'NUMERO DA CONTA'],
                                                                         as_index=False).sum()

    # Definição do DataFrame de Receitas de acordo com os dois digitos iniciais dos número de contas, para o caso,
    # inicio com 83.
    df_receitas = df_grupo.loc[df_grupo['NUMERO DA CONTA'].isin([83])]

    # Definição do DataFrame de Custos e Despesas de acordo com os dois digitos iniciais dos número de contas,
    # para o caso, inicio com 84 e 85, respectivamente.
    df_despesas = df_grupo.loc[df_grupo['NUMERO DA CONTA'].isin([84, 85])]

    # Formação da plotagem do gráfico de barras.

    # Tamanho total do eixo x (horizontal).
    tam = pd.Series([x for x in range(len(df_grupo['DATA'].drop_duplicates()))], dtype='int64')
    # Variável para definição da largura das barras
    width = 0.20
    # Tamanho do eixo de Receitas (importante para meses que não tiverem dados)
    tam_r = pd.Series([x for x in range(len(df_receitas['DATA'].drop_duplicates()))], dtype='int64')
    # Tamanho do eixo de Custos e Despesas (importante para meses que não tiverem dados)
    tam_d = pd.Series([x for x in range(len(df_despesas['DATA'].drop_duplicates()))], dtype='int64')
    # Definição de um figura vazia e do seu tamanho
    figura, eixo = plt.subplots(figsize=(10, 6))
    # Definição da barra que irá conter os dados de receita, há uma divisão do espaço em que ela ocupa.
    r = eixo.bar(tam_r - width / 2, df_receitas['SALDOFINAL'], width=width, label='Receitas')
    d = eixo.bar(tam_d + width / 2, df_despesas['SALDOFINAL'], width=width, label='Despesas')
    eixo.set_xticks(tam, df_grupo['DATA'].drop_duplicates())
    eixo.axes.bar_label(r, padding=3)
    eixo.axes.bar_label(d, padding=3)
    eixo.set_title('Demonstração do Resultado do Exercício')
    eixo.set_xlabel('Período')
    eixo.set_ylabel('Valor em R$')
    eixo.legend()

    return plt.show()


# Gráfico de pizza do confronto de Receitas e Despesas do período para as contas de resultado com início 8.
def demonstracao_do_resultado_pizza(de_mes, de_ano, ate_mes, ate_ano):
    if '' == str(de_mes).strip() or \
            '' == str(de_ano).strip() or \
            '' == str(ate_mes).strip() or \
            '' == str(ate_ano).strip():
        raise ex.CamposEmBranco('Existem campos em branco que deveriam ter sido preenchidos.')

    demes = int(de_mes)
    deano = int(de_ano)
    atemes = int(ate_mes)
    ateano = int(ate_ano)

    # Ultimo dia da data de partida (de) e da data limite (ate) para obter o resultado da condição de verdadeiro
    # ou falso. Além disso, ocore a tranformação os valores em datetime.
    ultimo_de = monthrange(deano, demes)[1]
    ultimo_ate = monthrange(ateano, atemes)[1]
    de_data = date(deano, demes, ultimo_de)
    ate_data = date(ateano, atemes, ultimo_ate)

    # Condição para seleção de uma data limite (Até) ser menor que a data de partida (De).
    if de_data > ate_data:
        raise ex.DataPosteriorMenor('A data posterior (Até) é menor que a data de partida (De).')

    # Condição para o caso de não existir dados no arquivo que correspondam ao ponto de partida (De).
    if ManP.verificar_ponto_de_partida_balancete(demes, deano) is False:
        raise ex.PontoDePartidaInexistente('Não existem dados para o ponto de partida inicial.')

    # Data limite que consta no arquivo.
    limite = ManP.verificar_limite_balancete()

    # No caso da data limite (Até) ser maior do que a data limite do arquivo, os nossos parâmetros recebem o ano
    # e o mês da data limite do arquivo.
    if ate_data > limite:
        atemes = limite.month
        ateano = limite.year

    # Leitura do arquivo csv que guarda as informações do balancete.
    df_dre = pd.read_csv('BALANCETE.csv')

    # Transformação do tipo de dado para float64.
    df_dre['SALDOFINAL'] = df_dre['SALDOFINAL'].replace({',': '.'}, regex=True).astype({'SALDOFINAL': 'float64'})

    # Filtro por tipo de conta, neste caso, estamos utilizando somente contas de resultado (com início 8)
    # Para a análise que iremos fazer. Além disso, é definida a extensão do período (de data, até data) e
    # também as contas que possuem saldo final maior do que 0.
    df_dre = df_dre.loc[(df_dre['NUMERO DA CONTA'].str.startswith('8')) &
                        ((df_dre['MES'] >= demes) & (df_dre['MES'] <= atemes)) &
                        ((df_dre['ANO'] >= deano) & (df_dre['ANO'] <= ateano)) &
                        (df_dre['SALDOFINAL'] > 0), :]

    # Indice contendo o número inicial de cada conta para posterior separação entre contas de receita e despesa.
    indice = df_dre['NUMERO DA CONTA'].str.replace('.', '', regex=False).str.extract(r'(\S{2})').astype('int64')

    # Atribuição do número inicial das contas de receita e despesa para o número da conta do df_dre.
    df_dre['NUMERO DA CONTA'] = indice[0]

    # Aplicação de transformação em um tipo datetime com a junção das colunas ['MES'] e ['ANO'] para que
    # seja possível transformar em um formato desejado de 'MES/ANO' (ex: '07/2022').
    df_dre['DATA'] = pd.to_datetime(df_dre['MES'].astype('str').str.cat(df_dre['ANO'].astype('str')),
                                    format='%m%Y').dt.strftime('%m/%Y')

    # Agrupamento de contas para que não existam contas identicas sendo divididas em duas ou mais fatias do gráfico
    # por conta da definição dos períodos. Para o nosso caso, mais de uma período definido resulta na soma
    # dos dados de resultado de ambos os períodos.
    df_dre = df_dre[['NUMERO DA CONTA',
                     'DESCRICAO DA CONTA',
                     'SALDOFINAL']].groupby(['NUMERO DA CONTA', 'DESCRICAO DA CONTA'], as_index=False).sum()

    # Função para formatar o texto de rótulo de dados percentuais do gráfico.
    def texto_da_fatia(pct, valor):
        valor = round((valor.sum() * (pct / 100)))
        return f'{pct:.2f}%\nR${valor:.2f}'

    # Formação da plotagem do gráfico de pizza
    figurap, eixop = plt.subplots(figsize=(12, 6))
    eixop.pie(x=df_dre['SALDOFINAL'], autopct=lambda pct: texto_da_fatia(pct, df_dre['SALDOFINAL']),
              pctdistance=1.2,
              textprops={
                  'size': 8,
                  'weight': 'semibold',
              })
    eixop.legend(labels=list(df_dre['DESCRICAO DA CONTA']), title='Receita X Despesas',
                 loc='center right', bbox_to_anchor=(1.1, 0, 0.5, 1.4))
    eixop.set_title(
        label=f'Receitas, Custos e Despesas - {de_data.month}/{de_data.year} a {ate_data.month}/{ate_data.year}',
        fontdict={'fontsize': 15, 'fontweight': 'semibold'})

    return plt.show()


# Gráfico de linhas com dados sobre a variação patrimonial durante os períodos.
def balanco_patrimonial_linha(de_mes, de_ano, ate_mes, ate_ano):
    if '' == str(de_mes).strip() or \
            '' == str(de_ano).strip() or \
            '' == str(ate_mes).strip() or \
            '' == str(ate_ano).strip():
        raise ex.CamposEmBranco('Existem campos em branco que deveriam ter sido preenchidos.')

    demes = int(de_mes)
    deano = int(de_ano)
    atemes = int(ate_mes)
    ateano = int(ate_ano)

    # Ultimo dia da data de partida (de) e da data limite (ate) para obter o resultado da condição de verdadeiro
    # ou falso. Além disso, ocore a tranformação os valores em datetime.
    ultimo_de = monthrange(deano, demes)[1]
    ultimo_ate = monthrange(ateano, atemes)[1]
    de_data = date(deano, demes, ultimo_de)
    ate_data = date(ateano, atemes, ultimo_ate)

    # Condição para seleção de uma data limite (Até) ser menor que a data de partida (De).
    if de_data > ate_data:
        print(de_data, ate_data)
        raise ex.DataPosteriorMenor('A data posterior (Até) é menor que a data de partida (De).')

    # Condição para o caso de não existir dados no arquivo que correspondam ao ponto de partida (De).
    if ManP.verificar_ponto_de_partida_balanco_patrimonial(demes, deano) is False:
        raise ex.PontoDePartidaInexistente('Não existem dados para o ponto de partida inicial.')

    # Data limite que consta no arquivo.
    limite = ManP.verificar_limite_balanco_patrimonial()

    # No caso da data limite (Até) ser maior do que a data limite do arquivo, os nossos parâmetros recebem o ano
    # e o mês da data limite do arquivo.
    if ate_data > limite:
        atemes = limite.month
        ateano = limite.year

    # Leitura do arquivo csv que guarda as informações do Balanço Patrimonial.
    df_balanco_patrimonial = pd.read_csv('BALANCO PATRIMONIAL.csv')

    # Definição da abrangência do período definido nos campos (De) e (Ate).
    df_balanco_patrimonial = df_balanco_patrimonial.loc[(
                                                                (df_balanco_patrimonial['MES_REF'] >= demes) &
                                                                (df_balanco_patrimonial['ANO_REF'] >= deano)
                                                        ) &
                                                        (
                                                                (df_balanco_patrimonial['MES_REF'] <= atemes) &
                                                                (df_balanco_patrimonial['ANO_REF'] <= ateano)
                                                        ), :].reset_index(drop=True)

    # Mudança de tipo de dado para o campo de valor.
    df_balanco_patrimonial['VALOR'] = df_balanco_patrimonial.VALOR.str.replace(',', '.').astype('float64')

    # Aplicação de transformação em um tipo datetime com a junção das colunas ['MES_REF'] e ['ANO_REF'] para que
    # seja possível transformar em um formato desejado de 'MES/ANO' (ex: '07/2022').
    df_balanco_patrimonial['DATA'] = pd.to_datetime(
        df_balanco_patrimonial['MES_REF'].astype('str')
            .str
            .cat(df_balanco_patrimonial['ANO_REF'].astype('str')), format='%m%Y') \
        .dt.strftime('%m/%Y')

    # Filtro para manter somente as contas sintéticas de Ativo e Passivo que agregam os valores das contas que
    # compõe o grupo da qual elas são superiores.
    df_balanco_patrimonial = df_balanco_patrimonial.loc[df_balanco_patrimonial['NUMERO_DA_CONTA'].isin(['1', '2'])]

    # Definição de um sub-DataFrame que irá auxiliar na alocação das anotações de texto para representar rótulos
    # de dados de linhas. Ele será utilizado como base para as localizaçãoes x e y, horizontal e vertical,
    # respectivamente.
    a = pd.DataFrame(
        {
            'VALOR': (df_balanco_patrimonial
                      .loc[df_balanco_patrimonial['DESCRICAO_DA_CONTA']
                      .isin(['SI ATIVO', 'ATIVO']), 'VALOR']
                      .reset_index(drop=True) -  # Subtração
                      df_balanco_patrimonial
                      .loc[df_balanco_patrimonial['DESCRICAO_DA_CONTA']
                      .isin(['SI PASSIVO', 'PASSIVO']), 'VALOR']
                      .reset_index(drop=True)
                      ),
            'DATA': df_balanco_patrimonial['DATA'].drop_duplicates().reset_index(drop=True)
        }
    )

    # Posição dos valores que irão ser anotados nos rótulos de dados das linhas de acordo com o índice deles.
    posicao_valor = (
            df_balanco_patrimonial.
            loc[df_balanco_patrimonial['DESCRICAO_DA_CONTA']
            .isin(['SI ATIVO', 'ATIVO']), 'VALOR'].reset_index(drop=True) -
            df_balanco_patrimonial
            .loc[df_balanco_patrimonial['DESCRICAO_DA_CONTA']
            .isin(['SI PASSIVO', 'PASSIVO']), 'VALOR'].reset_index(drop=True)
    )

    # Definição do tamanho do eixo X de acordo com os valores únicos de datas.
    tamanho = [x for x in df_balanco_patrimonial['DATA'].drop_duplicates().reset_index(drop=True).index]

    # Formação da plotagem do gráfico de linha.
    fig, ax = plt.subplots()
    ax.plot(
        tamanho,
        (df_balanco_patrimonial.loc[
             df_balanco_patrimonial['DESCRICAO_DA_CONTA'].isin(['SI ATIVO', 'ATIVO']), 'VALOR'].reset_index(drop=True) -
         df_balanco_patrimonial.loc[
             df_balanco_patrimonial['DESCRICAO_DA_CONTA'].isin(['SI PASSIVO', 'PASSIVO']), 'VALOR'].reset_index(
             drop=True)),
        'o-'
    )
    ax.grid()
    ax.set_xticks(tamanho,
                  df_balanco_patrimonial
                  .loc[df_balanco_patrimonial['DESCRICAO_DA_CONTA'].isin(['SI ATIVO', 'ATIVO']), 'DATA'])
    ax.set_title('Variação Patrimonial')
    ax.set_xlabel('Período')
    ax.set_ylabel('Valor em R$')

    # Condição para alocação das anotações de rótulos de linha baseando-se na quantidade de períodos
    # que foram definidos para análise.
    if len(tamanho) == 1:
        for posicao in tamanho:
            ax.annotate(f"R${posicao_valor[posicao]}",
                        xy=(posicao, float(posicao_valor[posicao])),
                        xytext=(posicao - 0.01, float(posicao_valor[posicao]) + 6),
                        size=15)
    else:
        for posicao in tamanho:
            ax.annotate(f"R${posicao_valor[posicao]}",
                        xy=(posicao, float(posicao_valor[posicao])),
                        xytext=(posicao - 0.1, float(posicao_valor[posicao]) + 6),
                        size=15)

    return plt.show()
