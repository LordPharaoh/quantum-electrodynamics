import pyqtgraph.opengl as gl


class Main3DView(gl.GLViewWidget):
    def __init__(self):
        super(Main3DView, self).__init__()
        self.addItem(gl.GLAxisItem())
