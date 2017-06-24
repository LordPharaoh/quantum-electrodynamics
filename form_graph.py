import pyqtgraph as pg
from random import uniform
from geometry import Point
from calc_norm import calc_norm
from pipeline import msg
from xicam import threads

class FormGraph(pg.PlotWidget):

    def __init__(self, emitters=None, middles=None, detectors=None, radius=2E-8, index_refraction=1 + 2.67150153E-6):
        super(FormGraph, self).__init__(title="Form Factor of Sphere with Curved Paths",
                                        bottom="Q Value", left="Probability Density")
        self.index_refraction = index_refraction
        self.sphere_radius = radius

        # initialize emitters
        if emitters is None:
            self.emitters = [Point(0, -16, 0)]
        else:
            self.emitters = emitters
        if middles is None:
            self.middles = [Point(1E-20, 0, uniform(-1.5E-8, 1.5E-8)) for i in range(10)]
        else:
            self.middles = middles
        if detectors is None:
            # self.detectors = [Point(uniform(-4, 4), 10, uniform(-4, 4)) for i in range(10)]
            self.detectors = sorted([Point(0,  4, i*1E-7) for i in range(10)], key=lambda x: x.z)
        else:
            self.detectors = detectors

        # msg.logMessage("PROBABILITIES:" + str(self.probability_density))
        # msg.logMessage("Q VALUES:" + str(self.q_values))
        # msg.logMessage("DETECTORS:" + str(self.detectors))

        self.spi = pg.ScatterPlotItem()
        self.addItem(self.spi)


    def calc(self):# calculate and sum times for each path
        calcthread = threads.iterator(callback_slot=self.displayfeature)(self.loop_prob)
        calcthread()
        # features = list(self.loop_prob())
        # for feature in features:
        #     self.displayfeature(feature)

        self.probability_density = []
        self.q_values = []


    # TODO: Is iterator being run?
    # TODO: Is callback being called?

    def loop_prob(self):
        for d in self.detectors:
            probability_density, q_values = calc_norm(self.emitters, self.middles, (d,),
                                                      self.sphere_radius, self.index_refraction)
            yield probability_density,q_values

    def displayfeature(self,feature):
        probability_density, q_values = feature
        self.probability_density.append(probability_density)
        self.q_values.append(q_values)
        self.spi.addPoints(self.q_values, self.probability_density)
        msg.logMessage("added a point")


