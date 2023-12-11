from paho.mqtt import client as mqtt

MQTT_TOPIC_LOCK = "Smartlock"

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
    mobile.subscribe(MQTT_TOPIC_LOCK)
    return mobile


def request_to_unlock(mobile):
    mobile.publish(MQTT_TOPIC_LOCK, "Request to Unlock")

def request_to_lock(mobile):
    mobile.publish(MQTT_TOPIC_LOCK, "Request to lock")

def main():
    mobile = start_session()
    #user_password = input("Please Enter your password: ")
    request_to_unlock(mobile)
    #mobile.pub(MQTT_TOPIC_LOCK, user_password)

main()