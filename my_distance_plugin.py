from qgis.PyQt.QtWidgets import QAction, QDialog
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject, QgsDistanceArea, QgsPointXY
from qgis.gui import QgsMapToolEmitPoint
from .ui_distance_dialog import Ui_DistanceDialog

# คลาสสำหรับหน้าต่าง Dialog
class DistanceDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DistanceDialog()
        self.ui.setupUi(self)

# คลาสสำหรับจับจุดที่ผู้ใช้คลิก
class DistanceMapTool(QgsMapToolEmitPoint):
    def __init__(self, canvas, callback):
        super().__init__(canvas)
        self.canvas = canvas
        self.callback = callback

    def canvasReleaseEvent(self, event):
        point = self.toMapCoordinates(event.pos())
        self.callback(point)

# คลาสหลักของปลั๊กอิน
class DistancePlugin:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.action = None
        self.dialog = None
        self.tool = None
        self.points = []

    def initGui(self):
        self.action = QAction(
            QIcon("C:/Users/LENOVO/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/my_distance_plugin/icon.png"),
            "Distance Calculator",
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Distance Calculator", self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&Distance Calculator", self.action)

    def run(self):
        self.dialog = DistanceDialog()
        self.dialog.show()
        self.tool = DistanceMapTool(self.canvas, self.capture_point)
        self.canvas.setMapTool(self.tool)

    def capture_point(self, point):
        self.points.append(point)
        if len(self.points) == 2:
            d = QgsDistanceArea()
            d.setEllipsoid('WGS84')
            dist = d.measureLine(self.points[0], self.points[1]) / 1000
            self.dialog.ui.resultLabel.setText(f"Distance: {dist:.2f} km")
            self.points = []
