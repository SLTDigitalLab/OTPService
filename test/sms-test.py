from threading import Thread
import requests



def send_sms(mobile: str):
    data = {
        "mobile": mobile,
        "msg": "This is a test SMS. Please don't reply to this SMS."
    }
    headers = {
        "X-Api-Key": "atr_3QIWpyDc53MiVz0_-AZYJw"
    }

    response = requests.post("http://localhost:8000/api/v1/sms/send-marketing", json=data, headers=headers)
    if response.status_code == 200:
        print(f"{mobile} :: SMS sent successfully")
    else:
        print(f"{mobile} :: Failed to send SMS. Reason: ")
        print(response.text)
            

m1 = ["0704724708", "0754104592", "0704724664", "0717550776"]
m2 = ["0704724665", "0714170928", "0710451452", "0704720713"]
def send_loop(mobiles):
    print("new thread starting...")
    for mobile in mobiles:
        send_sms(mobile)


t1 = Thread(target=send_loop, kwargs={"mobiles": m1}).start()
t2 = Thread(target=send_loop, kwargs={"mobiles": m2}).start()
# t3 = Thread(target=send_loop).start()
# t4 = Thread(target=send_loop).start()
# t5 = Thread(target=send_loop).start()