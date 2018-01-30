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


class Windows(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(50,50, 500,500)
        lat = QtWidgets.QLineEdit(self)
        long = QtWidgets.QLineEdit(self)
        lat.setValidator(QDoubleValidator(60.0, 160.0, 3))
        long.setValidator(QDoubleValidator(20.0, 80.0, 3))
        print(long.text())
        okbut = QtWidgets.QPushButton("OK", self)
        latLabel = QtWidgets.QLabel("Enter Latitude", self)
        longLabel = QtWidgets.QLabel("Enter Longitude", self)
        okbut.move(150,100)
        latLabel.move(20,50)
        longLabel.move(220,50)
        lat.move(100, 50)
        long.move(300, 50)

        self.show()
        okbut.clicked.connect()

        df = self.scrapper(lat.text(), long.text())
        self.mainfunc(df)




    def scrapper(self, lat, long):
        page = requests.get("http://forecast.weather.gov/MapClick.php?lon="+str(-98)+"&lat="+str(47))

        # http: // forecast.weather.gov / MapClick.php?lat = "+str(lat)+" & lon = "+str(long)

        soup = BeautifulSoup(page.content, 'html.parser')
        seven_day = soup.find(id='seven-day-forecast')

        seven_day.find_all('p', {'class': 'period-name'})

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
        for i in range(0,8):
            self.pd.append(QtWidgets.QLabel(df['period'][i], self))
            self.pd[i].move(100 + (i * 150), 200)


        self.temp = []
        for i in range(0,8):
            self.temp.append(QtWidgets.QLabel(df['temperature'][i], self))
            self.temp[i].setFont(QFont('Times New Roman', 16))
            self.temp[i].move(100+(i*150), 300)


        self.sd = []
        self.pic = []
        for i in range(0,8):
            self.sd.append(QtWidgets.QLabel(df['short_desc'][i], self))
            self.sd[i].move(100+(i*150), 550)
            self.pic.append(QtWidgets.QLabel(self))
            if "Cloudy" in df['short_desc'][i]:
                self.pic[i].setPixmap(QPixmap('c3.svg').scaled(115,115, Qt.KeepAspectRatio))

            else:
                if "Rainy" in df['short_desc'][i]:

                    self.pic[i].setPixmap(QPixmap('rainy.png').scaled(115,115, Qt.KeepAspectRatio))
                else:
                    if "Sunny" in df['short_desc'][i]:
                        self.pic[i].setPixmap(QPixmap('sunny.svg').scaled(115,115, Qt.KeepAspectRatio))

            self.pic[i].move(60 + (i * 152), 400)
            self.pic[i].resize(170,170)


        b1.clicked.connect(QCoreApplication.instance().quit)

        self.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win_obj = Windows()
    win_obj.show()
    sys.exit(app.exec_())
