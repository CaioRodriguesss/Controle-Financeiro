import PySimpleGUI as sg
import excessoes as ex
from controle_financeiro import ControleFinanceiro
import graficos

CF = ControleFinanceiro('P CONTAS.csv', 'LIVRO RAZAO.csv', 'BALANCETE.csv', 'BALANCO PATRIMONIAL.csv')


class InterfaceGrafica:
    def __init__(self):
        pass

    @staticmethod
    def iniciar():

        # === LAYOUT PRINCIPAL === #

        # Layout principal com botões para seleção da INTERFACE GRÁFICA desejada. Cada botão possui um key que gera um
        # evento de entrada em outras interfaces do programa com função de operação real.
        prin_tam = (34, 1)
        principal_layout = [
            [sg.T('TELAS PARA CONTROLE FINANCEIRO', justification='center', size=(70, 1))],
            [sg.B('Incluir Conta', key='-PRININCCON-', size=prin_tam),
             sg.B('Manutenção Plano de Contas', key='-PRINMANPL-', size=prin_tam)],
            [sg.B('Saldos Iniciais', key='-PRINSALDINI-', size=prin_tam),
             sg.B('Manutenção Saldos Iniciais', key='-PRINMANSALDINI-', size=prin_tam)],
            [sg.B('Lançamentos', key='-PRINLANC-', size=prin_tam),
             sg.B('Manutenção Lançamentos', key='-PRINMANRA-', size=prin_tam)],
            [sg.B('Balancete de Verificação', key='-PRINBALAN-', size=prin_tam),
             sg.B('Manutenção Balancete', key='-PRINMANBA-', size=prin_tam)],
            [sg.B('Apuração do Resultado', key='-PRINAPR-', size=prin_tam),
             sg.B('Manutenção Apuração do Resultado', key='-PRINMANAPR-', size=prin_tam)],
            [sg.B('Balanço Patrimonial', key='-PRINBP-', size=prin_tam),
             sg.B('Manutenção Balanço Patrimonial', key='-PRINMBP-', size=prin_tam)],
            [sg.B('Gráfico Demonstração do Resultado', key='-PRINGDRE-', size=prin_tam),
             sg.B('Gráfico Balanço Patrimonial', key='-PRINGBP-', size=prin_tam)]
        ]

        window = sg.Window(title='Interface para controle financeiro', layout=principal_layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break

            # === INTERFACE GRÁFICA DE INCLUSAO DE CONTAS NO PLANO DE CONTAS === #

            # A identificação de evento é feita pelo ínicio '-PC(...)-', sigla para "P"lano de "C"ontas.
            if event == '-PRININCCON-':
                pc_t_tam = (20, 1)
                pc_i_tam = (51, 1)
                pc_layout = [
                    [sg.T('Número da Conta', size=pc_t_tam), sg.In(key='-PCNUMCON-', size=pc_i_tam, enable_events=True),
                     sg.T('Descrição da conta', size=pc_t_tam), sg.In(key='-PCDESCCON-', size=pc_i_tam)],
                    [sg.T('Tipo de Conta (A / S)', size=pc_t_tam),
                     sg.Radio(text='Analítica', group_id='TPC', key='-PCTIPOA-'),
                     sg.Radio(text='Sintética', group_id='TPC', key='-PCTIPOS-', size=(31, 1)),
                     sg.T('Conta Mãe', size=pc_t_tam),
                     sg.Combo([i for i in CF.contas_sinteticas], key='-PCMAE-', size=pc_i_tam, readonly=True)],
                    [sg.Push(), sg.B(key='-PCVIS-', button_text='Visualizar Plano de Contas'),
                     sg.B(key='-PCCRIAR-', button_text='Criar'),
                     sg.B(key='-PCLIMP-', button_text='Limpar'),
                     sg.B(key='-PCCANC-', button_text='Cancelar')],
                    [sg.T('Conta Criada', size=pc_t_tam), sg.Multiline(key='-PCEFET-', size=(127, 10))],
                ]
                window2 = sg.Window('Inclusão de Contas no Plano de Contas', layout=pc_layout)
                while True:
                    event2, values2 = window2.read()
                    if event2 == sg.WIN_CLOSED or event2 == '-PCCANC-':
                        break
                    if event2 == '-PCNUMCON-' and values2['-PCNUMCON-'] and \
                            values2['-PCNUMCON-'][-1] not in '0123456789.,':
                        window2['-PCNUMCON-'].update(value=values2['-PCNUMCON-'][0:-1])
                    tipo = ''
                    if values2['-PCTIPOA-']:
                        tipo = 'A'
                    if values2['-PCTIPOS-']:
                        tipo = 'S'
                    if event2 == '-PCVIS-':
                        layout_visualizar_plano_de_contas = [
                            [sg.T('PLANO DE CONTAS', size=(85, 1), justification='center')],
                            [sg.Table(headings=[c for c in CF.plano_de_contas[0]],
                                      values=[c for c in CF.plano_de_contas[1:]],
                                      key='-PCVISPDC-', justification='left')],
                            [sg.B('Ok', key='-PCVISBOK-')]
                        ]
                        window2_1 = sg.Window(title='Plano de Contas', layout=layout_visualizar_plano_de_contas)
                        while True:
                            event2_1, values2_1 = window2_1.read()
                            if event2_1 == sg.WIN_CLOSED or event2_1 == '-PCVISBOK-':
                                break
                        window2_1.close()
                    if event2 == '-PCCRIAR-':
                        try:
                            CF.adicionar_conta(values2['-PCNUMCON-'], values2['-PCDESCCON-'], tipo, values2['-PCMAE-'])
                            CF.atualizar_plano_de_contas()
                            CF.atualizar_analiticas_sinteticas()
                            window2['-PCEFET-'].print(f"=======================================\n"
                                                      f"Número da conta: {values2['-PCNUMCON-']}\n"
                                                      f"Descrição da conta: {values2['-PCDESCCON-']}\n"
                                                      f"Tipo de conta: {'Analítica' if tipo == 'A' else 'Sintética'}\n"
                                                      f"Conta mãe: {values2['-PCMAE-']}\n"
                                                      )
                            window2['-PCMAE-'].update(values=[i for i in CF.contas_sinteticas])
                            for key in values2.keys():
                                if key != '-PCEFET-':
                                    window2[key].update('')
                        except ex.ContaOuDescricao:
                            sg.popup('Número da conta ou descrição da conta já está cadastrada.', title='Erro')
                        except ex.CamposEmBranco:
                            sg.popup('Campos obrigatórios não foram preenchidos.', title='Erro')
                        except ex.TipoContaInvalido:
                            sg.popup('Tipo de conta inválido.', title='Erro')
                    if event2 == '-PCLIMP-':
                        for key in values2.keys():
                            window2[key].update('')
                window2.close()

            # === INTERFACE GRÁFICA DE LANCAMENTOS CONTABEIS === #

            # A identificação de evento é feita pelo início '-LC(...)-', sigla pata "L"ançamentos "C"ontabeis.
            if event == '-PRINLANC-':
                lc_t_tam = (20, 1)
                lc_i_tam = (47, 1)
                lc_coluna_direita = [
                    [sg.T('Conta Debito', size=lc_t_tam),
                     sg.Combo([i for i in CF.contas_analiticas], key='-LCCONDEB-', size=lc_i_tam, readonly=True)],
                    [sg.T('Valor', size=lc_t_tam), sg.In(key='-LCVAL-', size=lc_i_tam, enable_events=True)],
                ]
                lc_coluna_esquerda = [
                    [sg.Text('Conta Credito', size=lc_t_tam),
                     sg.Combo([i for i in CF.contas_analiticas], key='-LCCONCRE-', size=lc_i_tam, readonly=True)],
                    [sg.T('Data Lancamento', size=lc_t_tam),
                     sg.In(key='-LCDATLAN-', size=lc_i_tam, enable_events=True)],
                ]
                lc_layout = [
                    [sg.Col(lc_coluna_direita), sg.Col(lc_coluna_esquerda)],
                    [sg.T(' Descricao', size=lc_t_tam), sg.In(key='-LCDESC-', size=(104, 1)),
                     sg.B(key='-LCBLAN-', button_text='Lançar'),
                     sg.B(key='-LCBLIM-', button_text='Limpar'), sg.B(key='-LCBSAIR-', button_text='Sair')],
                    [sg.T(' Lançamento efetuado', size=lc_t_tam), sg.Multiline(key='-LCEFET-', size=(125, 10))],
                ]
                window3 = sg.Window('Interface para Lançamentos Contáveis', layout=lc_layout)
                while True:
                    event3, values3 = window3.read()
                    if event3 == sg.WIN_CLOSED or event3 == '-LCBSAIR-':
                        break
                    if event3 == '-LCVAL-' and values3['-LCVAL-'] and values3['-LCVAL-'][-1] not in '0123456789,.':
                        window3['-LCVAL-'].update(value=values3['-LCVAL-'][0:-1])
                    if event3 == '-LCDATLAN-' and values3['-LCDATLAN-'] and \
                            values3['-LCDATLAN-'][-1] not in '0123456789/':
                        window3['-LCDATLAN-'].update(value=values3['-LCDATLAN-'][0:-1])
                    if len(values3['-LCDATLAN-']) > 10:
                        window3['-LCDATLAN-'].update(value=values3['-LCDATLAN-'][0:10])
                    if event3 == '-LCBLAN-':
                        try:
                            CF.ordem_de_inclusao(
                                CF.sequencia(),
                                CF.data_do_lancamento(values3['-LCDATLAN-']),
                                CF.conta_debito(CF.encontrar_conta(values3['-LCCONDEB-'])),
                                CF.descricao_conta_debito(values3['-LCCONDEB-']),
                                CF.conta_credito(CF.encontrar_conta(values3['-LCCONCRE-'])),
                                CF.descricao_conta_credito(values3['-LCCONCRE-']),
                                CF.valor_operacao(values3['-LCVAL-']),
                                CF.descricao_do_fato(values3['-LCDESC-']),
                                CF.data_de_inclusao()
                            )
                            CF.incluir_lancamento()
                            window3['-LCEFET-'].print(f"============================================\n"
                                                      f"DÉBITO: {values3['-LCCONDEB-']}\n"
                                                      f"CRÉDITO: {values3['-LCCONCRE-']}\n"
                                                      f"VALOR DA OPERAÇÃO: {values3['-LCVAL-']}\n"
                                                      f"DESCRIÇÃO DA OPERAÇÃO: {values3['-LCDESC-']}\n"
                                                      f"DATA DA OPERAÇÃO: "
                                                      f"{CF.data_do_lancamento(values3['-LCDATLAN-'])}\n"
                                                      )
                            for key in values3.keys():
                                if key != '-LCEFET-':
                                    window3[key].update(value='')
                        except ex.DiaInvalido:
                            sg.popup('Data inválida.O dia deve estar contido entre 01 e 31.', title='Erro')
                        except ex.MesInvalido:
                            sg.popup('Data inválida. O mês deve estar contido entre 01 e 12.', title='Erro')
                        except ex.AnoInvalido:
                            sg.popup(f'Data inválida. O ano deve ser igual ou posterior ao ano atual.', title='Erro')
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.', title='Erro')
                        except ex.DataIncompleta:
                            sg.popup('A data está incompleta.', title='Erro')
                    if event3 == '-LCBLIM-':
                        for key in values3.keys():
                            window3[key].update(value='')
                window3.close()

            # === INTERFACE GRÁFICA PARA ALTERACAO OU REMOCAO DO PLANO DE CONTAS === #

            # A identificação do evento é feita pelo ínicio '-APC(...)-', sigla para "A"ltera "P"lano de "C"ontas.
            # Na criação dos botões, como existem dois quadros, um para alterar e um para remover,
            # os botões que representam cada quadro têm distinções. Para o quadro alterar os botões estão com
            # o código de evento '-APCAP(...)-', sigla para "A"ltera "P"lano de "C"ontas "A"lterar "P"lano.
            # Para o quadro remover os botões estão com o código de evento '-APCRP(...)-',
            # sigla para sigla para "A"ltera "P"lano de "C"ontas "R"emover "P"lano.
            if event == '-PRINMANPL-':
                apc_colunas = ['Numero da conta a alterar', 'Numero da Conta', 'Descricao da Conta', 'Tipo Conta (S/A)',
                               'Conta Mae']
                apc_t_tam = (30, 1)
                apc_t_pad = (1, 1)
                apc_quadro_alterar_plano_contas = [
                    [sg.T(ind, size=(26, 1), pad=apc_t_pad) for ind in apc_colunas],
                    [sg.In(key='-APCSEQ-', size=apc_t_tam, pad=apc_t_pad, enable_events=True),
                     sg.In(key='-APCNUMCON-', size=apc_t_tam, pad=apc_t_pad, enable_events=True),
                     sg.In(key='-APCDESCCON-', size=apc_t_tam, pad=apc_t_pad),
                     sg.In(key='-APCTIPO-', size=apc_t_tam, pad=apc_t_pad, enable_events=True),
                     sg.In(key='-APCCMAE-', size=apc_t_tam, pad=apc_t_pad, enable_events=True)],
                ]
                apc_quadro_remover_plano_contas = [
                    [sg.T('Numero da Conta', size=(133, 1))],
                    [sg.In(key='-APCNUMER-', size=apc_t_tam, pad=apc_t_pad, enable_events=True)]
                ]
                apc_layout = [
                    [sg.Frame(title='ALTERAR PLANO DE CONTAS', layout=apc_quadro_alterar_plano_contas,
                              title_location='n')],
                    [sg.Push(), sg.B(key='-APCAPVIS-', button_text='Visualizar Plano de Contas'),
                     sg.B(key='-APCAPALT-', button_text='Alterar'),
                     sg.B(key='-APCAPLIMP-', button_text='Limpar'), sg.B(key='-APCAPCANC-', button_text='Cancelar')],

                    [sg.Frame(title='REMOVER CONTA DO PLANO DE CONTAS', layout=apc_quadro_remover_plano_contas,
                              title_location='n')],
                    [sg.Push(), sg.B(key='-APCRPREM-', button_text='Remover'),
                     sg.B(key='-APCRPLIMP-', button_text='Limpar'), sg.B(key='-APCRPCANC-', button_text='Cancelar')],
                ]
                window4 = sg.Window('Interface para Manutenção de Plano de Contas', layout=apc_layout)

                while True:
                    event4, values4 = window4.read()
                    # EVENTOS do quadro de alteração do plano de contas "apc_quadro_alterar_plano_contas" e dos botões
                    # relacionados ao quadro.
                    if event4 == sg.WIN_CLOSED or event4 == '-APCAPCANC-':
                        break
                    if event4 == '-APCSEQ-' and values4['-APCSEQ-'] and values4['-APCSEQ-'][-1] not in '0123456789.':
                        window4['-APCSEQ-'].update(value=values4['-APCSEQ-'][0:-1])
                    if event4 == '-APCNUMCON-' and values4['-APCNUMCON-'] and \
                            values4['-APCNUMCON-'][-1] not in '0123456789.':
                        window4['-APCNUMCON-'].update(value=values4['-APCNUMCON-'][0:-1])
                    if event4 == '-APCTIPO-' and values4['-APCTIPO-'] and values4['-APCTIPO-'][-1] not in 'SAsa':
                        window4['-APCTIPO-'].update(value=values4['-APCTIPO-'][0:-1])
                    if len(values4['-APCTIPO-']) > 1:
                        window4['-APCTIPO-'].update(value=values4['-APCTIPO-'][0:1])
                    if event4 == '-APCCMAE-' and values4['-APCCMAE-'] and values4['-APCCMAE-'][-1] not in '0123456789.':
                        window4['-APCCMAE-'].update(value=values4['-APCCMAE-'][0:-1])
                    if event4 == '-APCAPVIS-':
                        layout_visualizar_plano_de_contas = [
                            [sg.T('PLANO DE CONTAS', size=(85, 1), justification='center')],
                            [sg.Table(headings=[c for c in CF.plano_de_contas[0]],
                                      values=[c for c in CF.plano_de_contas[1:]],
                                      key='-APCAPVISPDC-', justification='left')],
                            [sg.B('Ok', key='-APCAPVISBOK-')]
                        ]
                        window4_1 = sg.Window(title='Plano de Contas', layout=layout_visualizar_plano_de_contas)
                        while True:
                            event4_1, values4_1 = window4_1.read()
                            if event4_1 == sg.WIN_CLOSED or event4_1 == '-APCAPVISBOK-':
                                break
                        window4_1.close()
                    if event4 == '-APCAPALT-':
                        try:
                            CF.alterar_plano_de_contas(
                                values4['-APCSEQ-'],
                                values4['-APCNUMCON-'],
                                values4['-APCDESCCON-'],
                                values4['-APCTIPO-'],
                                values4['-APCCMAE-']
                            )
                            CF.atualizar_plano_de_contas()
                            CF.atualizar_analiticas_sinteticas()
                            sg.popup('Conta atualizada com sucesso!', title='Atualização')
                            for k in values4.keys():
                                if k != '-APCNUMER-':
                                    window4[k].update(value='')
                        except ex.ContaNaoEncontrada:
                            sg.popup('Número de conta informado não foi encontrado.',
                                     title='Erro no quadro de alteração')
                        except ex.TipoContaInvalido:
                            sg.popup('Tipo de conta inválido.', title='Erro no quadro de alteração')
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Erro no quadro de alteração')
                    if event4 == '-APCAPLIMP-':
                        for k in values4.keys():
                            if k != '-APCNUMER-':
                                window4[k].update(value='')
                    # EVENTOS do quadro de remoção de conta do plano de contas "apc_quadro_remover_plano_contas" e dos
                    # botões relacionados ao quadro.
                    if event4 == '-APCRPCANC-':
                        break
                    if event4 == '-APCNUMER-' and values4['-APCNUMER-'] and values4['-APCNUMER-'][-1] not in \
                            '0123456789.':
                        window4['-APCNUMER-'].update(value=values4['-APCNUMER-'][0:-1])
                    if event4 == '-APCRPREM-':
                        try:
                            CF.remover_conta(values4['-APCNUMER-'])
                            CF.atualizar_plano_de_contas()
                            CF.atualizar_analiticas_sinteticas()
                            sg.popup('Conta removida com sucesso!', title='Remoção')
                            window4['-APCNUMER-'].update(value='')
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Erro no quadro de remoção')
                        except ex.ContaNaoEncontrada:
                            sg.popup('Número de conta informado não foi encontrado.', title='Erro no quadro de remoção')
                    if event4 == '-APCRPLIMP-':
                        window4['-APCNUMER-'].update(value='')

                window4.close()

            # === INTERFACE GRAFICA PARA ALTERACAO OU REMOCAO NO LIVRO RAZAO === #

            # A identificação de evento é feita pelo início '-ARZ(...)-', sigla para "A"ltera "R"a"Z"ao.
            # Na criação dos botões, como existem dois quadros, um para alterar e um para remover, os botões
            # que representam cada quadro têm distinções. Para o quadro alterar os botões estão com o código de
            # evento '-ARZAR(...)-', sigla para "A"ltera "R"a"Z"ão "A"lterar "R"azão.
            # Para o quadro remover os botões estão com o código de evento '-ARZRE(...)-',
            # sigla para "A"ltera "R"azão "RE"mover.
            if event == '-PRINMANRA-':
                arz_colunas = ['NUM_LINHA_ALTERAR', 'DATA_FATO', 'CONTA_DEBITO', 'DESC_CONTA_DEB', 'CONTA_CREDITO',
                               'DESC_CONTA_CRED', 'VALOR', 'DESC_DO_FATO']
                arz_t_tam = (36, 1)
                arz_quadro_alterar_razao = [
                    [sg.T('PREENCHA SOMENTE OS CAMPOS QUE DEVEM SER ALTERADOS', size=(126, 1), justification='center',
                          background_color="red")],

                    [sg.T(i, size=(32, 1)) for i in arz_colunas[0:4]],

                    [sg.In(key='-ARZLIN-', size=arz_t_tam, enable_events=True),
                     sg.In(key='-ARZDFATO-', size=arz_t_tam, enable_events=True),
                     sg.In(key='-ARZCDEB-', size=arz_t_tam, enable_events=True),
                     sg.In(key='-ARZDESCDEB-', size=arz_t_tam)],

                    [sg.T(i, size=(32, 1)) for i in arz_colunas[4:]],

                    [sg.In(key='-ARZCCRE-', size=arz_t_tam, enable_events=True),
                     sg.In(key='-ARZDESCCRE-', size=arz_t_tam),
                     sg.In(key='-ARZVAL-', size=arz_t_tam, enable_events=True),
                     sg.In(key='-ARZDESCF-', size=arz_t_tam)],
                ]
                arz_quadro_remover_razao = [
                    [sg.T('Número da linha do lançamento', size=(133, 1))],
                    [sg.In(key='-ARZRELIN-', size=arz_t_tam)],
                ]
                arz_layout = [
                    [sg.Frame(title='ALTERAR LANCAMENTO DO RAZAO', layout=arz_quadro_alterar_razao,
                              title_location='n')],
                    [sg.Push(), sg.B(key='-ARZARALT-', button_text='Alterar'),
                     sg.B(key='-ARZARLIMP-', button_text='Limpar'), sg.B(key='-ARZARCANC-', button_text='Cancelar')],
                    [sg.Frame(title='REMOVER LANÇAMENTO DO RAZAO', layout=arz_quadro_remover_razao,
                              title_location='n')],
                    [sg.Push(), sg.B(key='-ARZREREM-', button_text='Remover'),
                     sg.B(key='-ARZRELIMP-', button_text='Limpar'), sg.B(key='-ARZRECANC-', button_text='Cancelar')],
                ]
                window5 = sg.Window('Interface para Manutenção do Livro Razão', layout=arz_layout)

                while True:
                    event5, values5 = window5.read()
                    if event5 == sg.WIN_CLOSED or event5 == '-ARZARCANC-':
                        break
                    if event5 == '-ARZLIN-' and values5['-ARZLIN-'] and values5['-ARZLIN-'][-1] not in '0123456789':
                        window5['-ARZLIN-'].update(value=values5['-ARZLIN-'][0:-1])
                    if event5 == '-ARZDFATO-' and values5['-ARZDFATO-'] and \
                            values5['-ARZDFATO-'][-1] not in '0123456789/':
                        window5['-ARZDFATO-'].update(value=values5['-ARZDFATO-'][0:-1])
                    if len(values5['-ARZDFATO-']) > 10:
                        window5['-ARZDFATO-'].update(value=values5['-ARZDFATO-'][0:10])
                    if event5 == '-ARZCDEB-' and values5['-ARZCDEB-'] and values5['-ARZCDEB-'][-1] not in '0123456789.':
                        window5['-ARZCDEB-'].update(value=values5['-ARZCDEB-'][0:-1])
                    if event5 == '-ARZCCRE-' and values5['-ARZCCRE-'][0:] and \
                            values5['-ARZCCRE-'][-1] not in '.0123456789':
                        window5['-ARZCCRE-'].update(value=values5['-ARZCCRE-'][0:-1])
                    if event5 == '-ARZVAL-' and values5['-ARZVAL-'] and values5['-ARZVAL-'][-1] not in '0123456789.,':
                        window5['-ARZVAL-'].update(value=values5['-ARZVAL-'][0:-1])
                    if event5 == '-ARZARALT-':
                        try:
                            CF.alterar_razao(
                                numero_linha=values5['-ARZLIN-'],
                                data_lancamento=values5['-ARZDFATO-'],
                                conta_deb=values5['-ARZCDEB-'],
                                desc_conta_deb=values5['-ARZDESCDEB-'],
                                conta_cre=values5['-ARZCCRE-'],
                                desc_conta_cre=values5['-ARZDESCCRE-'],
                                valor=values5['-ARZVAL-'],
                                descricao_fato=values5['-ARZDESCF-']
                            )
                            CF.atualizar_livro_razao()
                            sg.popup('Lançamento alterado com sucesso!', title='Alteração no lançamento')
                            for i in values5.keys():
                                if i != '-ARZLINHA-':
                                    window5[i].update(value='')
                        except ex.ExclusaoNaoPermitida:
                            sg.popup('Os rótulos das colunas não podem ser alterados.', title='Erro')
                        except ex.CamposEmBranco:
                            sg.popup('O campo de sequência deve ser preenchido para efetuar uma alteração',
                                     title='Erro')
                        except ex.NenhumaAlteracaoDefinida:
                            sg.popup('Todos os campos passíveis de alteração estão em branco.', title='Erro')
                    if event5 == '-ARZARLIMP-':
                        for i in values5.keys():
                            if i != '-ARZLINHA-':
                                window5[i].update(value='')

                    if event5 == '-ARZRECANC-':
                        break
                    if event5 == '-ARZREREM-':
                        try:
                            CF.remover_lancamento(values5['-ARZRELIN-'])
                            CF.atualizar_livro_razao()
                            sg.popup(f"Linha {str(values5['-ARZRELIN-']).strip()} removida com sucesso!",
                                     title='Remoção do lançamento')
                            window5['-ARZRELIN-'].update(value='')
                        except ex.ExclusaoNaoPermitida:
                            sg.popup('Os rótulos das colunas não podem ser removidos.', title='Erro')
                        except ex.CamposEmBranco:
                            sg.popup('O campo de sequência deve ser preenchido para efetuar uma remoção.')
                    if event5 == '-ARZRELIMP-':
                        window5['-ARZRELIN-'].update(value='')

                window5.close()

            # === INTERFACE GRÁFICA EVENTO DE INCLUSÃO DE SALDOS INICIAIS NAS CONTAS ANALÍTICAS === #

            if event == '-PRINSALDINI-':
                si_t_tam = (12, 1)
                si_i_tam = (20, 1)
                layout_saldo_inicial = [
                    [sg.T('MES', size=si_t_tam),
                     sg.Combo(key='-SIMES-', values=[x for x in range(1, 13)], readonly=True, size=si_i_tam),
                     sg.T('ANO', size=si_t_tam),
                     sg.Combo(key='-SIANO-', values=[x for x in range(2022, 2026)], readonly=True, size=si_i_tam)],
                    [sg.T('CONTA', size=si_t_tam),
                     sg.Combo(key='-SICONTA-', values=[c for c in CF.contas_analiticas], readonly=True, size=si_i_tam)],
                    [sg.T('SALDO INICIAL', size=si_t_tam), sg.In(key='-SISALDO-', size=si_i_tam, enable_events=True)],
                    [sg.Push(), sg.B(key='-SIBVISSI-', button_text='Visualizar Saldo Inicial'),
                     sg.B(key='-SIBADIC-', button_text='Adicionar'),
                     sg.B(key='-SIBLIMP-', button_text='Limpar'), sg.B(key='-SIBCANC-', button_text='Cancelar')]
                ]
                window6 = sg.Window(title='Saldos Iniciais', layout=layout_saldo_inicial)

                while True:
                    event6, values6 = window6.read()
                    if event6 == sg.WIN_CLOSED or event6 == '-SIBCANC-':
                        break
                    if event6 == '-SISALDO-' and values6['-SISALDO-'] and values6['-SISALDO-'][-1] not in \
                            '0123456789,.':
                        window6['-SISALDO-'].update(values6['-SISALDO-'][0:-1])
                    if event6 == '-SIBVISSI-':
                        si_layout_visualizar_saldo_inicial = [
                            [sg.T('SALDOS INICIAIS DAS CONTAS')],
                            [sg.Table(headings=[c for c in CF.saldo_inicial[0][0:7]],
                                      values=[c for c in CF.saldo_inicial[1:][0:7]], justification='left')],
                            [sg.B(key='-SIVISSIBOK-', button_text='OK')],
                        ]
                        window6_1 = sg.Window(title='Tabela Saldo Inicial', layout=si_layout_visualizar_saldo_inicial,
                                              resizable=True)

                        while True:
                            event6_1, values6_1 = window6_1.read()
                            if event6_1 == sg.WIN_CLOSED or event6_1 == '-SIVISSIBOK-':
                                break
                        window6_1.close()

                    if event6 == '-SIBADIC-':
                        try:
                            CF.incluir_saldo_inicial(
                                sequencia=CF.sequencia_balancete(),
                                tipo='SALDOINICIAL',
                                mes=values6['-SIMES-'],
                                ano=values6['-SIANO-'],
                                numero_conta=values6['-SICONTA-'],
                                desc_conta=values6['-SICONTA-'],
                                saldo_inicial=values6['-SISALDO-'],
                                movto_deb=0,
                                movto_cre=0,
                                saldo_final=values6['-SISALDO-']
                            )
                            CF.atualizar_balancete()
                            sg.popup(f"Saldo inicial da conta {values6['-SICONTA-']} incluído com sucesso!",
                                     title='Inclusão de Saldo Inicial')
                            for i in values6.keys():
                                window6[i].update(value='')
                        except ex.ContaComSaldoInicial:
                            sg.popup(f"A conta {values6['-SICONTA-']} já possui um saldo inicial.",
                                     title='Erro Saldo Inicial')
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter ser preenchidos.',
                                     title='Erro Saldo Inicial')
                    if event6 == '-SIBLIMP-':
                        for i in values6.keys():
                            window6[i].update(value='')  # Falta a visualização do balancete
                window6.close()

            # === INTERFACE GRÁFICA EVENTO DE ALTERAÇÃO DO SALDO INICIAL DO BALANCETE DE VERIFICAÇÃO === #

            if event == '-PRINMANSALDINI-':
                asi_t_tam = (27, 1)
                asi_i_tam = (30, 1)
                asi_p_tam = (2, 2)

                asi_colunas = ['LINHA A ALTERAR', 'MES', 'ANO', 'CONTA', 'SALDO INICIAL']

                asi_quadro_alteracao = [
                    [sg.T(x, size=asi_t_tam, pad=asi_p_tam) for x in asi_colunas],
                    [sg.In(key='-ASILIN-', size=asi_i_tam, pad=asi_p_tam),
                     sg.Combo(key='-ASIMES-', values=[x for x in range(1, 13)], size=asi_i_tam, pad=asi_p_tam,
                              readonly=True),
                     sg.Combo(key='-ASIANO-', values=[x for x in range(2022, 2026)], size=asi_i_tam, pad=asi_p_tam,
                              readonly=True),
                     sg.Combo(key='-ASICONTA-', values=[c for c in CF.contas_analiticas], size=asi_i_tam, pad=asi_p_tam,
                              readonly=True),
                     sg.In(key='-ASISALDIN-', size=asi_i_tam, pad=asi_p_tam)]
                ]

                asi_quadro_remocao = [
                    [sg.T('REMOCAO', size=(138, 1))],
                    [sg.In(key='-ASIREMOV-', size=asi_i_tam)]
                ]

                asi_layout = [
                    [sg.Frame(title='Alterar Saldo Inicial', layout=asi_quadro_alteracao)],
                    [sg.Push(), sg.B(key='-ASIVISSI-', button_text='Visualizar Saldo Inicial'),
                     sg.B(key='-ASIALALT-', button_text='Alterar'), sg.B(key='-ASIALLIMP-', button_text='Limpar'),
                     sg.B(key='-ASIALCANC-', button_text='Cancelar')],
                    [sg.Frame(title='Remover Saldo Inicial', layout=asi_quadro_remocao)],
                    [sg.Push(), sg.B(key='-ASIREREM-', button_text='Remover'),
                     sg.B(key='-ASIRELIMP-', button_text='Limpar'),
                     sg.B(key='-ASIRECANC-', button_text='Cancelar')]
                ]

                window7 = sg.Window(title='Alterações no Saldo Inicial', layout=asi_layout)

                while True:
                    event7, values7 = window7.read()
                    # Evento de alteração do balancete
                    if event7 == sg.WIN_CLOSED or event7 == '-ASIALCANC-':
                        break
                    if event7 == '-ASIVISSI-':
                        asi_layout_visualizar_saldo_inicial = [
                            [sg.T('SALDO INCIAL DAS CONTAS')],
                            [sg.Table(headings=[c for c in CF.saldo_inicial[0][0:7]],
                                      values=[c for c in CF.saldo_inicial[1:][0:7]])],
                            [sg.B(key='-ASIVISSIBOK-', button_text='OK')]
                        ]
                        window7_1 = sg.Window(title='Tabela Saldo Inicial', layout=asi_layout_visualizar_saldo_inicial)

                        while True:
                            event7_1, values7_1 = window7_1.read()
                            if event7_1 == sg.WIN_CLOSED or event7_1 == '-ASIVISSIBOK-':
                                break
                        window7_1.close()

                    if event7 == '-ASIALALT-':
                        try:
                            CF.alterar_balancete(
                                numero_linha=values7['-ASILIN-'],
                                mes=values7['-ASIMES-'],
                                ano=values7['-ASIANO-'],
                                numero_conta=values7['-ASICONTA-'],
                                saldo_inicial=values7['-ASISALDIN-'],
                                saldo_final=values7['-ASISALDIN-'],
                            )
                            CF.atualizar_balancete()
                            sg.popup(f"Linha {values7['-ASILIN-']} alterada com sucesso!",
                                     title='Alteração Saldo Inicial')
                            for i in values7.keys():
                                if i != '-ASIREMOV-':
                                    window7[i].update(value='')
                        except ex.ExclusaoNaoPermitida:
                            sg.popup('Exclusão não permitida. Os rótulos de colunas não podem ser alterados.',
                                     title='Erro - Linha proibida')
                        except ex.CamposEmBranco:
                            sg.popup('O campo de sequência deve ser preenchido para efetuar uma alteração.',
                                     title='Erro - Linha em branco')
                    if event7 == '-ASIALLIMP-':
                        for i in values7.keys():
                            if i != '-ASIREMOV-':
                                window7[i].update(value='')
                    # EVENTO DE REMOÇÃO DO BAÇANCETE
                    if event7 == '-ASIRECANC-':
                        break
                    if event7 == '-ASIREREM-':
                        try:
                            CF.remover_saldo_inicial_balancete(values7['-ASIREMOV-'])
                            CF.atualizar_balancete()
                            sg.popup(f"Linha {values7['-ASIREMOV-']} removida com sucesso!",
                                     title='Remoção Saldo Inicial')
                            window7['-ASIREMOV-'].update(value='')
                        except ex.ExclusaoNaoPermitida:
                            sg.popup('Os rótulos das colunas não podem ser removidos.', title='Erro - Linha proibida')
                        except ex.CamposEmBranco:
                            sg.popup('O campo de sequência deve ser preenchido para efetuar uma remoção.',
                                     title='Erro - Linha em branco')
                    if event7 == '-ASIRELIMP-':
                        window7['-ASIREMOV-'].update(value='')
                window7.close()  # Falta implementar a visulização do balancete

            # INTERFACE GRÁFICA EVENTO DE GERAÇÃO DO BALANCETE DO PERÍODO
            if event == '-PRINBALAN-':

                balan_layout = [
                    [sg.T('Mes'), sg.Combo(key='-BALANMES-', values=[x for x in range(1, 13)], readonly=True),
                     sg.T('Ano'), sg.Combo(key='-BALANANO-', values=[x for x in range(2022, 2026)], readonly=True)],
                    [sg.B(key='-BALANBVIS-', button_text='Visualizar Balancete'),
                     sg.B(key='-BALANBGER-', button_text='Gerar'),
                     sg.B(key='-BALANBLIMP-', button_text='Limpar'), sg.B(key='-BALANBCANC-', button_text='Cancelar')]
                ]

                window8 = sg.Window(title='Balancete', layout=balan_layout)

                while True:
                    event8, values8 = window8.read()
                    if event8 == sg.WIN_CLOSED or event8 == '-BALANBCANC-':
                        break
                    if event8 == '-BALANBVIS-':
                        pass
                    if event8 == '-BALANBGER-':
                        try:
                            CF.gerar_balancete(
                                mes=values8['-BALANMES-'],
                                ano=values8['-BALANANO-']
                            )
                            CF.atualizar_balancete()
                            sg.popup('Balancete de Verificação atualizado com sucesso!', title='Balancete gerado')
                            for i in values8.keys():
                                window8[i].update(value='')

                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Balancete Registrado')
                        except ex.BalancetePeriodoRegistrado:
                            sg.popup('O balancete do período especificado já está registrado.',
                                     title='Balancete Registrado')
                        except ex.BalanceteFicaraVazio:
                            sg.popup('O Livro Razão não possui movimento no período especificado. '
                                     'O Balancete ficaria vazio.',
                                     title='Balancete Vazio')

                    if event8 == '-BALANBLIMP-':
                        for i in values8.keys():
                            window8[i].update(value='')
                window8.close()

            # === INTERFACE GRÁFICA EVENTO DE MANUTENCÃO DO BALANCETE DO PERÍODO (EXCLUSÃO DE DADOS) === #
            if event == '-PRINMANBA-':

                manba_layout = [
                    [sg.T('Mes'), sg.Combo(key='-MANBAMES-', values=[x for x in range(1, 13)], readonly=True),
                     sg.T('Ano'), sg.Combo(key='-MANBAANO-', values=[x for x in range(2022, 2026)], readonly=True)],
                    [sg.B(key='-MANBABEXC-', button_text='Excluir'), sg.B(key='-MANBABLIMP-', button_text='Limpar'),
                     sg.B(key='-MANBABCANC-', button_text='Cancelar')]
                ]

                window9 = sg.Window(title='Manutenção Balancete', layout=manba_layout)

                while True:

                    event9, values9 = window9.read()
                    if event9 == sg.WIN_CLOSED or event9 == '-MANBABCANC-':
                        break
                    if event9 == '-MANBABEXC-':
                        try:
                            CF.remover_balancete(
                                mes=values9['-MANBAMES-'],
                                ano=values9['-MANBAANO-']
                            )
                            CF.atualizar_balancete()
                            sg.popup('Balancete do período excluído com sucesso.', title='Exclusão Balancete')
                            for i in values9.keys():
                                window9[i].update(value='')

                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Exclusão Balancete')
                        except ex.BalancetePeriodoSemDados:
                            sg.popup('Não existe balancete para o período especificado.', title='Exclusao Balancete')

                    if event9 == '-MANBABLIMP-':
                        for i in values9.keys():
                            window9[i].update(value='')

                window9.close()

            # === INTERFACE GRÁFICA DE LANÇAMENTOS DE COMPENSAÇÃO DAS CONTAS DE RESULTADO PARA APURAÇÃO DO
            # RESULTADO DO PERÍODO. === #

            if event == '-PRINAPR-':
                apr_layout = [
                    [sg.T('Mes'), sg.Combo(key='-APRMES-', values=[x for x in range(1, 13)], readonly=True),
                     sg.T('Ano'), sg.Combo(key='-APRANO-', values=[x for x in range(2022, 2026)], readonly=True)],
                    [sg.B(key='-APRBGER-', button_text='Gerar'), sg.B(key='-APRBLIMP-', button_text='Limpar'),
                     sg.B(key='-APRBCANC-', button_text='Cancelar')]
                ]

                window10 = sg.Window(title='Apuração do Resultado do Exercício', layout=apr_layout)

                while True:
                    event10, values10 = window10.read()

                    if event10 == sg.WIN_CLOSED or event10 == '-APRBCANC-':
                        break

                    if event10 == '-APRBGER-':
                        try:
                            CF.apuracao_do_resultado_lancamentos(
                                mes=values10['-APRMES-'],
                                ano=values10['-APRANO-']
                            )
                            sg.popup('Lançamentos de apuração do resultado efetuados.', title='Apuração do Resultado')
                            for i in values10.keys():
                                window10[i].update(value='')
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter ser preenchidos.',
                                     title='Apuração do Resultado')
                        except ex.BalancetePeriodoSemDados:
                            sg.popup('Ainda não existem dados no balancete para o período especificado.',
                                     title='Apuração do Resultado')
                        except ex.LancamentosApuracaoDoResultadoExistentes:
                            sg.popup('Já existem lançamentos de compensação das contas de resultado para o período.'
                                     ' Exclua o período anterior para continuar.', title='Apuração do Resultado')
                        #### except Verificar se no balancete o período não estamos tentando compensar contas de resultado
                        # de um mês anterior ao último compensado.
                        # a exclusão não tem verificacao

                    if event10 == '-APRBLIMP-':
                        for i in values10.keys():
                            window10[i].update(value='')

                window10.close()

            # INTERFACE GRÁFICA DE REMOCAÇÃO DE LANÇAMENTOS DE COMPENSAÇÃO DAS CONTAS DE RESULTADO === #.

            if event == '-PRINMANAPR-':
                man_apr_layout = [
                    [sg.T('Mes'), sg.Combo(key='-MANAPRMES-', values=[x for x in range(1, 13)], readonly=True),
                     sg.T('Ano'), sg.Combo(key='-MANAPRANO-', values=[x for x in range(2022, 2026)], readonly=True)],
                    [sg.B(key='-MANAPRBEXCL-', button_text='Excluir'), sg.B(key='-MANAPRBLIMP-', button_text='Limpar'),
                     sg.B(key='-MANAPRBCANC-', button_text='Cancelar')]
                ]

                window11 = sg.Window(title='Manutenção Apuração do Resultado', layout=man_apr_layout)

                while True:
                    event11, values11 = window11.read()

                    if event11 == sg.WIN_CLOSED or event11 == '-MANAPRBCANC-':
                        break

                    if event11 == '-MANAPRBEXCL-':
                        try:
                            CF.apuracao_do_resultado_lancamentos_exclusao(
                                mes=values11['-MANAPRMES-'],
                                ano=values11['-MANAPRANO-']
                            )
                            sg.popup('Lançamentos de apuração do resultado excluídos.',
                                     title='Exclusão Apuração do Resultado')
                            for i in values11.keys():
                                window11[i].update(value='')
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter ser preenchidos.',
                                     title='Manutenção Apuração do Resultado')
                        except ex.LancamentosApuracaoDoResultadoInexistentes:
                            sg.popup('Não existem lançamentos de compensação das contas de resultado no período '
                                     'especificado para excluir.', title='Manutenção Apuração do Resultado')

                    if event11 == '-MANAPRBLIMP-':
                        for i in values11.keys():
                            window11[i].update(value='')

                window11.close()

            # === INTERFACE GRAFICA PARA GERAR O BALANCO PATRIMONIAL DE UM DETERMINADO PERIODO === #

            if event == '-PRINBP-':

                bp_layout = [
                    [sg.T('Mes'), sg.Combo(key='-BPMES-', values=[x for x in range(1, 13)], readonly=True),
                     sg.T('Ano'), sg.Combo(key='-BPANO-', values=[x for x in range(2022, 2026)], readonly=True)],
                    [sg.B(key='-BPBSI-', button_text='Incluir Saldo Inicial'),
                     sg.B(key='-BPBGER-', button_text='Gerar'), sg.B(key='-BPBLIMP-', button_text='Limpar'),
                     sg.B(key='-BPBCANC-', button_text='Cancelar')],
                    [sg.B(key='-BPBVISBP-', button_text='Visualizar Balanço Patrimonial')]
                ]

                window12 = sg.Window(title='Gerar Balanço Patrimonial', layout=bp_layout)

                while True:
                    event12, values12 = window12.read()

                    if event12 == sg.WIN_CLOSED or event12 == '-BPBCANC-':
                        break

                    if event12 == '-BPBSI-':
                        try:
                            CF.gerar_saldo_inicial_balanco_patrimonial(
                                mes=values12['-BPMES-'],
                                ano=values12['-BPANO-']
                            )
                            CF.incluir_balanco_patrimonial()
                            CF.organizar_balanco_patrimonial()
                            CF.atualizar_balanco_patrimonial()
                            sg.popup('Saldo inicial incluído no Balanço Patrimonial.',
                                     title='Balanço Patrimonial Saldo Inicial')
                            for i in values12.keys():
                                window12[i].update(value='')
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Balanço Patrimonial Saldo Inicial')
                        except ex.SaldoInicialExistenteNoBalancoPatrimonial:
                            sg.popup('Já existe Saldo Inicial no Balanço Patrimonial para o período.',
                                     title='Balanço Patrimonial Saldo Inicial')
                        except ex.BalanceteSemSaldoInicial:
                            sg.popup('Não existe Saldo Inicial no balancete para o período especificado.',
                                     title='Balanço Patrimonial Saldo Inicial')

                    if event12 == '-BPBGER-':
                        try:
                            CF.gerar_balanco_patrimonial(
                                mes=values12['-BPMES-'],
                                ano=values12['-BPANO-']
                            )
                            CF.incluir_balanco_patrimonial()
                            CF.organizar_balanco_patrimonial()
                            CF.atualizar_balanco_patrimonial()
                            sg.popup('Balanço Patrimonial gerado com sucesso!', title='Balanço Patrimonial')
                            for i in values12.keys():
                                window12[i].update(value='')
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Balanço Patrimonial')
                        except ex.BalancetePeriodoSemDados:
                            sg.popup('Ainda não existem dados no balancete para o período especificado.',
                                     title='Balanço Patrimonial')
                        except ex.LancamentosApuracaoDoResultadoInexistentes:
                            sg.popup('O Balanço Patrimonial não pode ser gerado sem a Apuração do Resultado do '
                                     'período especificado.',
                                     title='Balanço Patrimonial')
                        except ex.BalancoPatrimonialExistente:
                            sg.popup('Já existe um Balanco Patrimonial para o período especificado.',
                                     title='Balanço Patrimonial')

                    if event12 == '-BPBLIMP-':
                        for i in values12.keys():
                            window12[i].update(value='')

                    # === SUB-INTERFACE GRAFICA PARA VISUALIZAR O BALANCO PATRIMONIAL DE UM DETERMINADO PERIODO === #

                    if event12 == '-BPBVISBP-':  # limitar a visualização para o período especificado
                        bp_layout_visualizar_balanco_patrimonial = [
                            [sg.T('Balanço Patrimonial')],
                            [sg.Table(key='-BPVISBPBP-', headings=[x for x in CF.balanco_patrimonial[0]],
                                      values=[x for x in CF.balanco_patrimonial[1:]])],
                            [sg.B(key='-BPVISBPBOK-', button_text='Ok')]
                        ]

                        window12_1 = sg.Window(title='Balanço Patrimonial',
                                               layout=bp_layout_visualizar_balanco_patrimonial)

                        while True:
                            event12_1, values12_1 = window12_1.read()

                            if event12_1 == sg.WIN_CLOSED or event12_1 == '-BPVISBPBOK-':
                                break

                        window12_1.close()

                window12.close()

            # === INTERFACE GRAFICA PARA MANUTENCAO DO BALANCO PATRIMONIAL (EXCLUSAO DE DADOS) === #

            if event == '-PRINMBP-':

                man_bp_layout = [
                    [sg.T('Mes'), sg.Combo(key='-MANBPMES-', values=[x for x in range(1, 13)], readonly=True),
                     sg.T('Ano'), sg.Combo(key='-MANBPANO-', values=[x for x in range(2022, 2026)], readonly=True)],
                    [sg.B(key='-MANBPBEXCL-', button_text='Excluir'), sg.B(key='-MANBPBLIMP-', button_text='Limpar'),
                     sg.B(key='-MANBPBCANC-', button_text='Cancelar')]
                ]

                window13 = sg.Window(title='Manutenção Balanço Patrimonial', layout=man_bp_layout)

                while True:
                    event13, values13 = window13.read()

                    if event13 == sg.WIN_CLOSED or event13 == '-MANBPBCANC-':
                        break

                    if event13 == '-MANBPBEXCL-':
                        try:
                            CF.excluir_balanco_patrimonial_periodo(
                                mes=values13['-MANBPMES-'],
                                ano=values13['-MANBPANO-']
                            )
                            CF.atualizar_balanco_patrimonial()
                            sg.popup(
                                f"Balanco Patrimonial de {values13['-MANBPMES-']} {values13['-MANBPANO-']} excluído.",
                                title='Excluir Balanco Patrimonial')
                            for i in values13.keys():
                                window13[i].update(value='')
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Excluir Balanço Patrimonial')
                        except ex.BalancoPatrimonialInexistente:
                            sg.popup('Não existe Balanço Patrimonial no período especificado para ser excluído',
                                     title='Excluir Balanço Patrimonial')

                    if event13 == '-MANBPBLIMP-':
                        for i in values13.keys():
                            window13[i].update(value='')

                window13.close()

            # === INTERFACE GRAFICA PARA PLOTAR GRAFICO DE RESULTADO DO EXERCÍCIO === #

            if event == '-PRINGDRE-':

                gdre_layout = [
                    [sg.T('De: '), sg.T('Mes'),
                     sg.Combo(values=[x for x in range(1, 13)], key='-GDREDEMES-', readonly=True),
                     sg.T('Ano'), sg.Combo(values=[x for x in range(2022, 2026)], key='-GDREDEANO-', readonly=True)],
                    [sg.T('Até:'), sg.T('Mes'),
                     sg.Combo(values=[x for x in range(1, 13)], key='-GDREATEMES-', readonly=True),
                     sg.T('Ano'), sg.Combo(values=[x for x in range(2022, 2026)], key='-GDREATEANO-', readonly=True)],
                    [sg.Push(), sg.B(key='-GDREBBAR-', button_text='Barras'),
                     sg.B(key='-GDREBPIZ-', button_text='Pizza'), sg.B(key='-GDREBLIMP-', button_text='Limpar'),
                     sg.B(key='-GDREBCANC-', button_text='Cancelar')]
                ]

                window14 = sg.Window(title='Grafico Demonstração do Resultado', layout=gdre_layout)

                while True:
                    event14, values14 = window14.read()

                    if event14 == sg.WIN_CLOSED or event14 == '-GDREBCANC-':
                        break

                    if event14 == '-GDREBBAR-':
                        try:
                            graficos.demonstracao_do_resultado_barras(
                                de_mes=values14['-GDREDEMES-'],
                                de_ano=values14['-GDREDEANO-'],
                                ate_mes=values14['-GDREATEMES-'],
                                ate_ano=values14['-GDREATEANO-']
                            )
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Graficos DRE')
                        except ex.DataPosteriorMenor:
                            sg.popup('A data posterior (Até) é menor que a data de partida (De).',
                                     title='Graficos DRE')
                        except ex.PontoDePartidaInexistente:
                            sg.popup('Não existem dados para o ponto de partida inicial.', title='Graficos DRE')

                    if event14 == '-GDREBPIZ-':
                        try:
                            graficos.demonstracao_do_resultado_pizza(
                                de_mes=values14['-GDREDEMES-'],
                                de_ano=values14['-GDREDEANO-'],
                                ate_mes=values14['-GDREATEMES-'],
                                ate_ano=values14['-GDREATEANO-']
                            )
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Graficos DRE')
                        except ex.DataPosteriorMenor:
                            sg.popup('A data posterior (Até) é menor que a data de partida (De).',
                                     title='Graficos DRE')
                        except ex.PontoDePartidaInexistente:
                            sg.popup('Não existem dados para o ponto de partida inicial.', title='Graficos DRE')

                    if event14 == '-GDREBLIMP-':
                        for i in values.keys():
                            window14[i].update(value='')

                    window14.close()

            # === INTERFACE GRAFICA PARA PLOTAR GRAFICO DE VARIAÇÃO PATRIMONIAL === #

            if event == '-PRINGBP-':

                gbp_layout = [
                    [sg.T('De: '), sg.T('Mes'),
                     sg.Combo(values=[x for x in range(1, 13)], key='-GBPDEMES-', readonly=True),
                     sg.T('Ano'), sg.Combo(values=[x for x in range(2022, 2026)], key='-GBPDEANO-', readonly=True)],
                    [sg.T('Até:'), sg.T('Mes'),
                     sg.Combo(values=[x for x in range(1, 13)], key='-GBPATEMES-', readonly=True),
                     sg.T('Ano'), sg.Combo(values=[x for x in range(2022, 2026)], key='-GBPATEANO-', readonly=True)],
                    [sg.Push(), sg.B(key='-GBPBLIN-', button_text='Linha'),
                     sg.B(key='-GBPBLIMP-', button_text='Limpar'),
                     sg.B(key='-GBPBCANC-', button_text='Cancelar')]
                ]

                window15 = sg.Window(title='Gráfico Balanço Patrimonial', layout=gbp_layout)

                while True:
                    event15, values15 = window15.read()

                    if event15 == sg.WIN_CLOSED or event15 == '-GBPBCANC-':
                        break

                    if event15 == '-GBPBLIN-':
                        try:
                            graficos.balanco_patrimonial_linha(
                                de_mes=values15['-GBPDEMES-'],
                                de_ano=values15['-GBPDEANO-'],
                                ate_mes=values15['-GBPATEMES-'],
                                ate_ano=values15['-GBPATEANO-']
                            )
                            # Apagar dados das linhas?
                        except ex.CamposEmBranco:
                            sg.popup('Existem campos em branco que deveriam ter sido preenchidos.',
                                     title='Grafico Balanço Patrimonial')
                        except ex.DataPosteriorMenor:
                            sg.popup('A data posterior (Até) é menor que a data de partida (De).',
                                     title='Grafico Balanço Patrimonial')
                        except ex.PontoDePartidaInexistente:
                            sg.popup('Não existem dados para o ponto de partida inicial.',
                                     title='Grafico Balanço Patrimonial')

                    if event15 == '-GBPBLIMP-':
                        for i in values15.keys():
                            window15[i].update(value='')

                window15.close()

                # FEITO - importante - agrupar os valores no balanço patrimonial para as contas sinteticas
                # FEITO - falta colocar o saldo inicial no balanço patrimonial
                # FEITO - Falta colocar as excessões do saldo inicial
                # FEITO- falta fazer a função de manutenção do balanço patrimonial
                # FEITO - Organizar o balanço patrimonial, porque os dados são anexados, não sobrepostos
                # PENDENTE - Botões de visualizar tem que visualizar de acordo com o período
                # FEITO - Falta colocar excessões na manutenção do Balanco Patrimonial
                # FEITO - controle_financeiro entender a linha 594 e 494
                # FEITO - O balanço patrimonial tá gerando mais de um período
                # FEITO - Tem que arrumar os códigos dos eventos, alguns estão sem o -EVENTO-
                # FEITO - Criar excessões do grafico de barras da DRE (Sem dados para o periodo)
                # FEITO - Criar excessões do grafico de pizza da DRE
                # FEITO - Desenvolver gráfico de linhas para o balanço patrimonial
                # PENDENTE - Testar excessoes grafi ode linha bp
                # FEITO - Rotulo de dados não aparece no grafico de linha bp com só um mes de periodo
        window.close()  # tem que pensar em como fazer o balancete, é bom saBER USAR o pandas, sqlite3 no futuro
