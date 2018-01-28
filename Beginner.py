# coding: utf-8

# In[1]:


import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

# In[2]:



# coding: utf-8

# In[9]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


# In[10]:


page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")


# In[11]:


soup = BeautifulSoup(page.content,'html.parser')
seven_day = soup.find(id = 'seven-day-forecast')
tombstone = seven_day.find_all(class_ ='tombstone-container')


# In[12]:



overnight = tombstone[1].find('p',{'class':'period-name'}).get_text()
shortdesc = tombstone[1].find(class_ = 'short-desc').get_text()
temp = tombstone[1].find(class_ = 'temp').get_text()

img = tombstone[1].find("img")['title']


# In[13]:


# To distinguish oen tab from other if it ahs multiple attributes like class/id/etc
# seven_day.find_all('p',{'class':'period-name','extra':'attributes'})
seven_day.find_all('p',{'class':'period-name'})


# In[14]:


periods = seven_day.select(".period-name")
periods = [days.get_text() for days in periods]
short_desc = [sd.get_text() for sd in seven_day.select('.short-desc')]
temp = [t.get_text() for t in seven_day.select('.temp')]
img_desc = [im['title'] for im in seven_day.select('img')]



# In[15]:


df = pd.DataFrame({'period' : periods, 'short_desc': short_desc, 'temperature': temp, "description": img_desc})



# In[16]:





df['temperature'] = [(x.split(" ")[1] + ' °F') for x in df['temperature']]


# len(df['period'])
# type(df['period'])


# In[ ]:


# In[3]:


class Windows(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 200, 200)

        b1 = QtWidgets.QPushButton('Quit', self)
        b1.move(620, 640)
        self.setWindowTitle('Weather Forecast')

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
                self.pic[i].setPixmap(QtGui.QPixmap('cloudy.png'))

            else:
                if "Rainy" in df['short_desc'][i]:

                    self.pic[i].setPixmap(QtGui.QPixmap('rainy.png'))
                else:
                    if "Sunny" in df['short_desc'][i]:
                        self.pic[i].setPixmap(QtGui.QPixmap('sunny.png'))
            self.pic[i].move(60 + (i * 150), 400)
            self.pic[i].resize(130,130)


        b1.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win_obj = Windows()
    sys.exit(app.exec_())
