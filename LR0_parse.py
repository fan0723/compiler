import pickle
import pandas
from prettytable import PrettyTable

def pickle_load(load_path):
	with open(load_path + '.pickle', 'rb') as f:
		data = pickle.load(f)
		return data

def list_to_str(ls):
    s = ''.join(str(x) for x in ls)
    return s

def find_action(number, ele):
    act = complete_table.at[number, ele]
    return act
    
def shift(Stack, input, action):
    temp = input.pop(0)
    Stack.append(temp)
    Stack.append(int(action[action.find('s') + 1:]))
    return Stack, input

def reduce(Stack, action):
    rule = int(action[action.find('r') + 1:])
    reduce_action = grammer[rule]
    x = reduce_action.split('->')
    before = x[0]
    after = x[1]
    token = ''

    for i in range(len(Stack) - 1, -1, -1):
        if isinstance(Stack[i], str):
            token = Stack[i] + token
        if token == after:
            Stack = Stack[:i]
            Stack.append(before)
            break
    
    Go_to = complete_table.at[Stack[-2], Stack[-1]]
    Stack.append(Go_to)
    return Stack

def parsing(data):
    Stack = [0]
    input = list(data) + ['$']
    log = []
    Accept = False
    while(not Accept):
        action = find_action(Stack[-1], input[0])
        log.append([list_to_str(Stack), list_to_str(input), list_to_str(action)])
        if action == '':
            Accept = False
            break
        if action == 'Acc':
            Accept = True
            break
        if action[0] == 's':
            Stack, input = shift(Stack, input, action)
        elif action[0] == 'r':
            Stack = reduce(Stack, action)

    return Accept, log



# parsing_table = pickle_load('tables/parsing_table')
# return_table = pickle_load('tables/return_table')
grammer = pickle_load('tables/grammar')
complete_table = pickle_load('tables/complete_table')

filename = 'input/1_'
testdata = []
with open(filename + 'testdata.txt', 'r') as f:
	for i in f.readlines():
		testdata.append(i.strip())

for data in testdata:
    x, log = parsing(data)
    print('//////////////////////////////////////')
    print('parsing:', data)
    print('result: ', end = '')
    if x:
        print('Valid!')
    else:
        log[-1][-1] = 'X'
        print('Invalid!')

    col = ['stack', 'input', 'action']
    PT = PrettyTable()
    PT.field_names = col
    PT.align['stack'] = 'l'
    PT.align['input'] = 'r'
    PT.align['action'] = 'c'

    for i in log:
        PT.add_row(i)

    print(PT)