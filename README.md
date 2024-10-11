# 8-Puzzle

## Inteligência Artificial

Atividade proposta pelo professor **Leonardo Machado**, na disciplina de Inteligência Artificial.

## Descrição da Atividade

O objetivo desta atividade é implementar duas versões de uma função para o quebra-cabeça de 8: uma que copia e edita a estrutura de dados do nó pai e outra que modifica o estado pai diretamente (desfazendo as alterações conforme necessário). Também foram escritas versões de busca em profundidade de aprofundamento iterativo que utilizam essas funções, permitindo a comparação de desempenho entre as abordagens.

Link da Atividade (Questão 20): [AIMA Code - Exercícios de Busca](https://aimacode.github.io/aima-exercises/search-exercises/)

## Sobre o Jogo

O **8-Puzzle** é um jogo de tabuleiro em que o objetivo é mover as peças numeradas de 1 a 8 dentro de uma grade 3x3, com um espaço vazio representado pelo número `0`. O objetivo final é organizar as peças na seguinte configuração:


```
   [1,2,3]
   [4,5,6]
   [7,8,0]
```

### 8-Puzzle - Implementação

Este projeto implementa a solução do quebra-cabeça de 8 utilizando duas abordagens diferentes para manipulação de estados:

- **Cópia do Estado:** Esta abordagem utiliza a classe `NodeCopy`, que mantém a integridade dos estados visitados. Cada novo estado é uma cópia do estado anterior, garantindo que cada nó na árvore de busca seja independente. Embora essa abordagem consuma mais memória, evita interferências entre diferentes caminhos na busca.

- **Modificação Direta do Estado:** Utilizando a classe `NodeDirectModify`, esta abordagem altera o estado do nó atual em vez de criar cópias. Essa técnica pode economizar memória e potencialmente aumentar a velocidade, mas requer cuidados adicionais para garantir que estados anteriores não sejam alterados de forma indesejada.

### 8-Puzzle - Comparação

- **Cópia do Estado:** Por criar novas cópias a cada movimento, esta abordagem não corre o risco de alterar estados anteriores, garantindo acesso a todos os estados já explorados. No entanto, a criação de cópias pode aumentar o tempo de execução e o uso de memória, especialmente em soluções mais longas.

- **Modificação Direta do Estado:** Alterar o estado atual tende a ser mais rápido do que criar novas cópias, o que pode resultar em uma resolução mais rápida do quebra-cabeça. Contudo, a alteração direta dos estados pode levar a revisitas indesejadas a estados já explorados, tornando a busca menos eficiente.

- **Casos Sem Solução:** Para estados em que o quebra-cabeça não possui solução, ambos os métodos podem terminar rapidamente, resultando em tempos de execução próximos de zero, já que a verificação de solução é feita antes da busca profunda.

- **Casos Com Solução:** A versão que faz cópias pode levar mais tempo devido à sobrecarga de criar novos nós, mas oferece maior confiabilidade ao evitar revisitas a estados. Por outro lado, a versão que modifica diretamente pode ser mais rápida, mas corre o risco de se perder em caminhos já explorados.
