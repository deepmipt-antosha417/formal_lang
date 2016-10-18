from itertools import product


Alphabet = ['a', 'b', 'c']


class FSM:
    def __init__(self):
        self.nodes = [[], []]

    def create(self, char):
        self.nodes[0].append([char, 1])
        return self

    def __repr__(self):
        res = 'Number of states: ' + str(len(self.nodes)) + '\n'
        res += 'States:\t|\tTransitions:\n'
        state_num = 0
        for state in self.nodes:
            res += str(state_num) + '\t\t|\t' + str(state) + '\n'
            state_num += 1
        return res

    def len(self):
        return len(self.nodes)


def shift(nodes, shift_len):
    for i1 in range(len(nodes)):
        for j in range(len(nodes[i1])):
            nodes[i1][j][1] += shift_len
    return nodes


def concat(first, second):
    res_fsm = FSM()
    res_fsm.nodes = first.nodes + shift(second.nodes, len(first.nodes))
    res_fsm.nodes[len(first.nodes) - 1].append(['', len(first.nodes)])
    return res_fsm


def add(first, second):
    res_fsm = FSM()
    res_fsm.nodes = [[]] + shift(first.nodes, 1) + shift(second.nodes, len(first.nodes) + 1) + [[]]
    res_fsm.nodes[0].append(['', 1])
    res_fsm.nodes[0].append(['', 1 + len(first.nodes)])
    res_fsm.nodes[len(first.nodes)].append(['', len(first.nodes) + len(second.nodes) + 1])
    res_fsm.nodes[len(first.nodes) + len(second.nodes)].append(['', len(first.nodes) + len(second.nodes) + 1])
    return res_fsm


def iteration(fsm):
    res_fsm = FSM()
    res_fsm.nodes = [[]] + shift(fsm.nodes, 1) + [[]]
    res_fsm.nodes[0].append(['', len(res_fsm.nodes) - 1])
    res_fsm.nodes[0].append(['', 1])
    res_fsm.nodes[len(res_fsm.nodes)-2].append(['', len(res_fsm.nodes) - 1])
    res_fsm.nodes[len(res_fsm.nodes)-2].append(['', 1])
    return res_fsm


def get_eps_neighbs(neighbors, fsm, state, recursion_depth=0):
    recursion_depth += 1
    if recursion_depth >= fsm.len() + 1:
        return set()
    for arrow in fsm.nodes[state]:
        if arrow[0] == '':
            neighbors.add(arrow[1])
            neighbors.union(get_eps_neighbs(neighbors, fsm, arrow[1], recursion_depth))
    return neighbors


def get_neighbors(neighbors, fsm, state, char, recursion_depth=0):
    #neighbors = set()
    recursion_depth += 1
    if recursion_depth >= fsm.len() + 1:
        return set()
    for arrow in fsm.nodes[state]:
        if arrow[0] == char:
            neighbors.add(arrow[1])
            get_eps_neighbs(neighbors, fsm, arrow[1])
        elif arrow[0] == '':
            neighbors.union(get_neighbors(neighbors, fsm, arrow[1], char, recursion_depth))
    #print '!!!', neighbors
    return neighbors


def intersect(first, second):
    res_fsm = FSM()
    res_fsm.nodes = []
    queue = [(0, 0)]
    current_state = 0
    while current_state != len(queue):
        state = queue[current_state]
        res_fsm.nodes.append([])
        for character in Alphabet:
            neighbors = set()
            first_neighbors = list(get_neighbors(neighbors, first, state[0], character))
            neighbors = set()
            second_neighbors = list(get_neighbors(neighbors, second, state[1], character))
            for new_state in product(first_neighbors, second_neighbors):
                if new_state not in queue:
                    queue.append(new_state)
                res_fsm.nodes[current_state].append([character, queue.index(new_state)])
        current_state += 1
    if (len(first.nodes) - 1, len(second.nodes) - 1) not in queue:
        return None
    final_state_index = queue.index((len(first.nodes) - 1, len(second.nodes) - 1))
    res_fsm.nodes.append([])
    res_fsm.nodes[final_state_index].append(['', len(res_fsm.nodes) - 1])
    return res_fsm


def shortest_word(fsm):
    inf = float('Inf')
    lengths = [inf]*len(fsm.nodes)
    lengths[0] = 0

    for step in range(len(fsm.nodes)):
        for i in range(len(fsm.nodes)):
            for j in range(len(fsm.nodes[i])):
                if lengths[fsm.nodes[i][j][1]] > lengths[i] + len(fsm.nodes[i][j][0]):
                    lengths[fsm.nodes[i][j][1]] = lengths[i] + len(fsm.nodes[i][j][0])
    return lengths[len(fsm.nodes) - 1]