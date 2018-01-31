# coding: utf-8

# In[1]:



from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import  *

# len(df['period'])
# type(df['period'])


# In[ ]:


# In[3]:


class Windows1(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.lat = QtWidgets.QLineEdit(self)
        self.long = QtWidgets.QLineEdit(self)
        self.okbut = QtWidgets.QPushButton("OK", self)
        latLabel = QtWidgets.QLabel("Enter Latitude", self)
        longLabel = QtWidgets.QLabel("Enter Longitude", self)
        self.okbut.move(150, 100)
        latLabel.move(20, 50)
        longLabel.move(220, 50)
        self.lat.move(100, 50)
        self.long.move(300, 50)
        self.okbut.clicked.connect(self.on_button_click)
        self.show()

    def on_button_click(self):
        x = self.lat.text()
        y = self.long.text()
        self.dailog = Windows2(x, y)
        self.dailog.show()
        self.close()



class Windows2(QtWidgets.QMainWindow):
    def __init__(self, lat1, long1):
        super().__init__()
        self.setGeometry(50,50, 500,500)

        df = self.scrapper(lat1, long1)
        """lat.text(), long.text()"""
        self.mainfunc(df)




    def scrapper(self, lat2, long2):
        page = requests.get("http://forecast.weather.gov/MapClick.php?lon="+str(long2)+"&lat="+str(lat2))

        # http: // forecast.weather.gov / MapClick.php?lat = "+str(lat)+" & lon = "+str(long)

        soup = BeautifulSoup(page.content, 'html.parser')
        seven_day = soup.find(id='seven-day-forecast')

        seven_day.find_all('p', {'class': 'period-name'})
        # place = soup.find()
        periods = seven_day.select(".period-name")
        periods = [days.get_text() for days in periods]
        short_desc = [sd.get_text() for sd in seven_day.select('.short-desc')]
        temp = [t.get_text() for t in seven_day.select('.temp')]
        img_desc = [im['title'] for im in seven_day.select('img')]

        df = pd.DataFrame({'period': periods, 'short_desc': short_desc, 'temperature': temp, "description": img_desc})

        df['temperature'] = [(x.split(" ")[1] + ' °F') for x in df['temperature']]
        return df

    def mainfunc(self, df):

        self.setWindowTitle('Weather Forecast')
        self.setWindowIcon(QIcon('icon.png'))
        self.bg = QtWidgets.QLabel(self)
        self.bg.resize(2500, 1000)
        self.bg.setStyleSheet("background-image: url(bg12.png);")

        b1 = QtWidgets.QPushButton('Quit', self)
        b1.move(620, 640)
        self.pd =[]
        for i in range(0,9):
            self.pd.append(QtWidgets.QLabel(df['period'][i], self))
            self.pd[i].move(60 + (i * 150), 200)


        self.temp = []
        for i in range(0,9):
            self.temp.append(QtWidgets.QLabel(df['temperature'][i], self))
            self.temp[i].setFont(QFont('Times New Roman', 16))
            self.temp[i].move(60+(i*150), 270)


        self.sd = []
        self.pic = []
        for i in range(0,9):
            self.sd.append(QtWidgets.QLabel(df['short_desc'][i], self))
            self.sd[i].move(60+(i*150), 400)
            self.sd[i].setWordWrap(True)
            self.sd[i].setGeometry(QRect(60+(i*150), 400,100,100))
            self.pic.append(QtWidgets.QLabel(self))
            if "Cloudy" in df['short_desc'][i]:
                self.pic[i].setPixmap(QPixmap('c3.svg').scaled(115,115, Qt.KeepAspectRatio))

            else:
                if "Rainy" in df['short_desc'][i]:

                    self.pic[i].setPixmap(QPixmap('rainy.png').scaled(115,115, Qt.KeepAspectRatio))
                else:
                    if "Sunny" in df['short_desc'][i]:
                        self.pic[i].setPixmap(QPixmap('sunny.svg').scaled(80,80, Qt.KeepAspectRatio))

            self.pic[i].move(40+(i*150), 320)
            self.pic[i].resize(100,100)


        b1.clicked.connect(QCoreApplication.instance().quit)

        self.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win_obj = Windows1()
    win_obj.show()
    sys.exit(app.exec_())
