from __future__ import division
from xicam.plugins import base
from PySide import QtCore, QtGui
from Main3DView import Main3DView
from form_graph import FormGraph


class QEDPlugin(base.plugin):

    name = 'QED'

    def __init__(self, *args, **kwargs):
        self.centerwidget = QtGui.QStackedWidget()
        self.rightwidget = None
        self.bottomwidget = None
        self.toolbbar = None
        #self.main_view = Main3DView()
        self.form_graph = FormGraph()
        # self.centerwidget.addWidget(self.main_view)
        self.centerwidget.addWidget(self.form_graph)
        super(QEDPlugin, self).__init__(*args, **kwargs)


    def openfiles(self, files, operation=None, operationname=None):
        self.form_graph.calc()
