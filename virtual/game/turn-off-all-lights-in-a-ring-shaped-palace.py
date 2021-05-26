import random
# https://puzzling.stackexchange.com/questions/10130/turn-off-all-lights-in-a-ring-shaped-palace

class Room:
    def __init__(self, state):
        self.state = state
        self.next = None
        self.prev = None
    def __repr__(self):
        return str(self.state)

class Palace:
    def __init__(self, sz):
        con=[Room(random.randint(0,1)) for _ in range(sz)]
        for i in range(sz):
            con[i].prev = con[(i-1)%sz]
            con[i].next = con[(i+1)%sz]
        self._sz = sz
        self.con = con
    def getRandom(self):
        return random.choice(self.con)
    def checkAll(self):
        for room in self.con:
            if room.state == 1:
                return False
        return True
    def __repr__(self):
        return str(self.con)
class Boss:
    def __init__(self, palace):
        self.palace = palace
    def feedBack(self):
        if self.palace.checkAll():
            return (1, "good job", self.palace._sz)
        else:
            if self.palace._sz<100:
                return (0, f"...this is the map...{palace}")
            else:
                return (0, f"wrong answer")

class Person:
    def __init__(self, room, boss):
        self.walkStep = 0
        self.room = room
        self.Boss = boss
    def toggleLightOn(self):
        self.room.state = 1
    def toggleLightOff(self):
        self.room.state = 0
    def gotoAdjRoom(self, direction):
        if direction==1:
            self.room = self.room.next
        else:
            self.room = self.room.prev
        self.walkStep+=1
    def getRoomState(self):
        return self.room.state
    def callBoss(self):
        return self.Boss.feedBack()

def yourAlgorithmExample(me):
    """ time O(4*2**ceil(log2(n))) """
    me.toggleLightOn()
    steps = 1
    while True:
        for _ in range(steps):
            me.gotoAdjRoom(1)
            me.toggleLightOff()
        for _ in range(steps):
            me.gotoAdjRoom(-1)
        if me.getRoomState()==0:
            break
        steps*=2
    me.toggleLightOff()

def yourAlgorithm(me):
    """ write algorithm here """
    pass

def solveSingle(me):
    yourAlgorithm(me)
    print(me.callBoss())
    print("walk steps", me.walkStep)

def test():
    for sz in range(1, 1001):
        palace = Palace(sz)
        me = Person(palace.getRandom(), Boss(palace))
        yourAlgorithm(me)
        assert me.callBoss()[0] == 1

palace = Palace(random.randint(131072, 131072))
me = Person(palace.getRandom(), Boss(palace))
solveSingle(me)