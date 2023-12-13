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


def request_to_unlock(mobile, password):
    mobile.publish(MQTT_TOPIC_LOCK_PUB, f'Request to Unlock: {password}')

def request_to_lock(mobile):
    mobile.publish(MQTT_TOPIC_LOCK_PUB, "Request to Lock")

def request_temp_pw(mobile, password):
    mobile.publish(MQTT_TOPIC_LOCK_PUB, f'Request to activate temp password: {password}')

def use_temp_pass():
    user_temp_pass = input("Please enter temp password:")

def on_message(client, userdata, msg):
    """
    Anytime a message is published to server this runs
    """
    strmsg = (msg.payload).decode()
    print("log", strmsg)
    if strmsg == 'Temp password needed':
        use_temp_pass()
    else:
        print(strmsg)
        exit()



def main():
    mobile = start_session()
    mobile.loop_start()
    mobile.on_message = on_message
    print("\nMenu:")
    print("1. Unlock")
    print("2. Lock")
    print("3. Activate Temporary Password")
    print("4. Exit")

    choice = input("Enter your choice (1-5): ")
    if choice == '1':
        user_password = input("Please enter your password: ")
        request_to_unlock(mobile, user_password)
    elif choice == '2':
        request_to_lock(mobile)
    elif choice == '3':
        user_password = input("Please enter the permanent password: ")
        request_to_unlock(mobile, user_password)
    elif choice == '4':
        print("Exiting program. Goodbye!")
        exit()
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
    time.sleep(40)
    mobile.disconnect()
    mobile.loop_stop()

main()