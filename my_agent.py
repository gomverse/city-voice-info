"""
사용자의 음성을 인식해서 텍스트로 변환 후 명령을 수행하는 프로그램

- 목표
서울 날씨 -> 현재 서울의 날씨는 *입니다. 온도는 *도 입니다
서울 시간과 날짜 -> 서울 기준 현재 *년 *월 *일이고 시간은 *시 *분 입니다
로스엔젤레스 시간 -> 로스엔젤레스 기준 현재 시간은 *시 *분 입니다

받을 건 4개
도시이름, 날짜, 시간, 날씨
만약 입력이 4개보다 적다면 기본값 설정

순서

1. 사용자 음성을 입력받고 텍스트로 변환
2. 해당 텍스트에 [도시이름, 날짜, 시간, 날씨]가 있는지 bool형태로 확인???
3. 확인 후 find_keyword 함수로 도시이름을 받기
4. 해당 도시의 날짜와 시간을 체크
5. 해당 도시의 날씨를 체크
6. 전부 종합해서 알려주기 <- 여기에 bool 형태가 들어간다?

"""

import datetime
from datetime import datetime, timedelta
from pytz import timezone
import speech_recognition as sr
import datetime
import requests
from io import BytesIO
from navertts import NaverTTS
from pydub import AudioSegment
from pydub.playback import play

# user_command = "로스앤젤레스의 시간을 알려주세요"  # 음성 입력으로 수정해야지

# city = find_keyword(cities_dict.keys(), user_command)  # 도시 이름을 반환받고
# city_info = datetime.today().astimezone(
#     timezone(cities_dict[city])
# )  # 해당 도시의 정보를 구한다

# city_info_to_date = datetime.fromisoformat(str(city_info))  # iso 형식 타임스태프를 파싱

# API_KEY = "3bf5025e7a056c6a9f654fd7714db04b"  # open weather API key
# BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
# city = None

# request_url = f"{BASE_URL}?appid={API_KEY}&q={city}&lang=kr"
# response = requests.get(request_url)

# if response.status_code == 200:  # 200은 성공

#     data = response.json()
#     city_name = data["name"]
#     weather = data["weather"][0]["description"]
#     temperature = round(data["main"]["temp"] - 273.15, 2)  # 켈빈 온도 사용

#     print("City:", city_name)
#     print("Weather:", weather)
#     print("Temperature:", temperature, "celsius")

# else:
#     print("An error occurred.", response.status_code)


# 도시이름, 날짜, 시간, 날씨를 받아서 bool 형태로 존재하는지 확인하기


# def get_today_text():
#     today = datetime.date.today()
#     return f"오늘은 {today.year}년 {today.month}월 {today.day}일 입니다"


# def get_time_text():
#     formatted = datetime.datetime.now().strftime("%p %I시 %M분")
#     formatted = formatted.replace("AM", "오전").replace("PM", "오후")
#     return f"지금 시간은 {formatted}입니다"


def find_keyword(keywords: list[str], sentence: str, default: str = "서울") -> str:
    """
    사용자 문장에서 도시 이름을 찾는다
    """

    found_city = [c for c in keywords if c in sentence]
    return (
        found_city[0] if found_city else default
    )  # 찾은 도시를 반환하거나 도시목록에서 찾을 수 없다면 "서울"을 반환


def command_naver_tts(user_command):
    """naver tts의 음성"""

    def command_naver_tts_sound(tts_text, date=False, time=False, weather=False):
        tts = NaverTTS(tts_text, lang="ko")
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp = BytesIO(fp.getvalue())
        my_sound = AudioSegment.from_file(fp, format="mp3")
        play(my_sound)

    if user_command == "input_command":
        command_naver_tts_sound("명령을 내려주세요")

    if user_command == "fail_recognize":
        command_naver_tts_sound("인식할 수 없습니다")
    else:
        city_name = find_keyword(cities_dict.keys(), user_command)
        date_exist = "날짜" in user_command
        time_exist = "시간" in user_command
        weather_exist = "날씨" in user_command


cities_dict = {  # 도시 목록
    "서울": "Asia/Seoul",
    "뉴욕": "America/New_York",
    "로스앤젤레스": "America/Los_Angeles",
    "파리": "Europe/Paris",
    "런던": "Europe/London",
}

user_msg1 = "서울의 날짜와 시간"
user_msg2 = "뉴욕의 시간과 날씨"
user_msg3 = "모름의 날씨"


# r = sr.Recognizer()
# microphone = sr.Microphone()
# c = 1

# while c > 0:
#     with microphone as source:
#         r.adjust_for_ambient_noise(source)  # 배경 소음을 측정하고
#         command_naver_tts("input_command")
#         audio = r.listen(source)  # 일정 크기 이상의 소리가 들리면 녹음
#     try:
#         text = r.recognize_google(audio, language="ko")
#     except:
#         command_naver_tts("fail_recognize")
#     else:
#         command_naver_tts(text)
#         c -= 1
