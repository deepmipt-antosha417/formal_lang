from FSM import FSM, concat, add, iteration, intersect, shortest_word


SIGMA = ['a', 'b', 'c']


def fsm_from_expression(expression):

    fsm_stack = []
    for char in expression:
        if char in SIGMA or char == '1':
            fsm = FSM()
            fsm_stack.append(fsm.create(char))
        elif char == '.':
            second_fsm = fsm_stack.pop()
            first_fsm = fsm_stack.pop()
            fsm_stack.append(concat(first_fsm, second_fsm))

        elif char == '+':
            first_fsm = fsm_stack.pop()
            second_fsm = fsm_stack.pop()
            fsm_stack.append(add(first_fsm, second_fsm))

        elif char == '*':
            fsm = fsm_stack.pop()
            fsm_stack.append(iteration(fsm))

    if len(fsm_stack) != 1:
        raise IndexError
    return fsm_stack[0]


def generate_exp_for_subword(char, degree):
    word_expr = 'abc++*'
    for i in range(degree):
        word_expr += char
    for i in range(degree - 1):
        word_expr += '.'
    word_expr += 'abc++*..'
    return word_expr


if __name__ == "__main__":
    expr_fsm = fsm_from_expression('aa*.').nodes

    k = 1
    letter = 'a'

    word = fsm_from_expression(generate_exp_for_subword(letter, k)).nodes

#ab+c.aba.*.bac.+.+*
#acb..bab.c.*.ab.ba.+.+*a.

    test_1 = fsm_from_expression('acb..bab.c.*.ab.ba.+.+*a.')
    test_2 = fsm_from_expression(generate_exp_for_subword('b', 3))

    print test_1

    fsm_t = intersect(test_1, test_2)
    print fsm_t

    print shortest_word(fsm_t)

