import numpy as np
import random
import time

# Essa é a versão que modifica o estado pai diretamente
class NodeDirectModify:
    def __init__(self, state):
        self.state = state
        self.depth = 1  # profundidade inicial como 1

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_depth(self):
        return self.depth

    def set_depth(self, depth):
        self.depth = depth

    def __hash__(self):
        return hash(tuple(map(tuple, self.state)))

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

class PuzzleDirectModify:
    def __init__(self):
        goal_state_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])  # matriz
        self.goal_state = NodeDirectModify(goal_state_matrix)  # colocando a matriz dentro do nó

        initial_state_matrix = np.zeros((3, 3), dtype=int)
        self.initial_state = NodeDirectModify(initial_state_matrix)
        self.limit = 1  # limite inicial
        self.max_depth_limit = 100  # limite máximo de profundidade, para nao ficar muito tempo procurando e acabar n achando

    def randomize_initial_state(self):
        self.initial_state.set_state(np.copy(self.goal_state.get_state()))

        for _ in range(10):
            i1, j1 = random.randint(0, 2), random.randint(0, 2)
            i2, j2 = random.randint(0, 2), random.randint(0, 2)
            self.swap(i1, j1, i2, j2, self.initial_state)

    def swap(self, i1, j1, i2, j2, actual_state):
        actual_state.state[i1][j1], actual_state.state[i2][j2] = actual_state.state[i2][j2], actual_state.state[i1][j1]

    def has_solution(self):
        flat_matrix = self.initial_state.get_state().flatten()
        inversions = sum(1 for i in range(len(flat_matrix)) for j in range(i + 1, len(flat_matrix))
                         if flat_matrix[i] != 0 and flat_matrix[j] != 0 and flat_matrix[i] > flat_matrix[j])
        return inversions % 2 == 0  # aqui ele retorna True se for par

    def evoke_ids(self, actual_state):
        while True:
            result = self.ids(actual_state, self.limit)

            if result is not None:
                return result
            self.limit += 1
            print(f"Aumentando o limite de profundidade para: {self.limit}")

    def ids(self, actual_state, limit):
        frontier = [actual_state]  # usando lista como pilha
        visited_states = set()

        while frontier:
            current_node = frontier.pop()
            print(f"Expandindo o nó com profundidade: {current_node.get_depth()}")
            self.print_state(current_node.get_state())

            if current_node == self.goal_state:
                return current_node  # encontrou a solução

            if current_node.get_depth() < limit + 1:  # se o nó atual estiver dentro do limite de profundidade
                for possibility in self.get_possible_actions(current_node):
                    if possibility not in visited_states:
                        visited_states.add(possibility)
                        print(f"Visitando estado:\n{self.array_to_string(possibility.get_state())}")  # Log de estado visitado
                        possibility.set_depth(current_node.get_depth() + 1)
                        frontier.append(possibility)
                    else:
                        print(f"Descartando estado (já visitado):\n{self.array_to_string(possibility.get_state())}")  # Log de estado descartado

            # Verificação de limite máximo de profundidade
            if current_node.get_depth() >= self.max_depth_limit:
                print(f"Limite máximo de profundidade alcançado: {self.max_depth_limit}. Interrompendo busca.")
                return None

        return None  # não encontrou solução

    def get_possible_actions(self, actual_state):
        possible_states = []
        empty_i, empty_j = np.argwhere(actual_state.get_state() == 0)[0]

        # Movimentos possíveis: cima, baixo, esquerda, direita
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (delta_i, delta_j)
        for di, dj in moves:
            new_i, new_j = empty_i + di, empty_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:  # Verifica se o movimento é válido
                # Faz a troca criando um novo estado
                new_state = np.copy(actual_state.get_state())
                new_state[empty_i][empty_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[empty_i][empty_j]
                possible_states.append(NodeDirectModify(new_state))  # Adiciona o novo estado ao conjunto de possibilidades

        return possible_states

    def print_state(self, state):
        for row in state:
            print(' '.join(map(str, row)))
        print()  # linha em branco

    def array_to_string(self, array):
        """Converte um array numpy para uma string para facilitar a exibição."""
        return '\n'.join(' '.join(map(str, row)) for row in array)

if __name__ == "__main__":
    puzzle_direct = PuzzleDirectModify()
    puzzle_direct.randomize_initial_state()

    if puzzle_direct.has_solution():
        print("Estado inicial embaralhado:")
        puzzle_direct.print_state(puzzle_direct.initial_state.get_state())
        time.sleep(3)  # Coloquei um delay para esperar antes de correr para a solução. Pra gente ver o problema
        print("\nBuscando solução...")
        solved_node = puzzle_direct.evoke_ids(puzzle_direct.initial_state)

        if solved_node is not None and solved_node == puzzle_direct.goal_state:
            print("\nSolução encontrada:")
            puzzle_direct.print_state(solved_node.get_state())
        else:
            print("\nNão foi possível encontrar uma solução.")
