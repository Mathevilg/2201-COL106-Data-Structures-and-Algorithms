class Heap :

    def __init__ (self, data=[]) :
        self.data = data
        self.len = len(self.data)
        self.buildHeap()

    def parent(self, i) :
        return (i-1)//2

    def leftChild(self, i) :
        if len(self.data) > (2*i + 1) :
            return (2*i + 1)
        else :
            return None

    def rightChild(self, i) :
        if len(self.data) > (2*i + 2):
            return (2*i + 2)
        else :
            return None

    def heapUp(self, x, arr) :
        i = x
        while i != 0 and self.data[(i-1)//2] > self.data[i] :
            self.data[(i-1)//2], self.data[i] = self.data[i], self.data[(i-1)//2]
            arr[self.data[i][1]] , arr[self.data[(i-1)//2][1]] = i , (i-1)//2
            i = (i-1)//2

    def enqueue(self, x, arr) :
        i = len(self.data)
        self.data.append(x)
        self.heapUp(i, arr)

    def heapDown(self, x, arr) :
        i = x
        while (2*i+1 < len(self.data) and self.data[i] > self.data[2*i+1]) or (2*i+2 < len(self.data) and self.data[i] > self.data[2*i+2]) :
            v = 0
            if 2*i + 2 < len(self.data) :
                if min(self.data[2*i+1], self.data[2*i+2]) == self.data[2*i+1] : 
                    v = 2*i + 1
                else :
                    v = 2*i + 2
            else :
                v = 2*i + 1
            self.data[i], self.data[v] = self.data[v], self.data[i]
            arr[self.data[i][1]] , arr[self.data[v][1]] = i , v
            i = v
    
    def extractMin(self) :
        w = self.data[0]
        x = self.data.pop()
        self.data[0] = x
        self.heapDown(0)
        return w

    def changeKey(self, u, x) :
        X = self.data[u]
        self.data[u] = x
        if X>x :
            self.heapUp(u)
        elif X<x :
            self.heapDown(u)

    def buildHeap(self) :
        a = [0]*len(self.data)
        for u in range (len(self.data) - 1, -1, -1) :
            self.heapDown(u, a)

inf = float('inf')
def listCollisions(M, x, v, m, T) :
    L = []
    for i in range (0, len(M)-1) :
        l = []                                                             # l contains time of next collision, i, last collision time
        if v[i] - v[i+1] > 0 : l.append((x[i+1] - x[i]) / (v[i] - v[i+1])) # collision
        else : l.append(inf)
        l.append(i)
        l.append(0)                                                        # last time when i collided
        L.append(l)

    L.append([inf, len(M)-1, 0])
    timeHeap = Heap(L)                                                     # timeHeap is heap of time of collisions 

    arr = [0]*len(M)
    for i in range (len(M)) :
        arr[timeHeap.data[i][1]] = i                                       # now ith element of arr has the value of the position of ith particle in the heap

    outputList = []
    numOfCollisions = 0

    while numOfCollisions < m :

        if timeHeap.data[0][0] > T : break
        else:
            i = timeHeap.data[0][1]

            x[i] += v[i] * (timeHeap.data[0][0] - timeHeap.data[0][2])    # update positions of ith and (i+1)st particle
            x[i+1] = x[i]
            
            v[i], v[i+1] = (2*M[i+1]*v[i+1] + v[i]*(M[i]-M[i+1]))/(M[i] + M[i+1]), (2*M[i]*v[i] + v[i+1]*(M[i+1]-M[i]))/(M[i] + M[i+1])

            if i > 0 and v[i-1] - v[i]  > 0 :                             # if (i-1)th and ith particle collide
                timeHeap.data[arr[i-1]][0] = (x[i] - x[i-1] + v[i-1]*timeHeap.data[arr[i-1]][2] - v[i]*timeHeap.data[0][0])/(v[i-1] - v[i])
            else :
                timeHeap.data[arr[i-1]][0] = inf

            if i+2 < len(timeHeap.data) and v[i+1] - v[i+2] > 0 :         # if (i+1)th and (i+2)nd particle collide
                timeHeap.data[arr[i+1]][0] = (x[i+2] - v[i+2]*timeHeap.data[arr[i+2]][2] - x[i+1] + v[i+1]*timeHeap.data[0][0])/(v[i+1] - v[i+2])
            else :
                timeHeap.data[arr[i+1]][0] = inf
            
            outputList.append((timeHeap.data[0][0], i, x[i]))

            timeHeap.data[0][2] = timeHeap.data[0][0]
            timeHeap.data[arr[i+1]][2] = timeHeap.data[0][0]
            timeHeap.data[0][0] = inf
        
            timeHeap.heapDown(0, arr)
            timeHeap.heapUp(arr[i+1], arr)
            timeHeap.heapDown(arr[i+1], arr)
            timeHeap.heapUp(arr[i-1], arr)
            timeHeap.heapDown(arr[i-1], arr)

            numOfCollisions += 1

    return outputList