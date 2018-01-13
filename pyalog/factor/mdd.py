import pandas as pd
class mdd:
    def __init__(self):
        self.mdd_min = 0
        self.mdd_max = 0
        # self.mdd_diff =0
        #self.mdd_period = 0
        self.mdd_rates = []
        self.mdd_diffs = []
        self.mdd_price_pair=[] #item(high,low)
        self.mdd_periods = []
        self.helper_position = None

    def update(self, price):
        '''max downdrawdonw'''
        if self.mdd_max < price:
            self.mdd_min = price
            self.mdd_period = 0
            self.mdd_max = price
            self.mdd_price_pair.append([self.mdd_max, self.mdd_min])
            self.mdd_diffs.append(0.0)
            self.mdd_rates.append(0.0)
            self.mdd_periods.append(0)

        if price < self.mdd_min:
            self.mdd_min = price
            self.mdd_price_pair[-1][1] = price
            self.mdd_diffs[-1] = diff=self.mdd_min - self.mdd_max
            self.mdd_rates[-1]= (diff / self.mdd_max * 100.0 )
        if price <= self.mdd_max:
            self.mdd_periods[-1] +=1

    def update_by_position(self, price, position):
        if position is None:
            if self.helper_position== None:
                return

        if self.helper_position != position:
            self.helper_position = position
            #self.update_close_position()
        self.update(price)

    def get_max_drawdown(self):
        if len(self.mdd_rates) == 0: return 0
        return min(self.mdd_rates)

    def get_drawdowns(self):

        return self.mdd_rates

    def save(self):
        dump_inst = {}
        #dump_inst['rate'] = self.mdd_rats

        #dump_inst['diff'] = self.mdd_diffs
        '''
        s_rate=dump_inst['rate']= pd.Series(self.mdd_rates,name='rate')
        s_period=dump_inst['period']=pd.Series(self.mdd_periods,name='period')
        s_diff=dump_inst['diff']= pd.Series(self.mdd_diffs,name = 'diff')

        '''


        df_mdd=pd.DataFrame()
        df_mdd['mdd_rates'] = self.mdd_rates
        df_mdd['mdd_periods'] =self.mdd_periods
        df_mdd['mdd_diffs'] =self.mdd_diffs
        dump_inst['table'] =df_mdd

        return dump_inst

    @staticmethod
    def load(inst):
        mdd_inst = mdd()
        '''
        mdd_inst.mdd_diffs = inst['diff'].values
        mdd_inst.mdd_rates = inst['rate'].values
        mdd_inst.mdd_periods = inst['period'].values
        '''
        df = inst['table']

        for each in df.columns:
            #member_name = each._data[0]
            mdd_inst.__dict__[each] = df[each].values


        return mdd_inst

    def view(self):
        '''
        print 'max draw down:', self.get_max_drawdown()
        print 'drawdown rate:', self.mdd_rates
        print 'drawdown:', self.mdd_diffs
        :return:
        '''

        print 'max draw down:', self.get_max_drawdown()
    def get_info(self):
        return {'max_draw_down': self.get_max_drawdown()}
    pass