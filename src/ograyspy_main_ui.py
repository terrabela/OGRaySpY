import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *

from ograyspy_class import Ograyspy
# from html_window_class import SimpleHtmlViewer

class MainWindow(QMainWindow):
    count = 0

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mdi = QMdiArea()

        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdi)

        # self.mdi.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        # self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.setCentralWidget(self.mdi)
        bar = self.menuBar()

        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("Open")
        file.addAction("Show spectrum graphic")
        file.addAction("Show Pandas dataframe")
        file.addAction("cascade")
        file.addAction("Tiled")
        file.addAction("Exit")
        file.triggered[QAction].connect(self.windowaction)
        self.setWindowTitle("MDI demo")

    def windowaction(self, q):
        print("triggered")

        if q.text() == "New":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("subwindow" + str(MainWindow.count))
            self.mdi.addSubWindow(sub)
            sub.show()

        if q.text() == "Open":
            fileName, _ = QFileDialog.getOpenFileName(self)
            if fileName:
                # This is a hack...
                # existing = self.findMdiChild(fileName)
                existing = True
                if existing:
                    MainWindow.count = MainWindow.count + 1
                    sub = QMdiSubWindow()
                    sub.setWidget(QTextEdit())
                    # sub.setWindowTitle("subwindow" + str(MainWindow.count))
                    sub.setWindowTitle(fileName)
                    self.mdi.addSubWindow(sub)
                    sub.show()

                    ogra = Ograyspy(batch_mode=False)
                    # to_be_found = 'Genie_Transfer'
                    # print('\nogra.define_files_folder(to_be_found)')
                    # ogra.define_files_folder(to_be_found)
                    ogra.a_spec_name = fileName
                    # AQUI: ativar gener_dataframe qdo estiver pronto.
                    ogra.perform_total_analysis(peak_sd_fact=3.0, gener_dataframe=True)
                    ogra.a_spec.spec_pks_df.to_html(buf='an_html_file.html')
                    # print(ogra.a_spec.spec_pks_df)
                    ogra.call_graphics()

        if q.text() == "Show spectrum graphic":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()
            web = QWebEngineView()
            web.load(QUrl("file:///C:/Users/mmaduar/PycharmProjects/OGRaySpY/src/gross_counts_graph.html"))
            sub.setWidget(web)
            sub.setWindowTitle("subwindow" + str(MainWindow.count))
            self.mdi.addSubWindow(sub)
            sub.show()

        if q.text() == "Show Pandas dataframe":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()
            web = QWebEngineView()
            web.load(QUrl("file:///C:/Users/mmaduar/PycharmProjects/OGRaySpY/src/my_file.html"))
            # 2022-Dez-23 PAREI AQUI - passar a saída de to_html como string
            # web.load(ogra.dataframe_html_string)
            sub.setWidget(web)
            sub.setWindowTitle("subwindow" + str(MainWindow.count))
            self.mdi.addSubWindow(sub)
            sub.show()

        if q.text() == "cascade":
            self.mdi.cascadeSubWindows()

        if q.text() == "Tiled":
            self.mdi.tileSubWindows()

        if q.text() == "Exit":
            QApplication.instance().exit()

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
