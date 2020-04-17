#!/usr/bin/env/python3

import os
from datetime import datetime, timedelta
from datetime import date
import pygal
from pygal import Config
from pygal import Pie
from pygal.style import Style
from pprint import pprint

# FIXME: Tooltips missing when network connection is not available
# Solution: copy pygal-tooltips.js to target dir
# Via: https://stackoverflow.com/questions/36322683/pygal-charts-not-displaying-tooltips-in-jupyter-ipython-notebook#45813876

class Charts:

    def get_default_chart_style(self):
        custom_style = Style(
            title_font_size = 18,
            label_font_size = 10,
            major_label_font_size = 12,
            value_font_size = 10,
            value_label_font_size = 10,
            tooltip_font_size = 14,
            legend_font_size = 12,
            no_data_font_size = 10,
            background = 'transparent'
        )

        return custom_style


    def get_default_chart_config(self):
        config = Config()
        config.show_legend = True
        config.legend_at_bottom = True
        config.print_values = True
        config.print_values_position = 'top'
        config.print_labels = True
        config.height = 400
        config.dynamic_print_values = True
        config.human_readable = True
        config.fill = True
        config.js = [] # pygal-tooltip.js inserted in HTML_FOOTER.tpl
        # ~ config.js = ['pygal-tooltips.js']
        # ~ config.js = ['http://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.js']

        return config

    def build_stats_expenses(self, amounts):
        CHART_FILE = 'chart_amounts_per_expenses.svg'
        custom_style = self.get_default_chart_style()
        config = self.get_default_chart_config()
        pie_chart = pygal.HorizontalBar(config, style=custom_style)
        pie_chart.legend_box_size=18
        pie_chart.title = 'Incomes and expenses per category'
        for category in amounts:
            if amounts[category] < 0:
                pie_chart.add(category,
                [{
                    'value': abs(amounts[category]),
                    'label': get_operation_type(category),
                    'xlink': 'http://en.wikipedia.org/wiki/First'
                }])

                # ~ pie_chart.add(get_operation_type(category), abs(amounts[category], 'xlink': 'http://en.wikipedia.org/wiki/First'))
        pie_chart.render_to_file(CHART_FILE)


    def build_stats_categories(self, amounts):
        CHART_FILE = 'chart_amounts_per_category.svg'
        custom_style = self.get_default_chart_style()
        config = self.get_default_chart_config()
        pie_chart = pygal.HorizontalBar(config, style=custom_style)
        pie_chart.legend_box_size=18
        #~ pie_chart.width = 300
        pie_chart.title = 'Incomes and expenses per category'
        for category in amounts:
            pie_chart.add(get_operation_type(category), abs(amounts[category]))
        pie_chart.render_to_file(CHART_FILE)


    def build_stats_total(self, incomes, expenses):
        CHART_FILE = '/tmp/chart_total_incomes_expenses.svg'
        custom_style = self.get_default_chart_style()
        config = self.get_default_chart_config()
        pie_chart = pygal.Bar(config, style=custom_style)
        pie_chart.legend_box_size=18
        pie_chart.title = ''

        pie_chart.add("Expenses: %10.2f €" % abs(expenses),
        [{
            'value': abs(expenses),
            # ~ 'label': 'Expenses: %10.2f €' % abs(expenses),
            'xlink': {
                'href': 'expenses.html',
                'target': '_self'}
        }])

        pie_chart.add("Incomes: %10.2f €" % abs(incomes),
        [{
            'value': abs(incomes),
            # ~ 'label': 'Incomes: %10.2f €' % abs(incomes),
            'xlink': {
                'href': 'incomes.html',
                'target': '_self'}
        }])
        pie_chart.render_to_file(CHART_FILE)
        return pie_chart.render()

    def build_stats_total_available_per_year(self, data):
        custom_style = self.get_default_chart_style()
        config = self.get_default_chart_config()
        CHART_FILE = '/tmp/chart_available_per_year.svg'
        items = []
        labels = []
        maxqty = 0
        for adate, qty in data:
            labels.append(adate)
            items.append((adate, qty))
            if qty > maxqty:
                maxqty = qty
            # ~ print ("%s\t%10.2f" % (adate.strftime("%Y"), qty))
        dateline = pygal.DateLine(config, style=custom_style, x_label_rotation=25, range=(-maxqty, maxqty*2))
        labels.sort()
        items.sort()
        # ~ print ("Labels: %s" % labels)
        # ~ print ("Items: %s" % items)
        dateline.x_labels = labels
        dateline.add("Serie", items)
        dateline.render_to_file(CHART_FILE)
        return dateline.render()


    def build_stats_total_available_per_month(self, data):
        custom_style = self.get_default_chart_style()
        config = self.get_default_chart_config()
        CHART_FILE = '/tmp/chart_available_per_month.svg'
        items = []
        labels = []
        maxqty = 0
        for adate, qty in data:
            labels.append("") #(adate.strftime("%b %Y"))
            items.append((adate, qty))
            if qty > maxqty:
                maxqty = qty
        dateline = pygal.DateLine(config, style=custom_style, x_label_rotation=25, range=(-1*maxqty/2, maxqty))
        labels.sort()
        items.sort()
        dateline.x_labels = labels
        dateline.add("Available per month", items)
        dateline.render_to_file(CHART_FILE)
        return dateline.render()

    def all_transactions(self, txs):
        custom_style = self.get_default_chart_style()
        config = self.get_default_chart_config()
        CHART_FILE = '/tmp/chart_all_transactons.svg'
        items = []
        labels = []
        maxqty = 0
        diff = 0
        days = set()
        tmp = {}
        for oid in txs:
            tx = txs[oid]
            adate = datetime.strptime(tx['date'], "%Y.%m.%d")
            # ~ adate = tx['date']
            days.add(adate)
            amount = tx['amount']
            try:
                diff = tmp[adate]
                tmp[adate] = diff + amount
            except:
                tmp[adate] = amount

        diff = 0
        for day in sorted(list(days)):
            focm = day.replace(day=1) # First day of this month
            ldpm = focm - timedelta(days=1)
            # ~ print(ldpm)
            amount = tmp[day]
            diff += amount
            labels.append("")
            items.append((day, diff))
            if diff > maxqty:
                maxqty = diff
        dateline = pygal.DateLine(config, style=custom_style, x_label_rotation=25, range=(-500, 1.5*maxqty))
        labels.sort()
        items.sort()
        dateline.x_labels = labels
        dateline.add("Incomes & Expenses evolution", items)
        dateline.render_to_file(CHART_FILE)
        return dateline.render()

    # ~ def build_incomes_per_year(self, report):
        # ~ incomes = report['incomes']
        # ~ custom_style = self.get_default_chart_style()
        # ~ config = self.get_default_chart_config()
        # ~ chart = pygal.Bar(config, style=custom_style)
        # ~ chart.title = 'Incomes'
        # ~ items = []
        # ~ for year in sorted(list(report['years'])):
            # ~ chart.add(year,
            # ~ [{
                # ~ 'value': abs(incomes['year'][year]),
                # ~ 'label': '%10.2f €' % abs(incomes['year'][year]),
                # ~ 'xlink': {
                    # ~ 'href': 'incomes_%s.html' % year,
                    # ~ 'target': '_self'}
            # ~ }])
        # ~ return chart.render()

    def build_incomes_per_year(self, report):
        incomes = report['incomes']
        custom_style = self.get_default_chart_style()
        config = self.get_default_chart_config()
        chart = pygal.DateLine(config, style=custom_style)
        items = []
        years = sorted(list(report['years']))
        for year in years:
            adate = datetime.strptime("%s" % year, "%Y")
            items.append((adate, incomes['year'][year]))
        chart.x_labels_major = years
        chart.add("Incomes", items)
        return chart.render()

    def build_incomes(self, report):
        custom_style = self.get_default_chart_style()
        config = self.get_default_chart_config()
        chart = pygal.DateLine(config, style=custom_style)
        months = sorted(list(report['months']))
        items = []
        pprint(report['incomes']['month'])
        for month in months:
            adate = datetime.strptime(month, "%Y.%m")
            items.append((adate, report['incomes']['month'][month]))
        chart.x_labels_major = months
        chart.add("Incomes", items)
        return chart.render()