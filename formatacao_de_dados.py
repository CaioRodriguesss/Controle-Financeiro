from datetime import date
import locale
import excessoes as ex

locale.setlocale(locale.LC_ALL, "pt_BR.utf-8")


class FormatacaoDeDados:

    def __init__(self):
        pass

    # Formata o número da conta com os ponto utilizados como convencao pelo sistema. Independentemente do valor sendo
    # inserido, a função irá considerar somente números para armazenamento.
    @staticmethod
    def formatar_conta(num_conta):
        numero_conta = ''
        if str(num_conta).strip() == '':
            return ''
        if len(str(num_conta).strip()) == 1:
            return num_conta
        if isinstance(num_conta, int):
            valor_temporario = []
            if len(str(num_conta)) > 0:
                for ind in str(num_conta):
                    valor_temporario.append(ind)
                    valor_temporario.append('.')
                valor_temporario.pop(-1)
                numero_conta = ''.join(valor_temporario)
        elif isinstance(num_conta.strip(), str) and not '':
            valor_temporario2 = []
            if len(str(num_conta)) > 0:
                for ind in str(num_conta):
                    if ind.isnumeric():
                        valor_temporario2.append(ind)
                        valor_temporario2.append('.')
                valor_temporario2.pop(-1)
                numero_conta = ''.join(valor_temporario2)
        else:
            raise Exception("O número informado é inválido")
        return numero_conta.strip()

    # Valida se o tipo de conta, SINTETICA OU ANALITICA, e seus caracteres de representação foram utilizados como
    # parâmetro. Os caracteres permitidos são S e A.
    @staticmethod
    def tipo_de_conta(tipo):
        if str(tipo).strip() == '':
            return ''
        tipo_conta = str(tipo).strip().upper()
        if tipo_conta not in ('A', 'S'):
            raise ex.TipoContaInvalido("Tipo de conta inválido. Tipos possíveis: A - Analítica ou S - Sintética")
        else:
            return tipo_conta

    # Formata a data para o padrão brasileiro ao receber datas no formato brasileiro XX/XX/XXXX, ou seja,
    # 2 dígitos para o dia, 2 dígitos para o mês e 4 dígitos para o ano.
    # A informação pode ser por meio de inteiros como o número 20041999, por texto '20041999' ou por texto
    # com formatacao de data '20/04/1999'. Baseando-se nisso, o dia, o mês e o ano passam por uma validação para
    # termos certeza de que estão dentro das faixas de valores permitidos.
    @staticmethod
    def formatar_data(data):
        param_data_atual = date.today()
        param_min_dia, param_max_dia = 1, 31
        param_min_mes, param_max_mes = 1, 12
        param_min_ano, param_max_ano = param_data_atual.year, 9999
        data_valor_temp = None
        armazena_inteiros = []
        if str(data).strip() == '':
            return ''
        for i in str(data):
            if i.isnumeric():
                armazena_inteiros.append(i)
        data_valor_temp = ''.join(armazena_inteiros)
        if len(data_valor_temp) == 8:
            pass
        else:
            raise ex.DataIncompleta('A data está incompleta ou mal formada.')
        var_dia, var_mes, var_ano = int(data_valor_temp[0:2]), int(data_valor_temp[2:4]), int(data_valor_temp[4:])
        if var_dia < param_min_dia or var_dia > param_max_dia:
            raise ex.DiaInvalido(f"Data inválida. O dia deve estar contido entre 01 e 31")
        if var_mes < param_min_mes or var_mes > param_max_mes:
            raise ex.MesInvalido(f"Data inválida. O mês deve estar contido entre 01 e 12")
        if var_ano < param_min_ano or var_ano > param_max_ano:
            raise ex.AnoInvalido(f"Data inválida. O ano deve estar contido entre {param_min_ano} e 9999")
        data_final = date(var_ano, var_mes, var_dia)
        return data_final.strftime('%x')

    # Formata o valor para um formato de valor monetário brasileiro, utilizando vírgula para separar os decimais.
    @staticmethod
    def formata_valor(valor):
        if valor != '':
            val = None
            if isinstance(valor, (int, float)):
                val = str(valor).replace('.', ',').strip()
            else:
                validar = valor.replace(',', '.')
                if type(float(validar)) is float:
                    val = valor
            return val
        else:
            raise ex.CamposEmBranco('O campo de valor não deve ficar em branco.')

    # Função para formatar o valor ao efetuar alguma alteração. Como foi definido que deixar um campo em branco
    # durante uma alteração não iria alterar o campo da sequência, precisamos retornar um vazio ao invés de uma
    # execessão de campos em branco durante o preenchimento.
    @staticmethod
    def formata_valor_alteracoes(valor):
        if str(valor).strip() != '':
            val = None
            if isinstance(valor, (int, float)):
                val = str(valor).replace('.', ',').strip()
            else:
                validar = valor.replace(',', '.')
                if type(float(validar)) is float:
                    val = valor
            return val
        else:
            return ''
