def highestpower2(n) : # highest power of 2 which divides n, TC is O(logn)
    i = -1
    while n>0 :
        if n%2 == 1 : return i + 1
        n //= 2
        i += 1
    return i

def partition(start,end) : # given start and end, partition and return a list which is used for processing
    if start==0 :
        if end == 1 : return [(0,0,0)] # (L[i], start, end)
        else :
            i = -1
            e = end
            while e>0 :
                e //= 2
                i += 1
            return [(i, 0, 2**i - 1)] + partition(2**i, end)
    else :
        if start == end : return []
        else :
            L = []
            while start < end :
                x = highestpower2(start)
                y = x
                while start + 2**y > end : y -= 1
                L.append((y, start, start + 2**y - 1))
                start += 2**y
            return L

def binarysearch(t, d, points, start, end, x_or_y) : # given tuple, d, points, start and end, returns the range (two pointers) which is contained from t-d to t+d
    xmin = t[x_or_y] - d
    xmax = t[x_or_y] + d
    if xmin > points[end][x_or_y] or xmax < points[start][x_or_y] : return None, None
    minindex = minBS(xmin, points, start, end, x_or_y)
    maxindex = maxBS(xmax, points, start, end, x_or_y)
    return minindex, maxindex

def minBS(x, points, i, j, x_or_y) :
    if points[i][x_or_y] >= x : return i
    low, high, mid, temp = i, j, i, i
    while low <= high :
        mid = (high + low) // 2
        if points[mid][x_or_y] < x : low, temp = mid + 1, mid + 1
        else : high, temp = mid - 1, mid
    return temp

def maxBS(x, points, i, j, x_or_y) :
    if points[j][x_or_y] <= x : return j
    low, high, mid, temp = i, j, i, j
    while low <= high :
        mid = (high + low) // 2
        if points[mid][x_or_y] > x : high, temp = mid - 1, mid - 1
        else: low, temp = mid + 1, mid
    return temp

def merge(ivalue, lst) : # modifying the list lst such that is becomes 'more' partially ordered
    l = []
    k = 0
    while k < len(lst) - len(lst)%ivalue :
        i = k
        j = k + ivalue//2
        while i<k+ivalue//2 and j<k+ivalue :
            if lst[i][1]<lst[j][1] :
                l.append(lst[i])
                i += 1
            else :
                l.append(lst[j])
                j += 1
        if i == k+ivalue//2 :
            while j<k+ivalue :
                l.append(lst[j])
                j += 1
        elif j == k+ivalue :
            while i<k+ivalue//2 :
                l.append(lst[i])
                i += 1
        k += ivalue

    if k!=len(lst) :
        i, j = k, k
        if k + ivalue//2 < len(lst) : j = k + ivalue//2
        if j==k :
            while i < len(lst) :
                l.append(lst[i])
                i += 1
        else :
            while i<k+ivalue//2 and j<len(lst) :
                if lst[i][1]<lst[j][1] :
                    l.append(lst[i])
                    i += 1
                else :
                    l.append(lst[j])
                    j += 1
            if i == k+ivalue//2 :
                while j<len(lst) :
                    l.append(lst[j])
                    j += 1
            elif j == len(lst) :
                while i<k+ivalue//2 :
                    l.append(lst[i])
                    i += 1
    return l

class PointDatabase :
    def __init__ (self, pointlist) :
        pointlist.sort()
        L = [pointlist]
        i = 2
        while i<2*len(pointlist) :
            L.append(merge(i, L[-1]))
            i *= 2
        self.L = L                       # L is a list of lists which represents the data structure we created for running fast queries in time O(nlogn)

    def searchNearby(self, q, d) :
        if self.L == [[]] : return []
        minindex, maxindex = binarysearch(q, d, self.L[0], 0, len(self.L[0])-1, 0)
        if minindex == None and maxindex == None : return []
        l = partition(minindex, maxindex+1)
        ans = []
        for x in l :
            i, j = binarysearch(q, d, self.L[x[0]], x[1], x[2], 1)
            if i == None and j == None : continue
            while i <= j :
                ans.append(self.L[x[0]][i])
                i += 1
        return ans