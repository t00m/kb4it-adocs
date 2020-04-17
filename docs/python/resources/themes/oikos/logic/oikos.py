import csv
import math

class Oikos:
    """Get data and generate all needed info from oikos.csv"""
    tx = {}
    report = {}

    def __init__(self, csvfile):
        self.csvfile = csvfile
        self.get_data()
        self.analyze()

    def get_data(self):
        data = {}
        with open(self.csvfile, newline='') as fcsv:
            n = 0
            sheet = csv.reader(fcsv, delimiter=',', quotechar='\"')
            for row in sheet:
                if n > 0:
                    oid = row[0]
                    self.tx[oid] = {}
                    self.tx[oid]['date'] = row[1]
                    self.tx[oid]['place'] = row[2]
                    self.tx[oid]['title'] = row[3]
                    self.tx[oid]['type'] = row[4]
                    self.tx[oid]['category'] = row[5]
                    self.tx[oid]['fromto'] = row[6]
                    self.tx[oid]['amount'] = float(row[7])
                n += 1

    def analyze(self):
        self.report['balance'] = {}
        self.report['balance']['all'] = 0
        self.report['balance']['year'] = {}
        self.report['balance']['month'] = {}
        self.report['balance']['incomes'] = 0
        self.report['balance']['expenses'] = 0
        self.report['incomes'] = {}
        self.report['incomes']['year'] = {}
        self.report['incomes']['month'] = {}
        self.report['expenses'] = {}
        self.report['expenses']['year'] = {}
        self.report['expenses']['month'] = {}
        self.report['places'] = {}
        self.report['years'] = set()
        self.report['months'] = set()

        for oid in self.tx:
            tx = self.tx[oid]
            tx_amount = tx['amount']
            tx_date = tx['date']
            tx_place = tx['place']

            # Get year and month and save them
            tx_year = tx['date'][:4]
            self.report['years'].add(tx_year)
            tx_month = tx['date'][:7]
            self.report['months'].add(tx_month)

            # Accumulated incomes and expenses
            if tx_amount >= 0:
                self.report['balance']['incomes'] += tx_amount
            else:
                self.report['balance']['expenses'] += tx_amount

            # Update total
            self.report['balance']['all'] += tx_amount

            # Type of transaction
            if tx_amount >= 0:
                tx_type = 'incomes'
            else:
                tx_type = 'expenses'

            # Places
            # ~ try:
                # ~ txs = self.report['places'][tx_place]
                # ~ txs.append(oid)
                # ~ self.report['places'][tx_place] = txs
            # ~ except:
                # ~ self.report['places'][tx_place] = [oid]


            # Update yearly incomes
            try:
                total_year = self.report[tx_type]['year'][tx_year]
                total_year += tx_amount
                self.report[tx_type]['year'][tx_year] = total_year
            except:
                total_year = tx_amount
                self.report[tx_type]['year'][tx_year] = total_year

            # Update monthly incomes/expenses
            try:
                total_month = self.report[tx_type]['month'][tx_month]
                total_month += tx_amount
                self.report[tx_type]['month'][tx_month] = total_month
            except:
                total_month = tx_amount
                self.report[tx_type]['month'][tx_month] = total_month

        for year in sorted(list(self.report['years'])):
            try:
                incomes_year = self.report['incomes']['year'][year]
            except:
                incomes_year = 0

            try:
                expenses_year = self.report['expenses']['year'][year]
            except:
                expenses_year = 0

            self.report['balance']['year'][year] = incomes_year + expenses_year

        # ~ past_month = 0
        # ~ for month in sorted(list(self.report['months'])):
            # ~ try:
                # ~ self.report['partial']['month'][month]
            # ~ except:
                # ~ self.report['partial']['month'][month] = 0

            # ~ try:
                # ~ incomes = self.report['incomes']['month'][month]
            # ~ except:
                # ~ incomes = 0

            # ~ try:
                # ~ expenses = self.report['expenses']['month'][month]
            # ~ except:
                # ~ expenses = 0

            # ~ cur_month = incomes + expenses
            # ~ self.report['partial']['month'][month] = cur_month + past_month
            # ~ past_month = self.report['partial']['month'][month]





    def get_report(self):
        return self.report

    def get_transactions(self):
        return self.tx











