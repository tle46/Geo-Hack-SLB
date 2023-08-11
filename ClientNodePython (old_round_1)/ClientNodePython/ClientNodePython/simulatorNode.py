import random
from cellState import CellState


class SimulatorNode():
    m_stepCount = 0
    m_money = 0
    m_width = 0
    m_height = 0
    m_X = 0
    m_Y = 0
    m_index = -1
    m_round = -1
    first = True

    # Not great variables for random strategy....
    m_buyIndex = -1

    # Something to store some cell information if you think self will be useful. You can use cellState Class
    m_cells = []

    def OnStep(self, request):
        result = ""
        try:
            self.m_stepCount += 1
            lastoperation = ''
            lastoperationstatus = False
            try:
                lastoperation, lastoperationstatus = self.ParseInput(request, lastoperation, lastoperationstatus)
            except:
                result += '<BR>Excep[tion while retreiving client information '

            # Maybe create a store to save the cell information if you plan on using it....
            # Look at the current production

            production = request.values['production']
            if production:
                listOfCellProduction = production.split(' ')[:-1]
                countOfProducingCells = len(listOfCellProduction)

                for i in range(0, countOfProducingCells):
                    prodinfo = listOfCellProduction[i].split(',')
                    if len(prodinfo) < 3:
                        pass
                    x = int(prodinfo[0])
                    y = int(prodinfo[1])
                    p = int(prodinfo[2])
                    # Looks like useful information, maybe we should do something with this?

            if self.m_buyIndex == -1:
                # Buy buy buy!
                self.m_X = random.randrange(0, self.m_width)
                self.m_Y = random.randrange(0, self.m_height)
                result += self.TryToPurchaseAt(self.m_X, self.m_Y)
                self.m_buyIndex = self.m_stepCount
            elif self.m_buyIndex == self.m_stepCount - 1:
                # Blindly try to drill
                result += self.TryToDrillAt(self.m_X, self.m_Y, True)
            elif self.m_buyIndex == self.m_stepCount - 2:
                # Blindly try to stimulate
                result += self.TryToStimulateAt(self.m_X, self.m_Y, True)
            elif self.m_buyIndex == self.m_stepCount - 3:
                # Buy buy buy!
                self.m_X = random.randrange(0, self.m_width)
                self.m_Y = random.randrange(0, self.m_height)
                result += self.TryToPurchaseAt(self.m_X, self.m_Y)
                self.m_buyIndex = self.m_stepCount
        except:
            result += '<BR>Exception while handling request. '

        return result

    def ParseInput(self, request, lastoperation, lastoperationstatus):
        for s in request.values:
            if s == 'round':
                self.m_round = int(request.values[s])
                if self.m_round == 0:
                    self.m_cells = None
                    self.m_width = 0
                    self.m_height = 0
            elif s == 'money':
                self.m_money = int(request.values[s])
            elif s == 'width':
                self.m_width = int(request.values[s])
            elif s == 'height':
                self.m_height = int(request.values[s])
            elif s == 'lastoperation':
                lastoperation = request.values[s]
            elif s == 'lastoperationstatus':
                lastoperationstatus = request.values[s] == 'True'
            elif s == 'index':
                self.m_index = int(request.values[s])

        return lastoperation, lastoperationstatus

    def TryToPurchaseAt(self, x, y):
        result = ''
        result += '<Execute>Buy</Execute>'
        result += '<BuyAtX>' + str(x) + '</BuyAtX>'
        result += '<BuyAtY>' + str(y) + '</BuyAtY>'
        return result

    def StopProduction(self, x, y):
        result = ''
        result += '<Execute>StopProduction</Execute><StopProductionAtX>' + str(x) + '</StopProductionAtX><StopProductionAtY>' + str(y) + '</StopProductionAtY>'
        return result

    def TryToExploreAt(self, x, y, slb):
        result = ''
        result += '<Execute>Explore</Execute>'
        result += '<ExploreAtX>' + str(x) + '</ExploreAtX>'
        result += '<ExploreAtY>' + str(y) + '</ExploreAtY>'
        result += '<ServiceProvider>'
        if slb:
            result += 'SLB'
        else:
            result += 'HAL'

        result += '</ServiceProvider>'
        return result

    def TryToDrillAt(self, x, y, slb):
        result = ''
        result += '<Execute>Drill</Execute>'
        result += '<DrillAtX>' + str(x) + '</DrillAtX>'
        result += '<DrillAtY>' + str(y) + '</DrillAtY>'
        result += '<ServiceProvider>'
        if slb:
            result += 'SLB'
        else:
            result += 'HAL'
        result += '</ServiceProvider>'
        return result

    def TryToStimulateAt(self, x, y, slb):
        result = ''
        result += '<Execute>Stimulate</Execute>'
        result += '<StimulateAtX>' + str(x) + '</StimulateAtX>'
        result += '<StimulateAtY>' + str(y) + '</StimulateAtY>'
        result += '<ServiceProvider>'
        if slb:
            result += 'SLB'
        else:
            result += 'HAL'
        result += '</ServiceProvider>'
        return result
