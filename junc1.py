import numpy as np

class junctionDef:
    def __init__(self, x, y, cap, canStop, fareProb=None, maxTraffic=0, src=0, sink=0):
        self.x = x
        self.y = y
        self.capacity = cap
        self.canStop = canStop
        self.fareProb = fareProb
        self.maxTraffic = maxTraffic
        self.tSrc = src
        self.tSink = sink

class streetDef:
    def __init__(self, nodeAIdx, nodeBIdx, dirA, dirB, biDirectional=True):
        self.nodeA = nodeAIdx  # first point (origin if one-way)
        self.nodeB = nodeBIdx  # second point (destination if one-way)
        self.dirA = dirA       # exit point from nodeA
        self.dirB = dirB       # exit point from nodeB
        self.bidirectional = biDirectional  # one-way or 2-way street?

# Basic parameters
worldX = 50
worldY = 50
trafficOn = False

# Fare probabilities
fareProbMagnet = lambda m: np.random.random() > 0.98
fareProbPopular = lambda p: np.random.random() > 0.992
fareProbSemiPopular = lambda s: np.random.random() > 0.995
fareProbNormal = lambda n: np.random.random() > 0.999

# Traffic sources and sinks
trafficSrcMinor = 1 if trafficOn else 0
trafficSrcSignificant = 2 if trafficOn else 0
trafficSrcMajor = 3 if trafficOn else 0
trafficSrcHub = 4 if trafficOn else 0
trafficSinkMinor = 1 if trafficOn else 0
trafficSinkSignificant = 2 if trafficOn else 0
trafficSinkMajor = 3 if trafficOn else 0
trafficSinkDrain = 4 if trafficOn else 0

# Create junctions
junctions = [
    junctionDef(0, 0, 2, True, src=trafficSrcMinor, sink=trafficSinkMinor),
    junctionDef(20, 0, 2, True, src=trafficSrcSignificant, sink=trafficSinkMinor),
    junctionDef(30, 0, 2, True, src=trafficSrcMajor, sink=trafficSinkMajor),
    junctionDef(49, 0, 2, True, src=trafficSrcMinor, sink=trafficSinkMinor),
    junctionDef(40, 5, 2, True),
    junctionDef(0, 10, 2, True, src=trafficSrcSignificant, sink=trafficSinkMinor),
    junctionDef(10, 10, 2, True, fareProb=fareProbSemiPopular, maxTraffic=12),
    junctionDef(20, 10, 2, True, maxTraffic=12),
    junctionDef(30, 10, 8, True, fareProb=fareProbPopular, maxTraffic=12, src=trafficSrcMajor, sink=trafficSinkDrain),
    junctionDef(40, 10, 4, True, fareProb=fareProbPopular, maxTraffic=12),
    junctionDef(49, 10, 2, True, src=trafficSrcSignificant, sink=trafficSinkSignificant),
    junctionDef(15, 15, 4, True, fareProb=fareProbPopular, maxTraffic=12),
    junctionDef(24, 15, 4, True, fareProb=fareProbSemiPopular, maxTraffic=12),
    junctionDef(30, 15, 4, True, fareProb=fareProbSemiPopular, maxTraffic=12),
    junctionDef(10, 20, 2, True),
    junctionDef(20, 20, 4, True, fareProb=fareProbSemiPopular, maxTraffic=12),
    junctionDef(10, 24, 2, True),
    junctionDef(20, 24, 4, True),
    junctionDef(24, 24, 8, True, fareProb=fareProbMagnet, maxTraffic=16, src=trafficSrcHub, sink=trafficSinkMajor),
    junctionDef(30, 24, 4, True),
    junctionDef(0, 35, 2, True, src=trafficSrcSignificant, sink=trafficSinkMajor),
    junctionDef(10, 35, 4, True, fareProb=fareProbPopular, maxTraffic=12),
    junctionDef(15, 35, 4, True, fareProb=fareProbSemiPopular, maxTraffic=12),
    junctionDef(20, 30, 4, True, fareProb=fareProbSemiPopular),
    junctionDef(24, 35, 4, True, fareProb=fareProbPopular, maxTraffic=12, src=trafficSrcMajor, sink=trafficSinkMajor),
    junctionDef(30, 30, 4, True),
    junctionDef(40, 30, 4, True, fareProb=fareProbSemiPopular, maxTraffic=12),
    junctionDef(49, 30, 2, True, src=trafficSrcMinor, sink=trafficSinkMinor),
    junctionDef(10, 40, 2, True),
    junctionDef(15, 40, 4, True, fareProb=fareProbPopular, maxTraffic=12),
    junctionDef(30, 40, 4, True, fareProb=fareProbSemiPopular, maxTraffic=12),
    junctionDef(40, 40, 2, True, maxTraffic=12),
    junctionDef(0, 49, 2, True, src=trafficSrcMinor, sink=trafficSinkMinor),
    junctionDef(15, 49, 2, True, src=trafficSrcSignificant, sink=trafficSinkMajor),
    junctionDef(30, 49, 2, True, src=trafficSrcMinor, sink=trafficSinkMinor),
    junctionDef(49, 49, 2, True, src=trafficSrcMinor, sink=trafficSinkMinor)
]



