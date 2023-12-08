import pickle
import pandas
from prettytable import PrettyTable

def pickle_load(load_path):
	with open(load_path + '.pickle', 'rb') as f:
		data = pickle.load(f)
		return data

def data_to_list(data):
    output = []
    ele = ''
    for i in data:
        ele += i
        if ele in terminal:
            output.append(ele)
            ele = ''
    
    if ele != '':
        return -1            
    return output

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

def draw_table(log):
    col = ['stack', 'input', 'action']
    PT = PrettyTable()
    PT.field_names = col
    PT.align['stack'] = 'l'
    PT.align['input'] = 'r'
    PT.align['action'] = 'c'

    for i in log:
        PT.add_row(i)

    print(PT)

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

def parsing(data, log, output_log):
    if(len(log) != 0):
        [Stack, input, action] = log
        output_log.pop()

    else:
        Stack = [0]
        input = data_to_list(data)
        if input == -1:
            print('Invalid character exist!')
            return False, -1

        input += ['$']
        action = find_action(Stack[-1], input[0])
    

    
    Accept = False
    que = []
    while(not Accept):        
        if action.find('/') != -1:
            # print('Shift Reduce Implict!')
            action_t = action.split('/')
            action = action_t[0]
            temp_log = log.copy()
            temp_output_log = output_log.copy()
            temp_output_log.append([list_to_str(Stack), list_to_str(input), list_to_str(action_t[1])])
            temp_log = [Stack.copy(), input.copy(), action_t[1]]
            que.append([temp_log, temp_output_log])
        
        log = [Stack.copy(), input.copy(), action]
        output_log.append([list_to_str(Stack), list_to_str(input), list_to_str(action)])
        
        if action == '':
            while(len(que) > 0):
                [temp_log, temp_output_log] = que.pop()
                Accept, output_log = parsing(data, temp_log, temp_output_log)
                if Accept:
                    break
            break
        if action == 'Acc':
            Accept = True
            break            
        if action[0] == 's':
            Stack, input = shift(Stack, input, action)
        elif action[0] == 'r':
            Stack = reduce(Stack, action)
        
        action = find_action(Stack[-1], input[0])

    return Accept, output_log
    

grammer = pickle_load('tables/grammar')
complete_table = pickle_load('tables/complete_table')
terminal = pickle_load('tables/terminal')
filename = pickle_load('tables/filename')

testdata = []
with open(filename + 'testdata.txt', 'r') as f:
	for i in f.readlines():
		testdata.append(i.strip())

for data in testdata:
    print('//////////////////////////////////////')
    print('parsing:', data)
    x, log = parsing(data, [], [])
    print('result: ', end = '')
    if x:
        print('Valid!')
    else:        
        print('Invalid!')
        if log == -1:
            continue
        log[-1][-1] = 'X'
    draw_table(log)
    