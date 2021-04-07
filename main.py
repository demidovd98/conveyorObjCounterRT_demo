##### Comments:
'''
# pyuic5 design.ui -o design.py

# pyinstaller --onefile -w main.py
'''
#-#-#


##### Imports:

### Video parsing:
import cv2 as cv # OpenCV
#import numpy as np
import FrameProcessor # Наш python файл с обработкой видео

### GUI:
from PyQt5 import QtWidgets, QtGui, QtCore #PyQT5
from PyQt5.QtWidgets import QTableWidgetItem
#from PyQt5 import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem ?

import design  #Наш конвертированный файл дизайна
from design import Ui_MainWindow  # Наш сгенерированный файл дизайна

### General:
# Time:
#import time
#from time import time
#from datetime import timedelta

# Additional GUI:
import sys  #Для передачи argv в QApplication
import os # Для отображения содержимого директории

#-#-#


##### Variables + Initialisations:

### Global variables list:
global prodList, prodListNumb, \
       prodOld, prodCurr

# GUI:
prodList = [] #Массив типов продукции
prodListNumb = 0 #Количество типов продукции

prodOld = ''
prodCurr = ''

#-#-# 


##### Classes:

### Вставка обработанного видео:
    # Адаптировано из ответа на вопрос https://stackoverflow.com/questions/39303008/load-an-opencv-video-frame-by-frame-using-pyqt
