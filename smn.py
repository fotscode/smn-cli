import subprocess
import json
from colorama import Fore
from datetime import date
import getopt
import requests
import sys


def get_token():
    return (
        requests.get("https://www.smn.gob.ar/pronostico")
        .text.split("localStorage.setItem('token', '")[1]
        .split("'")[0]
    )


def get_weather(location="4856"):
    res = requests.get(
        f"https://ws1.smn.gob.ar/v1/forecast/location/{location}",
        headers={"Authorization": f"JWT {get_token()}"},
    ).text
    return json.loads(res)


def get_localidad(name: str):
    name = name.replace(" ", "%20")
    url = "https://ws1.smn.gob.ar/v1/georef/location/search?name=" + name
    res = json.loads(requests.get(url).text)

    if len(res) == 0:
        print(f"{Fore.RED}ERROR:{Fore.RESET} localidad no encontrada")
        sys.exit(1)
    for i in range(len(res)):
        ciudad = res[i][1]
        departamento = res[i][2]
        provincia = res[i][3]
        num = res[i][0]
        print(
            f"{Fore.BLUE}{i}{Fore.RESET} - {ciudad} ({departamento}), {provincia} [{num}]"
        )
    return res


hash_day = {
    "early_morning": "0-6hs",
    "morning": "6-12hs",
    "afternoon": "12-18hs",
    "night": "18-24hs",
}

weekdays = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}


def get_info(time_of_day: str):
    if day[time_of_day]:
        hours = hash_day[time_of_day]
        if time_of_day == "morning" and day["early_morning"]:
            hours = "0-12hs"
        if time_of_day == "afternoon" and day["early_morning"]:
            hours = "12-24hs"
        rain_prob = day[time_of_day]["rain_prob_range"]
        rain_range = f"{rain_prob[0]}-{rain_prob[1]}%"
        temp = str(day[time_of_day]["temperature"]) + "°C"
        humidity = str(day[time_of_day]["humidity"]) + "%"
        if humidity == "None%":
            humidity = "0%"

        print(
            f'  {hours.ljust(7)} @ 🌡️ {Fore.RED}{temp.ljust(6)} {Fore.RESET}| 💦 {Fore.BLUE}{humidity.ljust(5)} {Fore.RESET}| ☔ {rain_range.ljust(5)} | {day[time_of_day]["weather"]["description"]}'
        )


dias = 1
localidad = None
options = "d:l:n:h"
long_options = ["dias=", "localidad=", "numero=", "help"]
try:
    opts, args = getopt.getopt(sys.argv[1:], options, long_options)
except getopt.GetoptError:
    print(f"{Fore.RED}ERROR{Fore.RESET} de argumentos")
    sys.exit(1)

for opt, arg in opts:
    if opt in ("-d", "--dias"):
        dias = int(arg)
    elif opt in ("-l", "--localidad"):
        res = get_localidad(arg)
        num = input("Ingrese el número de la localidad: ")
        localidad = res[int(num)][0]
    elif opt in ("-n", "--numero"):
        localidad = arg
    elif opt in ("-h", "--help"):
        print(
            "Uso: smn.py [OPCIONES]\n",
            "\t-d, --dias=NUMERO          cantidad de días a mostrar\n",
            "\t-l, --localidad=LOCALIDAD  nombre de la localidad\n",
            "\t-n, --numero=NUMERO        número de la localidad\n"
            "\t-h, --help                 muestra esta ayuda",
        )
        sys.exit(0)


if localidad is None:
    res = get_localidad(input("Ingrese el nombre de la localidad: "))
    num = input("Ingrese el número de la localidad: ")
    try:
        localidad = res[int(num)][0]
    except:
        print(f"{Fore.RED}ERROR{Fore.RESET} de input")
        sys.exit(1)

weather = get_weather(localidad)
ciudad = "Ciudad: " + weather["location"]["name"]
print(Fore.CYAN, ciudad.center(60, " "), Fore.RESET)
forecast = weather["forecast"]

count = 0
for day in forecast:
    if count == dias:
        break

    if str(date.today()) == day["date"]:
        print(Fore.YELLOW + "Hoy" + Fore.RESET, end=" ")
    print(
        Fore.GREEN + weekdays[date.fromisoformat(day["date"]).strftime("%A")], end=" "
    )

    # yyyy-mm-dd -> dd-mm-yyyy
    day["date"] = day["date"][8:10] + "-" + day["date"][5:7] + "-" + day["date"][0:4]

    print(day["date"] + Fore.RESET)
    get_info("early_morning")
    get_info("morning")
    get_info("afternoon")
    get_info("night")
    count += 1
