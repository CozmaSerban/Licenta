import Adafruit_DHT
import time
import requests
import datetime

token = "MmUyNjc5NzMtYmIwMS00NmJjLTg0MTMtZGRjMTI1NmRlZWQ4ZGVmN2IzZDQtMzRi_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
def func():
    while True:
        if datetime.datetime.now().hour == 7 and datetime.datetime.now().minute == 0:

            humidity, temperature = Adafruit_DHT.read_retry(11, 4)
            f = open("demo.txt", "r")
            temp, hum = f.read().split(" ")
            temperature = float(temp)
            humidity = float(hum)
            f.close()

            if humidity is not None and temperature is not None:
                url = "https://webexapis.com/v1/messages"

                payload = (
                    '{\n\t"roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vMjNlMDlmMjAtOTk5ZC0xMWVhLWJlOWMtNmYwYmE3NzgxNTY4",\n\t"text" : "'
                    + "Daily check Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(
                        temperature, humidity
                    )
                    + '"\n}'
                )
                headers = {
                    "Authorization": "Bearer " + token,
                    "Content-Type": "application/json",
                }
                print("trimite call")
                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                print("ARE NONE timp")
            time.sleep(70)
        elif datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 0:
            humidity, temperature = Adafruit_DHT.read_retry(11, 4)
            f = open("demo.txt", "r")
            temp, hum = f.read().split(" ")
            temperature = float(temp)
            humidity = float(hum)
            f.close()

            if humidity is not None and temperature is not None:
                url = "https://webexapis.com/v1/messages"
                payload = (
                    '{\n\t"roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vMjNlMDlmMjAtOTk5ZC0xMWVhLWJlOWMtNmYwYmE3NzgxNTY4",\n\t"text" : "'
                    + "Daily check Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(
                        temperature, humidity
                    )
                    + '"\n}'
                )
                headers = {
                    "Authorization": "Bearer " + token,
                    "Content-Type": "application/json",
                }
                print("trimite call")
                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                print("ARE NONE timp")
            time.sleep(70)

if __name__ == "__main__":
    func()
-----------------------------------------------------
import Adafruit_DHT
import datetime
import time
import requests
token = 'MmUyNjc5NzMtYmIwMS00NmJjLTg0MTMtZGRjMTI1NmRlZWQ4ZGVmN2IzZDQtMzRi_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'

def func():
    while True:
            humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        
            if humidity is not None and temperature is not None:
                print(str(temperature) +" " + str(datetime.datetime.now().minute)+ " " +str(datetime.datetime.now().second))
                f = open("demo.txt", "w")
                f.write(str(temperature)+" "+str(humidity))
                f.close()

                if temperature >= 27:
                    
                    url = "https://webexapis.com/v1/messages"

                    payload = "{\n\t\"roomId\": \"Y2lzY29zcGFyazovL3VzL1JPT00vMjNlMDlmMjAtOTk5ZC0xMWVhLWJlOWMtNmYwYmE3NzgxNTY4\",\n\t\"text\" : \""+'ALERTA ! Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)+"\"\n}"
                    headers = {
                            'Authorization': 'Bearer '+token,
                            'Content-Type': 'application/json'
                        }
                    print("trimite call")
                    response = requests.request("POST", url, headers=headers, data=payload)
            else:
                print("ARE NONE la secunda")
            time.sleep(300)

if __name__ == "__main__":
    func()