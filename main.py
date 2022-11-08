from flask import Flask
from flask import render_template

import requests
from bs4 import BeautifulSoup

import datetime


good_weather_list = ['Ясно', 'Малооблачно', 'Облачно с прояснениями']
bad_weather_list = ['Пасмурно', 'Гроза', 'Небольшой дождь', 'Дождь', 'Дождь с грозой', 'Ливень']


app = Flask(__name__, template_folder='')

@app.route('/weather')
def get_weather():
	# vars
	sunrise = ''
	sunset = ''

	sunrise_minutes = ''
	sunset_minutes = ''

	average_uv_index = ''
	weather_result = ''


	# current time
	current_hour = datetime.datetime.now().hour
	current_minute = datetime.datetime.now().minute
	current_time = f'{current_hour}:{current_minute}'


	# all data clear at 00:00 
	if (current_hour == 0) and (current_minutes == 0):
		weather_result = ''
		bad_weather_k = 0 
		good_weather_k = 0


	if (current_hour == 0) and (current_minute == 30):

		# sunrise, sunset, ultraviolet index general
		URL = 'https://yandex.ru/pogoda/kaliningrad/details'
		response = requests.get(URL)
		soup = BeautifulSoup(response.text, 'lxml')


		daylight_hours = soup.find('dd', attrs={'class': 'sunrise-sunset__value'})


		# sunrise
		sunrise = soup.find('dl',
			attrs={'class': 'sunrise-sunset__description sunrise-sunset__description_value_sunrise'})
		sunrise = sunrise.find('dd', attrs={'class': 'sunrise-sunset__value'})
		sunrise = sunrise.text
		sunrise_hour = int(sunrise[0:2])
		sunrise_minutes = int(sunrise[3:5])

		# sunset
		sunset = soup.find('dl',
			attrs={'class': 'sunrise-sunset__description sunrise-sunset__description_value_sunset'})
		sunset = sunset.find('dd', attrs={'class': 'sunrise-sunset__value'})
		sunset = sunset.text
		sunset_hour = int(sunset[0:2])
		sunset_minutes = int(sunset[3:5])


		# ultraviolet index
		uv_index = soup.find('dd', attrs={'class': 'forecast-fields__value'})
		uv_index = uv_index.text
		uv_index = uv_index[:2]

		# ultraviolet index filtration
		if uv_index[1] == ',':
			uv_index = uv_index[0]


		# weather general
		URL = 'https://kgd.ru/pogoda/1-pogoda-v-kaliningrade'
		response = requests.get(URL)
		soup = BeautifulSoup(response.text, 'lxml')

		# weather
		weather = soup.find('div', attrs={'class': 'weatherdesc'})
		weather = weather.text


	# weather counter
	if (current_minute == sunrise_minutes) and (current_hour < sunset_hour) and (current_hour >= sunrise_hour):
		# good weather
		for i in good_weather_list:
			if i in weather:
				good_weather_k += 1
		# bad weather
		for i in bad_weather_list:
			if i in weather:
				bad_weather_k += 1

		uv_index_all += uv_index
	

	# weather result
	if (current_minute == sunset_minutes) and (current_hour == sunset_hour):
		if bad_weather_k >= good_weather_k:
			weather_result = False
		else:
			weather_result = True

		average_uv_index = uv_index_all // daylight_hours


	return render_template('index.html',
						sunrise=sunrise,
						sunset=sunset,
						sunrise_minutes=sunrise_minutes,
						sunset_minutes=sunset_minutes,
						current_time=current_time,
						average_uv_index=average_uv_index,
						weather_result=weather_result)


if __name__ == '__main__':
	app.run(debug=False)