<h1>Projeto de Controle Financeiro</h1>

<h2>Em andamento...</h2>

- [x] Noções gerais
- [x] Guia de uso

<h2>O que me motivou</h2>

<p>Durante algum tempo, eu fiz uso de planilhas para efetuar o 
controle pessoal mensal de entradas e saídas monetárias,
implementando novas formas de processamento de acordo com a evolução
dos meus conhecimentos utilizando ferramentas como o Microsoft Excel. 
No entanto, comecei a enfrentar problemas de manutenção, consolidação
e encerramento de períodos ao manusear a ferramenta, me gerando
um certo incômodo ao realizar a tarefa.</p>

<h2>Descrição do projeto</h2>

<p>O projeto consiste em um conjunto de interfaces gráficas
com diferentes funcionalidades, baseadas na forma contábil de 
contabilização das movimentações monetárias e finalização dos períodos.
 Ele conta com funcionalidades como a inserção e manutenção 
de contas contábeis, a inserção e manutenção de lançamentos
contábeis e seus saldos iniciais, a consolidação do balancete 
de verificação, a apuração do resultado do exercício e a 
formação do balanço patrimonial. Além disso, também é possível visualizar
as informaões por meio de gráficos.</p>

<h2>Tecnologias utilizadas</h2>

<ul>
    <li>Python</li>
    <li>Pandas</li>
    <li>PySimpleGUI</li>
    <li>Matplotlib</li>
    <li>Pyinstaller</li>
    <li>CSV</li>
</ul>

<h2>Noções gerais</h2>

<h2>Instruções de download</h2>

<p>Para utilizar o programa, faça o download do arquivo zip chamado 
"dist.zip", na lista de arquivos deste repositório e extraia ele
em algum local no seu computador que você utiliza para armazenamento 
de informações. Após a extração, uma pasta chamada "dist" será gerada, 
clique nela, clique na pasta chamada "Controle Financeiro", procure
o arquivo executável chamado "Controle Financeiro" e envie um atalho
dele para a sua área de trabalho</p>

<img src="Imagens guia de uso/1 - atalho executavel - 1.png" >

<h2>Guia de uso</h2>
<ul>
<li><a href="#Inclusao-de-contas"> Inclusão de contas</a></li>
<li><a href="#Manutencao-de-contas"> Manutenção de contas</a></li>
    <ul>
        <li><a href="#Alteracao-de-contas"> 
             Alteração de contas no plano de contas</a></li>
        <li><a href="#Exclusao-de-contas"> 
             Exclusão de contas no plano de contas</a></li>
    </ul>
<li><a href="#Inclusao-de-si-contas"> Inclusão de saldo inicial das contas</a></li>
<li><a href="#Manutencao-si"> Manutenção do saldo inicial das contas </a></li>
    <ul>
        <li><a href="#Alteracao-si-de-contas"> 
             Alteração do saldo inicial das contas</a></li>
        <li><a href="#Exclusao-si-de-contas"> 
             Exclusao de conta com saldo inicial</a></li>
    </ul>
<li><a href="#Lancamentos"> Lançamentos</a></li>
<li><a href="#manutencao-lancamentos"> Manutenção dos lançamentos</a></li>
<li>Geração do balancete de verificação</li>
<li>Manutenção do balancete de verificação</li>
<li>Apuração do resultado do exercício</li>
<li>Manutenção da apuração do resultado do exercício</li>
<li>Geração do balanço patrimonial</li>
<li>Manutenção do balanço patrimonial</li>
<li>Graficos da demonstração do resultado</li>
<li>Grafico do balanço patrimonial</li>
</ul>


<h3 id="Inclusao-de-contas"> Inclusão de contas</h3>

<p>Inicialmente, o plano de contas já vem com algumas contas cadastradas
para facilitar o processo de inclusão, mas é possível efetuar a inclusão, 
alteração e exclusão de contas. Para fins de instrução, será explicado
como executar o processo.</p>

<ol>
    <li>Abra o programa que você enviou para sua área de trabalho.</li>
    <br>
    <img src="Imagens guia de uso/2 - inclusao de contas - 1.png">
    <br>
    <br>
    <li>Clique no botão "Incluir Conta".</li>
    <br>
    <img src="Imagens guia de uso/2 - inclusao de contas - 2.png">
    <br>
    <br>
    <li>Se você clicar no botão "Visualizar Plano de Contas", poderá
    ver as contas que já estão criadas e se basear nelas para a próxima
    inclusão. Iremos criar uma conta Analítica chamada de Conta teste
    como exemplo.</li>
    <br>
    <img src="Imagens guia de uso/2 - inclusao de contas - 3.png">
    <br>
    <br>
    <li>No campo número da conta, digite o número da conta que você 
    quer incluir. O número deve ser único, o sistema barrará as duplicidades.</li>
    <br>
    <li>No campo Descrição da conta, digite o nome da conta que você
    está criando.</li>
    <br>
    <li>No Tipo de conta (A / S), selecione o tipo Analítica para contas que 
    receberão movimentos e o tipo Sintética para contas que receberão
    somente os saldos</li>
    <br>
    <li>No campo Conta Mãe, selecione a conta Sintética que receberá
    os movimentos da conta que você está criando.</li>
    <br>
    <img src="Imagens guia de uso/2 - inclusao de contas - 4.png">
    <br>
    <br>
    <li>Por fim, clique no botão "Criar" para efetuar a inclusão. A 
    nova conta foi incluída no Plano de Contas.</li>
    <br>
    <img src="Imagens guia de uso/2 - inclusao de contas - 5.png">
