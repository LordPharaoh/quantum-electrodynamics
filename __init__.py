import xicam
from xicam.plugins import base
from xicam.plugins import base
from PySide import QtCore, QtGui
from Main3DView import Main3DView

class QEDPlugin(base.plugin):

    name = 'QED'

    def  __init__(self, *args, **kwargs):
        self.centerwidget = QtGui.QStackedWidget()
        self.rightwidget = None
        self.leftwidget = None
        self.bottomwidget = None
        self.toolbbar = None
        self.centerwidget.addWidget(Main3DView())
        super(QEDPlugin, self).__init__(*args, **kwargs)
