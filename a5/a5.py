from math import inf
def findMaxCapacity(n, links, s, t) :

    adjacencyList = [[] for i in range (n)]
    visited = [False] * n
    visitedvertices = 0

    for x in links :
        adjacencyList[x[0]].append((x[1], x[2]))
        adjacencyList[x[1]].append((x[0], x[2]))

    ans = [inf]*n
    prevlist = [0]*n
    heap = [(inf,s)]

    while visitedvertices<n and heap != [] :
        u = heap[0][1]
        if not visited[u] : visitedvertices += 1
        visited[u] = True
        heap[0], heap[-1] = heap[-1], heap[0]
        heap.pop()
        i = 0
        while (2*i+1 < len(heap) and heap[i] < heap[2*i+1]) or (2*i+2 < len(heap) and heap[i] < heap[2*i+2]) :
            if (2*i+1 < len(heap) and heap[i] < heap[2*i+1]) and not (2*i+2 < len(heap) and heap[i] < heap[2*i+2]) : v = 2*i + 1
            elif not (2*i+1 < len(heap) and heap[i] < heap[2*i+1]) and (2*i+2 < len(heap) and heap[i] < heap[2*i+2]) : v = 2*i + 2
            else :
                if heap[2*i+1] > heap[2*i+2] : v = 2*i + 1
                else : v = 2*i + 2
            heap[i], heap[v] = heap[v], heap[i]
            i = v

        for vertices in adjacencyList[u] :
            weight = vertices[1]
            v = vertices[0]
            if visited[v] : continue
            if min(ans[u],weight) > ans[v] or (ans[v] > min(ans[u], weight) and ans[v] == inf): 
                ans[v] = min(ans[u],weight)
                prevlist[v] = u
                i = len(heap)
                heap.append((ans[v], v)) 
                while i > 0 and heap[(i-1)//2] < heap[i] :
                    heap[(i-1)//2], heap[i] = heap[i], heap[(i-1)//2]
                    i = (i-1)//2
        if visited[t] : break

    route = [t]
    end = t
    while end!=s :
        route.append(prevlist[end])
        end = prevlist[end]
    route.reverse()
    return (ans[t], route)