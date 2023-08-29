import os

resousepath = os.path.dirname(os.path.abspath(__file__)) + '/resource/qrc/'
# os.system("pyrcc5 \"" + resousepath + "loginQrc.qrc\" -o \"" + resousepath + "loginQrc_rc.py\"")
# os.system("pyrcc5 \"" + resousepath + "mainQrc.qrc\" -o \"" + resousepath + "mainQrc_rc.py\"")

uipath = os.path.dirname(os.path.abspath(__file__)) + '/ui/'
# os.system("pyuic5 \"" + uipath + "login.ui\" --import-from=resource.qrc -o \"" + uipath + "login.py\"")
# os.system("pyuic5 \"" + uipath + "login_log.ui\" --import-from=resource.qrc -o \"" + uipath + "login_log.py\"")
# os.system("pyuic5 \"" + uipath + "login_reg.ui\" --import-from=resource.qrc -o \"" + uipath + "login_reg.py\"")
# os.system("pyuic5 \"" + uipath + "message_success.ui\" --import-from=resource.qrc -o \"" + uipath + "message_success.py\"")
# os.system("pyuic5 \"" + uipath + "main.ui\" --import-from=resource.qrc -o \"" + uipath + "main.py\"")

from PyQt5.QtWidgets import QApplication

from src.login_main import LoginMain

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    Ui_LoginMain = LoginMain()
    Ui_LoginMain.show()
    sys.exit(app.exec_())

