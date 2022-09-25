import pandas as pd
import locale
from datetime import date
from calendar import monthrange
import excessoes as ex

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# === MANIPILACAO DE DADOS COM O PANDAS === #

# === FUNCOES PARA CONSOLIDACAO DO BALANCETE === #

# Manipulação dos dados do livro razão para a formulação do balancete com o pandas. O retorno final é uma lista
# dos dados consolidados do balancete do período.
def consolidar_balancete(mes, ano):
    # Parametrise de mês e ano que estamos tratando.
    par_mes = int(mes)
    par_ano = int(ano)

    # Leitura do plano de contas para manter somente as contas analíticas.
    plano_de_contas = pd.read_csv('P CONTAS.csv')

    contas_analiticas = plano_de_contas[plano_de_contas['TIPO CONTA'] == 'A'].loc[
                        :, ['NUMERO DA CONTA', 'DESCRICAO DA CONTA']].reset_index()

    # Leitura do livro razão, formatação da data para datetime64, transformação do valor para float64  e definição
    # do período de apuração com os parâmetros.
    livro_razao = pd.read_csv('LIVRO RAZAO.csv', index_col='SEQUENCIA', dtype={'SEQUENCIA': 'int64'})

    livro_razao['VALOR'] = livro_razao['VALOR'].replace({',': '.'}, regex=True).astype('float64')

    livro_razao['DATA_FATO'] = pd.to_datetime(livro_razao['DATA_FATO'], format='%d/%m/%Y')
    livro_razao['DATA_INCL'] = pd.to_datetime(livro_razao['DATA_INCL'], format='%d/%m/%Y')

    livro_razao_do_periodo = livro_razao.loc[(livro_razao['DATA_FATO'].dt.month == par_mes) &
                                             (livro_razao['DATA_FATO'].dt.year == par_ano)
                                             ].sort_values(by='DATA_FATO').reset_index(drop=True)

    # Separação dos movimentos a debito e dos movimentos a credito do livro razao. Cada tabela é agrupada para
    # obter a soma dos movimentos totais de cada conta.
    debitos = livro_razao_do_periodo.loc[:, ['CONTA_DEBITO', 'DESC_CONTA_DEB', 'VALOR']]

    debitos = debitos.groupby(['CONTA_DEBITO', 'DESC_CONTA_DEB']).sum('VALOR').reset_index().rename(
        columns={'VALOR': 'MOVTO_DEB'})

    creditos = livro_razao_do_periodo.loc[:, ['CONTA_CREDITO', 'DESC_CONTA_CRED', 'VALOR']]

    creditos = creditos.groupby(['CONTA_CREDITO', 'DESC_CONTA_CRED']).sum('VALOR').reset_index().rename(
        columns={'VALOR': 'MOVTO_CRE'})

    # Leitura do saldo final do mês anterior para as contas que possuem saldo final. Definição do tipo de dados
    # e do período que deve ser analisado, no caso, o anterior ao mês atual.
    balancete_anterior = pd.read_csv('BALANCETE.csv')

    balancete_anterior.iloc[:, 6:] = balancete_anterior.iloc[:, 6:].replace({',': '.'}, regex=True).astype('float64')

    balancete_anterior = balancete_anterior[(balancete_anterior['MES'] == par_mes - 1) &
                                            (balancete_anterior['ANO'] == par_ano)]

    # Garantia de que o saldo final de um período não irá compor o saldo final de outro período para contas
    # de resultado do exercício, as contas de início 8.
    balancete_anterior.loc[balancete_anterior['NUMERO DA CONTA'].str.startswith('8'), 'SALDOFINAL'] = 0

    # Definição das colunas que compõe o balancete.
    balancete = pd.DataFrame(
        {
            'TIPO': ['NORMAL' for x in range(len(contas_analiticas))],
            'MES': [par_mes for x in range(len(contas_analiticas))],
            'ANO': [par_ano for x in range(len(contas_analiticas))],
            'CONTA': [x for x in contas_analiticas['NUMERO DA CONTA']],
            'DESC_CONTA': [x for x in contas_analiticas['DESCRICAO DA CONTA']]
        }
    )

    # Junções do balancete com o balancete_anterior para definir o saldo inicial e com o livro razão para definir
    # as movimentações do período.
    balancete = balancete.merge(balancete_anterior[['NUMERO DA CONTA', 'SALDOFINAL']],
                                left_on='CONTA',
                                right_on='NUMERO DA CONTA',
                                how='left'
                                ).merge(debitos[['CONTA_DEBITO', 'MOVTO_DEB']],
                                        left_on='CONTA',
                                        right_on='CONTA_DEBITO',
                                        how='left'
                                        ).merge(creditos[['CONTA_CREDITO', 'MOVTO_CRE']],
                                                left_on='CONTA',
                                                right_on='CONTA_CREDITO',
                                                how='left'
                                                ).rename(columns={'SALDOFINAL': 'SALDO INICIAL'}
                                                         ).fillna(0).drop(
        columns=['NUMERO DA CONTA', 'CONTA_DEBITO', 'CONTA_CREDITO'])

    balancete['SALDO_FINAL'] = 0.00

    contas_145 = balancete.CONTA.str.extract(r'(\S{1})').astype('int64')

    contas_8d = balancete['CONTA'].str.replace('.', '', regex=False).str.extract(r'(\S{2})').astype('int64')

    balancete['SALDO_FINAL'] = (balancete['SALDO INICIAL'] + balancete['MOVTO_DEB'] - balancete['MOVTO_CRE']).where(
        contas_145.loc[:, 0].isin([1, 4, 5]) | contas_8d.loc[:, 0].isin([84, 85]),
        (balancete['SALDO INICIAL'] - balancete['MOVTO_DEB'] + balancete['MOVTO_CRE'])
    )

    # Transformando o balancete finalizado em uma lista nos padrões de escrita do programa.
    lista_balancete = []
    lista_temporaria = []
    for index, row in balancete.iterrows():
        for r in row:
            lista_temporaria.append(r)
        lista_balancete.append(lista_temporaria.copy())
        lista_temporaria.clear()

    return lista_balancete


