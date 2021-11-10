from SATSolver import testKb, testLiteral

def print_result(result):
    if result==True:
            print('Yes.')
    elif result==False:
        print('No.')
    else:
        print('Unknown.')

if __name__ == '__main__':
    clauses = [[-1, 3], [-2, -3], [2, 3], [-3, 2, -1], [3, -2]]
    print('Knowledge base is satisfiable:',testKb(clauses))
    print('Is Amy a truth-teller?', end=' ')
    result = testLiteral(1,clauses)
    print_result(result)
    print('Is Bob a truth-teller?', end=' ')
    result = testLiteral(2,clauses)
    print_result(result)
    print('Is Cal a truth-teller?', end=' ')
    result = testLiteral(3,clauses)
    print_result(result)