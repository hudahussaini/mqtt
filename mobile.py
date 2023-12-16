import time
from paho.mqtt import client as mqtt

#topics that the Mobile client publishes to the Smart Lock
MQTT_TOPIC_LOCK_PUB= "Mobile"
TOPIC_ACTIVATE_TEMP_PUB = "Activate_Temp"
TOPIC_UNLOCK_WITH_TEMP_PUB = "Unlock_with_temp"

#topics that the Mobile client subscribes to
MQTT_TOPIC_LOCK_SUB= "Smartlock"
MQTT_TOPIC_BREAK = "Break"

CLIENTID = "mobile" #setting client ID
BROKER = "192.168.1.5" #setting shared Broker IP of external computer
PORT = 1883 #setting shared port for MQTT

def start_session(mobile):
    """
    This function is the first few steps needed to connect the client. 
    Uses the client ID initialized, connects it to the brokers and subscribes
    to respective topics.

    Input and Output: Client Object
    """
    mobile.connect(BROKER, PORT)
    mobile.subscribe(MQTT_TOPIC_LOCK_SUB)
    mobile.subscribe(MQTT_TOPIC_BREAK)
    return mobile

def on_connect(client, userdata, flags, rc):
    """
    Callback function that is executed and maintains 
    connection with broker once .connect() is called

    Input: MQTT client object, User data, Connect flags recieved, Result code recieved
    Output: None
    """
    print("Connected with result code "+str(rc))

def request_to_unlock(mobile, topic, password):
    """
    In order to unlock the Smart Lock Device, the client must publish a topic “Unlock_with_temp” 
    or the "Mobile" topic, in which the user can enter their password, which is encoded and sent to 
    the Smart Lock Device, along with the corresponding topic.

    Input: MQTT client object, Topic to Publish, User Password
    Output: Publish request + password to broker

    """
    mobile.publish(topic, f'Request to Unlock: {password}')

def request_to_lock(mobile):
    """
    This function indicates to the Smart Lock Device that the mobile client wants to lock the Smart Lock.
    The topic, “Mobile” is published to indicate that the mobile client is sending the lock request.
    
    Input: MQTT client object
    Output: Publish request to broker
    """
    mobile.publish(MQTT_TOPIC_LOCK_PUB, "Request to Lock")

def simulate_broken_lock(mobile):
    """
    To simulate entering a broken state for the Smart Lock Device, the mobile client is disconnected from the BROKER, using the “Break” topic.

    Input: MQTT client object
    Output: Publish message to broker
    """
    mobile.publish(MQTT_TOPIC_BREAK, "Lock is Broken!")

def view_lock_status(mobile):
    """
    This returns whether the Smart Lock Device is locked or unlocked, according to the contents of the prototype file, “lock_state.txt”.

    Input: MQTT client object
    Output: Publish request to broker
    """
    mobile.publish(MQTT_TOPIC_LOCK_PUB, "Lock status request")

def exit_request(mobile):
    """
    When the user wants to exit the program, this is published to the Smart Lock, which exits accordingly.

    Input: MQTT client object
    Output: Publish request to broker
    """
    mobile.publish(MQTT_TOPIC_LOCK_PUB, "Exit request")
    
def on_message(client, userdata, msg):
    """
    When a message is published by the Smart Lock to the BROKER, the on_message function decodes 
    and outputs the message from Smart Lock on the mobile client side.
    
    Input: MQTT client object
    Output: Message from smartlock through broker
    """
    strmsg = (msg.payload).decode()
    print("Message from smartlock: ", strmsg)

def main():
    mobile = mqtt.Client(CLIENTID) #initialize client
    mobile.on_connect = on_connect #verify connection
    start_session(mobile) #start session with mobile client
    mobile.loop_start() 
    mobile.on_message = on_message #get messages

    while True:
        time.sleep(0.5)
        print("\nMenu:") #display menu that user can choose from
        print("1. Unlock")
        print("2. Lock")
        print("3. Activate Temporary Password")
        print("4. Use Temporary Password")
        print("5. Simulate lock break")
        print("6. View current state of Smart Lock")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ") #parse user choice for each function input
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
            view_lock_status(mobile)
        elif choice == '7':
            print("Exiting program. Goodbye!")
            exit_request(mobile) #exit smart lock client
            mobile.disconnect() #disconnect from broker
            mobile.loop_stop()
            exit() #exit program
        else:
            print("Invalid choice. Please enter a number between 1 and 7.") #error catching

if __name__ == '''__main__''':
    main() #run main function