# Create streets
streets = [
    streetDef((0, 0), (10, 10), 'S', 'N', biDirectional=True),
    streetDef((0, 10), (10, 10), 'S', 'N', biDirectional=True),
    streetDef((0, 35), (10, 35), 'S', 'N', biDirectional=True),
    streetDef((0, 49), (10, 40), 'S', 'N', biDirectional=True),
    streetDef((10, 10), (10, 20), 'S', 'N', biDirectional=True),
    streetDef((10, 10), (15, 15), 'S', 'N', biDirectional=True),
    streetDef((10, 20), (10, 24), 'S', 'N', biDirectional=True),
    streetDef((10, 24), (10, 35), 'S', 'N', biDirectional=True),
    streetDef((10, 35), (10, 40), 'S', 'N', biDirectional=True),
    streetDef((10, 10), (20, 10), 'S', 'N', biDirectional=True),
    streetDef((10, 20), (15, 15), 'S', 'N', biDirectional=True),
    streetDef((10, 20), (20, 20), 'S', 'N', biDirectional=True),
    streetDef((10, 24), (20, 24), 'S', 'N', biDirectional=True),
    streetDef((10, 35), (15, 35), 'S', 'N', biDirectional=True),
    streetDef((10, 35), (15, 40), 'S', 'N', biDirectional=True),
    streetDef((10, 40), (15, 40), 'S', 'N', biDirectional=True),
    streetDef((15, 15), (20, 10), 'S', 'N', biDirectional=True),
    streetDef((15, 15), (20, 20), 'S', 'N', biDirectional=True),
    streetDef((20, 0), (20, 10), 'S', 'N', biDirectional=True),
    streetDef((20, 10), (20, 20), 'S', 'N', biDirectional=True),
    streetDef((20, 20), (20, 24), 'S', 'N', biDirectional=True),
    streetDef((20, 24), (20, 30), 'S', 'N', biDirectional=True),
    streetDef((15, 40), (15, 49), 'S', 'N', biDirectional=True),
    streetDef((20, 10), (30, 10), 'S', 'N', biDirectional=True),
    streetDef((20, 20), (24, 15), 'S', 'N', biDirectional=True),
    streetDef((20, 20), (24, 24), 'S', 'N', biDirectional=True),
    streetDef((20, 24), (24, 24), 'S', 'N', biDirectional=True),
    streetDef((20, 30), (24, 24), 'S', 'N', biDirectional=True),
    streetDef((20, 30), (24, 35), 'S', 'N', biDirectional=True),
    streetDef((15, 35), (24, 35), 'S', 'N', biDirectional=True),
    streetDef((15, 35), (15, 40), 'S', 'N', biDirectional=True),
    streetDef((15, 40), (30, 40), 'S', 'N', biDirectional=True),
    streetDef((24, 15), (24, 24), 'S', 'N', biDirectional=True),
    streetDef((24, 24), (24, 35), 'S', 'N', biDirectional=True),
    streetDef((24, 15), (30, 10), 'S', 'N', biDirectional=True),
    streetDef((24, 15), (30, 15), 'S', 'N', biDirectional=True),
    streetDef((24, 24), (30, 15), 'S', 'N', biDirectional=True),
    streetDef((24, 24), (30, 24), 'S', 'N', biDirectional=True),
    streetDef((24, 24), (30, 30), 'S', 'N', biDirectional=True),
    streetDef((24, 35), (30, 30), 'S', 'N', biDirectional=True),
    streetDef((24, 35), (30, 40), 'S', 'N', biDirectional=True),
    streetDef((30, 15), (40, 10), 'S', 'N', biDirectional=True),
    streetDef((30, 15), (30, 24), 'S', 'N', biDirectional=True),
    streetDef((30, 24), (30, 30), 'S', 'N', biDirectional=True),
    streetDef((30, 40), (30, 49), 'S', 'N', biDirectional=True),
    streetDef((30, 10), (30, 15), 'S', 'N', biDirectional=True),
    streetDef((30, 10), (40, 5), 'S', 'N', biDirectional=True),
    streetDef((30, 10), (40, 10), 'S', 'N', biDirectional=True),
    streetDef((30, 24), (40, 30), 'S', 'N', biDirectional=True),
    streetDef((30, 30), (40, 30), 'S', 'N', biDirectional=True),
    streetDef((30, 40), (40, 40), 'S', 'N', biDirectional=True),
    streetDef((30, 0), (30, 10), 'S', 'N', biDirectional=True),
    streetDef((40, 5), (49, 0), 'S', 'N', biDirectional=True),
    streetDef((40, 5), (40, 10), 'S', 'N', biDirectional=True),
    streetDef((40, 10), (40, 30), 'S', 'N', biDirectional=True),
    streetDef((40, 30), (40, 40), 'S', 'N', biDirectional=True),
    streetDef((15, 35), (20, 30), 'S', 'N', biDirectional=True),
    streetDef((40, 10), (49, 10), 'S', 'N', biDirectional=True),
    streetDef((40, 30), (49, 30), 'S', 'N', biDirectional=True),
    streetDef((40, 40), (49, 49), 'S', 'N', biDirectional=True),
]

