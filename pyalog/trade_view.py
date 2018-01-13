from trade_report import trade_report
import numpy as np

def struct(dict_data,level =0):
    keys = dict_data.keys()

    for each in keys:
        if type(dict_data[each]) == dict:
            print "\t"*level+each
            struct(dict_data[each],level+1)
        else:
            print "\t"*level+each," : ",type(dict_data[each])


def test_struct():
    g={'max drawdown': {'max_draw_down': -0.0091793289910554101},
     'trade': {'trade_mean': -0.019031141868512014, 'trade_std': 0.0, '-trade_num ': 0, '+trade_num ': 0,
               '-trade_std': 0, '+trade_std': 0, '+trade_mean': 0, 'trade_num ': 1, '-trade_mean': 0}}

    struct(g)
    z= {'1':{'4':{'7':{'g':1}}}}
    struct(z)

def check_bband():
    datas= {}
    for i in range(3,61):
        filename = "p"+str(i)+"-1102bband.pickle"
        print "---",filename,"-----"
        report = trade_report.load(filename)
        #datas[i]=report
        #report.view()
        datas[i] = report.get_info()
    print datas
    for i in range (3,61):
        rates = datas[i].rates()
        print 'num', len(rates)," mean: ",np.min(rates)," std:",np.std(rates)

def check_rsi():
    datas= {}
    for i in range(3,61):
        filename = "result/rsi/p"+str(i)+"-1301rsi.pickle"
        print "---",filename,"-----"
        report = trade_report.load(filename)
        #datas[i]=report
        #report.view()
        datas[i] = report.get_info()
        #struct(datas[i])

    struct(datas[3])
    for i in range (3,61):
        data = datas[i]['trade']
        print i,data
#        print "trad: ",data['trade_num '],data['trade_std'],data['trade_mean'],\
#            "+",data['+trade_num '],data['+trade_std'],data['+trade_mean'] ,\
#            "-",data['-trade_num '],data['-trade_std'],data['-trade_mean']

if __name__ == "__main__":
    check_rsi()
