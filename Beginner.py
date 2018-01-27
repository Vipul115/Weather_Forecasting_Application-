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

        periods1 = QtWidgets.QLabel(df['period'][0], self)
        periods1.move(100, 200)
        periods2 = QtWidgets.QLabel(df['period'][1], self)
        periods2.move(250, 200)
        periods3 = QtWidgets.QLabel(df['period'][2], self)
        periods3.move(400, 200)
        periods4 = QtWidgets.QLabel(df['period'][3], self)
        periods4.move(550, 200)
        periods5 = QtWidgets.QLabel(df['period'][4], self)
        periods5.move(700, 200)
        periods6 = QtWidgets.QLabel(df['period'][5], self)
        periods6.move(850, 200)
        periods7 = QtWidgets.QLabel(df['period'][6], self)
        periods7.move(1000, 200)
        periods8 = QtWidgets.QLabel(df['period'][7], self)
        periods8.move(1150, 200)

        temp1 = QtWidgets.QLabel(df['temperature'][0], self)
        temp1.setFont(QtGui.QFont('Times New Roman', 16))
        temp1.move(100, 300)
        temp2 = QtWidgets.QLabel(df['temperature'][1], self)
        temp2.setFont(QtGui.QFont('Times New Roman', 16))
        temp2.move(250, 300)
        temp3 = QtWidgets.QLabel(df['temperature'][2], self)
        temp3.setFont(QtGui.QFont('Times New Roman', 16))
        temp3.move(400, 300)
        temp4 = QtWidgets.QLabel(df['temperature'][3], self)
        temp4.setFont(QtGui.QFont('Times New Roman', 16))
        temp4.move(550, 300)
        temp5 = QtWidgets.QLabel(df['temperature'][4], self)
        temp5.setFont(QtGui.QFont('Times New Roman', 16))
        temp5.move(700, 300)
        temp6 = QtWidgets.QLabel(df['temperature'][5], self)
        temp6.setFont(QtGui.QFont('Times New Roman', 16))
        temp6.move(850, 300)
        temp7 = QtWidgets.QLabel(df['temperature'][6], self)
        temp7.setFont(QtGui.QFont('Times New Roman', 18))
        temp7.move(1000, 300)
        temp8 = QtWidgets.QLabel(df['temperature'][7], self)
        temp8.setFont(QtGui.QFont('Times New Roman', 16))
        temp8.move(1150, 300)

        sd1 = QtWidgets.QLabel(df['short_desc'][0], self)
        sd1.move(100, 500)
        sd2 = QtWidgets.QLabel(df['short_desc'][1], self)
        sd2.move(250, 500)
        sd3 = QtWidgets.QLabel(df['short_desc'][2], self)
        sd3.move(400, 500)
        sd4 = QtWidgets.QLabel(df['short_desc'][3], self)
        sd4.move(550, 500)
        sd5 = QtWidgets.QLabel(df['short_desc'][4], self)
        sd5.move(700, 500)
        sd6 = QtWidgets.QLabel(df['short_desc'][5], self)
        sd6.move(850, 500)
        sd7 = QtWidgets.QLabel(df['short_desc'][6], self)
        sd7.move(1000, 500)
        sd8 = QtWidgets.QLabel(df['short_desc'][7], self)
        sd8.move(1150, 500)
        b1.clicked.connect(QtCore.QCoreApplication.instance().quit)

        p1 = QtWidgets.QLabel(self)
        p1.setPixmap(QtGui.QPixmap('cloudy.png'))
        p1.move(850,400)
        p1.resize(200,200)
        self.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win_obj = Windows()
    sys.exit(app.exec_())
