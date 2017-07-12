import pyqtgraph as pg
from random import uniform
from geometry import Point
from c_ext.calc_norm import calc_norm
from pipeline import msg
from xicam import threads


class FormGraph(pg.PlotWidget):

    def __init__(self, emitters=None, middles=None, detectors=None, radius=2E-8, index_refraction= 1 - 2.67150153E-3):
        super(FormGraph, self).__init__(title="Form Factor of Sphere with Curved Paths",
                                        bottom="Q Value", left="Probability Density")
        self.index_refraction = index_refraction
        self.sphere_radius = radius

        # initialize emitters
        self.spi = pg.ScatterPlotItem()
        self.addItem(self.spi)

        self.probability_density, self.qz_values, self.qx_values = calc_norm((2E-8, 2E-8), (200, 200), (0, 1), (1, 2000), [[[0, 0, 0], radius, index_refraction]]);

        self.spi.addPoints(self.qz_values, self.probability_density, pen='r')

        """
        self.probability_density, self.qz_values, self.qx_values = calc_norm(self.emitters, self.middles, self.detectors,
                                                                             self.sphere_radius, 1)
        self.spi.addPoints(self.qz_values, self.probability_density, pen='b')
        """
        # self.rit = threads.RunnableIterator(self.iter_calc, callback_slot=self.plot)


    def calc(self):
        self.rit.run()

    def iter_calc(self):
        for d in self.detectors:
            probability_density, q_values = calc_norm(self.emitters, self.middles, (d,),
                                                      self.sphere_radius, self.index_refraction)
            yield probability_density, q_values

    def plot(self, feature):
        # UPDATE: This is never run even though the function itself is called in line 18 of Xi-cam/modpkgs/guiinvoker.py
        print("asdfasdfasdfasdfasdfasdf")
        probability_density, q_values = feature
        self.probability_density.append(probability_density)
        self.q_values.append(q_values)
        self.spi.addPoints(self.q_values, self.probability_density)
        msg.logMessage("added a point")
