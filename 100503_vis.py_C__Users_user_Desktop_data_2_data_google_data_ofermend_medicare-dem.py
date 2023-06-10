

# Vis module provides matlab-like plotting functions 
#  (as in http://www.mathworks.com/help/matlab/ref/plot.html)

from org.jfree.chart import ChartFactory
from org.jfree.chart import ChartPanel

from org.jfree.chart.plot import PlotOrientation
from org.jfree.chart.plot import XYPlot
from org.jfree.chart.plot import CategoryPlot

#from org.jfree.chart.axis import *

from org.jfree.chart.axis import CategoryAxis
from org.jfree.chart.axis import CategoryLabelPosition
from org.jfree.chart.axis import NumberAxis
from org.jfree.chart.axis import LogarithmicAxis

#from org.jfree.data.xy import *
from org.jfree.data.xy import XYSeries
from org.jfree.data.xy import XYSeriesCollection
from org.jfree.ui import ApplicationFrame
from org.jfree.ui import Layer
from org.jfree.ui import RectangleAnchor
from org.jfree.ui import RefineryUtilities
from org.jfree.ui import TextAnchor

import java.awt.Dimension

__all__ = ['hold', 'plot', 'xlabel', 'ylabel']

_hold = False
def hold(on=True):
    global _hold
    _hold = on

_chart = None
def plot(series, style='line', label=None, logx=False, logy=False):
    global _hold, _chart
    if _hold and _chart:
        try:
            _chart.addSeries(series)
            _chart.plot()
            return
        except: pass # probably chart type does not match

    styles = ['bar', 'hist', 'line', 'scatter']
    if style not in styles:
        raise "Supported chart styles:"+','.join(styles)

    c = None
    if style=='bar':
        c = BarChart(logx=logx,logy=logy)
    elif style=='hist':
        # Not implemented yet :)
        c = Histogram(logx=logx,logy=logy)
        raise "Histogram not supported yet. Please use bar chart"
    elif style=='line':
        c = LineChart(logx=logx,logy=logy)
    elif style in 'scatter':
        c = ScatterPlot(logx=logx,logy=logy)

    c.addSeries(series)
    c.plot()
    _chart = c

class AxisLabel:
    def __init__(self, text):
        self._text = text
    def text(self, label=None):
        if label:
            self._text = label
        return self._text

_xlabel = AxisLabel("x")
xlabel = _xlabel.text

_ylabel = AxisLabel("y")
ylabel = _ylabel.text

class MyChart(ApplicationFrame):
    def __init__(self, title="plot", logx=False, logy=False):
        ApplicationFrame.__init__(self, title)
        self.allSeries = []
        self._size = (800, 600)
        self.logx=logx
        self.logy=logy

    def windowClosing(self, evt):
        if evt.getWindow() == self:
            self.dispose()
        else:
            ApplicationFrame.windowClosing(self, evt)

    def addSeries(self, series, label=None):
        if not label:
            label = "series #"+str(len(self.allSeries)+1)

        xySeries = XYSeries(label)

        iterator = iter(series)
        t = iterator.next()

        if isinstance(t, tuple):
            if len(t) >= 3:
                raise "Series can have at most two columns"
            xySeries.add(t[0], t[1])
            for t in iterator:
                xySeries.add(t[0], t[1])
        else:
            xySeries.add(0, t)
            for i, t in enumerate(iterator):
                xySeries.add(i, t)

        self.allSeries.append(xySeries)

    def plot(self):
        chart = self.createChart()
        plot = chart.getXYPlot()
        if self.logx:
            logx = LogarithmicAxis("Log("+xlabel()+")")
            plot.setDomainAxis(logx)
        if self.logy:
            logy = LogarithmicAxis("Log("+ylabel()+")")
            plot.setRangeAxis(logy)

        chartPanel = ChartPanel(chart)
        chartPanel.setPreferredSize(java.awt.Dimension(self._size[0], self._size[1]))
        self.setContentPane(chartPanel)

        self.pack()
        self.setVisible(True)

class BarChart(MyChart):
    def createChart(self):
        dataset = XYSeriesCollection()
        for s in self.allSeries:
            dataset.addSeries(s)
        # title is None
        chart = ChartFactory.createXYBarChart( \
                    None, xlabel(), False, ylabel(), \
                    dataset, PlotOrientation.VERTICAL, \
                    True, True, False)
        return chart

class Histogram(MyChart):
    pass

class LineChart(MyChart):
    def createChart(self):
        dataset = XYSeriesCollection()
        for s in self.allSeries:
            dataset.addSeries(s)
        # title is None
        chart = ChartFactory.createXYLineChart( \
                    None, xlabel(), ylabel(), \
                    dataset, PlotOrientation.VERTICAL, \
                    True, True, False)
        return chart

class ScatterPlot(MyChart):
    def createChart(self):
        dataset = XYSeriesCollection()
        for s in self.allSeries:
            dataset.addSeries(s)
        # title is None
        chart = ChartFactory.createScatterPlot( \
                    None, xlabel(), ylabel(), \
                    dataset, PlotOrientation.VERTICAL, \
                    True, True, False)
        return chart
