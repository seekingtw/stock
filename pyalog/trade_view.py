from trade_report import trade_report

if __name__ == "__main__":
    for i in range(3,61):
        filename = "p"+str(i)+"-1102bband.pickle"
        print "---",filename,"-----"
        report = trade_report.load(filename)
        report.view()