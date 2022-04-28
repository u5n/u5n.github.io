pow3 = [3**i for i in range(17)]
def ts_get(self, i):
    return (self // pow3[i])%3

def ts_set(self, i, v):
    return self + pow3[i] * (-ts_get(self, i) + v)
