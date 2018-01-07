from trade_report import trade_report

if __name__ == "__main__":
    report = trade_report.load('1234.pickle')
    report.view()