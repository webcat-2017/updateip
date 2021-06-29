import sys
import os
from PyQt5.QtCore import QProcess
import time
import psutil
from ui_updateip import *
class AgentLA(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def check_status(self):
        try:
            status = self.service.status()
            if status == "running":
                self.ui.status.setText("Сервіс\n Запущено!")
                self.ui.status.setStyleSheet("color: rgb(0, 170, 0);")
                self.ui.start.setDisabled(True)
                self.ui.restart.setDisabled(False)
            elif status == "stopped":
                self.ui.status.setText("Сервіс\n Зупинений!")
                self.ui.status.setStyleSheet("color: rgb(255, 0, 0);")
                self.ui.stop.setDisabled(True)
                self.ui.restart.setDisabled(True)
        except:
            pass

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.check_status()
        self.setWindowIcon(QtGui.QIcon("img/icon.png"))
        self.setIconSize(QtCore.QSize(32, 32))
        self.ui.install.clicked.connect(self.install)
        self.ui.start.clicked.connect(self.start)
        self.ui.stop.clicked.connect(self.stop)
        self.ui.restart.clicked.connect(self.restart)

        self.show()

        try:
            self.service = psutil.win_service_get("UpdateIP")
        except Exception:
            self.ui.status.setText("Сервіс\n не встановлений!")
            self.ui.status.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.start.setDisabled(True)
            self.ui.stop.setDisabled(True)
            self.ui.restart.setDisabled(True)
            self.service = False
        if self.service:
            self.check_status()
            self.status = True
            self.ui.install.setText("Видалити")
        else:
            self.status = False
            self.ui.install.setText("Встановити")

    def install(self):
        if self.status:
            QProcess.execute("sc", ["stop", "UpdateIP"])
            QProcess.execute("sc", ["delete", "UpdateIP"])
            self.status = False
            self.ui.install.setText("Встановити")
            self.ui.status.setText("Сервіс\n не встановлений!")
            self.ui.status.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.start.setDisabled(True)
            self.ui.stop.setDisabled(True)
            self.ui.restart.setDisabled(True)
        else:
            path = os.getcwd() + r'\uip_service.exe'
            binpath = "binPath=%s" % path
            QProcess.execute("sc", ["create", "UpdateIP", binpath])
            QProcess.execute("sc", ["config", "UpdateIP", "start=auto"])
            #os.system("sc create AgentLA binPath=%s" % path)
            self.status = True
            self.ui.install.setText("Видалити")
            self.ui.status.setText("Сервіс\n встановлений!")
            self.ui.status.setStyleSheet("color: rgb(0, 170, 0);")
            self.ui.start.setDisabled(False)
            self.ui.stop.setDisabled(True)
            self.ui.restart.setDisabled(True)


    def start(self):
        QProcess.execute("sc", ["start", "UpdateIP"])
        self.ui.status.setText("Сервіс\n Запущено!")
        self.ui.status.setStyleSheet("color: rgb(0, 170, 0);")
        self.ui.start.setDisabled(True)
        self.ui.stop.setDisabled(False)
        self.ui.restart.setDisabled(False)

    def stop(self):
        QProcess.execute("sc", ["stop", "UpdateIP"])
        self.ui.status.setText("Сервіс\n Зупинений!")
        self.ui.status.setStyleSheet("color: rgb(255, 0, 0);")
        self.ui.stop.setDisabled(True)
        self.ui.start.setDisabled(False)
        self.ui.restart.setDisabled(True)

    def restart(self):
        QProcess.execute("sc", ["stop", "UpdateIP"])
        self.ui.status.setText("Сервіс\n Зупинений!")
        self.ui.status.setStyleSheet("color: rgb(255, 0, 0);")
        self.ui.status.repaint()
        time.sleep(3)
        QProcess.execute("sc", ["start", "UpdateIP"])
        self.ui.status.setText("Сервіс\n Запущено!")
        self.ui.status.setStyleSheet("color: rgb(0, 170, 0);")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = AgentLA()
    sys.exit(app.exec_())