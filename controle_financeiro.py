import csv
from formatacao_de_dados import FormatacaoDeDados as fdd
import excessoes as ex
from calendar import monthrange
import locale
from datetime import date
import manipulacoes_pandas as ManP

locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')


# === CONTROLE FINANCEIRO === #

# Controle dos movimentos financeiros pessoais baseado em contabilização contábil.

class ControleFinanceiro:

    # Leitura e escrita em listas dos dados armazenados nas tabelas dos arquivos em csv.
    def __init__(self, plano_de_contas_csv, livro_razao_csv, balancete_csv, balanco_patrimonial_csv):

        self.plano_de_contas_csv = plano_de_contas_csv
        self.livro_razao_csv = livro_razao_csv
        self.balancete_csv = balancete_csv
        self.balanco_patrimonial_csv = balanco_patrimonial_csv
        self.plano_de_contas = []
        self.livro_razao = []
        self.balancete_verificacao = []
        self.balanco_patrimonial = []
        self.saldo_inicial = []
        self.lancamento = []
        self.balanco_patrimonial_periodo = []
        self.contas_analiticas = []
        self.contas_sinteticas = []

        with open(self.plano_de_contas_csv, 'r', encoding='utf-8') as arquivo_plano_de_contas:
            leitura = csv.reader(arquivo_plano_de_contas)
            for dados in leitura:
                self.plano_de_contas.append(dados)

        with open(self.livro_razao_csv, 'r', encoding='utf-8') as arquivo_razao:
            leitura = csv.reader(arquivo_razao)
            for dados in leitura:
                self.livro_razao.append(dados)

        with open(self.balancete_csv, 'r', encoding='utf-8') as arquivo_balancete:
            leitura = csv.reader(arquivo_balancete)
            for dados in leitura:
                self.balancete_verificacao.append(dados)

        with open(self.balanco_patrimonial_csv, 'r', encoding='utf-8') as arquivo_balanco:
            leitura = csv.reader(arquivo_balanco)
            for dados in leitura:
                self.balanco_patrimonial.append(dados)

        with open(self.balancete_csv, 'r', encoding='utf-8') as arquivo_saldo_inicial:
            leitura = csv.reader(arquivo_saldo_inicial)
            linha = 0
            for dados in leitura:
                if linha == 0:
                    self.saldo_inicial.append(dados)
                    linha += 1
                if dados[1] == 'SALDOINICIAL':
                    self.saldo_inicial.append(dados)
                if dados[1] == 'NORMAL':
                    break

        self.atualizar_analiticas_sinteticas()

    def __repr__(self):
        return '<Classe: ControleFinanceiro>'

    # === MÉTODOS DEDICADOS À INCLUSÃO, ALTERAÇÃO E REMOÇÃO DE CONTAS NO PLANO DE CONTAS === #

    # Ordena o plano de contas com o método Bubble Sort.
    def ordenar_plano_de_contas(self):
        contador = 0
        while True:
            for ind in range(len(self.plano_de_contas) - 1):
                if ind > 0:
                    if self.plano_de_contas[ind][0] > self.plano_de_contas[ind + 1][0]:
                        contador += 1
                        armazena_valor_temp = self.plano_de_contas[ind]
                        self.plano_de_contas[ind] = self.plano_de_contas[ind + 1]
                        self.plano_de_contas[ind + 1] = armazena_valor_temp
            if contador == 0:
                break
            contador = 0

    # Verifica se as contas existem no plano de contas e efetua a validação de existência das contas.
    # Caso algum dos parâmetros já exista no plano de contas, a lista "resultado" recebe
    # o número 1 em um do seus índices ind[0] ou ind[1] e não permite a inclusão.
    def verificar_plano_de_contas(self, numero_da_conta, descricao_da_conta):
        resultado = [0, 0]
        for ind in self.plano_de_contas:
            if numero_da_conta == ind[0]:
                resultado[0] = 1
            if descricao_da_conta == ind[1]:
                resultado[1] = 1
        if resultado[0] == 0 and resultado[1] == 0:
            return True
        else:
            return False

    # Adciona uma nova conta ao plano de contas.
    # A classe de formatação de dados é chamada para formatar a entrada dos dados no plano de contas.
    def adicionar_conta(self, numero_da_conta, descricao_da_conta, tipo, conta_mae=''):
        if self.verificar_plano_de_contas(fdd.formatar_conta(numero_da_conta), descricao_da_conta) is True:
            if '' != str(numero_da_conta).strip() and str(descricao_da_conta).strip() and str(tipo).strip():
                self.plano_de_contas.append(
                    [fdd.formatar_conta(numero_da_conta), str(descricao_da_conta).strip().upper(),
                     fdd.tipo_de_conta(tipo), self.encontrar_conta(conta_mae)])
                if str(numero_da_conta).strip().startswith(('3', '4', '5'), 0) and fdd.tipo_de_conta(tipo).startswith(
                        'A', 0):
                    self.plano_de_contas.append(
                        [fdd.formatar_conta('8.' + numero_da_conta), str(descricao_da_conta).strip().upper(),
                         fdd.tipo_de_conta(tipo), '']
                    )
                self.ordenar_plano_de_contas()
            else:
                raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')
        else:
            raise ex.ContaOuDescricao('Conta ou descrição já cadastradas')

    # Visualização do plano de contas atual printado na tela.
    def visualizar_plano_de_contas(self):
        for ind in self.plano_de_contas:
            for i in ind:
                print(f'{i:<30s}', end='')
            print()

    # Encontrar contas no plano de contas baseando-se no nome da conta cadastrada no Plano de Contas.
    def encontrar_conta(self, descricao_da_conta):
        descricao = descricao_da_conta.strip().upper()
        if descricao == '':
            return ''
        for i in self.plano_de_contas:
            if descricao == str(i[1]).strip().upper():
                return str(i[0]).strip()

    # Altera qualquer campo do plano de contas utilizando o número da linha e da coluna como índices. '' foi
    # atribuído aos campos porque em caso de parâmetros com '', nenhuma alteração será feita no campo representado
    # pela linha e pela coluna. O novo valor é atribuído acessando a linha informada e a coluna baseando-se na
    # ordem dos índices da lista temporária que não possuem valor ''.
    def alterar_plano_de_contas(self, numero_conta_alterar, numero_da_conta='', descricao_conta='', tipo_conta='',
                                conta_mae=''):
        numero_conta = fdd.formatar_conta(numero_conta_alterar)
        if '' != numero_da_conta or descricao_conta or tipo_conta:
            lista_temp = [
                [fdd.formatar_conta(numero_da_conta), str(descricao_conta).strip().upper(),
                 str(tipo_conta).strip().upper(),
                 fdd.formatar_conta(conta_mae)],
            ]
        else:
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter sido preenchidos.')
        verificacao = False
        for ind, val in enumerate(self.plano_de_contas):
            if numero_conta == val[0].strip():
                verificacao = True
                for i in lista_temp:
                    for i2, v2 in enumerate(i):
                        if v2 != '':
                            self.plano_de_contas[ind][i2] = v2
                break
        if verificacao is False:
            raise ex.ContaNaoEncontrada('Número de conta informado não foi encontrado.')

    # Remove uma conta do plano de contas baseando-se no número da conta formato pelo método da Classe
    # FormatacaoDeDados nos casos em que esse número é encontrado no plano de contas utilizado.
    def remover_conta(self, numero_conta):
        numero = fdd.formatar_conta(numero_conta)
        if numero == '':
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter sido preenchidos.')
        verificacao = False
        for ind in self.plano_de_contas:
            if numero in ind[0]:
                self.plano_de_contas.pop(self.plano_de_contas.index(ind))
                verificacao = True
                break
        if verificacao is False:
            raise ex.ContaNaoEncontrada('Número de conta informado não foi encontrado.')

    # Atualiza o arquivo CSV com o plano de contas atual (self.plano_de_contas).
    def atualizar_plano_de_contas(self):
        with open(self.plano_de_contas_csv, 'w', encoding='utf-8', newline='') as arquivo:
            escrita = csv.writer(arquivo)
            escrita.writerows(self.plano_de_contas)

    # === MÉTODOS DEDICADOS À INCLUSÃO, ALTERAÇÃO E REMOÇÃO DE LANÇAMENTOS CONTÁBEIS === #

    # As funções abaixo serão utilizadas para inclusão dos dados de movimentos financeiros na tabela em csv.

    # Acessa diretamente o valor da coluna SEQUENCIA localizado na última linha e na primeira coluna para
    # saber qual o último número utilizado e manter a sequência sem lançamento repetidos.
    def sequencia(self):
        if len(self.livro_razao) == 1:
            return 1
        if isinstance(int(self.livro_razao[-1][0]), int):
            return int(self.livro_razao[-1][0]) + 1

    # Recebe o valor de data e utiliza a classe FormatacaoDeDados fdd para manter um padrão de data brasileiro, com
    # 2 dígitos para o dia, 2 dígitos para o mês e 4 dígitos para o ano XX/XX/XXXX.
    @staticmethod
    def data_do_lancamento(data):
        return fdd.formatar_data(data)

    # Recebe o número da conta débito que irá receber o lançamento em números inteiros ou texto e formata de acordo
    # com o padrão previamente estabelecido. Outra função "valida_conta" verifica a existência da conta no
    # plano de contas antes de prosseguir com o retorno da formatação.
    def conta_debito(self, numero_conta):
        conta_numero = fdd.formatar_conta(numero_conta)
        if self.validar_conta(conta_numero):
            return conta_numero

    # Recebe a descrição da conta débito. Esse valor vem do plano de contas.
    @staticmethod
    def descricao_conta_debito(descricao_conta_debito):
        descricao_debito = descricao_conta_debito.strip().upper()
        return descricao_debito

    # Recebe o número da conta crédito que irá receber o lançamento em números inteiros ou texto e formata de acordo
    # com o padrão previamente estabelecido. Outra função "valida_conta" verifica a existência da conta no
    # plano de contas antes de prosseguir com o retorno da formatação.
    def conta_credito(self, numero_conta):
        conta_numero = fdd.formatar_conta(numero_conta)
        if self.validar_conta(conta_numero):
            return conta_numero

    # Recebe a descrição da conta débito. Esse valor vem do plano de contas.
    @staticmethod
    def descricao_conta_credito(descricao_conta_credito):
        descricao_credito = descricao_conta_credito.strip().upper()
        return descricao_credito

    # Recebe o valor da operação. O retorno é dado pela função da classe de formação de dados "FormatacaoDeDados fdd"
    # para que fique em um padrão brasileiro de valores monetários, separando os decimais com vírgula.
    @staticmethod
    def valor_operacao(valor_opr):
        return fdd.formata_valor(valor_opr)

    # Descrição livre para o fato gerador da operação, seja ela de saída ou entrada monetária.
    @staticmethod
    def descricao_do_fato(desc_fato):
        descricao_fato = desc_fato.strip().upper()
        return descricao_fato

    # A data de inclusão é uma função que utiliza o dia atual para preenchimento do campo. O método "date" da classe
    # datetime foi importado para trazer o valor de data atual que precisamos.
    @staticmethod
    def data_de_inclusao():
        v_data_inclusao = date.today().strftime("%x")
        return v_data_inclusao

    # Determina a ordem de inclusão dos dados no livro razão. Durante a chamada, usaremos as
    # funções para formatar os dados diretamente nos parâmetros.
    def ordem_de_inclusao(self, sequencia, data_lancamento, conta_deb, desc_conta_deb, conta_cre,
                          desc_conta_cre, valor, descricao_fato, data_inclusao):
        if '' != str(sequencia).strip() and str(data_lancamento).strip() and str(conta_deb).strip() and \
                str(desc_conta_deb).strip() and str(conta_cre).strip() and str(desc_conta_cre).strip() and \
                str(valor).strip() and str(descricao_fato).strip():
            self.lancamento.extend(
                [sequencia, data_lancamento, conta_deb, desc_conta_deb, conta_cre, desc_conta_cre,
                 valor, descricao_fato, data_inclusao])
            self.livro_razao.append(
                [sequencia, data_lancamento, conta_deb, desc_conta_deb, conta_cre, desc_conta_cre,
                 valor, descricao_fato, data_inclusao])
        else:
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')

    # Busca o número da conta no plano de contas atual para validar a existência. Dentro das chamadas
    # deve ir formatada pela função classe FormatacaoDeDados.
    def validar_conta(self, conta_num):
        valida = False
        for ind in self.plano_de_contas:
            if conta_num in ind:
                valida = True
                break
        if valida:
            return True
        else:
            raise Exception("Conta não encontrada no plano de contas")

    # Atualiza as contas analíticas e sintéticas para leitura isolada na Interface Grafica.
    def atualizar_analiticas_sinteticas(self):
        self.contas_analiticas.clear()
        self.contas_sinteticas.clear()
        for ind in self.plano_de_contas:
            if ind[2].strip() == 'A':
                self.contas_analiticas.append(ind[1])
            if ind[2].strip() == 'S':
                self.contas_sinteticas.append(ind[1])

    def atualizar_saldo_inicial(self):
        self.saldo_inicial.clear()
        for ind in self.balancete_verificacao[:1]:
            self.saldo_inicial.append(ind)
        for ind in self.balancete_verificacao[1:]:
            if ind[1] == 'SALDOINICIAL':
                self.saldo_inicial.append(ind)
            if ind[1] == 'NORMAL':
                break

    # Altera qualquer campo do razão utilizando o numero da linha e da coluna como índices. None foi atribuído aos
    # campos porque em caso de parâmetros com None, nenhuma alteração será feita no campo representado pela linha e
    # pela coluna. O novo valor é atribuído acessando a linha informada e a coluna baseando-se na ordem dos índices
    # da lista temporária que não possuem valor None.
    def alterar_razao(self, numero_linha, sequencia='', data_lancamento='', conta_deb='', desc_conta_deb='',
                      conta_cre='', desc_conta_cre='', valor='', descricao_fato='', data_inclusao=date.today()):
        if str(numero_linha).strip() == '':
            raise ex.CamposEmBranco('O campo de sequência deve ser preenchido para efetuar uma alteração.')
        if str(numero_linha).strip() != '' and \
                str(data_lancamento).strip() == '' and \
                str(conta_deb).strip() == '' and \
                str(desc_conta_deb).strip() == '' and \
                str(conta_cre).strip() == '' and \
                str(desc_conta_cre).strip() == '' and \
                str(valor).strip() == '' and \
                str(descricao_fato).strip() == '':
            raise ex.NenhumaAlteracaoDefinida('Todos os campos passíveis de alteração estão em branco.')
        num_linha = int(numero_linha)
        if num_linha < 1:
            raise ex.ExclusaoNaoPermitida('Os rótulos das colunas não podem ser alterados.')
        lista_temp = [[sequencia, fdd.formatar_data(data_lancamento), fdd.formatar_conta(conta_deb), desc_conta_deb,
                       fdd.formatar_conta(conta_cre), str(desc_conta_cre).strip().upper(),
                       fdd.formata_valor_alteracoes(valor),
                       str(descricao_fato).strip().upper(), data_inclusao.strftime('%x')]]
        for ind in lista_temp:
            for i, v in enumerate(ind):
                if v != '':
                    self.livro_razao[num_linha][i] = v

    # Remove qualquer lancamento do razão utilizando o número da linha como índice (remove a linha inteira)
    def remover_lancamento(self, numero_linha):
        if str(numero_linha).strip() == '':
            raise ex.CamposEmBranco('O campo de sequência deve ser preenchido para efetuar uma remoção.')
        num_linha = int(numero_linha)
        if num_linha < 1:
            raise ex.ExclusaoNaoPermitida('Os rótulos das colunas não podem ser removidos.')
        for i, v in enumerate(self.livro_razao):
            if str(num_linha).strip() == v[0]:
                self.livro_razao.pop(i)
                break

    # Atualiza  o livro razão após a alteração no razão
    def atualizar_livro_razao(self):
        with open(self.livro_razao_csv, 'w', encoding='utf-8', newline='') as novo_arquivo_razao:
            escrita = csv.writer(novo_arquivo_razao)
            escrita.writerows(self.livro_razao)

    # Faz a inclusão do lançamento no arquivo de livro razão em formato csv. Mais precisamente, deve
    # ser chamada após a conclusão de um evento  de envio de informações.
    def incluir_lancamento(self):
        with open(self.livro_razao_csv, 'a', encoding='utf-8', newline='') as arquivo_inclusao:
            escrita = csv.writer(arquivo_inclusao, delimiter=',')
            escrita.writerow(self.lancamento)
            self.lancamento.clear()

    # === MÉTODOS PARA GERENCIAR O SALDO INICIAL QUE IRÁ CONSTAR NO BALANCETE === #

    # Define a sequência de entradas no balancete de verificação com base nas sequências já preenchidas.
    def sequencia_balancete(self):
        if len(self.balancete_verificacao) == 1:
            return 1
        if isinstance(int(self.balancete_verificacao[-1][0]), int):
            return int(self.balancete_verificacao[-1][0]) + 1

    # Inclui um saldo inicial para um conta ANALÍTICA com base no mês anterior ao de início de uso do controle
    # financeiro, o tipo de lançamento é definido pela atribuição na colunad de "TIPO" como 'SALDOINICIAL'.
    def incluir_saldo_inicial(self, sequencia, tipo, mes, ano, numero_conta, desc_conta, saldo_inicial, movto_deb,
                              movto_cre,
                              saldo_final):
        if '' == str(sequencia).strip() or \
                '' == str(tipo).strip() or \
                '' == str(mes).strip() or \
                '' == str(ano).strip() or \
                '' == str(numero_conta) or \
                '' == str(desc_conta).strip() or \
                '' == str(saldo_inicial).strip() or \
                '' == str(movto_deb).strip() or \
                '' == str(movto_cre).strip() or \
                '' == str(saldo_final).strip():
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')
        self.balancete_verificacao.append(
            [sequencia, tipo, mes, ano, self.verificar_conta_com_saldo_inicial(self.encontrar_conta(numero_conta)),
             str(desc_conta).strip().upper(), saldo_inicial, movto_deb, movto_cre, saldo_final]
        )

        lista_ordenar_balancete = ManP.ordernar_balancete(self.balancete_verificacao)

        self.balancete_verificacao.clear()

        for _, val in enumerate(lista_ordenar_balancete):
            self.balancete_verificacao.append([val[0], val[1], val[2], val[3], val[4], val[5], val[6],
                                               val[7], val[8], val[9]])

        self.atualizar_saldo_inicial()

    # Faz a inclusão das inclusões e alterações feitas na lista self.balancete_verificacao no arquivo CSV
    # balancete.
    def atualizar_balancete(self):
        with open(self.balancete_csv, 'w', encoding='utf-8', newline='') as arquivo_saldo:
            escrita = csv.writer(arquivo_saldo, delimiter=',')
            escrita.writerows(self.balancete_verificacao)

    # Altera o balancete com base nos campos que não estão com valor vazio ''.
    def alterar_balancete(self, numero_linha, sequencia='', tipo='', mes='', ano='', numero_conta='', desc_conta='',
                          saldo_inicial='', movto_deb='', movto_cre='', saldo_final=''):
        if str(numero_linha).strip() == '':
            raise ex.CamposEmBranco('O campo de sequência deve ser preenchido para efetuar uma remoção.')
        lista_temp = [
            [sequencia, tipo, mes, ano, self.encontrar_conta(numero_conta), desc_conta, saldo_inicial, movto_deb,
             movto_cre, saldo_final]
        ]
        num_linha = int(numero_linha)
        if num_linha < 1:
            raise ex.ExclusaoNaoPermitida('Exclusão não permitida. Os rótulos de colunas não podem ser removidos.')
        for ind in lista_temp:
            for i, v in enumerate(ind):
                if v != '':
                    self.balancete_verificacao[num_linha][i] = v

    # Verifica se um conta de saldo inicial já possui um saldo inicial registrado.
    def verificar_conta_com_saldo_inicial(self, numero_conta):
        lista_conta_saldo_inicial = []
        for i in self.balancete_verificacao:
            if str(i[1]).strip() == 'SALDOINICIAL' and i[4] == numero_conta:
                raise ex.ContaComSaldoInicial(f"A conta {numero_conta} já possui um saldo inicial.")
        return numero_conta

    # Remove uma sequência de saldo inicial do balancete.
    def remover_saldo_inicial_balancete(self, numero_linha):
        if str(numero_linha).strip() == '':
            raise ex.CamposEmBranco('O campo de sequência deve ser preenchido para efetuar uma remoção.')
        num_linha = int(numero_linha)
        if num_linha < 1:
            raise ex.ExclusaoNaoPermitida('Os rótulos das colunas não podem ser removidos.')
        for i, v in enumerate(self.balancete_verificacao):
            if str(num_linha).strip() == v[0]:
                self.balancete_verificacao.pop(i)
                break

        lista_ordenar_balancete = ManP.ordernar_balancete(self.balancete_verificacao)

        self.balancete_verificacao.clear()

        for _, val in enumerate(lista_ordenar_balancete):
            self.balancete_verificacao.append([val[0], val[1], val[2], val[3], val[4], val[5], val[6],
                                               val[7], val[8], val[9]])

        self.atualizar_saldo_inicial()

    # === MÉTODOS PARA CONSOLIDAR OS MOVIMENTOS A CREDITO E A DEBITO DO BALANCETE === #

    # Função que chama as manipulações efetuadas com o Pandas para gerar o Balancete de Verificação do período
    # especificado.
    def gerar_balancete(self, mes, ano):
        if mes == '' or ano == '':
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')

        par_mes = int(mes)
        par_ano = int(ano)

        ManP.verificar_movimento_razao(par_mes, par_ano)

        ManP.verificar_periodo_balancete(par_mes, par_ano)

        lista_balancete = ManP.consolidar_balancete(par_mes, par_ano)

        for _, val in enumerate(lista_balancete):
            self.balancete_verificacao.append([1, val[0], val[1], val[2], val[3], val[4], val[5], val[6],
                                               val[7], val[8]])

        lista_ordenar_balancete = ManP.ordernar_balancete(self.balancete_verificacao)

        self.balancete_verificacao.clear()

        for _, val in enumerate(lista_ordenar_balancete):
            self.balancete_verificacao.append([val[0], val[1], val[2], val[3], val[4], val[5], val[6],
                                               val[7], val[8], val[9]])

    # === MÉTODOS PARA REMOVER DADOS DO BALANCETE === #

    # Função que chama as manipulações efetuadas com o Pandas para remover o Balancete de Verificação
    # de um determinado período.
    def remover_balancete(self, mes, ano):
        if mes == '' or ano == '':
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')

        par_mes = int(mes)
        par_ano = int(ano)

        ManP.verificar_periodo_exclusao(par_mes, par_ano)

        lista_remover_balancete = ManP.excluir_balancete(par_mes, par_ano)

        self.balancete_verificacao.clear()
        self.balancete_verificacao.append(['SEQUENCIA', 'TIPO', 'MES', 'ANO', 'NUMERO DA CONTA', 'DESCRICAO DA CONTA',
                                           'SALDO INICIAL', 'MOVTO_DEB', 'MOVTO_CRE', 'SALDOFINAL'])

        for _, val in enumerate(lista_remover_balancete):
            self.balancete_verificacao.append(
                [self.sequencia_balancete(), val[0], val[1], val[2], val[3], val[4], val[5], val[6],
                 val[7], val[8]])

    # === MÉTODOS PARA APURAR O RESULTADO DO EXERCÍCIO === #

    # Efetua lançamentos de compensação nas contas analíticas de resultado de Receitas, Custos e Despesas.
    # Utiliza o valor da soma das movimentações apurada pelo balancete de verificação.

    # Função que chama as manipulaões do pandas para efetuar a Apuração do Resultado do Exercício, objetivando
    # a liquidação de qualquer saldo nas contas de resultado, para que não virem o período com saldos iniciais.
    # O objetivo é que os valores de resultado que serão analisados em partes posteriores, como nos gráficos,
    # sejam feitos utilizando contas com início 8, que armazenarão esses valores.
    def apuracao_do_resultado_lancamentos(self, mes, ano):
        if mes == '' or ano == '':
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')

        par_mes = int(mes)
        par_ano = int(ano)
        ultimo_dia = monthrange(par_ano, par_mes)[1]

        if ManP.verificar_movimento_balancete_apuracao_do_resultado(par_mes, par_ano) is False:
            raise ex.BalancetePeriodoSemDados('Ainda não existem dados no balancete para o período especificado.')

        if ManP.verificar_lancamentos_apuracao_do_resultado(par_mes, par_ano):
            raise ex.LancamentosApuracaoDoResultadoExistentes(
                'Já existem lançamentos de compensação das contas de resultado para o período. '
                'Exclua o anterior para continuar.'
            )

        lista_lancamentos = ManP.lancamentos_apuracao_do_resultado(par_mes, par_ano)

        for _, val in enumerate(lista_lancamentos):
            if str(val[0]).startswith('3'):
                self.ordem_de_inclusao(
                    sequencia=self.sequencia(),
                    data_lancamento=date(par_ano, par_mes, ultimo_dia).strftime('%x'),
                    conta_deb=self.conta_debito(val[0]),
                    desc_conta_deb=val[1],
                    conta_cre=self.conta_credito(str('8.' + val[0])),
                    desc_conta_cre=val[1],
                    valor=val[2],
                    descricao_fato=f'APURACAO DO RESULTADO {str(par_mes) + str(par_ano)}',
                    data_inclusao=date.today().strftime('%x')
                )
            else:
                self.ordem_de_inclusao(
                    sequencia=self.sequencia(),
                    data_lancamento=date(par_ano, par_mes, ultimo_dia).strftime('%x'),
                    conta_deb=self.conta_debito(str('8.' + val[0])),
                    desc_conta_deb=val[1],
                    conta_cre=self.conta_credito(val[0]),
                    desc_conta_cre=val[1],
                    valor=val[2],
                    descricao_fato=f'APURACAO DO RESULTADO {str(par_mes) + str(par_ano)}',
                    data_inclusao=date.today().strftime('%x')
                )

            self.incluir_lancamento()

            # Após excluir uma apuração do resultado, temos que excluir e gerar novamente o balancete com os seus saldos
            # atualizados.
            self.remover_balancete(par_mes, par_ano)
            self.atualizar_balancete()
            self.gerar_balancete(par_mes, par_ano)
            self.atualizar_balancete()

    # Exclui os lançamentos feitos no Livro Razão para as contas de compensação do resultado, contas de número 8
    # como inicial.
    def apuracao_do_resultado_lancamentos_exclusao(self, mes, ano):
        if mes == '' or ano == '':
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')

        par_mes = int(mes)
        par_ano = int(ano)

        if ManP.verificar_lancamentos_apuracao_do_resultado(par_mes, par_ano) is False:
            raise ex.LancamentosApuracaoDoResultadoInexistentes(
                'Não existem lançamentos de compensação das contas de resultado no período especificado para excluir.'
            )

        lista_lancamentos_exclusao = ManP.excluir_lancamento_apuracao_do_resultado(par_mes, par_ano)

        self.livro_razao.clear()

        for _, v in enumerate(lista_lancamentos_exclusao):
            self.livro_razao.append([v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8]])
            """self.ordem_de_inclusao(
                sequencia=v[0],
                data_lancamento=v[1],
                conta_deb=v[2],
                desc_conta_deb=v[3],
                conta_cre=v[4],
                desc_conta_cre=v[5],
                valor=v[6],
                descricao_fato=v[7],
                data_inclusao=v[8]
            )"""

        self.atualizar_livro_razao()

        # Após excluir uma apuração do resultado, temos que excluir e gerar novamente o balancete com os seus saldos
        # atualizados.
        self.remover_balancete(par_mes, par_ano)  # Quando removo os lançamentos a mão do arquivo. dá erro de excessão
        self.atualizar_balancete()
        self.gerar_balancete(par_mes, par_ano)
        self.atualizar_balancete()

    # === MÉTODOS PARA GERAR O BALANCO PATRIMONIAL === #

    # Função para escrever os dados da lista self.balanco_patrimonial no arquivo csv do Balanco Patrimonial.
    def incluir_balanco_patrimonial(self):
        with open('BALANCO PATRIMONIAL.csv', 'a', encoding='utf-8', newline='') as arquivo_bp:
            escrita = csv.writer(arquivo_bp)
            escrita.writerows(self.balanco_patrimonial_periodo)
            self.balanco_patrimonial_periodo.clear()

    # Função para atualizar o Balanço Patrimonial.
    def atualizar_balanco_patrimonial(self):
        with open('BALANCO PATRIMONIAL.csv', 'w', encoding='utf-8', newline='') as arquivo_bp:
            escrita = csv.writer(arquivo_bp)
            escrita.writerows(self.balanco_patrimonial)

    # Função para gerar o Balanço Patrimonial de um determinado período utilizando as manipulações feitas com
    # o Pandas.
    def gerar_balanco_patrimonial(self, mes, ano):
        if mes == '' or ano == '':
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')

        par_mes = int(mes)
        par_ano = int(ano)

        if ManP.verificar_movimento_balancete_apuracao_do_resultado(par_mes, par_ano) is False:
            raise ex.BalancetePeriodoSemDados('Ainda não existem dados no balancete para o período especificado.')

        if ManP.verificar_lancamentos_apuracao_do_resultado(par_mes, par_ano) is False:
            raise ex.LancamentosApuracaoDoResultadoInexistentes(
                'O Balanço Patrimonial não pode ser gerado sem a Apuração do Resultado do período especificado.'
            )

        if ManP.verificar_movimento_balanco_patrimonial(par_mes, par_ano):
            raise ex.BalancoPatrimonialExistente('Já existe um Balanco Patrimonial para o período especificado.')

        lista_balanco_patrimonial = ManP.consolidar_balanco_patrimonial(par_mes, par_ano)

        for ind in lista_balanco_patrimonial:
            self.balanco_patrimonial_periodo.append(ind)

    # Função para incluir os valores de Saldo Inicial no Balanço Patrimonial de um determinado período.
    def gerar_saldo_inicial_balanco_patrimonial(self, mes, ano):
        if mes == '' or ano == '':
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')

        par_mes = int(mes)
        par_ano = int(ano)

        if ManP.verificar_saldo_inicial_no_balanco_patrimonial(par_mes, par_ano) is True:
            raise ex.SaldoInicialExistenteNoBalancoPatrimonial(
                'Já existe Saldo Inicial no Balanço Patrimonial para o período.'
            )

        if ManP.verificar_saldo_inicial_no_balancete(par_mes, par_ano) is False:
            raise ex.BalanceteSemSaldoInicial('Não existe Saldo Inicial no balancete para o período especificado.')

        lista_balanco_patrimonial_saldo_inicial = ManP.saldo_inicial_balanco_patrimonial(par_mes, par_ano)

        for ind in lista_balanco_patrimonial_saldo_inicial:
            self.balanco_patrimonial_periodo.append(ind)

    # Função para organizar o balanço patrimonial.
    def organizar_balanco_patrimonial(self):

        lista = ManP.balanco_patrimonial_organizar()

        self.balanco_patrimonial.clear()

        for valor in lista:
            self.balanco_patrimonial.append(valor)

    # === MÉTODOS PARA EXCLUIR O BALANCO PATRIMONIAL === #

    # Função para excluir o balanco Patrimonial.
    def excluir_balanco_patrimonial_periodo(self, mes, ano):
        if mes == '' or ano == '':
            raise ex.CamposEmBranco('Existem campos em branco que deveriam ter ser preenchidos.')

        par_mes = int(mes)
        par_ano = int(ano)

        if ManP.verificar_movimento_balanco_patrimonial(par_mes, par_ano) is False:
            raise ex.BalancoPatrimonialInexistente(
                'Não existe Balanço Patrimonial no período especificado para ser excluído.')

        lista_balanco_patrimonial_apos_exclusao = ManP.excluir_balanco_patrimonial(par_mes, par_ano)

        self.balanco_patrimonial.clear()

        for valor in lista_balanco_patrimonial_apos_exclusao:
            self.balanco_patrimonial.append(valor)