import time
from paho.mqtt import client as mqtt

MQTT_TOPIC_LOCK_SUB= "Mobile"
MQTT_TOPIC_LOCK_PUB= "Smartlock"
TOPIC_ACTIVATE_TEMP_SUB = "Activate_Temp"
TOPIC_UNLOCK_WITH_TEMP_SUB = "Unlock_with_temp"
TOPIC_BREAK = "Break"
FINAL_PASSWORD = 'QWERTY123'
TEMP_PASSWORD = "12345678"
Temp_Activated = False
loop_end = False

CLIENTID = "SmartLock"
#setting IP to the network IP that both computers are on 
BROKER = "192.168.1.5"
#mosquitto runs on port 1883
PORT = 1883

def start_smartlock(lock):
    """
    This function is the first few steps needed to set up the client. 
    Uses the client ID initialized, connects it to the brokers and subscribes
    to respective topics. Also sets a LWT in case of unexpected disconnect

    Input and Output: Client Object
    """
    lock.will_set(TOPIC_BREAK, "Lock is Broken!", qos=0, retain=False)
    lock.connect(BROKER, PORT)
    #subscriptions start - Could also have done in list 
    lock.subscribe(MQTT_TOPIC_LOCK_SUB)
    lock.subscribe(TOPIC_ACTIVATE_TEMP_SUB)
    lock.subscribe(TOPIC_UNLOCK_WITH_TEMP_SUB)
    lock.subscribe(TOPIC_BREAK)
    #subscription ends
    return lock

def on_connect(client, userdata, flags, rc):
    """
    Callback function that is executed and maintains 
    connection with broker once .connect() is called

    Input: MQTT client object, User data, Connect flags recieved, Result code recieved
    Output: None

    """
    print("Connected with result code "+str(rc))

def read_lock_state():
    """
    Prototype lock:
    lock_state.txt will READ state (1 - unlocked or 0 - locked)
    Input: None
    Output: return current lock state
    """
    with open ('lock_state.txt', 'r') as f:
        #read in file and remove whitespace
        lock_state = f.read().strip()
        return lock_state

def display_lock_state(lock):
    """
    Uses read_lock_state function to check state and then
    print current state to broker.

    Topic: "Smartlock"

    Input: Lock Client Object
    Output: Publish state to broker
    """
    if read_lock_state() == '0':
        lock.publish(MQTT_TOPIC_LOCK_PUB, "Smart Lock is locked.")
    elif read_lock_state() == '1':
        lock.publish(MQTT_TOPIC_LOCK_PUB, "Smart Lock is unlocked.")
    else:
        lock.publish(MQTT_TOPIC_LOCK_PUB, "Error: cannot determine state of lock.")

def update_lock_state(new_state):
    """
    Based on the user locking or unlocking, the new state needs to be updated.
    Here we are printing a message to user to indicate the new state the lock
    will be entering into. We are also updating the lock state file. 

    Input: state (1 or 0)
    Output: None
    """
    # 1 - unlocked
    if new_state == 1:
        print("Entering unlocked state.")
    # 0 - locked
    elif new_state == 0:
        print('Entering locked state.')
    else:
        print('Error, unknown state entered.')
    with open('lock_state.txt', 'w+') as f:
        f.write(str(new_state))


def lock_door(lock):
    """
    Lock door function:
    1. Checks if the smart lock is already in the desired state. If it's not, change the state and 
    publish to broker. 
    If this was real we would call a function to actually lock the door, to prototype we change the 
    text file which represents the physical lock being changed.
    If it is currently unlocked (1) then we can lock or else user will recieve an error.

    Input: lock client object
    Output: Publish updates to broker
    """
    if read_lock_state() == '0':
        lock.publish(MQTT_TOPIC_LOCK_PUB, "\nError: the door is already locked. Please choose another option:")
        print("Error occurred. Mobile client is already locked.")
        return
    elif read_lock_state() == '1':
        update_lock_state(0)
        print("Mobile Client is Locking")
        lock.publish(MQTT_TOPIC_LOCK_PUB, "Locking Door")
    else:
        lock.publish(MQTT_TOPIC_LOCK_PUB, "Error: unable to update lock status.")

