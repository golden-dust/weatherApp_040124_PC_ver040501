import requests                 # pip install requests
from bs4 import BeautifulSoup   # pip install beautifulsoup4

inputArea = input("날씨를 조회하려는 지역을 입력하세요 : ")

weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}+날씨")
# 네이버에서 한남동 날씨로 검색한 결과 html 파일 가져오기

# weatherHtml = requests.get("https://search.naver.com/search.naver?&query=한남동+날씨")

# print(weatherHtml.text)

weatherSoup = BeautifulSoup(weatherHtml.text, "html.parser")
# print(weatherSoup)

areaText = weatherSoup.find("h2", {"class":"title"}).text   # 날씨 지역 이름 가져오기
areaText = areaText.strip()
print(areaText)

tempText = weatherSoup.find("div", {"class":"temperature_text"}).text
# tempText = tempText.strip(" ")[5:]  # 공백 주의 -> 공백 제거하기
templist = tempText.split(" ")
tempText = templist[2][2:].strip()
# print(templist)

todayWeatherText = weatherSoup.find("span", {"class": "weather before_slash"}).text.strip()
# Error!! 'NoneType' object has no attribute 'text'

try:    # 어제보다 기온이 떨어진 경우에는 에러가 남 'temperature down'으로 바뀌어서
        # 그래서 try / except로 바꿔줌
    yesterdayTempText = weatherSoup.find("span", {"class":"temperature up"}).text.strip()
except:
    yesterdayTempText = weatherSoup.find("span", {"class": "temperature down"}).text.strip()

perceived_temp = weatherSoup.find("dd", {"class": "desc"}).text.strip()

print("현재", tempText, todayWeatherText, "/", "체감", perceived_temp)

print("어제보다", yesterdayTempText)



todayInfoText = weatherSoup.select("ul.today_chart_list>li")    # 미세먼지, 초미세먼지, 자외선, 일몰
# 미세먼지
dust1Info = todayInfoText[0].find("span", {"class":"txt"}).text.strip()
# print(todayInfoText)
# print(todayInfoText[0])
print("미세먼지:", dust1Info)

# 초미세먼지
dust2Info = todayInfoText[1].find("span", {"class":"txt"}).text.strip()
print("초미세먼지:", dust2Info)

# 자외선
uv_info = weatherSoup.find("li", {"class":"item_today level1"}).text.strip()
uvText = str(uv_info.split(" ")[-1])
print(uvText)