</ol>

<h3 id="Manutencao-de-contas"> Manutenção de contas</h3>

<p>A tela para manutenção do plano de contas permite alterar alguns
campos do plano de contas baseando-se no número da conta. Além disso,
também é possível efetuar a exclusão de uma conta utilizando o 
número da conta como base.</p>

<h4 id="Alteracao-de-contas"> Alteração de conta no plano de contas</h4>

<ol>
    <li>Clique na tela do plano de contas no menu de telas.</li>
    <br>
    <li>Visualize a conta que deseja alterar no plano de contas
    clicando no botão "Visualizar Plano de Contas".</li>
    <br>
    <img src="Imagens guia de uso/3 - manutencao de contas - 1.png">
    <br>
    <br>
    <li>Vamos alterar a conta que criamos anteriormente como teste, 
    alterando o campo de número da conta e de descrição da conta.
    Para isso, basta colocar o número da conta no campo de "Número
    da conta a alterar" e preencher somente os campos que você
    deseja alterar. Os campos em branco não serão alterados.</li>
    <br>
    <img src="Imagens guia de uso/3 - manutencao de contas - 2.png">
    <br>
    <br>
    <li>Clique no botão "Ok" da pop-up de confirmação.</li>
    <br>
    <img src="Imagens guia de uso/3 - manutencao de contas - 3.png">
    <br>
    <br>
    <li>Clique no botão de "Visualizar Plano de Contas" novamente, 
    busque pelo novo número de conta que você passou ou pelo antigo
    número, caso não tenha alterado o número e verifique as 
    modificações. Como é possível perceber, o número e a descrição foram
    alterados.</li>
    <br>
    <img src="Imagens guia de uso/3 - manutencao de contas - 4.png">
    <br>
    <p>Observe. Caso queira fazer algum tipo de alteração na conta
    que não seja o campo de "Descricao da Conta", é mais aconselhável
    que seja efetuada a exclusão da conta que você criou.</p>
</ol>

<h4 id="Exclusao-de-contas"> Exclusão de conta no plano de contas</h4>

<ol>
    <li>Clique na tela do plano de contas no menu de telas.</li>
    <br>
    <li>Visualize as contas para identificar o número da conta que 
        deverá ser excluída.</li>
    <li>Informe o número da conta que você deseja excluir e 
        clique no botão de "Remover". Aqui, vamos excluir
        a conta 5.1.7 que alteramos para 5.1.8 e acabou ficando
        fora da ordem padrão.</li>
    <br>
    <img src="Imagens guia de uso/3 - manutencao de contas - 5.png">
    <br>
    <br>
    <li>Clique no botão de "Ok" na pop-up de confirmação.</li>
    <br>
    <img src="Imagens guia de uso/3 - manutencao de contas - 6.png">
    <br>
    <br>
    <li>Após visualizar novamente o plano de contas, é possível constatar
        que a conta que informamos foi excluída.</li>
    <br>
    <img src="Imagens guia de uso/3 - manutencao de contas - 7.png">
</ol>

<h3 id="Inclusao-de-si-contas"> Inclusão de saldo inicial das contas </h3>

<ol>
    <li>Clique no botão de "Saldo inicial" no menu de telas.</li>
    <br>
    <li>Irá abrir a tela de inclusão de saldo inicial para as contas.</li>
    <p>As contas disponíveis para receber um valor de saldo inicial
    são somente as contas do tipo analítica, as contas do tipo sintética
    apenas agregam valores das contas analíticas filhas dentro do seu escopo.</p>
    <li>Selecione o mês e o ano para consideração, o ideal é que você considere
    como dados para saldo inicial o período anterior ao que você utilizará 
    para início do controle. Para o exemplo, utilizarei as contas 
    Banco Inter e Banco Itau.</li>
    <br>
    <img src="Imagens guia de uso/4 - inclusao saldo inicial - 1.png">
    <br>
    <br>
    <img src="Imagens guia de uso/4 - inclusao saldo inicial - 2.png">
    <br>
    <br>
    <li>Ao clicar no botão de "Visualizar Saldo Inicial", é possível
    verificar as adições feitas no saldo inicial das contas que selecionamos.</li>
    <br>
    <img src="Imagens guia de uso/4 - inclusao saldo inicial - 3.png">
