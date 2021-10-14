from pandas import *
from prettytable import PrettyTable

def reconstructB(y, L):
    B = [[] for i in range(len(y))]
    
    for i in range(len(y)):
        #add to cols
        for j in range(len(y)):
            B[j].insert(0, y[j])
    
        
        B.sort(key=lambda x: "".join(x))
        p = PrettyTable()
        for row in B:
            p.add_row(row)
        print(p.get_string(header=False, border=False))
        print('\n')
        

reconstructB('cbbacabab', 0)