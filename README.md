<h1>Projeto de Controle Financeiro</h1>



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
<li>Inclusão de saldo inicial das contas</li>
<li>Manutenção do saldo inicial das contas</li>
<li>Lançamentos</li>
<li>Manutenção dos lançamentos</li>
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

























