class CellState:
    m_X = 0
    m_Y = 0
    m_bPurchased = False

    def __init__(self, x, y):
        self.m_X = x
        self.m_Y = y

    def X(self):
        return self.m_X

    def Y(self):
        return self.m_Y

    m_probability = 1
    offset = False
    offsetted = False

    #only used by offset nodes
    drilled = False
    fracked = False

    def getProbability(self):
        return self.m_probability

    def setProbability(self, value):
        if self.m_probability != 0:
            if value < 0:
                self.m_probability = 0
            else:
                self.m_probability = value

    def BanCell(self):
        self.m_probability = 0

    def MarkAsPurchased(self):
        self.m_bPurchased = True

    def Purchased(self):
        return self.m_bPurchased

    m_tryPurchase = False

    def getTryPurchase(self):
        return self.m_tryPurchase

    def setTryPurchase(self, value):
        self.m_tryPurchase = value

    m_estimatedReserve = 0

    def getEstimatedReserve(self):
        return self.m_estimatedReserve

    def setEstimatedReserve(self, value):
        self.m_estimatedReserve = value

    m_recoverableReserve = 0

    def getRecoverableReserve(self):
        return self.m_recoverableReserve

    def setRecoverableReserve(self, value):
        self.m_recoverableReserve = value

    m_bIsProducing = False

    def getProducing(self):
        return self.m_bIsProducing

    def setProducing(self, value):
        self.m_bIsProducing = value

    m_bIsProducingStopRequested = False

    def getProducingStopRequested(self):
        return self.m_bIsProducingStopRequested

    def setProducingStopRequested(self, value):
        self.m_bIsProducingStopRequested = value

    m_production = 0

    def getProduction(self):
        return self.m_production

    def setProduction(self, value):
        self.m_production = value

    m_isDrilled = False

    def getDrilled(self):
        return self.m_isDrilled

    def setDrilled(self, value):
        self.m_isDrilled = value

    m_isExplored = False

    def getExplored(self):
        return self.m_isExplored

    def setExplored(self, value):
        self.m_isExplored = value

    m_flagForStim = False

    def getFlagForStim(self):
        return self.m_flagForStim

    def setFlagForStim(self, value):
        self.m_flagForStim = value

    m_stimed = False

    def getStimmed(self):
        return self.m_stimed

    def setStimmed(self, value):
        self.m_stimed = value
