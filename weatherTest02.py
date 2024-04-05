import requests                 # pip install requests
from bs4 import BeautifulSoup   # pip install beautifulsoup4

# inputArea = input("날씨를 조회하려는 지역을 입력하세요 : ")

# weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}+날씨")
# 네이버에서 한남동 날씨로 검색한 결과 html 파일 가져오기

weatherHtml = requests.get("https://search.naver.com/search.naver?&query=발렌시아+날씨")
# print(weatherHtml.text)

weatherSoup = BeautifulSoup(weatherHtml.text, "html.parser")
# print(weatherSoup)

# 날씨 지역 이름 가져오기
areaText = weatherSoup.find("h2", {"class":"title"}).text
areaText = areaText.strip()
print(areaText)

# 현재 날씨 가져오기
tempText = weatherSoup.find("div", {"class":"temperature_text"}).text
# tempText = tempText.strip(" ")[5:]  # 공백 주의 -> 공백 제거하기
templist = tempText.split(" ")
tempText = templist[2][2:].strip()
# print(templist)
print(tempText)


# 날씨 제공자 가져오기
provider = weatherSoup.find("strong", {"class":"provider _provider"}).text

# 날씨 제공자가 '기상청'이면 -> 국내 날씨 / 아니면 -> 국외 날씨
if provider == "기상청":
    # 현재 날씨
    todayWeatherText = weatherSoup.find("span", {"class": "weather before_slash"}).text.strip()

    # 어제와 비교
    yesterdayTempText = weatherSoup.find("span", {"class":"temperature up"}).text.strip()

    # 체감 온도
    perceived_temp = weatherSoup.find("dd", {"class": "desc"}).text.strip()

    # 미세먼지, 초미세먼지, 자외선, 일몰 정보 선택하기
    todayInfoText = weatherSoup.select("ul.today_chart_list>li")

    # 미세먼지
    dust1Info = todayInfoText[0].find("span", {"class":"txt"}).text.strip()
    # print(todayInfoText)
    # print(todayInfoText[0])

    # 초미세먼지
    dust2Info = todayInfoText[1].find("span", {"class": "txt"}).text.strip()

    # 출력
    print("현재", tempText, todayWeatherText, "/", "체감", perceived_temp)
    print("어제보다", yesterdayTempText)
    print("미세먼지:", dust1Info)


    print("초미세먼지:", dust2Info)

else:
    weatherInfo = weatherSoup.find("div",{"class":"temperature_text"}).text.strip()
    uv_info = weatherSoup.find("dl", {"class":"summary_list"}).text.strip()
    uvText = str(uv_info.split(" ")[-1])
    print(weatherInfo)
    print(uvText)