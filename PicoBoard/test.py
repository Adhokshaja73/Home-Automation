# # python 3.6

# import random
# import time

# from paho.mqtt import client as mqtt_client


# broker = 'broker.emqx.io'
# port = 1883
# topic = "MY_HOME_BOARD_STATUS"
# # generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqxxt'
# password = 'publicxt'

# def connect_mqtt():
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to MQTT Broker!")
#         else:
#             print("Failed to connect, return code %d\n", rc)

#     client = mqtt_client.Client(client_id)
#     client.username_pw_set(username, password)
#     client.on_connect = on_connect
#     client.connect(broker, port)
#     return client


# def publish(client):
#     msg_count = 0
#     while True:
#         time.sleep(1)
#         msg = f"messages: {msg_count}"
#         result = client.publish(topic, "red light on")
#         # result: [0, 1]
#         status = result[0]
#         if status == 0:
#             print(f"Send `{msg}` to topic `{topic}`")
#         else:
#             print(f"Failed to send message to topic {topic}")
#         msg_count += 1


# def run():
#     client = connect_mqtt()
#     client.loop_start()
#     publish(client)


# if __name__ == '__main__':
#     run()
# from bs4 import BeautifulSoup
# import requests
# headers = {
# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


# def weather(city):
# 	city = city.replace(" ", "+")
# 	res = requests.get(
# 		f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
# 	print("Searching...\n")
# 	soup = BeautifulSoup(res.text, 'html.parser');p = soup.select('#wob_dcp')[0].getText().strip()
# 	location = soup.select('#wob_loc')[0].getText().strip()
# 	time = soup.select('#wob_dts')[0].getText().strip()
# 	info = soup.select('#wob_dc')[0].getText().strip()
# 	weather = soup.select('#wob_tm')[0].getText().strip()
      

  
  
# 	print(location,"\n p - ",p)
# 	print(time)
# 	print(info)
# 	print(weather+"°C")
 

# city = input("Enter the Name of City -> ")
# city = city+" weather"
# weather(city)
# print("Have a Nice Day:)")

# This code is contributed by adityatri
