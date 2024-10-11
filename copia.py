import numpy as np
import random
import time

# esse aqui está pronto
# Esta classe representa um nó no quebra-cabeça que copia o estado do tabuleiro.

class NodeCopy: # aqui o nó do Copia
    def __init__(self, state): # aqui ele vai inicializar o nó com Estado e profundidade
        self.state = state  # Estado atual do nó
        self.depth = 1  # profundidade

    def get_state(self):
        return self.state  # get do estado atual

    def set_state(self, state):
        self.state = state  # set para um novo estado

    def get_depth(self):
        return self.depth  # get do depth = profunidade atual

    def set_depth(self, depth):
        self.depth = depth

    def copy(self): # aqui ele vai retornar uma copoia do nó atual
        return NodeCopy(np.copy(self.state))

    def __hash__(self):
        return hash(tuple(map(tuple, self.state)))  # Permite que o nó seja usado em conjuntos

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

class EightPuzzle:  ## aqui é o jogo em si
    def __init__(self):
        goal_state_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]) # nossa matriz 3x3
        self.goal_state = NodeCopy(goal_state_matrix)  # Armazena o estado objetivo em um nó

        initial_state_matrix = np.zeros((3, 3), dtype=int)
        self.initial_state = NodeCopy(initial_state_matrix)  # Armazena o estado inicial em um nó
        self.limit = 1  # limite inicial de profundidade

    def randomize_initial_state(self): # randomizar
        self.initial_state.set_state(np.copy(self.goal_state.get_state()))

        for _ in range(10):
            i1, j1 = random.randint(0, 2), random.randint(0, 2)
            i2, j2 = random.randint(0, 2), random.randint(0, 2)
            self.swap(i1, j1, i2, j2, self.initial_state)  # Troca duas peças

    def swap(self, i1, j1, i2, j2, actual_state):
        actual_state.state[i1][j1], actual_state.state[i2][j2] = actual_state.state[i2][j2], actual_state.state[i1][j1]

    def has_solution(self):
        flat_matrix = self.initial_state.get_state().flatten()
        inversions = sum(1 for i in range(len(flat_matrix)) for j in range(i + 1, len(flat_matrix))
                         if flat_matrix[i] != 0 and flat_matrix[j] != 0 and flat_matrix[i] > flat_matrix[j])
        return inversions % 2 == 0  # Retorna True se o número de inversões for par

    def evoke_ids(self, actual_state): # Busca em Profundidade de Aprofundamento
        while True:
            result = self.ids(actual_state, self.limit)

            if result is not None:
                return result  # Retorna a solução encontrada
            self.limit += 1  # Aumenta o limite de profundidade
            print(f"Limite de profundidade aumentado para: {self.limit}")

    def ids(self, actual_state, limit):
        frontier = [actual_state]  # Usando lista como pilha
        visited_states = set()  # Conjunto para armazenar estados visitados

        while frontier:
            current_node = frontier.pop()  # Remove o nó do topo da pilha
            print(f"Expandindo o nó com profundidade: {current_node.get_depth()}")
            self.print_state(current_node.get_state())  # Imprime o estado atual

            if current_node == self.goal_state:
                return current_node  # Encontrou a solução

            if current_node.get_depth() < limit + 1:  # Se o nó atual estiver dentro do limite de profundidade
                for possibility in self.get_possible_actions(current_node):
                    if possibility not in visited_states:
                        possibility.set_depth(current_node.get_depth() + 1)  # Atualiza a profundidade do novo estado +1
                        frontier.append(possibility)  # Adiciona o novo estado à pilha
                        visited_states.add(possibility)  # Marca como visitado

        return None  # Não encontrou solução

    def get_possible_actions(self, actual_state):
        possible_states = []  # Lista para armazenar estados possíveis
        empty_i, empty_j = np.argwhere(actual_state.get_state() == 0)[0]  # Encontra a posição do espaço vazio (0)

        # Movimentos possíveis: cima, baixo, esquerda, direita
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (delta_i, delta_j)
        for di, dj in moves:
            new_i, new_j = empty_i + di, empty_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:  # Verifica se o movimento é válido
                new_state = actual_state.copy()
                self.swap(empty_i, empty_j, new_i, new_j, new_state)  # Faz a troca no novo estado
                possible_states.append(new_state)

        return possible_states  # Aqui retorna a lista de estados possíveis

    def print_state(self, state):
        for row in state:
            print(' '.join(map(str, row)))
        print()

# Classe para o Puzzle que faz cópia
class PuzzleWithCopy(EightPuzzle):
    def get_possible_actions(self, actual_state):
        possible_states = []  # Lista para armazenar os estados possiveis
        empty_i, empty_j = np.argwhere(actual_state.get_state() == 0)[0]  # Posição do espaço vazio

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in moves:
            new_i, new_j = empty_i + di, empty_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:  # Verifica se o movimento é válido
                new_state = actual_state.copy()
                new_state.set_state(np.copy(actual_state.get_state()))
                self.swap(empty_i, empty_j, new_i, new_j, new_state)
                possible_states.append(new_state)

        return possible_states

if __name__ == "__main__":
    puzzle = PuzzleWithCopy()
    puzzle.randomize_initial_state()

    if puzzle.has_solution():  # vai verificar se o estado inicial tem solução
        print("Estado inicial embaralhado:")
        puzzle.print_state(puzzle.initial_state.get_state())  # Imprime o estado inicial
        time.sleep(3)  # Espera antes de correr para a solução para a gente ver o estado inicial do puzzle
        print("\nBuscando solução...")
        solved_node = puzzle.evoke_ids(puzzle.initial_state)  # Inicia a busca pela solução

        if solved_node is not None and solved_node == puzzle.goal_state:
            print("\nSolução encontrada:")
            puzzle.print_state(solved_node.get_state())  # Imprime a solução encontrada
        else:
            print("\nNão foi possível encontrar uma solução.")
