import sys
from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication

# https://stackoverflow.com/questions/63102395/displaying-web-page-with-pyqt5-webengine
#
# https://codeloop.org/python-how-to-make-browser-in-pyqt5-with-pyqtwebengine/

app = QApplication(sys.argv)

web = QWebEngineView()

# web.load(QUrl("file:///C:/Users/mmaduar/PycharmProjects/OGRaySpY/src/my_file.html"))
web.load(QUrl("file:///C:/Users/mmaduar/PycharmProjects/OGRaySpY/src/gross_counts_graph.html"))

web.show()

sys.exit(app.exec_())