class VideoCapture(QtWidgets.QWidget):
    def __init__(self, filename, parent):
        #super(QtWidgets.QWidget, self).__init__()
        super(VideoCapture, self).__init__(parent)
        self.cap = cv.VideoCapture(str(filename))
        self.video_frame = QtWidgets.QLabel()
        parent.layout.addWidget(self.video_frame)
                
    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        if ret == True:
            isRet = True
            frame = FrameProcessor.FrameProcess(frame, isRet)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap.fromImage(img)
            self.video_frame.setPixmap(pix)
        else:
            isRet = False
            FrameProcessor.FrameProcess(frame, isRet)

        #else:
            #return 0

    def start(self, parent):
        # Timer for Frame update:
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(30) # Warning float => int ???

        # Timer for Text update:
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(parent.changeText)
        self.timer2.start(30) # Warning float => int ???

    def pause(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(QtWidgets.QWidget, self).deleteLater()


### Шаблон экрана:
class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        global tableIsObjectData

        # Для доступа к переменным, методам и т.д. в файле design.py
        super(ExampleApp, self).__init__()
        self.setupUi(self)  # Для инициализации нашего дизайна
        
        # Инициализация переменных:
        FrameProcessor.Initialize() # Переход на файл с обработкой видео


        ### Собственные привязки в GUI:
        # Кнопки:
        self.btnStart.clicked.connect(self.startCount) #Начать счёт
        self.btnStop.clicked.connect(self.stopCount) #Остановить счёт
        
        self.btnEnCalibrParam.clicked.connect(self.showParamList) #Показать/Скрыть параметры калибровки
        self.btnCatalog.clicked.connect(self.updateProdList) #Обновить каталог(В будущем открыть каталог) 

        # Строки:
        #self.numberProductInBox.setFont(QtGui.QFont('SansSerif', 30)) # Изменение шрифта и размера
        #self.numberProductCons.setFont(QtGui.QFont('SansSerif', 20)) # Изменение шрифта и размера
        #self.numberProductAll.setFont(QtGui.QFont('SansSerif', 15)) # Изменение шрифта и размера
        #self.timer.setFont(QtGui.QFont('SansSerif', 20)) # Изменение шрифта и размера
        #self.label.setGeometry(QtCore.QRect(10, 10, 200, 200)) # Размеры

        # Таблицы:
        self.tableIsObject.clear() # Очистить ячейки таблицы
        tableIsObjectData = ['hi', 'hi'] # Подготовка данных для ввода в таблицу
        for id,text in enumerate(tableIsObjectData): # Ввод данных в таблицу
                    # Enumerate - Индексирование (id) элементов списка (text)
            text = str(text) # Преобразование в текст (т. к. enumerate преобразует текст в последоват-ть знаков)
            item = QTableWidgetItem(text) # item = значение text в текущем id
            self.tableIsObject.setItem(0, id, item) # Присваивание item в ячейку таблицы

        self.tableIsNoise.clear() # Очистить ячейки таблицы
        tableIsNoiseData = ['hi', 'hi'] # Подготовка данных для ввода в таблицу
        for id,text in enumerate(tableIsNoiseData): # Ввод данных в таблицу
                    # Enumerate - Индексирование (id) элементов списка (text)
            text = str(text) # Преобразование в текст (т. к. enumerate преобразует текст в последоват-ть знаков)
            item = QTableWidgetItem(text) # item = значение text в текущем id
            self.tableIsNoise.setItem(0, id, item) # Присваивание item в ячейку таблицы

        self.tableZoneCount.clear() # Очистить ячейки таблицы
        tableZoneCountData = [['hi', 'hi'], 
                              ['hi', 'hi']] # Подготовка данных для ввода в таблицу
        for id1,text1 in enumerate(tableZoneCountData): # Ввод данных в таблицу
                    # Enumerate - Индексирование (id) элементов списка (text)
                for id2,text2 in enumerate(text1): # Ввод данных в таблицу
                            # Enumerate - Индексирование (id) элементов списка (text)
                    text2 = str(text2) # Преобразование в текст (т. к. enumerate преобразует текст в последоват-ть знаков)
                    item = QTableWidgetItem(text2) # item = значение text в текущем id
                    self.tableZoneCount.setItem(id1, id2, item) # Присваивание item в ячейку таблицы

        self.tableZoneRef.clear() # Очистить ячейки таблицы
        tableZoneRefData = ['hi', 'hi', 'hi'] # Подготовка данных для ввода в таблицу
        for id,text in enumerate(tableZoneRefData): # Ввод данных в таблицу
                    # Enumerate - Индексирование (id) элементов списка (text)
            text = str(text) # Преобразование в текст (т. к. enumerate преобразует текст в последоват-ть знаков)
            item = QTableWidgetItem(text) # item = значение text в текущем id
            self.tableZoneRef.setItem(0, id, item) # Присваивание item в ячейку таблицы

        self.tableRefColourBord.clear() # Очистить ячейки таблицы
        tableRefColourBordData = [['hi', 'hi', 'hi'], 
                                  ['hi', 'hi', 'hi']] # Подготовка данных для ввода в таблицу
        for id1,text1 in enumerate(tableRefColourBordData): # Ввод данных в таблицу
                    # Enumerate - Индексирование (id) элементов списка (text)
                for id2,text2 in enumerate(text1): # Ввод данных в таблицу
                            # Enumerate - Индексирование (id) элементов списка (text)
                    text2 = str(text2) # Преобразование в текст (т. к. enumerate преобразует текст в последоват-ть знаков)
                    item = QTableWidgetItem(text2) # item = значение text в текущем id
                    self.tableRefColourBord.setItem(id1, id2, item) # Присваивание item в ячейку таблицы


        ### Запуск функций для инициализации окна GUI:
        self.updateProdList()
        self.changeText()

        # Скрыть параметры калибровки:
        self.showParamList()


        ### Инициализация видеофрейма:
        self.videoFileName = "cutted.avi"
        self.capture = None        
        self.startCapture()


    def changeText(self):
        global tableIsObjectData
        
        ### Обновить текст в GUI:
        # Получить текст из файла FrameProcessor:
        guiVars = FrameProcessor.GetVariable()
        '''
        print (guiVars) # For debugging
        '''

        # Обновить текст в окнах:
        self.numberProductInBox.setText(str(guiVars[0])) # Количество продукта в коробке
        self.numberProductCons.setText(str(guiVars[1])) # Количество продукта в партии
        self.numberProductAll.setText(str(guiVars[2])) # Количество продукта всего
        self.timer.setText(str(guiVars[3])) # Время с момента запуска программы

        self.numberPixels.setText(str(guiVars[4])) # Количество "белых" пикселей
        self.refColourHSV.setText(str(guiVars[5])) # Опорный цвет (HSV)


        # Обновить текст в таблицах:
        #Порог наличия объекта:
        self.tableIsObject.setItem(0, 0, QTableWidgetItem(str(guiVars[6])))
        self.tableIsObject.setItem(0, 1, QTableWidgetItem(str(guiVars[7])))

        #Порог наличия шумов:
        self.tableIsNoise.setItem(0, 0, QTableWidgetItem(str(guiVars[8])))
        self.tableIsNoise.setItem(0, 1, QTableWidgetItem(str(guiVars[9])))

        #Положение Зоны подсчёта:
        for id1,text1 in enumerate(guiVars[10]): # Ввод данных в таблицу
                    # Enumerate - Индексирование (id) элементов списка (text)
                for id2,text2 in enumerate(text1): # Ввод данных в таблицу
                            # Enumerate - Индексирование (id) элементов списка (text)
                    text2 = str(text2) # Преобразование в текст (т. к. enumerate преобразует текст в последоват-ть знаков)
                    item = QTableWidgetItem(text2) # item = значение text в текущем id
                    self.tableZoneCount.setItem(id1, id2, item) # Присваивание item в ячейку таблицы

        #Положение Опорной зоны
        self.tableZoneRef.setItem(0, 0, QTableWidgetItem(str(guiVars[11])))
        self.tableZoneRef.setItem(0, 1, QTableWidgetItem(str(guiVars[12])))
        self.tableZoneRef.setItem(0, 2, QTableWidgetItem(str(guiVars[13])))

        
        #Границы опорного цвета:
        for id,text in enumerate(guiVars[14]): # Ввод данных в таблицу
                    # Enumerate - Индексирование (id) элементов списка (text)
            text = str(text) # Преобразование в текст (т. к. enumerate преобразует текст в последоват-ть знаков)
            item = QTableWidgetItem(text) # item = значение text в текущем id
            self.tableRefColourBord.setItem(0, id, item) # Присваивание item в ячейку таблицы

        for id,text in enumerate(guiVars[15]): # Ввод данных в таблицу
                    # Enumerate - Индексирование (id) элементов списка (text)
            text = str(text) # Преобразование в текст (т. к. enumerate преобразует текст в последоват-ть знаков)
            item = QTableWidgetItem(text) # item = значение text в текущем id
            self.tableRefColourBord.setItem(1, id, item) # Присваивание item в ячейку таблицы
            

        ### Текущий выбранный продукт:
        global prodList, prodListNumb, \
            prodCurr, prodOld  
        prodOld = prodCurr
        prodCurr = self.listProduct.currentText() #Текущий выбранный из списка в GUI (listProduct) продукт
        '''
        print (prodCurr) # For debugging
        '''


    def startCapture(self):
        if not self.capture: 
            self.capture = VideoCapture(self.videoFileName, self.videoContainer)
        self.capture.start(self)


    def updateProdList(self): # Обновить список типов продукции:
        global prodList, prodListNumb, \
            prodCurr, prodOld        
    
        #directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'IDlist directory', 'IDlist/')
        directory = os.getcwd() + '\prodList' #Выбор директории расположения списка продукции:
            #Текущая директория скрипта + \папка хранения файлов продукции

        #if directory:  # не продолжать выполнение, если нет директории (Что-то проверить)
        prodList.clear() #Очистка массива типов продукции (от старого и на всякий случай)
        self.listProduct.clear() # Очистка списка типов продукции в GUI (listProduct - из design.py) (от старого и на всякий случай)
        
        for file_name in os.listdir(directory):  #Для каждого файла в директории
            x = file_name
            x = x.partition('.')[0]
            prodList.append(x)
            self.listProduct.addItem(x)

        prodListNumb = len(prodList) # Количество найденных типов продуктов

        self.changeText()
        
        #prodOld = prodCurr
        #prodCurr = self.listProduct.currentText() #Текущий выбранный из списка в GUI (listProduct) продукт

        #currN = self.listID.currentIndex() #Номер выбранного продукта (порядковый номер из списка)
        #print (prodList[currN])

        '''
        print (prodListNumb) #For debugging
        print (prodList) #For debugging
        print (prodCurr) #For debugging
        '''

        #curr = IDlist[self.listID.currentIndex()]
        #curr = IDlist[currN]
        #print (curr)



    def showParamList(self): # Показать/Скрыть панель параметров калибровки
        if self.btnEnCalibrParam.isChecked():
            self.tableIsObject.show()
            self.label_10.show()
            self.tableZoneCount.show()
            self.label_17.show()
            self.tableRefColourBord.show()
            self.label_18.show()
            #
            self.label_16.show()
            self.tableIsNoise.show()
            self.label_11.show()
            self.tableZoneRef.show()
            self.label_13.show()
            self.numberPixels.show()
            self.label_12.show()
            self.refColourHSV.show()
        else:
            self.tableIsObject.hide()
            self.label_10.hide()
            self.tableZoneCount.hide()
            self.label_17.hide()
            self.tableRefColourBord.hide()
            self.label_18.hide()
            #
            self.label_16.hide()
            self.tableIsNoise.hide()
            self.label_11.hide()
            self.tableZoneRef.hide()
            self.label_13.hide()
            self.numberPixels.hide()
            self.label_12.hide()
            self.refColourHSV.hide()

        self.adjustSize()
        

    def startCount(self): # Начать счёт

        self.adjustSize()

        #self.adjustSize()
        #return 0


    def stopCount(self): # Остановка по введённому коду
        #self.widget.show()
        self.centralwidget.adjustSize()


        return 0

        #sys.exit()
        
#-#-#


##### Main:
     
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    #window.setWindowTitle("ОмБекон: Счёт продукции, конвейер №х")
    window.show()  # Показываем окно
    window.inputProductNumber.setFocus()

    #adjustSize()

    sys.exit(app.exec_()) # и запускаем приложение ???

#-#-#
    
    
##### Доп штуки:

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

def keyPressEvent(self, e): # НЕ РАБОТАЕТ
    if e.key() == Qt.Key_F12:
        self.close()

#-#-#
