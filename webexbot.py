# from __future__ import print_function # Needed if you want to have console output using Flask
import requests
from pyzbar import pyzbar
import sys
import json
import os
import cv2
import time
from flask import Flask, request

# You can get it on https://developer.webex.com/endpoint-messages-post.html
token = 'ZmVkZmNlMzctMjc4MC00NmMyLWI3MzUtZTdhMjk3MjhhNDE0MTk1ZmY1YzAtZmY4_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'

app = Flask(__name__)


# all request for localhost:5000/  will reach this method
@app.route("/", methods=['POST'])
def webhook():

    # Get the json data
    json = request.json

    # Retrieving message ID, person ID, email and room ID from message received

    message_id = json["data"]["id"]
    user_id = json["data"]["personId"]
    email = json["data"]["personEmail"]
    room_id = json["data"]["roomId"]

    print(message_id, file=sys.stdout)
    print(user_id, file=sys.stdout)
    print(email, file=sys.stdout)
    print(room_id, file=sys.stdout)

    if user_id != 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8zYWM1NjAwYi1iODdmLTQ1ZTItOGM0My0xMjU3ZTJhMzY4NGM':

        # Loading the message with the message ID

        global token  # Retrieving token from Global variable

        header = {"Authorization": "Bearer %s" % token}
        get_rooms_url = "https://api.ciscospark.com/v1/messages/" + message_id
        api_response = requests.get(
            get_rooms_url, headers=header, verify=False)
        response_json = api_response.json()
        message = response_json
        print(message)
        if "text" in response_json:
            url = "https://webexapis.com/v1/messages"

            payload = "{\n  \"attachments\": [\n    {\n      \"contentType\": \"application/vnd.microsoft.card.adaptive\",\n      \"content\": {\n        \"$schema\": \"http://adaptivecards.io/schemas/adaptive-card.json\",\n        \"type\": \"AdaptiveCard\",\n        \"version\": \"1.0\",\n        \"body\": [\n          {\n            \"type\": \"ColumnSet\",\n            \"columns\": [\n              {\n                \"type\": \"Column\",\n                \"width\": 2,\n                \"items\": [\n                  {\n                    \"type\": \"TextBlock\",\n                    \"text\": \"Greetings, "+email+"! What do you want to do ?\"\n                  },\n                  {\n                    \"type\": \"Input.ChoiceSet\",\n                    \"id\": \"asset_option\",\n                    \"style\": \"compact\",\n                    \"isMultiSelect\": false,\n                    \"value\": \"1\",\n                    \"choices\": [\n                      {\n                        \"title\": \"Loan Assets\",\n                        \"value\": \"loan\"\n                      },\n                      {\n                        \"title\": \"Import Assets\",\n                        \"value\": \"import\"\n                      },\n                      {\n                        \"title\": \"Delete Assets\",\n                        \"value\": \"delete\"\n                      },\n                      {\n                      \t\"title\": \"Search Assets\",\n                      \t\"value\": \"search\"\n                      }\n                    ]\n                  }\n                ]\n              }\n            ]\n          }\n        ],\n        \"actions\": [\n          {\n            \"type\": \"Action.Submit\",\n            \"title\": \"Submit\"\n          }\n        ]\n      }\n    }\n  ],\n  \"toPersonId\": \""+user_id+"\",\n  \"text\": \" \"\n}"
            headers = {
                'Authorization': 'Bearer ZmVkZmNlMzctMjc4MC00NmMyLWI3MzUtZTdhMjk3MjhhNDE0MTk1ZmY1YzAtZmY4_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f',
                'Content-Type': 'application/json'
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)
        else:

            print(response_json['files'][0])
            # print(message, file= sys.stdout)
            picture = requests.get(response_json['files'][0], headers=header)
            # print(picture.content)

            print('******************', file=sys.stdout)
            f = open('./image.jpeg', 'wb')
            f.write(picture.content)
            f.close()
            image = cv2.imread('./image.jpeg')
            os.remove('./image.jpeg')
            barcodes = pyzbar.decode(image)

            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                text = "{}({})".format(barcodeData, barcodeType)
                print(text)
                url = "https://webexapis.com/v1/messages"

                payload = "{\n\t\"toPersonId\": \"" + \
                    message['personId']+"\",\n\t\"text\" : \""+text+"\"\n}"
                headers = {
                    'Authorization': 'Bearer '+token,
                    'Content-Type': 'application/json'
                }

                response = requests.request(
                    "POST", url, headers=headers, data=payload)

                print(response.text.encode('utf8'))

        return "Success!"

    else:
        print("intru aici")
        return "It's my own messages ... ignoring it"


os.popen("pkill ngrok")  # clearing previous sessions of ngrok (if any)
os.popen("ngrok http 5000 &")  # Opening Ngrok in background
time.sleep(5)  # Leaving some time to Ngrok to open
# Getting public URL on which NGROK is listening to
term_output_json = os.popen('curl http://127.0.0.1:4040/api/tunnels').read()
tunnel_info = json.loads(term_output_json)
public_url = tunnel_info['tunnels'][0]['public_url']


# Registering Webhook
header = {"Authorization": "Bearer %s" %
          token, "content-type": "application/json"}
requests.packages.urllib3.disable_warnings()  # removing SSL warnings
post_message_url = "https://api.ciscospark.com/v1/webhooks"

