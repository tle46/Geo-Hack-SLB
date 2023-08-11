class CellState:
    m_X = 0
    m_Y = 0

    def __init__(self, x, y):
        self.m_X = x
        self.m_Y = y

    lastProduction = 0

    m_production = 0

    m_bIsProducing = False


    # NOTHING BELOW THIS IS USED

    m_bPurchased = False

    m_tryPurchase = False

    m_estimatedReserve = 0

    m_recoverableReserve = 0

    m_bIsProducingStopRequested = False

    m_isDrilled = False

    m_isExplored = False

    m_flagForStim = False

    m_stimed = False
