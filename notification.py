import requests
import sys

def send_ifttt_notification(event_name, webhook_key, value1=None, value2=None, value3=None):
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{webhook_key}"
    payload = {'value1': value1, 'value2': value2, 'value3': value3}
    response = requests.post(url, json=payload)
    print(response)
    if response.status_code == 200:
        print("IFTTT notification sent successfully:")
        print("\t"+value1)
        print("\t"+value2)
        print("\t"+value3)
    else:
        print("Failed to send IFTTT notification.")

# Replace 'event_name' with the name of your IFTTT event
event_name = 'sent'

# Replace 'webhook_key' with your IFTTT webhook key
webhook_key = sys.argv[0]

#read file with content to send

path = "/home/pi/legodeals/"
f = open(path+"formatted.csv", "r")
#content = ""
for line in f:
    elements = line.split(";")
    #Decide if deal is good
    if float(elements[2]) < 0.5:
        value1 = "🟩"
    elif float(elements[2]) < 1.2:
        value1 = "🟨"
    else:
        value1 = "🟥"
    # Replace the values below as per your requirement (optional)
    value1 += elements[1]
    value2 = 'https://allegrolokalnie.pl/oferty/klocki/lego-17865'
    value3 = elements[0]
    send_ifttt_notification(event_name, webhook_key, value1, value2, value3)