# Função para verificar se já existe um balancete fechado para o período especificado. O pandas foi utilizado para
# fazer a leitura do balancete e iterar sobre o resultado final.
def verificar_periodo_balancete(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)
    par_cod_ano = str(par_mes).strip() + str(par_ano).strip()

    balancete_fechado = pd.read_csv('BALANCETE.csv', usecols=['MES', 'ANO']).drop_duplicates().reset_index(drop=True)

    balancete_fechado['COD_ANO'] = balancete_fechado[['MES', 'ANO']].astype('str').apply(''.join, axis=1)

    if par_cod_ano in balancete_fechado['COD_ANO'].__iter__():
        raise ex.BalancetePeriodoRegistrado('O balancete do período especificado já está registrado.')


# Função para verificar se existe movimento no razão para o período especificado, caso exista, o balancete pode ser
# gerado. O pandas foi utilizado para fazer a leitura do livro razão e para iterar sobre o resultado final.
def verificar_movimento_razao(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)
    par_cod_ano = str(par_mes).strip() + str(par_ano).strip()

    livro_razao_datas = pd.read_csv('LIVRO RAZAO.csv', usecols=['DATA_FATO', 'DATA_INCL']).rename(
        columns={'DATA_FATO': 'MES', 'DATA_INCL': 'ANO'})

    livro_razao_datas['MES'] = pd.to_datetime(livro_razao_datas['MES'], format='%d/%m/%Y')

    livro_razao_datas['ANO'] = livro_razao_datas['MES'].dt.year
    livro_razao_datas['MES'] = livro_razao_datas['MES'].dt.month

    livro_razao_datas = livro_razao_datas.drop_duplicates().reset_index(drop=True)

    livro_razao_datas['COD_ANO'] = livro_razao_datas[['MES', 'ANO']].astype('str').apply(''.join, axis=1)

    if par_cod_ano not in livro_razao_datas['COD_ANO'].__iter__():
        raise ex.BalanceteFicaraVazio(
            'O Livro Razão não possui movimento no período especificado. O Balancete ficaria vazio.')


