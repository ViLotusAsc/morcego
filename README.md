# Jogo Multiplayer com Pygame e Discord

## Descrição

Este projeto consiste em um jogo multiplayer estilo roleta russa, desenvolvido com Pygame e integrado ao Discord. Os jogadores podem interagir com o jogo tanto pela interface gráfica (UI) criada com Pygame quanto por comandos no Discord.

## Estrutura Técnica

- Tela Pygame:

Criada utilizando a biblioteca Pygame para a interface gráfica.
Conectada a um arquivo JSON para armazenamento e atualização de dados do jogo.
Alimentada constantemente por informações do jogo e do Discord.
- Threads:

O código executa duas threads simultaneamente:


Thread do jogo: responsável pela execução da lógica do jogo e atualização da tela Pygame.

Thread do bot Discord: responsável pela interação com o Discord, leitura de comandos e envio de atualizações.


- Interação com Discord:

Utiliza a API do Discord para comunicação entre o jogo e o Discord.
Cada comando enviado no Discord é lido pela API e interpretado pelo código.
A interpretação gera uma nova versão do arquivo JSON, uma resposta visual no Discord e o envio do arquivo JSON atualizado para um chat previamente designado.
## Jogabilidade

- Mecânica básica:

Simula uma roleta russa com balas aleatórias que podem ser falsas ou verdadeiras.
Os jogadores alternam turnos, escolhendo se desejam atirar ou utilizar itens.
- Itens:

Lupa: permite ao jogador ver a natureza da bala (falsa ou verdadeira).

Faca: causa o dobro de dano no próximo disparo.

Caixa: recupera uma vida.

Lata: retira a bala atual da jogada.


Os itens são utilizados através do comando "dUse item" no Discord, seguido do nome do item.
A utilização de um item modifica o arquivo JSON e envia a nova versão para o Discord, sincronizando a informação com o outro jogador.
## Instruções para uso

# Variáveis de Comando 

Primeiramente, cada jogador deve definir qual será sua variável que permitirá que utilize os comandos do bot. Para fazer isso ele deverá enviar o seguinte comando na caixa de mensagens privadas do bot 

- comname X
Onde X é a letra que ele escolhe para colocar antes de cada comando. Este valor é armazenado no arquivo JSON e referido no código como
```data_life["player1]["command_set]```
É interessantre que um dos players instancie a string "d" como sua variável por questões de jogabilidade dentro do código, no qual atribui um nome específico para esta variável.

# Channel Set
Antes de jogar também, é fundamental que o próximo comando a ser feito por cada jogador seja o: 
- 
 

## Dependências (adicionar aqui)
