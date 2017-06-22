from __future__ import division
from xicam.plugins import base
from PySide import QtCore, QtGui
from Main3DView import Main3DView

class QEDPlugin(base.plugin):

    name = 'QED'

    def __init__(self, *args, **kwargs):
        self.centerwidget = QtGui.QStackedWidget()
        self.rightwidget = None
        self.leftwidget = None
        self.bottomwidget = None
        self.toolbbar = None
        self.main_view = Main3DView()
        self.centerwidget.addWidget(self.main_view)
        super(QEDPlugin, self).__init__(*args, **kwargs)


