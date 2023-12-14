import time
from paho.mqtt import client as mqtt

MQTT_TOPIC_LOCK_PUB= "Mobile"
TOPIC_ACTIVATE_TEMP_PUB = "Activate_Temp"
TOPIC_UNLOCK_WITH_TEMP_PUB = "Unlock_with_temp"
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


def request_to_unlock(mobile, topic, password):
    mobile.publish(topic, f'Request to Unlock: {password}')

def request_to_lock(mobile):
    mobile.publish(MQTT_TOPIC_LOCK_PUB, "Request to Lock")


def on_message(client, userdata, msg):
    """
    Anytime a message is published to server this runs
    """
    strmsg = (msg.payload).decode()
    print("Message from smartlock: ", strmsg)


def main():
    mobile = start_session()
    mobile.loop_start()
    mobile.on_message = on_message

    print("\nMenu:")
    print("1. Unlock")
    print("2. Lock")
    print("3. Activate Temporary Password")
    print("4. Use Temporary Password")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")
    if choice == '1':
        user_password = input("Please enter your password: ")
        request_to_unlock(mobile, MQTT_TOPIC_LOCK_PUB, user_password)
    elif choice == '2':
        request_to_lock(mobile)
    elif choice == '3':
        user_password = input("Please enter the permanent password: ")
        request_to_unlock(mobile, TOPIC_ACTIVATE_TEMP_PUB, user_password)
    elif choice == '4':
        user_temp_password = input("Please enter the temp password: ")
        request_to_unlock(mobile, TOPIC_UNLOCK_WITH_TEMP_PUB, user_temp_password)
    elif choice == '5':
        print("Exiting program. Goodbye!")
        exit()
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
        
    time.sleep(40)
    mobile.disconnect()
    mobile.loop_stop()

main()