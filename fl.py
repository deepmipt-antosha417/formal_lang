from FSM import FSM, concat, add, iteration


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

if __name__ == "__main__":
    expr_fsm = fsm_from_expression('a*ab+.').nodes
    print len(expr_fsm)
    print
    for i in range(len(expr_fsm)):
        print i, expr_fsm[i]

    k = 1
    letter = 'a'
    word_expr = 'ab+*'
    for i in range(k):
        word_expr += letter
    for i in range(k-1):
        word_expr += '.'
    word_expr += 'ab+*..'

    word = fsm_from_expression(word_expr).nodes
    print len(word)
    print
    for i in range(len(word)):
        print i, word[i]
