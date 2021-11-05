from collections import namedtuple
def manacher_parity(s, parity):
    n = len(s)
    P = [0]*n
    ans = 0
    cen = (0,0)
    for i in range(n):
        if cen[1] > i:
            l = 2*cen[0]-i
            if P[l] < cen[1] - i:
                P[i] = P[l]
                continue
            else:
                P[i] = cen[1] - i
        while (il:=i-P[i]-parity)>=0 and (ir:=i+P[i]+1)<n and s[il]==s[ir]:
            P[i]+=1
        if i+P[i]>cen[1]:
            cen = (i+P[i], i)
        ans = max(ans, P[i]*2 + parity)
    return ans

def manacher(s):
    return max(manacher_parity(s, 1), manacher_parity(s, 0))