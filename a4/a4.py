import random
import math
# in every comment made, log(x) refers to log2(x) (i.e. log x base 2)

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

# pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

	# Time Complexity - O((m+n)log(m/eps))
	# Space somplexity - O(k+log(n)+log(m/eps)) 

# pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

	# Time Complexity - O((m+n)log(m/eps))
	# Space somplexity - O(k+log(n)+log(m/eps)) 


# return appropriate N that satisfies the error bounds
def findN(eps,m):
    # let a = f(p) mod q and b = f(x[i:i+m]) mod q, 
	# false positives will be reported when a=b but p!=x[i:i+m]
	# number of primes factors less than |a-b| is at most log|a-b|
	# |a-b| can take maximum value of 26^m (also its average value is O(26^m))
	# the number of primes q_i(s) less than N (Pi(N)) is >= n/(2*log(n))
	# now, the number of primes which will give false positives out of these Pi(N) primes is log(|a-b|)
	# so the probability of false positives eps = log|a-b|/Pi(N)
	# eps >= 2*log|a-b|*log(N)/N for all |a-b|
	# therefore eps >= 2*log26*m*log(N)/N
	# to solve this in O(1) we can make the following approximation -
	# for N>=16, sqrt(N) >= log(N), therefore we can solve the weaker ineqality eps >= 2*log26*m/sqrt(N)
	# therefore N >= (2*log26*m/eps)^2
	# even if N<16, (2*log(26)*m/eps)^2 would be greater than 88 so we can directly return (2*log26*m/eps)^2

	return math.ceil((2*math.log2(26)*m/eps)**2)

# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):

	fp, fx = 0, 0                                                              # fp is f(p) and fx is f(x[i:i+m]) which will be pre evaluated (fx is evaluated for i=0) 
	pow_store = 1                                                              # stores value of 26^y mod q, so that it takes O(log(q)) space
	for i in range (len(p)-1, -1, -1) :                                        # m (=len(p)) iterations, each taking O(log(q)) time because the % (modulo) operator will take O(log(q)) time
		fp += (ord(p[i]) - 65)*(pow_store) % q     
		fp %= q                                                                # ensuring that fp takes O(log(q)) bits for storing f(p)

		fx += (ord(x[i]) - 65)*(pow_store) % q
		fx %= q                                                                # ensuring that fx takes O(log(q)) bits for storing f(x[i:i+m])
		
		pow_store = (pow_store*26) % q

	L = []                                                                     # L is the list of indices of x which 'match' pattern p
	pow_26_m = 1                                                               # storing 26^m which takes O(log(m)) time (assuming fast power is used for the evaluation) and O(log(q)) bits storage
	for j in range (len(p)) :
		pow_26_m = (pow_26_m * 26) % q
	
	for i in range (0, len(x)-len(p)) :                   					   # n-m iterations, each taking O(log(q)) time because the % (modulo) operator will take O(log(q)) time
		if fx == fp : L.append(i)
		fx = (fx*26 + (ord(x[i+len(p)]) - 65) - ((ord(x[i]) - 65)*pow_26_m)%q+q) % q # ensuring that fx takes O(log(q)) bits for storing f(x[i:i+m])
	if fx == fp : L.append(len(x)-len(p))                                      # checking 'match' for i = n-m
	return L

	# Time complexity of modPatternMatch - O(2*m*log(q) + log(m) + (n-m)*log(q)) i.e. O((m+n)log(q))
	# Space complexity of modPatternMatch - storing i, pow_26_m and L takes log(n), log(q) and k bits of space respectively, therefore S.C. is O(k + log(n) + log(q)) 


# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x) :

	fp, fx, pos_q = 0, 0, -1                                                   # fp is f(p), fx is f(x[i:i+m]) and pos_q is position of "?" in p which will be pre evaluated (fx is evaluated for i=0)
	pow_store = 1                                                              # stores value of 26^y mod q, so that it takes O(log(q)) space
	for i in range (len(p)-1, -1, -1) :                                        # m (=len(p)) iterations, each taking O(log(q)) time because the % (modulo) operator will take O(log(q)) time
		if p[i] != "?" :                                                       # "?" is treated as "A", and when any character alphabet is compared with "?", that character is treated as "A"
			fp += (ord(p[i]) - 65)*(pow_store) % q
			fp %= q                                                            # ensuring that fp takes O(log(q)) bits for storing f(p)
		else : 
			pos_q = i
		fx += (ord(x[i]) - 65)*(pow_store) % q
		fx %= q                                                                # ensuring that fx takes O(log(q)) bits for storing f(x[i:i+m])

		pow_store = (pow_store*26) % q

	L = []                                                                     # L is the list of indices of x which 'match' pattern p
	pow_26_m = 1                                                               # storing 26^m which takes O(log(m)) time (assuming fast power is used for the evaluation) and O(log(q)) bits storage
	for j in range (len(p)) :
		pow_26_m = (pow_26_m * 26) % q

	pow_26_posq = 1                                                            # storing 26^(m-pos_q-1) which takes O(log(m-pos_q-1)) time (assuming fast power is used for the evaluation) and O(log(q)) bits storage
	for j in range (len(p) - pos_q - 1) :
		pow_26_posq = (pow_26_posq * 26) % q
	                               
	for i in range (len(x)-len(p)) :
		if (fx - (((ord(x[i + pos_q]) - 65)*pow_26_posq) % q)+ q) % q == fp : L.append(i)
		fx = (fx*26 + (ord(x[i+len(p)]) - 65) - ((ord(x[i]) - 65)*pow_26_m)%q + q) % q # ensuring that fx takes O(log(q)) bits for storing f(x[i:i+m])
	
	if (fx - ((ord(x[len(x) - len(p) + pos_q]) - 65)*pow_26_posq) % q+q) % q == fp : L.append(len(x)-len(p)) # checking 'match' for i = n-m
	return L

	# Time complexity of modPatternMatchWildcard - O(2*m*log(q) + log(m) + O(log(m-pos_q-1)) + (n-m)*log(q)) i.e. O((m+n)log(q))
	# Space complexity of modPatternMatch - storing i, pow_26_m, pow_26_posq and L takes log(n), log(q), log(q) and k bits of space respectively, therefore S.C. is O(k + log(n) + log(q)) 