def unlock_door(lock):
    """
    unlock door function:
    1. Checks if the smart lock is already in the desired state. If it's not, change the state and 
    publish to broker. 
    If this was real we would call a function to actually unlock the door
    Send signal back to mobile saying door is unlocked
    """
    print("Mobile Client has requested to Unlock")
    # if Temp_Activated == True:
    #     lock.publish(MQTT_TOPIC_LOCK_PUB, "Temp password needed")
    if read_lock_state() == '0':
        update_lock_state(1)
        lock.publish(MQTT_TOPIC_LOCK_PUB, "*click* *click* the door has been unlocked")
        return

    elif read_lock_state() == '1':
        lock.publish(MQTT_TOPIC_LOCK_PUB, "\nError: the door is already unlocked. Please choose another option:")
        print("Error occurred. Mobile client is already unlocked.")
        return
    else:
        lock.publish(MQTT_TOPIC_LOCK_PUB, "Error: unable to update lock status.")


def check_password(lock, strmessage, topic):
    """
    Check password with final password 
    """
    str_message_pass = strmessage.split(": ", 1)
    #str message is an array with [request, password]
    password = str_message_pass[1]
    print("User Password Entered: ", password)
    if FINAL_PASSWORD == password:
        if topic == TOPIC_ACTIVATE_TEMP_SUB:
            Activate_Temp(lock)
        else:
            unlock_door(lock)
            #lock.loop_forever(10.0)
            #lock.loop_start()
            #time.sleep(10)
            #lock.publish(MQTT_TOPIC_LOCK_PUB, "Door locking...10 seconds of inactivity")
            #lock.loop_stop()
            #lock door for saftey after 10 secondsß
        #    lock_door(lock)
            

    else:
        lock.publish(MQTT_TOPIC_LOCK_PUB, "password is wrong")
        #temp_password(lock)

def Activate_Temp(lock):
    global Temp_Activated
    Temp_Activated = True
    lock.publish(MQTT_TOPIC_LOCK_PUB, f"temp pw activated.\nYour temporary password is: {TEMP_PASSWORD}")
    

def Dectivate_temp():
    global Temp_Activated
    Temp_Activated = False

def use_temp_pw_to_unlock(lock, strmsg):
    str_message_pass = strmsg.split(": ", 1)
    #str message is an array with [request, password]
    user_temp_password = str_message_pass[1]
    if user_temp_password == TEMP_PASSWORD and Temp_Activated:
        unlock_door(lock)
        Dectivate_temp()
    else:
        lock.publish(MQTT_TOPIC_LOCK_PUB, "\nError: Password is wrong, temp password not activated, or temp password re-usal attempted. Please choose another option and try again: ")

def simulate_broken_lock(client):
    # Simulate the lock entering a broken state
    client.disconnect()

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    """
    Anytime a message is published to server this runs
    """
    strmsg = (msg.payload).decode()
    strtopic = msg.topic
    if strtopic == MQTT_TOPIC_LOCK_SUB:
        if strmsg == ("Request to Lock"):
            lock_door(client)
        elif strmsg == ("Lock status request"):
            display_lock_state(client)
        elif strmsg == ("Exit request"):
            global loop_end
            loop_end = True
            return loop_end
        else:
            check_password(client, strmsg, MQTT_TOPIC_LOCK_SUB)
    #elif strmsg == ("Request to Lock"):
        #lock_door(client)
    elif strtopic == TOPIC_ACTIVATE_TEMP_SUB:
        check_password(client, strmsg, TOPIC_ACTIVATE_TEMP_SUB)
    elif strtopic == TOPIC_UNLOCK_WITH_TEMP_SUB:
        use_temp_pw_to_unlock(client, strmsg)
    elif strtopic == TOPIC_BREAK:
        print("simulating broken lock")
        simulate_broken_lock(client)
    else:
        exit()


def main():
    lock = mqtt.Client(CLIENTID)
    lock.on_connect = on_connect
    if read_lock_state() == '1':
        update_lock_state(0)
        print("Resetting to Default State 0: Locked")
    else:
        print("Default State 0: Locked")
    start_smartlock(lock)
    while loop_end != True:
        lock.loop_start()
        lock.on_message = on_message
        #time.sleep(40)
    if loop_end == True:
        lock.disconnect()
        lock.loop_stop()
        exit()
main()