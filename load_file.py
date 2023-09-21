import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QObject, QRectF, Qt, QTextStream, QFile
from PySide2.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QTextEdit
from PySide2.QtGui import QPixmap


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.file_Select_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.file_Select_Btn.setGeometry(QtCore.QRect(1082, 80, 121, 28))
        self.file_Select_Btn.setObjectName("file_Select_Btn")
        self.file_Select_Btn.setText("Load Image")
        self.load_text_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.load_text_Btn.setGeometry(QtCore.QRect(1082, 80, 121, 28))
        self.load_text_Btn.setObjectName("load_text_Btn")
        self.load_text_Btn.setText("Load Text")
        self.gridLayout.addWidget(self.file_Select_Btn)
        self.gridLayout.addWidget(self.load_text_Btn)
        MainWindow.setCentralWidget(self.centralWidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)

        # Initialize UI
        self.setupUi(self)
        self.file_Select_Btn.clicked.connect(self.showImage)
        self.load_text_Btn.clicked.connect(self.showText)

    def tr(self, text):
        return QObject.tr(self, text)

    def showImage(self):
        path_to_file, _ = QFileDialog.getOpenFileName(self, self.tr("Load Image"), self.tr("~/Desktop/"), self.tr("Images (*.jpg)"))

        self.image_viewer = ImageViewer(path_to_file)
        self.image_viewer.show()

    def showText(self):
        path_to_file, _ = QFileDialog.getOpenFileName(self,
                                                      self.tr("Load Txt"),
                                                      self.tr("~/Desktop/"),
                                                      self.tr("Plain Text (*.txt)"))

        self.text_viewer = TextViewer(path_to_file)
        self.text_viewer.show()

class ImageViewer(QWidget):
    def __init__(self, image_path):
        super().__init__()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.load_image(image_path)

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.scene.addPixmap(pixmap)
        self.view.fitInView(QRectF(0, 0, pixmap.width(), pixmap.height()), Qt.KeepAspectRatio)
        self.scene.update()

class TextViewer(QWidget):
    def __init__(self, text_path):
        super().__init__()
        self.some_text =  "Este é um texto qualquer."
        fi = QFile(text_path)
        in_stream = QTextStream(fi)
        stri = in_stream.readAll()
        print (stri)
        # print(texto)
        # self.some_text = texto
        #
        self.view = QTextEdit(self.some_text)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
