# === EXCESSOES GENERICAS === #

class ContaOuDescricao(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class CamposEmBranco(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class TipoContaInvalido(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class DataIncompleta(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class DiaInvalido(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class MesInvalido(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class AnoInvalido(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class ContaNaoEncontrada(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class ExclusaoNaoPermitida(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class SequenciaNaoEncontrada(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class NenhumaAlteracaoDefinida(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


# === BALANCETE DE VERIFICACAO PARA DEFINICAO DO SALDO INICIAL === #

# Excessão para uma conta que já possui saldo inicial.
class ContaComSaldoInicial(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


# === BALANCETE DE VERIFICACAO === #

# Para tentativas de geração um novo balancete para um período que já possui um balancete.
class BalancetePeriodoRegistrado(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


# Para tentativas de gerar um balancete sem dados de movimento no razão.
class BalanceteFicaraVazio(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


# Para verificar se o balancete possui dados para serem excluídos.
class BalancetePeriodoSemDados(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


# Para verificar se já existem lançamentos de compensação das contas de resultado. Será lançada ao tentar incluir
# lançamentos para um determinado período.
class LancamentosApuracaoDoResultadoExistentes(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


# Para verificar se existem dados de lançamentos de compensação de contas de resultados para serem excluídos. Será
# utilizado quando tentarmos excluir um apuração do resultado, sendo lançada a excessão caso não exista lançamentos
# para excluir.
class LancamentosApuracaoDoResultadoInexistentes(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


# === EXCESSOES PARA O SALDO INICIAL DO BALANCO PATRIMONIAL === #

class BalanceteSemSaldoInicial(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class SaldoInicialExistenteNoBalancoPatrimonial(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


# === EXCESSOES PARA O BALANCO PATRIMONIAL === #

# Para verificar se já existe balanco patrimonial consolidado do período especificado.
class BalancoPatrimonialExistente(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class BalancoPatrimonialInexistente(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


# === EXCESSOES PARA OS GRAFICOS === #

# Para verificar se a data limite (até) é menor que a data de partida (de).
class DataPosteriorMenor(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class PontoDePartidaInexistente(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)
