#! /usr/bin/python3
# line : 与えられた文字列
# token : 文字の型と値を保持する辞書型


def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

# 掛け算のtokenを作成する関数
def read_multiple(line, index):
    token = {'type': 'MULTI'}
    return token, index + 1

# 割り算のtokenを作成する関数
def read_devision(line, index):
    token = {'type': 'DEVIDE'}
    return token, index + 1

# 鉤括弧の処理をする関数
def read_right(line, index):
    token = {'type': 'RIGHT'}
    return token, index + 1

def read_left(line, index):
    token = {'type': 'LEFT'}
    return token, index + 1

# tokenのリストを作成
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        # 掛け算
        elif line[index] == '*':
            (token, index) = read_multiple(line, index)
        # 割り算
        elif line[index] == '/':
            (token, index) = read_devision(line,index)
        elif line[index] == ')':
            (token, index) = read_right(line,index)
        elif line[index] == '(':
            (token, index) = read_left(line,index)

        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token) # 辞書型なので順序を維持
    return tokens

# 後置に変換して計算する方法
# tokens
# 2+3*4→3 4 * 2 +

OPERATE = {'PLUS','MINUS','MULTI','DEVIDE'}
PLUS_MINUS = {'PLUS','MINUS'}
MULTI_DEVIDE = {'MULTI','DEVIDE'}

# 中置記法を後置に変換
def change_to_postfix(tokens):
    stack = []
    output = []
    
    for token in tokens:
        token_type = token['type']
        
        if token_type in OPERATE:
            # stackが空のときは何もせず演算子をstackに積む
            if len(stack) == 0:
                stack.append(token)
                continue
            top = stack.pop()
            top_type = top['type']
            
            #直近が（のときは、topを戻し演算子をstackに積む
            if top_type == 'LEFT':  
                stack.append(top)
                stack.append(token)
                
            # 例えばtoken:*,top:/の時→tokenをstackにいれてtopを出力
            elif token_type in MULTI_DEVIDE and top_type in MULTI_DEVIDE or token_type in PLUS_MINUS and top_type in PLUS_MINUS:
                output.append(top)
                stack.append(token)
            # 
            elif token_type in MULTI_DEVIDE and top_type in PLUS_MINUS:
                # topを元に戻す
                stack.append(top)
                stack.append(token)
            elif token_type in PLUS_MINUS and top_type in MULTI_DEVIDE:
                while top_type != 'LEFT':
                    if len(stack) == 0:
                        output.append(top)
                        break
                    output.append(top)
                    top = stack.pop()
                    top_type = top['type']
 
                stack.append(token)

        if token_type == 'NUMBER':
            output.append(token)

        if token_type == 'RIGHT':
            print(stack)
            if len(stack) == 0:
                print("Invalid")
                exit(1)
            top = stack.pop()
            top_type = top['type']
            while top_type != 'LEFT':
                print(top)
                output.append(top)
                top = stack.pop()
                top_type = top['type']

        if token_type == 'LEFT':
            stack.append(token)

    while len(stack) > 0:
        top = stack.pop()
        output.append(top)
      
    return output



# 後置記法を計算
def evaluate_postfix(tokens):
    stack = []
    for token in tokens:
        token_type = token['type']
        
        if token_type == 'NUMBER':
            stack.append(token['number'])
        elif token_type in OPERATE:
            num1 = stack.pop()
            num2 = stack.pop()
            
            if token_type == 'PLUS':
                stack.append(num2+num1)
            elif token_type == 'MINUS':
                stack.append(num2-num1)
            elif token_type == 'MULTI':
                stack.append(num2*num1)
            elif token_type == 'DEVIDE':
                stack.append(num2/num1)
                

    return stack.pop()

def evaluate_2(tokens):
    tokens_postfix = change_to_postfix(tokens)
    return evaluate_postfix(tokens_postfix)


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate_2(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    
    test("1+2")
    test("1.0+2.1-3")
    test("1*2")
    test("1+2*2")
    test("5+0.6*2")
    
    test("1/2")
    
    test("1-2/2")

    test("(1+2)")
    test("(1+2)+1")

    test("2*(2+3)")
    test("(2/(2+3))")

    test("(3.0+4*(2-1))")

    test("(2+3)*2")
    test("(2+3)/2")

    test("(2*(2+3))*1")
    test("(3.0+4*(2-1))*2")
    test("(3.0+4*(2-1))/5")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate_2(tokens)
    print("answer = %f\n" % answer)