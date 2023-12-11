import time
from paho.mqtt import client as mqtt

MQTT_TOPIC_LOCK_PUB= "Mobile"
MQTT_TOPIC_LOCK_SUB= "Smartlock"

CLIENTID = "mobile"
BROKER = "localhost"
PORT = 1883

def start_session():
    """
    takes in password and lock and unlock
    subscribe to mobile
    """
    mobile = mqtt.Client(CLIENTID)
    mobile.connect(BROKER, PORT)
    mobile.subscribe(MQTT_TOPIC_LOCK_SUB)
    return mobile


def request_to_unlock(mobile):
    mobile.publish(MQTT_TOPIC_LOCK_PUB, "Request to Unlock")

def request_to_lock(mobile):
    mobile.publish(MQTT_TOPIC_LOCK_PUB, "Request to lock")

def on_message(client, userdata, msg):
    """
    Anytime a message is published to server this runs
    """
    print(msg.topic+" "+str(msg.payload))


def main():
    mobile = start_session()
    user_password = input("Please Enter your password: ")
    #request_to_unlock(mobile)
    mobile.publish(MQTT_TOPIC_LOCK_PUB, user_password)

    mobile.on_message = on_message

    time.sleep(40)
    mobile.disconnect()
    mobile.loop_stop()

main()