def min_repr(s):
    """
    input: string s
    output: 
        `min( range(n), key=(lambda i:(s+s)[i:i+n]) )` 
            if key same, it find the one with min index
    time: O(n)
    application: hash of cyclic string
    """
    ans = 0
    can = 1
    n = len(s)
    s2 = s+s
    while can < n:
        # loop inv: all((s+s)[i:i+n]>(s+s)[ans:ans+n] for i in range(can))
        n_match = 0
        while n_match < n and s2[ans+n_match]==s2[can+n_match]: n_match += 1
        if n_match == n: return ans
        if s2[ans+n_match] < s2[can+n_match]:
            can += n_match + 1
        else:
            ans, can = can, max(can+1, ans + n_match + 1)
    
    return ans
    return s2[ans:ans+n]

if __name__ == "__main__":
    import random, string
    n = 500
    for _ in range(10000):
        s = ''.join(random.choices(string.ascii_lowercase, k = n))
        s2 = s+s
        assert min_repr(s) == min(range(n), key=lambda i:s2[i:i+n])
        