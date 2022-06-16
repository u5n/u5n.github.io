import sys; sys.path.append('../../')
from plib.ds.mixDeque import MixDeque
import random
import operator
from plib._util import measure

"""
test speed only
"""
A = [random.randrange(100000) for _ in range(100000)]
@measure(10)
def random_queue_opt():
    q = MixDeque(lambda l,r:l if l>r else r)
    for r in A:
        if r <= 50000:
            q.append(r)
        else:
            if q:
                q.popleft()

@measure(10)
def random_queue_popmore():
    q = MixDeque(operator.add)
    for r in A:
        if r <= 30000:
            q.append(r)
        else:
            if q:
                q.popleft()