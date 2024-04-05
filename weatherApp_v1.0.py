import sys
import requests
import time
import threading
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *  # 윈도우 설정

form_class = uic.loadUiType("ui/weatherUi.ui")[0]
# ui 폴더 내에 디자인된 ui 불러오기

class WeatherApp(QMainWindow, form_class):
    # constructor
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨 검색 프로그램")
        self.setWindowIcon(QIcon("img/Image20240405114239.png"))
        self.statusBar().showMessage("WEATHER SEARCH APP VER 0.7")

        self.search_btn.clicked.connect(self.search_weather)
        self.search_btn.clicked.connect(self.refreshTimer)
        self.area_input.returnPressed.connect(self.search_weather)  # 엔터키 누르면 실행
        self.area_input.returnPressed.connect(self.refreshTimer)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 윈도우를 항상 맨 위로 유지

        threading.Timer(30, self.refreshTimer).start()
        # threading.Timer(초, 함수).start()

    def refreshTimer(self):
        self.search_weather()
        print("refresh")
        threading.Timer(600, self.refreshTimer).start()

    def search_weather(self):
        inputArea = self.area_input.text()  # () 잊지 말기!

        weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}+날씨")
        weatherSoup = BeautifulSoup(weatherHtml.text, "html.parser")

        areaText = weatherSoup.find("h2", {"class": "title"}).text  # 날씨 지역 이름 가져오기
        areaText = areaText.strip()
        print(areaText)
        self.area_out.setText(areaText)

        tempText = weatherSoup.find("div", {"class": "temperature_text"}).text
        templist = tempText.split(" ")
        tempText = templist[2][2:].strip()
        print(tempText)
        self.temp_out.setText(tempText)

        try:
            todayWeatherText = weatherSoup.find("span", {"class": "weather before_slash"}).text.strip()
            self.setWeatherImg(todayWeatherText)
            print(todayWeatherText)

            perceived_temp = weatherSoup.find("dd", {"class": "desc"}).text.strip()
            print(perceived_temp)
            self.p_temp_out.setText(f"체감 {perceived_temp}")
            print(f"체감: {perceived_temp}")

            try:  # 어제보다 기온이 떨어진 경우에는 에러가 남 'temperature down'으로 바뀌어서
                # 그래서 try / except로 바꿔줌
                yesterdayTempText = weatherSoup.find("span", {"class": "temperature up"}).text.strip()
            except:
                yesterdayTempText = weatherSoup.find("span", {"class": "temperature down"}).text.strip()
            finally:
                self.comprsn_yest.setText(f"어제보다 {yesterdayTempText}")
                print(f"비교: {yesterdayTempText}")

            todayInfoText = weatherSoup.select("ul.today_chart_list>li")  # 미세먼지, 초미세먼지, 자외선, 일몰

            print(todayInfoText[0].text)
            print(todayInfoText[1].text)
            # 미세먼지
            dust1Info = todayInfoText[0].find("span", {"class": "txt"}).text.strip()
            dust2Info = todayInfoText[1].find("span", {"class": "txt"}).text.strip()
            self.fdust_out.setText(dust1Info)
            self.sfdust_out.setText(dust2Info)
            print(dust1Info, dust2Info)

            # 자외선
            uv_info = weatherSoup.find("li", {"class": "item_today level1"}).text.strip()
            print(uv_info)
            uvText = uv_info[4:]
            self.uv_out.setText(uvText)
            print(uvText)

            # 습도
            humidityInfo = weatherSoup.find("dl", {"class": "summary_list"}).text.strip().split(" ")
            humidityText = str(humidityInfo[5])
            self.hum_out.setText(humidityText)
            print(humidityText)
        except:
            try:
                todayWeatherRaw = weatherSoup.find("p", {"class": "summary"}).text.strip()
                todayWeatherInfo = todayWeatherRaw.split(" ")

                todayWeatherText = " ".join(todayWeatherInfo[:-2])
                print(todayWeatherText)
                self.setWeatherImg(todayWeatherText)

                perceived_temp = str(todayWeatherInfo[-1])
                print(perceived_temp)
                self.p_temp_out.setText(f"체감 {perceived_temp}")

                uv_info = weatherSoup.find("dl", {"class": "summary_list"}).text.strip()
                uvText = str(uv_info.split(" ")[-1])
                print(uvText)
                self.uv_out.setText(uvText)

                # 습도
                humidityText = weatherSoup.select("div.temperature_info>dl.summary_list>dd.desc")[3].text
                print(humidityText)
                self.hum_out.setText(humidityText)

                self.comprsn_yest.setText(f"날씨 비교 정보 없음")
                self.fdust_out.setText("-")
                self.sfdust_out.setText("-")

            except:
                QMessageBox.warning(self, "입력 오류", f"{inputArea}의 날씨를 찾을 수 없습니다. 올바른 지역을 다시 입력하세요.")

    def setWeatherImg(self, weatherText):    # 날씨에 따른 이미지 출력
        if "맑음" in weatherText or "화창" in weatherText:
            weatherImage = QPixmap("img/yellow-sun-16526.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
            # ui에 준비된 label 이름에 이미지 출력
        elif "흐림" in weatherText:
            weatherImage = QPixmap("img/blue-cloud-and-weather-16527.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif "구름" in weatherText:
            weatherImage = QPixmap("img/blue-clouds-and-yellow-sun-16529.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif "비" in weatherText or weatherText == "소나기":
            weatherImage = QPixmap("img/downpour-rainy-day-16531.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif "눈" in weatherText:
            weatherImage = QPixmap("img/snow-and-blue-cloud-16540.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
        else:
            self.weather_img.setText(weatherText)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WeatherApp()
    win.show()
    sys.exit(app.exec_())