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
    exploration = 5 # initial exploration value this doesnt really matter
    frackValue = 0 # this is value below which we choose not to frack

    step = -1 # initial

    border = 3
    yStep = 8
    xStep = 8

    x = 0
    y = 0

    exploreCenter = False
    offsetX = 4
    offsetY = 4

    # Something to store some cell information if you think self will be useful. You can use cellState Class
    m_cells = []
    cells_dict = {}

    def OnStep(self, request):
        result = ""
        try:
            self.m_stepCount += 1
            lastoperation = ''
            lastoperationstatus = False
            lastoperationvalues = 0
            
            try:
                response = self.ParseInput(request, lastoperation, lastoperationstatus, lastoperationvalues)
                lastoperation = response[0]
                lastoperationstatus = response[1]
                lastoperationvalues = response[2]
                try:
                    lastoperationvalues = float(lastoperationvalues) 
                except:
                    lastoperationvalues = 0

                result += str("<log> lastoperationvalues: " + str(lastoperationvalues) + " </log>")
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

                    if (x,y) in self.cells_dict:
                        if p == self.cells_dict[(x,y)].m_production and self.cells_dict[(x,y)].m_bIsProducing == True:
                            self.cells_dict[(x,y)].m_bIsProducing = False
                            self.m_stepCount -= 1
                            return self.StopProduction(x,y)
                        self.cells_dict[(x,y)].m_production = p

                    ##if self.exploreCenter == True:
                    #if (x,y) in self.cells_dict:
                    #    try:    
                    #        if self.cells_dict[(x,y)].offset == True:
                    #            if self.cells_dict[(x,y)].drilled == False:
                    #                result += self.TryToDrillAt(x, y, True)
                    #                self.cells_dict[(x,y)].m_bIsProducing = True
                    #                self.cells_dict[(x,y)].drilled = True
                    #                return result
                    #        if self.cells_dict[(x,y)].offsetted == False and self.cells_dict[(x,y)].m_production + self.cells_dict[(x + self.xStep,y)].m_production + self.cells_dict[(x,y + self.yStep)].m_production + self.cells_dict[(x + self.xStep,y + self.yStep)].m_production >= 1:
                    #            
                    #            self.cells_dict[(x,y)].offsetted = True
#
                    #            result += self.TryToPurchaseAt(x + self.offsetX, y + self.offsetY)
#
                    #            current_cell = CellState(x + self.offsetX, y + self.offsetY)
                    #            self.cells_dict[(x + self.offsetX, y + self.offsetY)] = current_cell
                    #            self.cells_dict[(x + self.offsetX, y + self.offsetY)].offset = True
                    #            return result
                    #    except:
                    #        pass        

            #result += str("<log> buyIndex: " + str(self.m_buyIndex) + "</log>")
            result += str("<log> step: " + str(self.step) + "</log>")

            if self.step == -1:
                # INITIAL BUY
                self.x = 0
                self.y = 0

                self.m_X = self.border
                self.m_Y = self.border

                result += self.TryToPurchaseAt(self.m_X, self.m_Y)

                self.step += 1

                return result
            
            result += "<log> lastOperation: " + str(lastoperation) + "</log>"
            result += "<log> lastOperationStatus: " + str(lastoperationstatus) + "</log>"

            if lastoperationstatus == True:
                self.step += 1
                if self.step == 3: # when done
                    self.step = 0
                #elif self.step == 2: # when drill
                #    self.exploration = lastoperationvalues #save exploration value
                #elif self.step == 2 and lastoperationvalues == 0:
                #    self.step = 0 # dont drill if exploration too low
                #elif self.step == 3 and lastoperationvalues <= self.frackValue: # when fracking
                #    self.step = 0 # dont frack if exploration too low
            else:
                self.step = 0

                
            result += str("<log> Updated step: " + str(self.step) + "</log>")

            if self.step == 0:
                # BUY
                if self.border + self.x + self.xStep > self.m_width:
                    self.x = 0
                    self.y += self.yStep
                    if self.y + self.yStep - self.border > self.m_height:
                        self.x = 0
                        self.y = 0
                        self.exploreCenter = True

                else:
                    self.x += self.xStep

                if self.exploreCenter and self.cells_dict[(self.border + self.x, self.border + self.y)].m_production + self.cells_dict[(self.border + self.x + self.xStep,self.border + self.y)].m_production + self.cells_dict[(self.border + self.x,self.border + self.y + self.yStep)].m_production + self.cells_dict[(self.border + self.x + self.xStep,self.border + self.y + self.yStep)].m_production >= 100:
                    #result += str("<log> Updated step: " + str(self.step) + "</log>")
                    #if self.cells_dict[(self.x,self.y)].m_production >= 0:#+ self.cells_dict[(self.x + self.offsetX,self.y)].m_production + self.cells_dict[(self.x,self.y + self.offsetY)].m_production + self.cells_dict[(self.x + self.offsetX,self.y + self.offsetY)].m_production) > 2:
                        self.m_X = self.x + self.border + self.offsetX
                        self.m_Y = self.y + self.border + self.offsetY

                        
                else:
                    self.m_X = self.x + self.border
                    self.m_Y = self.y + self.border

                result += self.TryToPurchaseAt(self.m_X, self.m_Y)
            #elif self.step == 1:
            #    # EXPLORE
            #    result += self.TryToExploreAt(self.m_X, self.m_Y, "SLB")
            elif self.step == 1:
                # DRILL
                result += self.TryToDrillAt(self.m_X, self.m_Y, True)
                current_cell = CellState(self.m_X, self.m_Y)

                current_cell.m_bIsProducing = True

                self.cells_dict[(self.m_X, self.m_Y)] = current_cell
            elif self.step == 2:
                # STIMULATION
                result += self.TryToStimulateAt(self.m_X, self.m_Y, True)
            else:
                result += str("<log> ERROR: STEP IS WRONG. YOU SHOULD NOT SEE THIS MESSAGE. </log>")
        except:
            result += '<BR>Exception while handling request. '
        return result

    def ParseInput(self, request, lastoperation, lastoperationstatus, lastoperationvalues):
        lastoperationvalues = 0
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
            elif s == 'lastoperationvalue':
                lastoperationvalues = str(request.values[s])
            elif s == 'index':
                self.m_index = int(request.values[s])

        return [lastoperation, lastoperationstatus, lastoperationvalues]

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
