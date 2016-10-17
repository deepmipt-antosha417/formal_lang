class FSM:
    def __init__(self):
        self.nodes = [[], []]

    def create(self, char):
        self.nodes[0].append([char, 1])
        return self

    def __repr__(self):
        return str(self.nodes)


def shift(nodes, shift_len):
    for i1 in range(len(nodes)):
        for j in range(len(nodes[i1])):
            nodes[i1][j][1] += shift_len
    return nodes


def concat(first, second):
    res_fsm = FSM()
    res_fsm.nodes = first.nodes + shift(second.nodes, len(first.nodes))
    res_fsm.nodes[len(first.nodes) - 1].append(['e', len(first.nodes)])
    return res_fsm


def add(first, second):
    res_fsm = FSM()
    res_fsm.nodes = [[]] + shift(first.nodes, 1) + shift(second.nodes, len(first.nodes) + 1) + [[]]
    res_fsm.nodes[0].append(['e', 1])
    res_fsm.nodes[0].append(['e', 1 + len(first.nodes)])
    res_fsm.nodes[len(first.nodes)].append(['e', len(first.nodes) + len(second.nodes) + 1])
    res_fsm.nodes[len(first.nodes) + len(second.nodes)].append(['e', len(first.nodes) + len(second.nodes) + 1])
    return res_fsm


def iteration(fsm):
    res_fsm = FSM()
    res_fsm.nodes = [[]] + shift(fsm.nodes, 1) + [[]]
    res_fsm.nodes[0].append(['e', len(res_fsm.nodes) - 1])
    res_fsm.nodes[0].append(['e', 1])
    res_fsm.nodes[len(res_fsm.nodes)-2].append(['e', len(res_fsm.nodes) - 1])
    res_fsm.nodes[len(res_fsm.nodes)-2].append(['e', 1])
    return res_fsm
