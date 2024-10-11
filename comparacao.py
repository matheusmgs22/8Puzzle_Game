import numpy as np
import random
import time

## Aqui faz a comparação entre as duas Versões. Vemos que a modificação direta é levemente mais rapida que a cópia.

# Versão que faz cópia do estado
class NodeCopy:
    def __init__(self, state):
        self.state = state
        self.depth = 1

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_depth(self):
        return self.depth

    def set_depth(self, depth):
        self.depth = depth

    def copy(self):
        return NodeCopy(np.copy(self.state))

    def __hash__(self):
        return hash(tuple(map(tuple, self.state)))

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

class EightPuzzleCopy:
    def __init__(self):
        goal_state_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.goal_state = NodeCopy(goal_state_matrix)
        initial_state_matrix = np.zeros((3, 3), dtype=int)
        self.initial_state = NodeCopy(initial_state_matrix)
        self.limit = 1

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
        return inversions % 2 == 0

    def evoke_ids(self, actual_state):
        print("Resolvendo com cópia...")
        while True:
            result = self.ids(actual_state, self.limit)
            if result is not None:
                return result
            self.limit += 1

    def ids(self, actual_state, limit):
        frontier = [actual_state]
        visited_states = set()

        while frontier:
            current_node = frontier.pop()
            if current_node == self.goal_state:
                return current_node
            if current_node.get_depth() < limit + 1:
                for possibility in self.get_possible_actions(current_node):
                    if possibility not in visited_states:
                        possibility.set_depth(current_node.get_depth() + 1)
                        frontier.append(possibility)
                        visited_states.add(possibility)
        return None

    def get_possible_actions(self, actual_state):
        possible_states = []
        empty_i, empty_j = np.argwhere(actual_state.get_state() == 0)[0]
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in moves:
            new_i, new_j = empty_i + di, empty_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = actual_state.copy()
                new_state.set_state(np.copy(actual_state.get_state()))
                self.swap(empty_i, empty_j, new_i, new_j, new_state)
                possible_states.append(new_state)
        return possible_states
import numpy as np
import random
import time

# Versão que modifica diretamente o estado
class NodeDirectModify:
    def __init__(self, state):
        self.state = state
        self.depth = 1

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

class EightPuzzleDirectModify:
    def __init__(self):
        goal_state_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.goal_state = NodeDirectModify(goal_state_matrix)
        initial_state_matrix = np.zeros((3, 3), dtype=int)
        self.initial_state = NodeDirectModify(initial_state_matrix)
        self.limit = 1

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
        return inversions % 2 == 0

    def evoke_ids(self, actual_state):
        print("Resolvendo com modificação direta...")
        while True:
            result = self.ids(actual_state, self.limit)
            if result is not None:
                return result
            self.limit += 1

    def ids(self, actual_state, limit):
        frontier = [actual_state]
        visited_states = set()

        while frontier:
            current_node = frontier.pop()
            if current_node == self.goal_state:
                return current_node
            if current_node.get_depth() < limit + 1:
                for possibility in self.get_possible_actions(current_node):
                    # Evita recalcular ou visitar o mesmo estado
                    if possibility not in visited_states:
                        possibility.set_depth(current_node.get_depth() + 1)
                        frontier.append(possibility)
                        visited_states.add(possibility)
        return None

    def get_possible_actions(self, actual_state):
        possible_states = []
        empty_i, empty_j = np.argwhere(actual_state.get_state() == 0)[0]
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for di, dj in moves:
            new_i, new_j = empty_i + di, empty_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                # Salvar estado anterior para evitar interferência em outros nós
                previous_state = np.copy(actual_state.get_state())

                self.swap(empty_i, empty_j, new_i, new_j, actual_state)

                possible_states.append(NodeDirectModify(np.copy(actual_state.get_state())))

                actual_state.set_state(previous_state)

        return possible_states

# Função para comparar tempos de execução com mensagens de carregamento
def compare_versions():
    # Gera um unico estado inicial aleatorio
    print("Gerando estado inicial aleatório...")
    puzzle_copy = EightPuzzleCopy()
    puzzle_copy.randomize_initial_state()

    # Imprime o estado inicial do quebra-cabeça
    print("Estado inicial do quebra-cabeça (será resolvido por ambas as versões):")
    print(puzzle_copy.initial_state.get_state())

    # Passar o mesmo estado inicial para a versão com modificação direta
    puzzle_direct = EightPuzzleDirectModify()
    puzzle_direct.initial_state.set_state(np.copy(puzzle_copy.initial_state.get_state()))

    # Versão com cópia
    print("Iniciando versão com cópia...")
    start_time = time.time()
    has_solution_copy = puzzle_copy.has_solution()
    if has_solution_copy:
        puzzle_copy.evoke_ids(puzzle_copy.initial_state)
    copy_time = time.time() - start_time
    print(f"Versão com cópia finalizada. Tempo: {copy_time:.6f} segundos, Solução: {has_solution_copy}") ## É False quando não tem solução

    # Versão com modificação direta
    print("Iniciando versão com modificação direta...")
    start_time = time.time()
    has_solution_direct = puzzle_direct.has_solution()
    if has_solution_direct:
        puzzle_direct.evoke_ids(puzzle_direct.initial_state)
    direct_modify_time = time.time() - start_time
    print(f"Versão com modificação direta finalizada. Tempo: {direct_modify_time:.6f} segundos, Solução: {has_solution_direct}") ## É False quando não tem solução


if __name__ == "__main__":
    compare_versions()