# Função Excluir o balancete de um determinado período.
def excluir_balancete(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    balancete_periodo_excluir = pd.read_csv('BALANCETE.csv').drop(columns='SEQUENCIA')

    indices = balancete_periodo_excluir.loc[(balancete_periodo_excluir['MES'] == par_mes) &
                                            (balancete_periodo_excluir['ANO'] == par_ano), 'MES'].index

    balancete_periodo_excluir.drop(index=indices, axis=0, inplace=True)

    lista_remover_balancete = []
    lista_temporaria = []
    for index, row in balancete_periodo_excluir.iterrows():
        for r in row:
            lista_temporaria.append(r)
        lista_remover_balancete.append(lista_temporaria.copy())
        lista_temporaria.clear()

    return lista_remover_balancete


# Função Verificar se existe período no balancete para ser excluído. A diferença da função "verificar_movimento_razao"
# é que a função "verificar_movimento_razao" verifica se existe e a função abaixo se não existe.
def verificar_periodo_exclusao(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)
    par_cod_ano = str(par_mes).strip() + str(par_ano).strip()

    balancete_fechado = pd.read_csv('BALANCETE.csv', usecols=['TIPO', 'MES', 'ANO'])

    balancete_fechado = balancete_fechado[balancete_fechado['TIPO'] == 'NORMAL'].drop_duplicates().reset_index(
        drop=True)

    balancete_fechado['COD_ANO'] = balancete_fechado[['MES', 'ANO']].astype('str').apply(''.join, axis=1)

    if par_cod_ano not in balancete_fechado['COD_ANO'].__iter__():
        raise ex.BalancetePeriodoSemDados('Não existe balancete para o período especificado.')


# Função para ordenar a lista self.balancete que recebe os dados da leitura do balancete.
def ordernar_balancete(lista):
    iter(lista)
    lista_balancete = lista
    balancete_sequencia = pd.DataFrame(data=lista_balancete[1:], columns=lista_balancete[0])

    balancete_sequencia[['MES', 'ANO']] = balancete_sequencia[['MES', 'ANO']].astype({'MES': 'int64', 'ANO': 'int64'})

    balancete_sequencia.sort_values(by=['ANO', 'MES', 'NUMERO DA CONTA'], inplace=True)

    balancete_sequencia['SEQUENCIA'] = [x for x in range(1, len(balancete_sequencia.index) + 1)]

    lista_balancete_ordenado = [[x for x in balancete_sequencia.keys()]]
    lista_temporaria = []
    for _, row in balancete_sequencia.iterrows():
        for r in row:
            lista_temporaria.append(r)
        lista_balancete_ordenado.append(lista_temporaria.copy())
        lista_temporaria.clear()

    return lista_balancete_ordenado


# === FUNCÕES PARA APURACAO DO RESULTADO DO EXERCÍCIO === #

# Função para manuseio do balancete para Apuração do Resultado do Exercício.
def lancamentos_apuracao_do_resultado(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    balancete = pd.read_csv('BALANCETE.csv')

    balancete = balancete.loc[(balancete['MES'] == par_mes) & (balancete['ANO'] == par_ano), :]

    inicial_contas_analiticas = balancete['NUMERO DA CONTA'].str.extract(r'(\S{1})').astype('int64')

    balancete = balancete.loc[
        inicial_contas_analiticas[0].isin([3, 4, 5]), ['NUMERO DA CONTA', 'DESCRICAO DA CONTA', 'SALDOFINAL']
    ].astype({'SALDOFINAL': 'float64'})

    balancete = balancete.loc[balancete['SALDOFINAL'] > 0, :]

    lista_lancamentos_apuracao_do_resultado = []
    lista_temp = []
    for index, row in balancete.iterrows():
        for r in row:
            lista_temp.append(r)
        lista_lancamentos_apuracao_do_resultado.append(lista_temp.copy())
        lista_temp.clear()

    return lista_lancamentos_apuracao_do_resultado


# Função para exclusão dos lançamentos de um determinado período da Apuração do Resultado do Exercício.
def excluir_lancamento_apuracao_do_resultado(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    codigo_apuracao = f'APURACAO DO RESULTADO {str(par_mes) + str(par_ano)}'

    lancamentos_exclusao = pd.read_csv('LIVRO RAZAO.csv')

    lancamentos_exclusao.drop(
        labels=lancamentos_exclusao[lancamentos_exclusao['DESC_DO_FATO'] == codigo_apuracao].index, inplace=True
    )

    lancamentos_exclusao['SEQUENCIA'] = lancamentos_exclusao.index + 1

    lista_lancamentos_apos_exclusao = [[x for x in lancamentos_exclusao.keys()]]
    lista_temp = []
    for index, row in lancamentos_exclusao.iterrows():
        for r in row:
            lista_temp.append(r)
        lista_lancamentos_apos_exclusao.append(lista_temp.copy())
        lista_temp.clear()

    return lista_lancamentos_apos_exclusao


# Função para verificar se existem lançamentos de um determinado período da Apuração do Resultado do Exercício.
def verificar_lancamentos_apuracao_do_resultado(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    codigo_apuracao = f'APURACAO DO RESULTADO {str(par_mes) + str(par_ano)}'

    verificar_lancamentos = pd.read_csv('LIVRO RAZAO.csv')

    verificar_lancamentos = verificar_lancamentos.loc[
        verificar_lancamentos['DESC_DO_FATO'] == codigo_apuracao, 'DESC_DO_FATO'].drop_duplicates()

    if codigo_apuracao in verificar_lancamentos.__iter__():
        return True
    else:
        return False


# Função para verificar se existe movimento no balancete de verificação para o período especificado, antes de efetuar
# a geração dos lançamentos de compensação de contas de resultado.
def verificar_movimento_balancete_apuracao_do_resultado(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)
    par_cod_ano = str(par_mes).strip() + str(par_ano).strip()

    balancete_fechado = pd.read_csv('BALANCETE.csv', usecols=['TIPO', 'MES', 'ANO'])

    balancete_fechado = balancete_fechado[balancete_fechado['TIPO'] == 'NORMAL'].drop_duplicates().reset_index(
        drop=True)

    balancete_fechado['COD_ANO'] = balancete_fechado[['MES', 'ANO']].astype('str').apply(''.join, axis=1)

    if par_cod_ano in balancete_fechado['COD_ANO'].__iter__():
        return True
    else:
        return False


# === FUNCOES PARA GERAÇÃO DO SALDO INICIAL DO BALANCO PATRIMONIAL  === #

# Função para incluir o SALDO INICIAL no BALANCO PATRIMONIAL do período especificado.
def saldo_inicial_balanco_patrimonial(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    balanco_patrimonial = pd.read_csv('P CONTAS.csv')
    balanco_patrimonial = balanco_patrimonial.loc[balanco_patrimonial[
                                                      'NUMERO DA CONTA'].str.startswith(('1', '2'), 0), :]

    balancete = pd.read_csv('BALANCETE.csv')
    balancete = balancete.loc[
        (balancete['TIPO'] == 'SALDOINICIAL') & (balancete['MES'] == par_mes) & (balancete['ANO'] == par_ano)]

    balanco_patrimonial = balanco_patrimonial.merge(
        right=balancete[['NUMERO DA CONTA', 'SALDOFINAL']],
        left_on='NUMERO DA CONTA',
        right_on='NUMERO DA CONTA',
        how='left'
    ).fillna(0).rename(columns={'SALDOFINAL': 'VALOR'})

    balanco_patrimonial[['MES_REF', 'ANO_REF']] = par_mes, par_ano

    balanco_patrimonial['DATA_INCL'] = date.today().strftime('%x')

    balanco_patrimonial['DESCRICAO DA CONTA'] = 'SI ' + balanco_patrimonial['DESCRICAO DA CONTA']

    lista_balanco_patrimonial = []
    lista_temp = []
    for index, row in balanco_patrimonial.iterrows():
        for r in row:
            lista_temp.append(r)
        lista_balanco_patrimonial.append(lista_temp.copy())
        lista_temp.clear()

    # Parte de atribuição dos saldos para as contas sintéticas com os dados de SALDO INICIAL
    plano_de_contas = pd.read_csv('P CONTAS.csv')

    plano_de_contas = plano_de_contas.loc[
        plano_de_contas['NUMERO DA CONTA'].str.startswith(('1', '2'), 0),
        ['NUMERO DA CONTA', 'CONTA MAE']
    ]

    conta_mae_unica = pd.DataFrame(balanco_patrimonial['CONTA MAE']).drop_duplicates().astype('str')

    conta_mae_unica.sort_values(by=['CONTA MAE'], ascending=False, inplace=True)

    dict_pc = {}
    dict_conta_mae = {}
    dict_valor = {}

    for ind, val in plano_de_contas[['NUMERO DA CONTA', 'CONTA MAE']].iterrows():
        dict_pc[val[0]] = val[1]

    for i in conta_mae_unica['CONTA MAE'].__iter__():
        dict_conta_mae[i] = 0.00

    for ind, val in balanco_patrimonial[['NUMERO DA CONTA', 'VALOR']].iterrows():
        if val[0] in dict_valor:
            dict_valor[val[0]] += float(str(val[1]).replace(',', '.'))
        else:
            dict_valor[val[0]] = float(str(val[1]).replace(',', '.'))

    for key in dict_conta_mae:
        for key2, val2 in dict_pc.items():
            if key == val2:
                for key3, val3 in dict_valor.items():
                    if key2 == key3:
                        dict_conta_mae[val2] += float(val3)
                dict_valor[val2] = float(dict_conta_mae[val2])

    for key, val in dict_conta_mae.items():
        for ind2, val2 in enumerate(lista_balanco_patrimonial):
            if str(key) == str(val2[0]):
                lista_balanco_patrimonial[ind2][4] = val

    return lista_balanco_patrimonial


# Função para verificar se existe saldo inicial no balancete do período específicado. Retorna booleanos.
def verificar_saldo_inicial_no_balancete(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    balancete = pd.read_csv('BALANCETE.csv')

    balancete = balancete.loc[
        (balancete['TIPO'] == 'SALDOINICIAL') & (balancete['MES'] == par_mes) & (balancete['ANO'] == par_ano)]

    if len(balancete['TIPO']) > 0:
        return True
    else:
        return False


# Função para verificar se já existe saldo inicial no Balanço Patrimonial.
def verificar_saldo_inicial_no_balanco_patrimonial(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    balanco_patrimonial = pd.read_csv('BALANCO PATRIMONIAL.csv')

    balanco_patrimonial = balanco_patrimonial.loc[
        (balanco_patrimonial['MES_REF'] == par_mes) & (balanco_patrimonial['ANO_REF'] == par_ano)
        ]

    for dado in balanco_patrimonial['DESCRICAO_DA_CONTA'].__iter__():
        if 'SI' in dado:
            return True
        else:
            return False


# === FUNCOES PARA GERAÇÃO DO BALANCO PATRIMONIAL COM MOVIMENTOS NORMAIS === #

# Função para gerar o BALANCO PATRIMONIAL do período especificado
def consolidar_balanco_patrimonial(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    # Parte de consolidação utilizando o movimento do período.
    balanco_patrimonial = pd.read_csv('P CONTAS.csv')
    balanco_patrimonial = balanco_patrimonial.loc[balanco_patrimonial[
                                                      'NUMERO DA CONTA'].str.startswith(('1', '2'), 0), :]

    balancete = pd.read_csv('BALANCETE.csv')
    balancete = balancete.loc[(balancete['MES'] == par_mes) & (balancete['ANO'] == par_ano)]

    balanco_patrimonial = balanco_patrimonial.merge(
        right=balancete[['NUMERO DA CONTA', 'SALDOFINAL']],
        left_on='NUMERO DA CONTA',
        right_on='NUMERO DA CONTA',
        how='left'
    ).fillna(0).rename(columns={'SALDOFINAL': 'VALOR'})

    balanco_patrimonial[['MES_REF', 'ANO_REF']] = par_mes, par_ano

    balanco_patrimonial['DATA_INCL'] = date.today().strftime('%x')

    lista_balanco_patrimonial = []
    lista_temp = []
    for index, row in balanco_patrimonial.iterrows():
        for r in row:
            lista_temp.append(r)
        lista_balanco_patrimonial.append(lista_temp.copy())
        lista_temp.clear()

    # Parte de atribuição dos saldos para as contas sintéticas.
    plano_de_contas = pd.read_csv('P CONTAS.csv')

    plano_de_contas = plano_de_contas.loc[
        plano_de_contas['NUMERO DA CONTA'].str.startswith(('1', '2'), 0),
        ['NUMERO DA CONTA', 'CONTA MAE']
    ]

    conta_mae_unica = pd.DataFrame(balanco_patrimonial['CONTA MAE']).drop_duplicates().astype('str')

    conta_mae_unica.sort_values(by=['CONTA MAE'], ascending=False, inplace=True)

    dict_pc = {}
    dict_conta_mae = {}
    dict_valor = {}

    for ind, val in plano_de_contas[['NUMERO DA CONTA', 'CONTA MAE']].iterrows():
        dict_pc[val[0]] = val[1]

    for i in conta_mae_unica['CONTA MAE'].__iter__():
        dict_conta_mae[i] = 0.00

    for ind, val in balanco_patrimonial[['NUMERO DA CONTA', 'VALOR']].iterrows():
        if val[0] in dict_valor:
            dict_valor[val[0]] += float(str(val[1]).replace(',', '.'))
        else:
            dict_valor[val[0]] = float(str(val[1]).replace(',', '.'))

    for key in dict_conta_mae:
        for key2, val2 in dict_pc.items():
            if key == val2:
                for key3, val3 in dict_valor.items():
                    if key2 == key3:
                        dict_conta_mae[val2] += float(val3)
                dict_valor[val2] = float(dict_conta_mae[val2])

    for key, val in dict_conta_mae.items():
        for ind2, val2 in enumerate(lista_balanco_patrimonial):
            if str(key) == str(val2[0]):
                lista_balanco_patrimonial[ind2][4] = val

    return lista_balanco_patrimonial


# Função para organizar o Balanço Patrimonial.
def balanco_patrimonial_organizar():
    organizar_bp = pd.read_csv('BALANCO PATRIMONIAL.csv')
    organizar_bp.sort_values(by=['ANO_REF', 'MES_REF'], axis=0, inplace=True)

    lista_balanco_patrimonial = [[x for x in organizar_bp.keys()]]
    lista_temp = []
    for index, row in organizar_bp.iterrows():
        for r in row:
            lista_temp.append(r)
        lista_balanco_patrimonial.append(lista_temp.copy())
        lista_temp.clear()

    return lista_balanco_patrimonial


# Função para verificar se existe movimento no Balanço Patrimonial de um determinado período.
def verificar_movimento_balanco_patrimonial(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    par_cod_ano = str(par_mes).strip() + str(par_ano).strip()

    bp_movimento = pd.read_csv('BALANCO PATRIMONIAL.csv', usecols=['MES_REF', 'ANO_REF'])

    bp_movimento.drop_duplicates(inplace=True)

    bp_movimento['COD_ANO'] = bp_movimento[['MES_REF', 'ANO_REF']].astype('str').apply(func=''.join, axis=1)

    if par_cod_ano in bp_movimento['COD_ANO'].__iter__():
        return True
    else:
        return False


# Função para excluir o Balanço Patrimonial do período especificado.
def excluir_balanco_patrimonial(mes, ano):
    par_mes = int(mes)
    par_ano = int(ano)

    balanco_patrimonial_excluir = pd.read_csv('BALANCO PATRIMONIAL.csv')

    balanco_patrimonial_excluir.drop(labels=balanco_patrimonial_excluir.loc[
        (balanco_patrimonial_excluir['MES_REF'] == mes) & (balanco_patrimonial_excluir['ANO_REF'] == ano)
        ].index, inplace=True)

    balanco_patrimonial_excluir.sort_values(by=['ANO_REF', 'MES_REF', 'NUMERO_DA_CONTA'], inplace=True)

    lista_balanco_patrimonial_apos_exclusao = [[x for x in balanco_patrimonial_excluir.keys()]]
    lista_temp = []
    for index, row in balanco_patrimonial_excluir.iterrows():
        for r in row:
            lista_temp.append(r)
        lista_balanco_patrimonial_apos_exclusao.append(lista_temp.copy())
        lista_temp.clear()

    return lista_balanco_patrimonial_apos_exclusao


# === FUNÇÕES PARA O GRAFICO DE BARRAS E PIZZA DA DEMONSTRAÇÃO DO RESULTADO DO EXERCICIO === #

# Função para verificar se existe período para ser utilizado como ponto de partida (De) na definição dos dados que
# gerarão o gráfico de barras.
def verificar_ponto_de_partida_balancete(de_mes, de_ano):
    cod_ano = str(de_mes).strip() + str(de_ano).strip()

    df_b = pd.read_csv('BALANCETE.csv', usecols=['TIPO', 'MES', 'ANO'])

    df_b = df_b.loc[df_b['TIPO'] == 'NORMAL']

    df_b = df_b.drop_duplicates()

    df_b['COD_ANO'] = df_b['MES'].astype('str').str.cat(df_b['ANO'].astype('str'))

    for dado in df_b['COD_ANO'].__iter__():
        if cod_ano == dado:
            return True
    return False


# Função para retornar o último período em formato datetitime.date que contém dados.
def verificar_limite_balancete():
    df_b = pd.read_csv('BALANCETE.csv', usecols=['TIPO', 'MES', 'ANO'])

    df_b = df_b.loc[df_b['TIPO'] == 'NORMAL', :]

    df_b = df_b.drop_duplicates()

    lista = []

    for _, valor in df_b[['MES', 'ANO']].iterrows():
        lista.append(date(year=int(valor['ANO']),
                          month=int(valor['MES']),
                          day=monthrange(year=int(valor['ANO']), month=int(valor['MES']))[1]
                          )
                     )

    return max(lista)


# === FUNÇÕES PARA O GRAFICO DE LINHAS DO BALANCO PATRIMONIAL === #

# Função para verificar se existe período para ser utilizado como ponto de partida (De) na definição dos dados que
# gerarão o gráfico de linhas.
def verificar_ponto_de_partida_balanco_patrimonial(de_mes, de_ano):
    cod_ano = str(de_mes).strip() + str(de_ano).strip()

    df_balanco_patrimonial = pd.read_csv('BALANCO PATRIMONIAL.csv',
                                         usecols=['MES_REF', 'ANO_REF']).drop_duplicates().reset_index(drop=True)

    df_balanco_patrimonial.insert(
        2, 'COD_ANO', df_balanco_patrimonial['MES_REF'].astype('str').str.cat(
            df_balanco_patrimonial['ANO_REF'].astype('str')
        )
    )

    for dado in df_balanco_patrimonial['COD_ANO'].__iter__():
        if cod_ano == dado:
            return True
    return False


# Função para retornar o último período em formato datetitime.date que contém dados.
def verificar_limite_balanco_patrimonial():
    df_balanco_patrimonial = pd.read_csv('BALANCO PATRIMONIAL.csv',
                                         usecols=['MES_REF', 'ANO_REF']).drop_duplicates().reset_index(drop=True)

    lista = []

    for _, valor in df_balanco_patrimonial.iterrows():
        lista.append(
            date(
                year=int(valor[1]),
                month=int(valor[0]),
                day=monthrange(int(valor[1]), int(valor[0]))[1]
            )
        )

    return max(lista)