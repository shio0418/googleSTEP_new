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
def read_unaryminus(line, index):
    token = {'type': 'UNARY_MINUS'}
    return token, index + 1

def read_abs(line, index):
    if line[index:index+3] == 'abs':
        token = {'type': 'ABS'}
        print(token)
        return token, index + 3
    else:
        print("Invalid")
        exit(1)

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
            if tokens[-1]['type'] == 'LEFT':
                (token, index) = read_unaryminus(line, index)
            else:
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
        elif line[index] == 'a':
            (token, index) = read_abs(line,index)


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
# 単項演算子の場合。もっとも結びつきが強い
UNARY = {'UNARY_MINUS','ABS'}

# 中置記法を後置に変換
# 入力　中置記法のtokens
# 出力  後置記法のtokens
def change_to_postfix(tokens):
    # stack:まだ処理していない演算子を入れておく
    # output:後置記法を入れていく
    stack = []
    output = []
    print(tokens)
    for token in tokens:
        token_type = token['type']
        # ここら辺関数にするといいかも
        if token_type in OPERATE:
            # stackが空のときは何もせず演算子をstackに積む
            if len(stack) == 0:
                stack.append(token)
                continue
            top = stack.pop()
            # stack最上位のtoken
            top_type = top['type']

            #直近が（のときは、topを戻し演算子をstackに積む
            if top_type == 'LEFT':
                stack.append(top)
                stack.append(token)

            # 演算子の優先順位を考慮しながらstackとoutputを更新

            # 直近が単行演算子の場合は、これを優先。
            elif top_type in UNARY:
                output.append(top)
                stack.append(token)

            # token と top の優先順位が同じ時
            # 例えばtoken:*,top:/の時→tokenをstackにいれてtopを出力
            # token->current_tokenの方が見やすい
            elif token_type in MULTI_DEVIDE and top_type in MULTI_DEVIDE or token_type in PLUS_MINUS and top_type in PLUS_MINUS:
                # 今回扱う演算子は全て左結合なので、topを先に出力
                output.append(top)
                stack.append(token)
            
            # tokenの方が優先順位が高い時
            # どちらもstackに積み直す
            elif token_type in MULTI_DEVIDE and top_type in PLUS_MINUS:
                # topを元に戻す
                stack.append(top)
                stack.append(token)

            # topの方が優先順位が高い時
            # plusとminusは、最後に処理して大丈夫なのでstackに積んである演算子を全て出力
            elif token_type in PLUS_MINUS and top_type in MULTI_DEVIDE:
                while top_type != 'LEFT':
                    if len(stack) == 0:
                        output.append(top)
                        break
                    output.append(top)
                    top = stack.pop()
                    top_type = top['type']

                stack.append(token)

        # 数字の時は無条件に出力
        if token_type == 'NUMBER':
            output.append(token)
        # (-1)とかabsの時は、数字の直後にtokenを出力
        if token_type in UNARY:
            stack.append(token)

        # 右カッコの時は、stackからLEFTを探し出すまでstackの演算子を全て出力する
        if token_type == 'RIGHT':
            if len(stack) == 0:
                print("Invalid")
                exit(1)
            top = stack.pop()
            top_type = top['type']
            while top_type != 'LEFT':
                output.append(top)
                top = stack.pop()
                top_type = top['type']

        if token_type == 'LEFT':
            stack.append(token)

    # stackに残っている演算子を全て出力
    while len(stack) > 0:
        top = stack.pop()
        output.append(top)

    return output



# 後置記法を計算
def evaluate_postfix(tokens):
    stack = []
    print("koko",tokens)
    for token in tokens:
        token_type = token['type']

        if token_type == 'NUMBER':
            stack.append(token['number'])
        elif token_type in UNARY:
            num1 = stack.pop()
            if token_type == 'UNARY_MINUS':
                stack.append((-1) * num1)
            elif token_type == 'ABS':
                stack.append(abs(num1))
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


    assert(len(stack) == 1)
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
    test("2+(3*4)+2-1*3")

    test("(-1)+2")
    test("(-1)*(-2)")
    
    test("abs(-1)")
    test("abs(-1+2)*2*(-1)")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate_2(tokens)
    print("answer = %f\n" % answer)



