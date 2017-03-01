import random
import matplotlib.pyplot as plt

M = {}
print 'Please enter the value of Epsilon: '
epsilon = float(input())

def max_q(M):
    tmp = []
    for a in M['action']:
        tmp.append(M['action'][a]['q'])
    return max(tmp)

if __name__ == '__main__':
    for i in range(12):
        M[i] = {}
        M[i]['name'] = 'S'+str(i+1)
        M[i]['label'] = [i/4+1,i%4+1]
        M[i]['action'] = {}

    M['actions'] = ['up','down','left','right']
    for item in range(12):
        if M[item]['label'][1] < 4:
            M[item]['action']['right'] = {}
            M[item]['action']['right']['dest'] = (M[item]['label'][0]-1)*4+M[item]['label'][1]
        if M[item]['label'][1] > 1:
            M[item]['action']['left'] = {}
            M[item]['action']['left']['dest'] = (M[item]['label'][0]-1)*4+M[item]['label'][1]-2
        if M[item]['label'][0] < 3:
            M[item]['action']['down'] = {}
            M[item]['action']['down']['dest'] = (M[item]['label'][0])*4+M[item]['label'][1]-1
        if M[item]['label'][0] > 1:
            M[item]['action']['up'] = {}
            M[item]['action']['up']['dest'] = (M[item]['label'][0]-2)*4+M[item]['label'][1]-1
    for item in range(12):
        for a in M[item]['action']:
            M[item]['action'][a]['q'] = random.randint(0,9)*0.0001
            if not (M[item]['action'][a]['dest']):
                M[item]['action'][a]['q'] = -1
            if M[item]['action'][a]['dest'] == 5:
                M[item]['action'][a]['reward'] = 100
            else:
                M[item]['action'][a]['reward'] = 0
    M[5]['action'] = {}
    
    M['abs'] = []

    itr = 0
    while (itr < 100):
        state = random.randint(0,11)
        s = 0
        while state != 5:
            if state == 5:
                break
            for a in M[state]['action']:
                if  M[state]['action'][a]['q'] == max_q(M[state]):
                    a_prime = a
            factor = random.randint(0,9)
            if factor > (1-epsilon)*10:
                a = list(M[state]['action'])[random.randint(0,len(M[state]['action'])-1)]
            else:
                a = a_prime

            if M[state]['action'][a]['dest'] == 5:
                s += abs(M[state]['action'][a]['reward'] - M[state]['action'][a]['q'])
                M[state]['action'][a]['q'] = M[state]['action'][a]['reward']+0
            else:
                s += abs(M[state]['action'][a]['reward']+0.9*max_q(M[M[state]['action'][a]['dest']]) - M[state]['action'][a]['q'])
                M[state]['action'][a]['q'] = M[state]['action'][a]['reward']+0.9*max_q(M[M[state]['action'][a]['dest']])

            state = M[state]['action'][a]['dest']

        M['abs'].append(s)
        itr += 1

    M['table'] = []
    for i in range(12):
        M['table'].append([-1,-1,-1,-1])
    for item in range(12):
        if item != 5:
            for a in M[item]['action']:
                M['table'][item][M['actions'].index(a)] = M[item]['action'][a]['q']

    print '\t',
    for i in range(len(M['actions'])):
        print M['actions'][i]+'\t',
    print
    for i in range(len(M['table'])):
        print  M[i]['name']+'\t',
        for j in range(4):
            print str('%.2f' % M['table'][i][j])+'\t',
        print

    plt.plot(M['abs'])
    plt.show()