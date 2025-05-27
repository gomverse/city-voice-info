"""
사용자의 음성을 인식해서 텍스트로 변환 후 명령을 수행하는 프로그램

-기능
서울 날씨 -> 서울 기준 현재 날씨는 *입니다. 온도는 *도 입니다.
서울 시간과 날짜 -> 서울 기준 현재 *년 *월 *일 입니다. 시간은 *시 *분 입니다.
로스엔젤레스 시간 -> 로스엔젤레스 기준 현재 시간은 *시 *분 입니다.
"""

import datetime
from pytz import timezone
import speech_recognition as sr
import datetime
import requests
import time
from io import BytesIO
from navertts import NaverTTS
from pydub import AudioSegment
from pydub.playback import play


def find_city(keywords: list[str], sentence: str, default: str = "서울") -> str:
    """
    사용자의 명령에서 도시 이름을 찾는다
    """

    found_city = [c for c in keywords if c in sentence]
    return (
        found_city[0] if found_city else default
    )  # 찾은 도시를 반환하거나 도시목록에서 찾을 수 없다면 "서울"을 반환


def get_weather(city: str) -> tuple:
    """
    도시의 날씨와 온도를 반환한다
    """

    city = city.replace("_", " ")  # 도시이름을 open weather에서 찾을 수 있도록 변경

    API_KEY = "3bf5025e7a056c6a9f654fd7714db04b"  # API key
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}&lang=kr"
    response = requests.get(request_url)

    data = response.json()
    weather = data["weather"][0]["description"]  # 날씨 구하기
    temperature = round(data["main"]["temp"] - 273.15, 2)  # 섭씨 온도 구하기

    return weather, temperature  # 날씨와 온도를 튜플 형태로 반환


def clova_voice(tts_text: str, date=False, time=False, weather=False) -> None:
    """
    Clova voice를 이용해 음성 출력
    """
    tts = NaverTTS(tts_text, lang="ko")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)  # 포인터를 처음으로 돌리고
    my_sound = AudioSegment.from_file(fp, format="mp3")
    my_sound += AudioSegment.silent(duration=200)
    play(my_sound)
    # time.sleep(len(my_sound) / 1000 + 0.1)
    # fp = BytesIO()
    # tts.write_to_fp(fp)
    # fp = BytesIO(fp.getvalue())
    # my_sound = AudioSegment.from_file(fp, format="mp3")
    # play(my_sound)


def command_tts(user_command: str) -> None:
    """
    사용자 명령을 받고 해당 명령에 해당하는 정보를 가져와 음성으로 출력
    """

    if user_command == "input_command":
        clova_voice("명령을 내려주세요")

    elif user_command == "fail_recognize":
        clova_voice("인식할 수 없습니다")

    else:
        city_name = find_city(cities_dict.keys(), user_command)
        date_exist = "날짜" in user_command
        time_exist = "시간" in user_command
        weather_exist = "날씨" in user_command

        city = find_city(cities_dict.keys(), user_command)
        city_info = datetime.datetime.today().astimezone(timezone(cities_dict[city]))
        city_info_to_date = datetime.datetime.fromisoformat(
            str(city_info)
        )  # iso 형식 타임스태프를 파싱

        full_voice = f"{city_name} 기준 현재"

        if date_exist == True:
            city_date = f"날짜는 {city_info_to_date.year}년 {city_info_to_date.month}월 {city_info_to_date.day}일 입니다."
            full_voice += city_date
        if time_exist == True:
            city_time = f"시간은 {city_info_to_date.hour}시 {city_info_to_date.minute}분 입니다."
            full_voice += city_time
        if weather_exist == True:
            weather = get_weather(cities_dict.get(city_name).split("/")[-1])
            city_weather = f"날씨는 {weather[0]}, 온도는 {weather[1]:.0f}도 입니다."
            full_voice += city_weather

        clova_voice(full_voice)


cities_dict = {  # 도시 목록
    "서울": "Asia/Seoul",
    "뉴욕": "America/New_York",
    "로스앤젤레스": "America/Los_Angeles",
    "파리": "Europe/Paris",
    "런던": "Europe/London",
}

r = sr.Recognizer()
microphone = sr.Microphone()

while True:
    with microphone as source:
        r.adjust_for_ambient_noise(source)  # 배경 소음을 측정하고
        command_tts("input_command")  # 명령을 내려주세요 음성
        audio = r.listen(source)  # 일정 크기 이상의 소리가 들리면 녹음
    try:
        text = r.recognize_google(audio, language="ko")  # 사용자 음성을 텍스트로 변환
    except:
        command_tts("fail_recognize")  # 사용자 음성 인식 실패 시
    else:
        if "종료" in text:
            clova_voice("프로그램을 종료합니다.")
            break
        command_tts(text)  # 성공했다면 command_tts에 사용자 명령을 보냄
