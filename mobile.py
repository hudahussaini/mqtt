import time
from paho.mqtt import client as mqtt

MQTT_TOPIC_LOCK_PUB= "Mobile"
TOPIC_ACTIVATE_TEMP_PUB = "Activate_Temp"
TOPIC_UNLOCK_WITH_TEMP_PUB = "Unlock_with_temp"
MQTT_TOPIC_LOCK_SUB= "Smartlock"
MQTT_TOPIC_BREAK = "Break"

CLIENTID = "mobile"
BROKER = "localhost"
PORT = 1883

def start_session(mobile):
    """
    takes in password and lock and unlock
    subscribe to mobile
    """
    mobile.connect(BROKER, PORT)
    mobile.subscribe(MQTT_TOPIC_LOCK_SUB)
    mobile.subscribe(MQTT_TOPIC_BREAK)
    return mobile

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def request_to_unlock(mobile, topic, password):
    mobile.publish(topic, f'Request to Unlock: {password}')

def request_to_lock(mobile):
    mobile.publish(MQTT_TOPIC_LOCK_PUB, "Request to Lock")

def simulate_broken_lock(mobile):
    # Simulate the lock entering a broken state
    mobile.publish(MQTT_TOPIC_BREAK, "Lock is Broken!")

def on_message(client, userdata, msg):
    """
    Anytime a message is published to server this runs
    """
    strmsg = (msg.payload).decode()
    print("Message from smartlock: ", strmsg)


def main():
    mobile = mqtt.Client(CLIENTID)
    mobile.on_connect = on_connect
    start_session(mobile)
    mobile.loop_start()
    mobile.on_message = on_message

    print("\nMenu:")
    print("1. Unlock")
    print("2. Lock")
    print("3. Activate Temporary Password")
    print("4. Use Temporary Password")
    print("5. Simulate lock break")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")
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
        simulate_broken_lock(mobile)
    elif choice == '6':
        print("Exiting program. Goodbye!")
        exit()
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")

    time.sleep(40)
    mobile.disconnect()
    mobile.loop_stop()

main()