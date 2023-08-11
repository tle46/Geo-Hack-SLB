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

    m_buyIndex = -1
    # exploration = 5 # initial exploration value this doesnt really matter

    # pass 0 = first pass with double xStep
    # pass 1 = optimized midpoint fill
    # pass 2 = fill remaining
    # pass 3 = explore center
    passStep = 0

    # step -1 = Initial
    # step 0 = buy
    # step 1 = explore
    # step 2 = drill
    # step 3 = frack
    step = -1

    border = 3
    yStep = 8
    xStep = 8

    x = 0
    y = 0

    offsetX = 4
    offsetY = 4
    
    m_cells = []

    
    cells_dict = {} # cell state dict

    
    midpoint_counter = 0
    midpoint_list = []

    center_counter = 0
    center_list = []

    create_first_list = True
    list_of_points = []
    r1_index = 0

    def OnStep(self, request):
        result = ""
        delete_later = 0
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

                    if (x,y) in self.cells_dict:
                        self.cells_dict[(x,y)].lastProduction = p - self.cells_dict[(x,y)].m_production

                        if p == self.cells_dict[(x,y)].m_production and self.cells_dict[(x,y)].m_bIsProducing == True:
                            self.cells_dict[(x,y)].m_bIsProducing = False
                            self.m_stepCount -= 1
                            return self.StopProduction(x,y)
                        self.cells_dict[(x,y)].m_production = p

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
                if self.step == 4: # when done
                    self.step = 0
                #elif self.step == 2: # when drill
                #    self.exploration = lastoperationvalues #save exploration value
                #elif self.step == 2 and lastoperationvalues == 0:
                #    self.step = 0 # dont drill if exploration too low
                elif self.step == 3 \
                    and (self.m_X, self.m_Y) in self.cells_dict.keys() \
                    and self.cells_dict[(self.m_X, self.m_Y)].lastProduction <= 0:
                    # When fracking
                    self.step = 0 # Don't frack if exploration too low
            else:
                self.step = 0

                
            result += str("<log> Updated step: " + str(self.step) + "</log>")

            if self.step == 0:
                if self.create_first_list == True:
                    current_x = 0
                    current_y = 0
                    while current_y + self.border < self.m_height:
                            while current_x + self.border < self.m_width:
                                self.list_of_points.append((current_x,current_y))
                                current_x += 2 * self.xStep
                            current_x = 0
                            current_y += self.yStep
                
                    self.create_first_list = False
                    random.shuffle(self.list_of_points)
                if self.passStep == 0:
                    result += "<HI>" + str(self.list_of_points) + "</HI>"
                    # BUY
                    self.x = self.list_of_points[self.r1_index][0]
                    result += "<BYE></BYE>"
                    self.y = self.list_of_points[self.r1_index][1]
                    self.r1_index += 1
                
                result += str("<log> passStep: " + str(self.passStep) + "</log>")
                
                if self.passStep == 1:
                    #try:
                    #    while (self.cells_dict[(self.border + self.x, self.border + self.y)].m_production \
                    #    + self.cells_dict[(self.border + self.x + 2 * self.xStep,self.border + self.y)].m_production \
                    #    >= 50) == False:
                    #        self.x += 2 * self.xStep
                    #except:
                    #    pass

                    if self.midpoint_counter == 0:
                        temp_x = self.border
                        temp_y = self.border
                        temp_dict = {}
                        while (temp_y < self.m_height):
                            while temp_x < self.m_width:
                                corners_prod = 0
                                try:
                                    corners_prod += self.cells_dict[(temp_x, temp_y)].m_production
                                except:
                                    corners_prod += 0
                                try:
                                    corners_prod += self.cells_dict[(temp_x + 2 * self.xStep, temp_y)].m_production
                                except:
                                    corners_prod += 0
                                if corners_prod > 0:
                                    temp_dict[(temp_x + self.xStep, temp_y)] = corners_prod
                                temp_x += self.xStep * 2
                            temp_y += self.yStep
                            temp_x = self.border
                        self.midpoint_list = sorted(temp_dict.items(), key=lambda x:x[1], reverse=True)

                    # Explore centers
                    
                    try:
                        self.m_X = self.midpoint_list[self.midpoint_counter][0][0]
                        self.m_Y = self.midpoint_list[self.midpoint_counter][0][1]
                        self.midpoint_counter += 1
                        result += "<4></4>"
                    except:
                        self.passStep = 3

                if self.passStep == 3:
                    if self.center_counter == 0:
                        #jtedit
                        temp_x = self.border
                        temp_y = self.border
                        temp_dict = {}
                        while (temp_y < self.m_height - self.yStep):
                            while temp_x < self.m_width:
                                corners_prod = 0
                                try:
                                    corners_prod += self.cells_dict[(temp_x, temp_y)].m_production
                                except:
                                    corners_prod += 0
                                try:
                                    corners_prod += self.cells_dict[(temp_x + self.xStep, temp_y)].m_production
                                except:
                                    corners_prod += 0
                                try:
                                    corners_prod += self.cells_dict[(temp_x, temp_y + self.yStep)].m_production
                                except:
                                    corners_prod += 0
                                try:
                                    corners_prod += self.cells_dict[(temp_x + self.xStep, temp_y + self.yStep)].m_production
                                except:
                                    corners_prod += 0
                                if corners_prod > 0:
                                    temp_dict[(temp_x + self.offsetX, temp_y + self.offsetY)] = corners_prod
                                temp_x += self.xStep
                            temp_y += self.yStep 
                            temp_x = self.border
                        self.center_list = sorted(temp_dict.items(), key=lambda x:x[1], reverse=True)

                    # Explore centers
                    self.m_X = self.center_list[self.center_counter][0][0]
                    self.m_Y = self.center_list[self.center_counter][0][1]
                    self.center_counter += 1
                    result += "<4></4>"

                if self.passStep == 0:
                    # Normal x, y calculations
                    self.m_X = self.x + self.border
                    self.m_Y = self.y + self.border
                    if self.r1_index == len(self.list_of_points):
                        self.passStep = 1

                # Try to purchase
                result += self.TryToPurchaseAt(self.m_X, self.m_Y)
            if self.step == 1:
                # EXPLORE
                # result += self.TryToExploreAt(self.m_X, self.m_Y, "SLB")
                self.step += 1
            if self.step == 2:
                # DRILL
                result += self.TryToDrillAt(self.m_X, self.m_Y, True)
                current_cell = CellState(self.m_X, self.m_Y)

                current_cell.m_bIsProducing = True

                self.cells_dict[(self.m_X, self.m_Y)] = current_cell
            if self.step == 3:
                # STIMULATION
                result += self.TryToStimulateAt(self.m_X, self.m_Y, True)
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