# 要修正
# 再帰を使う方法
# index管理にてこずり、一旦諦めました、、
# debugしていたためprintまみれです、、、

# 一応方針としては、evaluateで開始→evaluate_roopで基本のループを回す
# →カッコ(LEFT)が見つかったらevaluate_bracketsを呼び出す
# →(RIGHT)がくるまでevaluate_bracketsを再帰
# RIGHTが来たらLEFTからRIGHTまでをdelete

# 全部同じリストで色々やろうとしたのが良くなかったんですかね、、
#

def evaluate(tokens):
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    answer = 0
    return evaluate_roop(tokens,index,answer)

def evaluate_roop (tokens,index,answer):
    while index < len(tokens):
        # 丸カッコを発見したらevaluate_bracketsを呼び出す

        if tokens[index]['type'] == 'LEFT':
            tokens.pop(index)
            tokens,index,brackets_ans = evaluate_brackets(tokens,index,answer)
            tokens.insert(index,{'type':'NUMBER','number':brackets_ans})

            print("いまここ",index,brackets_ans)



        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTI':
                tokens.pop(index-1)
                #演算子を消去したので、インデックスが１ずれる
                num = tokens.pop(index-1)
                #tokens[index - 2] debug
                tokens[index - 2]['number'] *= num['number']
            elif tokens[index - 1]['type'] == 'DEVIDE':
                tokens.pop(index-1)
                num = tokens.pop(index-1)
                tokens[index - 2]['number'] /= num['number']

            # 足し算・引き算の場合何もせずリストに追加
            elif tokens[index - 1]['type'] != 'MINUS' and tokens[index - 1]['type'] != 'PLUS':
                print('Invalid syntax1',tokens[index - 1]['type'],index)
                exit(1)
        index += 1


    #ループをやり直す
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax2')
                exit(1)
        index += 1
    assert index == len(tokens)
    return answer


# 丸カッコの中の処理を行う関数
def evaluate_brackets (tokens,index,answer):

    tokens.insert(index, {'type': 'PLUS'}) # Insert a dummy '+' token
    first_index = index
    print("firstindex",first_index)
    # ( を消去

    while index < len(tokens):
        # 丸カッコを発見したらevaluate_bracketsを呼び出す
        if tokens[index]['type'] == 'LEFT':
            tokens.pop(index)
            left_index = index
            tokens,index,brackets_ans = evaluate_brackets(tokens,index,answer)
            index = left_index
            tokens.insert(left_index,{'type':'NUMBER','number':brackets_ans})
            print("追加しました！！")
            print("カッコの中身",tokens,tokens[left_index])

        if tokens[index]['type'] == 'RIGHT':
            break


        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTI':
                tokens.pop(index-1)
                #演算子を消去したので、インデックスが１ずれる!
                num = tokens.pop(index-1)
                tokens[index - 2]['number'] *= num['number']
            elif tokens[index - 1]['type'] == 'DEVIDE':
                tokens.pop(index-1)
                num = tokens.pop(index-1)
                tokens[index - 2]['number'] /= num['number']

            # 足し算・引き算の場合何もせずリストに追加
            elif tokens[index - 1]['type'] != 'MINUS' and tokens[index - 1]['type'] != 'PLUS':
                print('Invalid syntax3')
                exit(1)
        index += 1

    #ループをやり直す
    index = first_index
    print("カッコのインデックス",index,tokens)

    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax4')
                exit(1)
        elif tokens[index]['type'] == 'RIGHT':
            print("今から消す",tokens[first_index:index+1])
            del tokens[first_index:index+1]

            return tokens,first_index,answer
        index += 1




