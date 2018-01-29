# coding: utf-8

# In[1]:



from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

# len(df['period'])
# type(df['period'])


# In[ ]:


# In[3]:


class Windows(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        df = self.scrapper()
        self.mainfunc(df)



    def scrapper(self):




        page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")



        soup = BeautifulSoup(page.content, 'html.parser')
        seven_day = soup.find(id='seven-day-forecast')
        #tombstone = seven_day.find_all(class_='tombstone-container')



        #overnight = tombstone[1].find('p', {'class': 'period-name'}).get_text()
        #shortdesc = tombstone[1].find(class_='short-desc').get_text()
        #temp = tombstone[1].find(class_='temp').get_text()

        #img = tombstone[1].find("img")['title']

        # To distinguish oen tab from other if it ahs multiple attributes like class/id/etc
        # seven_day.find_all('p',{'class':'period-name','extra':'attributes'})
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
        self.setWindowIcon(QtGui.QIcon('icon.png'))
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
            self.temp[i].setFont(QtGui.QFont('Times New Roman', 16))
            self.temp[i].move(100+(i*150), 300)


        self.sd = []
        self.pic = []
        for i in range(0,8):
            self.sd.append(QtWidgets.QLabel(df['short_desc'][i], self))
            self.sd[i].move(100+(i*150), 550)
            self.pic.append(QtWidgets.QLabel(self))
            if "Cloudy" in df['short_desc'][i]:
                self.pic[i].setPixmap(QtGui.QPixmap('c3.svg').scaled(115,115, QtCore.Qt.KeepAspectRatio))

            else:
                if "Rainy" in df['short_desc'][i]:

                    self.pic[i].setPixmap(QtGui.QPixmap('rainy.png').scaled(115,115, QtCore.Qt.KeepAspectRatio))
                else:
                    if "Sunny" in df['short_desc'][i]:
                        self.pic[i].setPixmap(QtGui.QPixmap('sunny.svg').scaled(115,115, QtCore.Qt.KeepAspectRatio))

            self.pic[i].move(60 + (i * 152), 400)
            self.pic[i].resize(170,170)


        b1.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win_obj = Windows()
    sys.exit(app.exec_())
