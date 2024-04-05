import sys
import requests
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

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


            perceived_temp = weatherSoup.find("dd", {"class": "desc"}).text.strip()
            self.p_temp_out.setText(f"체감 {perceived_temp}")
            print(f"체감: {perceived_temp}")

            try:  # 어제보다 기온이 떨어진 경우에는 에러가 남 'temperature down'으로 바뀌어서
                # 그래서 try / except로 바꿔줌
                yesterdayTempText = weatherSoup.find("span", {"class": "temperature up"}).text.strip()
            except:
                yesterdayTempText = weatherSoup.find("span", {"class": "temperature down"}).text.strip()
            self.comprsn_yest.setText(f"어제보다 {yesterdayTempText}")
            print(f"비교: {yesterdayTempText}")

            todayInfoText = weatherSoup.select("ul.today_chart_list>li")  # 미세먼지, 초미세먼지, 자외선, 일몰
            # 미세먼지
            dust1Info = todayInfoText[0].find("span", {"class": "txt"}).text.strip()
            dust2Info = todayInfoText[1].find("span", {"class": "txt"}).text.strip()
            self.fdust_out.setText(dust1Info)
            self.sfdust_out.setText(dust2Info)
            print(dust1Info, dust2Info)

        except:
            try:
                todayWeatherRaw = weatherSoup.find("p", {"class": "summary"}).text.strip()
                todayWeatherInfo = todayWeatherRaw.split(" ")

                todayWeatherText = " ".join(todayWeatherInfo[:-2])
                print(todayWeatherText)
                self.setWeatherImg(todayWeatherText)

                perceived_temp = str(todayWeatherInfo[-1])
                self.p_temp_out.setText(f"체감 {perceived_temp}")

                self.comprsn_yest.setText(f"날씨 비교 정보 없음")
                self.fdust_out.setText("-")
                self.sfdust_out.setText("-")

            except:
                QMessageBox.warning(self, "입력 오류", f"{inputArea}의 날씨를 찾을 수 없습니다. 올바른 지역을 다시 입력하세요.")

    def setWeatherImg(self, weatherText):    # 날씨에 따른 이미지 출력
        if weatherText == "맑음":
            weatherImage = QPixmap("img/yellow-sun-16526.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
            # ui에 준비된 label 이름에 이미지 출력
        elif weatherText == "흐림":
            weatherImage = QPixmap("img/blue-cloud-and-weather-16527.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "구름많음":
            weatherImage = QPixmap("img/blue-clouds-and-yellow-sun-16529.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "비" or weatherText == "소나기":
            weatherImage = QPixmap("img/downpour-rainy-day-16531.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "눈":
            weatherImage = QPixmap("img/snow-and-blue-cloud-16540.png")
            self.weather_img.setPixmap(QPixmap(weatherImage))
        else:
            self.weather_img.setText(weatherText)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WeatherApp()
    win.show()
    sys.exit(app.exec_())