from FSM import FSM, concat, add, iteration, intersect, shortest_word, SIGMA


def fsm_from_expression(exp):

    fsm_stack = []
    for char in exp:
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


def generate_exp_for_subword(char, deg):
    word_expr = 'abc++*'
    for i in range(deg):
        word_expr += char
    for i in range(deg - 1):
        word_expr += '.'
    word_expr += 'abc++*..'
    return word_expr


if __name__ == "__main__":
    input_data = raw_input()
    data = str.split(input_data)
    expression = data[0]
    letter = data[1]
    degree = int(data[2])

    try:
        expr_fsm = fsm_from_expression(expression)
        word = fsm_from_expression(generate_exp_for_subword(letter, degree))

        fsm_final = intersect(expr_fsm, word)

        if fsm_final is not None:
            print shortest_word(fsm_final)
        else:
            print 'INF'
    except IndexError:
        print 'Unable to solve. Wrong RegExp.'

