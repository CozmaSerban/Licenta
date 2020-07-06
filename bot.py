import requests  
from datetime import datetime as dt
trash = 0
while True:
    if dt.now().second == 0 and trash == 0:
        print("Sending ping")
        trash = 1
        url = "https://webexapis.com/v1/messages"

        payload = "{\n\t\"roomId\": \"" + \
                "Y2lzY29zcGFyazovL3VzL1JPT00vYWE5Y2MyMWMtZjUwMC0zZTI2LWJjMjctODUzMTZiM2M1OTVi"+"\",\n\t\"text\" : \""+"ping"+"\"\n}"
        headers = {
                'Authorization': 'Bearer YzJhMjUyMmEtNDNjYi00OThhLTk1N2YtOTE5YjI2OTMwYmMyOTgwYzU5ODktZGUw_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f',
                'Content-Type': 'application/json'
                }

        response = requests.request("POST", url, headers=headers, data=payload)
    elif dt.now().second != 0:
        trash = 0
        print("Changed to 0")