# Preparing the payload to register. We are only interested in messages here, but feel free to change it
payload = {
    "resource": "messages",
    "event": "all",
    "targetUrl": public_url,
    "name": "MyWonderfulWebHook"
}

api_response = requests.post(
    post_message_url, json=payload, headers=header, verify=False)  # Registering webhook

if api_response.status_code != 200:
    print('Webhook registration Error !')
    exit(0)

# header = {"Authorization": "Bearer %s" % token, "content-type": "application/json"}
# requests.packages.urllib3.disable_warnings() #removing SSL warnings
# post_message_url = "https://api.ciscospark.com/v1/webhooks"

# # Preparing the payload to register. We are only interested in messages here, but feel free to change it
payload = {
    "resource": "attachmentActions",
    "event": "created",
    "targetUrl": public_url+"/cards",
    "name": "CardsWebHook"
}
print(payload)
api_response = requests.post(
    post_message_url, json=payload, headers=header, verify=False)  # Registering webhook

if api_response.status_code != 200:
    print('Webhook CARD registration Error !')
    exit(0)


def how_many_card(toWho):
    # payload = "{\n\t\"toPersonId\": \"" + \
    #     toWho+"\",\n\t\"text\" : \""+text+"\"\n}"
    payload = "{\n  \"attachments\": [\n    {\n      \"contentType\": \"application/vnd.microsoft.card.adaptive\",\n      \"content\": {\n        \"$schema\": \"http://adaptivecards.io/schemas/adaptive-card.json\",\n        \"type\": \"AdaptiveCard\",\n        \"version\": \"1.0\",\n        \"body\": [\n          {\n            \"type\": \"ColumnSet\",\n            \"columns\": [\n              {\n                \"type\": \"Column\",\n                \"width\": 2,\n                \"items\": [\n                  {\n                    \"type\": \"TextBlock\",\n                    \"text\": \"How many items ?\"\n                  },\n                  {\n                    \"type\": \"Input.Text\",\n                    \"id\": \"assets_number\",\n                    \"style\": \"compact\",\n                    \"value\": \"1\"}\n                ]\n              }\n            ]\n          }\n        ],\n        \"actions\": [\n          {\n            \"type\": \"Action.Submit\",\n            \"title\": \"Submit\"\n          }\n        ]\n      }\n    }\n  ],\n  \"toPersonId\": \""+toWho+"\",\n  \"text\": \" \"\n}"
    print(json.loads(payload))
    headers = {
        'Authorization': 'Bearer '+token,
        'Content-Type': 'application/json'
    }
    url = "https://webexapis.com/v1/messages"

    response = requests.request(
        "POST", url, headers=headers, data=payload)

def to_client_card(toWho):
    payload = "{\n  \"attachments\": [\n    {\n      \"contentType\": \"application/vnd.microsoft.card.adaptive\",\n      \"content\": {\n        \"$schema\": \"http://adaptivecards.io/schemas/adaptive-card.json\",\n        \"type\": \"AdaptiveCard\",\n        \"version\": \"1.0\",\n        \"body\": [\n          {\n            \"type\": \"ColumnSet\",\n            \"columns\": [\n              {\n                \"type\": \"Column\",\n                \"width\": 2,\n                \"items\": [\n                  {\n                    \"type\": \"TextBlock\",\n                    \"text\": \"Please fill client details:\"\n                  },\n                  {\n                    \"type\": \"Input.Text\",\n                    \"id\": \"organization_name\",\n           \"placeholder\": \"Petrom\",\n          \"style\": \"compact\"\n                    },\n {\n                    \"type\": \"Input.Text\",\n                    \"id\": \"client_info\",\n       \"placeholder\": \"Georgescu Florescu\",\n                 \"style\": \"compact\"\n                   },\n   {\n                    \"type\": \"TextBlock\",\n                    \"text\": \"How many items ?\"\n                  },\n      {\n                    \"type\": \"Input.Text\",\n                    \"id\": \"assets_number\",\n       \"placeholder\": \" 2\",\n                 \"style\": \"compact\"\n                   }         ]\n              }\n            ]\n          }\n        ],\n        \"actions\": [\n          {\n            \"type\": \"Action.Submit\",\n            \"title\": \"Submit\"\n          }\n        ]\n      }\n    }\n  ],\n  \"toPersonId\": \""+toWho+"\",\n  \"text\": \" \"\n}"
    print(json.loads(payload))
    headers = {
        'Authorization': 'Bearer '+token,
        'Content-Type': 'application/json'
    }
    url = "https://webexapis.com/v1/messages"

    response = requests.request(
        "POST", url, headers=headers, data=payload)

# all request for localhost:5000/  will reach this method


@app.route("/cards", methods=['POST'])
def cards():
    print(request.get_json())

    url = "https://webexapis.com/v1/attachment/actions/" + \
        request.get_json()['data']['id']

    headers = {
        'Authorization': 'Bearer ZmVkZmNlMzctMjc4MC00NmMyLWI3MzUtZTdhMjk3MjhhNDE0MTk1ZmY1YzAtZmY4_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    print(json.loads(response.text))
    if 'asset_option' in json.loads(response.text)['inputs']:
        if json.loads(response.text)['inputs']['asset_option'] == "loan":
            to_client_card(json.loads(response.text)['personId'])
            # how_many_card(json.loads(response.text)['personId'])
    return {"MUIE": 123}


if __name__ == '__main__':
    app.run(host='localhost', use_reloader=True, debug=True)
