class mdd:
    def __init__(self):
        self.mdd_min = 0
        self.mdd_max = 0
        # self.mdd_diff =0
        self.mdd_period = 0
        self.mdd_rates = []
        self.mdd_diffs = []
        self.helper_position = None

    def update(self, price):
        '''max downdrawdonw'''
        if self.mdd_max < price:
            if self.mdd_min < self.mdd_max:
                diff = self.mdd_min - self.mdd_max
                # self.mdd_rates.append([diff,diff/self.mdd_max ])
                self.mdd_rates.append(diff / self.mdd_max * 100.0 * -1)
                self.mdd_diffs.append(diff)
            self.mdd_min = price
            self.mdd_period = 0
            self.mdd_max = price

        if price < self.mdd_min:
            self.mdd_min = price
        if price <= self.mdd_max:
            self.mdd_period = self.mdd_period + 1

    def update_close_position(self):
        self.mdd_max = 0
        self.mdd_min = 0
        self.mdd_period = 0

    def update_by_position(self, price, position):
        if position is None:
            if self.helper_position== None:
                return
            else:
                self.mdd_period= self.mdd_period+1
                return

        if self.helper_position != position:
            self.helper_position = position
            #self.update_close_position()
        self.update(price)

    def get_max_drawdown(self):
        if self.mdd_min < self.mdd_max:
            diff = self.mdd_min - self.mdd_max
            # self.mdd_rates.append([diff,diff/self.mdd_max ])
            self.mdd_rates.append(diff / self.mdd_max * 100.0 * -1)
            self.mdd_diffs.append(diff)
            self.mdd_max = 0#reset
            self.mdd_min =0
        if len(self.mdd_rates) == 0: return 0
        return min(self.mdd_rates)

    def get_drawdowns(self):

        return self.mdd_rates

    def save(self):
        dump_inst = {}
        dump_inst['rate'] = self.mdd_rates
        dump_inst['period'] = self.mdd_period
        dump_inst['diff'] = self.mdd_diffs
        return dump_inst

    @staticmethod
    def load(inst):
        mdd_inst = mdd()
        mdd_inst.mdd_diffs = inst['diff']
        mdd_inst.mdd_rates = inst['rate']
        mdd_inst.mdd_period = inst['period']
        return mdd_inst

    def view(self):
        print 'max draw down:', self.get_max_drawdown()
        print 'drawdown rate:', self.mdd_rates
        print 'drawdown:', self.mdd_diffs

    pass