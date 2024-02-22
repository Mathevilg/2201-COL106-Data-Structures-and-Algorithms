class Stack :
    def __init__(self) :                                                # initialise Stack, setting filled attribute to 0
        self._data = [0]
        self._filled = 0
    def __len__(self) :                                                 # length of Stack is the value of filled  
        return self._filled
    def push(self, e) :
        if len(self._data) > self._filled :                             # If e can be pushed without growing the array
            self._data[self._filled] = e
        else :                                                          # Grow the stack to with length of array twice the previous one
            a = (2*len(self._data)) * [0]
            for i in range (self._filled) :
                a[i] = self._data[i]
            self._data = a
            self._data[self._filled] = e
        self._filled += 1
    def pop(self) :                                                     # To pop last element, decrease filled by 1 and return topmost element
        y = self._filled - 1
        x = self._data[y]
        self._data[y] = 0
        self._filled = y
        return x
    def top(self) :                                                     # return topmost element
        return self._data[self._filled - 1]

def evalSimpleStr(i, P) :                                               # given a pointer i and string P, returns the evaluated expression, final pointer and distance till a nested intruction comes
    ans, dis = [0,0,0], 0
    k = i
    while k < len(P) and (P[k] == '-' or P[k] == '+'):
        dis += 1                                                        # increase distance by 1
        if P[k] == '+' :                                                # if '+', add 1 to appropriate coordinate
            if P[k+1] == 'X' : ans[0] += 1
            elif P[k+1] == 'Y' : ans[1] += 1
            else : ans[2] += 1
        else :                                                          # if '-', subtract 1 to appropriate coordinate               
            if P[k+1] == 'X' : ans[0] -= 1
            elif P[k+1] == 'Y' : ans[1] -= 1
            else : ans[2] -= 1
        k += 2
    return (ans, k, dis)

def num(i, P) :                                                         # returns the number before the '(' bracket
    j = 0
    while P[i+j] != '(' :
        j += 1
    return (int(P[i:i+j]), j)

def findPositionandDistance(P) :

    coord, mul, distance = Stack(), Stack(), Stack()                    # initialise coord, mul, distance to empty stacks
    coord.push([0,0,0])
    distance.push(0)
 
    i = 0                                                               # initialise a counter which moves from 0 to len(P)-1
    while i<len(P) :
        if str.isnumeric(P[i]) :                                        # if we encounter a digit
            numreturn = num(i,P)
            mul.push(numreturn[0])
            if P[i-1] == '(' :                                          # push [0,0,0] and 0 to coord and distance if P[i-1] == '('
                coord.push([0,0,0])                                     # dont care if i > 0 or not as '(' comes only if i >= 1
                distance.push(0)

            i += numreturn[1] + 1                                       # i points to expression after 'number(' 

        elif (P[i] == '-' or P[i] == '+') :                             # if we encounter '+' or '-' then process the string until nested expression ends or starts
            evaled = evalSimpleStr(i,P)

            if P[i-1] == '(' :                                          # if P[i-1] == '(', dont worry if i > 0 or not as '(' comes only if i >= 1
                coord.push(evaled[0])
                distance.push(evaled[2])
            else :                                                      # if P[i-1] == ')' or i == 0
                x = coord.pop()
                coord.push([evaled[0][j] + x[j] for j in range (3)])
                distance.push(evaled[2] + distance.pop())

            i = evaled[1]

        else :                                                          # If P[i] == ')'
            if P[i-1] == '(' :                                          # if there is no expression inside two parenthesis, i.e. '()'
                coord.push([0,0,0])
                distance.push(0)

            x = [w*mul.top() for w in coord.pop()]
            y = coord.pop()

            coord.push([x[i]+y[i] for i in range (3)])
            distance.push(mul.pop()*distance.pop() + distance.pop())

            i += 1
    
    final_coord = coord.top()      
    return [final_coord[0], final_coord[1], final_coord[2], distance.top()]