</ol>

<h3 id="Manutencao-si"> Manutenção do saldo inicial das contas </h3>

<p>A tela de manutenção do saldo inicial também é dividida entre alterações
nos campos incluídos de saldo inicial e na exclusão total da informação
de uma conta com saldo inicial. Trataremos sobre as duas funções.</p>

<h4 id="Alteracao-si-de-contas"> Alteração do saldo inicial das contas</h4>

<ol>
    <li>Abra a tela "Manutenção Saldos Iniciais".</li>
    <br>
    <li>Clique no botão de "Visualizar Saldo Inicial" para visualizar
    as contas que possuem saldo inicial e a linha que representa
    o dado que você quer alterar.</li>
    <br>
    <img src="Imagens guia de uso/4 - inclusao saldo inicial - 3.png">
    <br>
    <br>
    <li>Para efetuar uma atualização de dados nos campos, utilizamos a
    parte da tela de manutenção de saldo iniciais dentro do quadro de 
    "Alterar Saldo Inicial"</li>
    <br>
    <img src="Imagens guia de uso/5 - manutencao saldo inicial - 1.png">
    <br>
    <br>
    <li>Para alterarmos o saldo da conta "BANCO INTER", basta
    selecionar o número da linha que a informação se encontra e preencher
    o campo de "SALDO INICIAL" com o novo valor.</li>
    <br>
    <img src="Imagens guia de uso/5 - manutencao saldo inicial - 2.png">
    <br>
    <br>
    <img src="Imagens guia de uso/5 - manutencao saldo inicial - 3.png">
    <br>
    <p>As alterações só ocorrem com o preenchimento de um ou mais campos 
    que queremos alterar. Deixar qualquer campo passível de preenchimento 
    sem preenchimento, não efetua nenhuma alteração.</p>
    <li>É possível efetuar a alteração de mais de um campo ao mesmo tempo.
    Vamos fazer a alteração de todos os campos possíveis na linha 2.</li>
    <br>
    <img src="Imagens guia de uso/5 - manutencao saldo inicial - 4.png">
    <br>
    <img src="Imagens guia de uso/5 - manutencao saldo inicial - 5.png">
</ol>

<h4 id="Exclusao-si-de-contas"> Exclusão de conta com saldo inicial</h4>

<p>Ainda na tela de "Manutenção Saldos Iniciais", também podemos
   efetuar a exclusão de um registo utilizando o número da linha
   que está localizado o dado.</p>

<ol>
    <li>Clique no botão de "Visualizar Saldo Inicial" para
    identificar corretamente o número da linha que você deseja
    excluir.</li>
    <br>
    <li>Para efetuar uma exclusão de registro, utilizamos a parte
    da tela dentro do quadro "Remover Saldo Inicial".</li>
    <br>
    <img src="Imagens guia de uso/5 - manutencao saldo inicial - 6.png">
    <br>
    <br>
    <li>Agora, preenchemos o campo "REMOCAO" com o número do registro
    que queremos excluir.</li>
    <br>
    <img src="Imagens guia de uso/5 - manutencao saldo inicial - 7.png">
    <br>
    <br>
    <li>Visualize os dados para ter certeza da exclusão.</li>
    <br>
    <img src="Imagens guia de uso/5 - manutencao saldo inicial - 8.png">
</ol>

<h3 id="Lancamentos"> Lançamentos</h3>

<p>Os lançamentos</p>

<ol>
    <li>Abra a tela chamada "Lançamentos"</li>
    <br>
    <img src="Imagens guia de uso/6 - lancamentos - 1.png">
    <br>
    <br>
    <li>Selecione a conta que deve receber um valor a débito, a conta
    que deve receber um valor a crédito, o valor da operação, 
    a data que ocorreu a operação e informe uma descrição do ocorrido
    para manter o histórico.</li>
    <p>Como exemplo, iremos supor que alguém tenha ido ao cabeleireiro, 
    cortado o cabelo e tenha pago o serviço utilizando o débito 
    automático do cartão do banco (débito em conta). O lançamento
    seria como a seguir:</p>
    <br>
    <img src="Imagens guia de uso/6 - lancamentos - 2.png">
    <br>
    <br>
    <li>Clique em lançar para efetuar o lançamento, gerando uma mensagem
    na tela de lançamento efetuado com o lançamento feito.</li>
    <br>
    <img src="Imagens guia de uso/6 - lancamentos - 3.png">
    <br>
    <br>
    <li>É possível visualizar o lançamento efetuado
    preenchendo os campos para visualização de lançamentos. Preencha
    o mês e o ano de partida e o mês e o ano de limite para visualizar
    os lançamentos dentro deste perído, por último, clique no botão
    "Visualizar Lançamentos".</li>
    <br>
    <img src="Imagens guia de uso/6 - lancamentos - 4.png">
</ol>

<h3 id="manutencao-lancamentos"> Manutenção dos Lançamentos</h3>



















