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

CLIENTID = "SmartLock"
BROKER = "localhost"
PORT = 1883

def start_smartlock(lock):
    """
    takes in password and lock and unlock
    subscribe to mobile
    """
    lock.will_set(TOPIC_BREAK, "Lock is Broken!", qos=0, retain=False)
    lock.connect(BROKER, PORT)
    lock.subscribe(MQTT_TOPIC_LOCK_SUB)
    lock.subscribe(TOPIC_ACTIVATE_TEMP_SUB)
    lock.subscribe(TOPIC_UNLOCK_WITH_TEMP_SUB)
    lock.subscribe(TOPIC_BREAK)
    return lock

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def lock_door(lock):
    """
    If this was real we would call a function to actually lock the door
    Send signal back to mobile saying door is locked
    """
    print("Mobile Client is Locking")
    lock.publish(MQTT_TOPIC_LOCK_PUB, "Locking Door")

def unlock_door(lock):
    """
    If this was real we would call a function to actually unlock the door
    Send signal back to mobile saying door is unlocked
    """
    print("Mobile Client is Unlocking")
    # if Temp_Activated == True:
    #     lock.publish(MQTT_TOPIC_LOCK_PUB, "Temp password needed")
    lock.publish(MQTT_TOPIC_LOCK_PUB, "*click* *click* the door has been unlocked")

def check_password(lock, strmessage, topic):
    """
    Check password with final password 
    """
    str_message_pass = strmessage.split(": ", 1)
    #str message is an array with [request, password]
    password = str_message_pass[1]
    print(password)
    if FINAL_PASSWORD == password:
        if topic == TOPIC_ACTIVATE_TEMP_SUB:
            Activate_Temp(lock)
        else:
            unlock_door(lock)
            lock.loop_forever(10.0)
            #lock door for saftey after 10 secondsß
            lock_door(lock)
    else:
        lock.publish(MQTT_TOPIC_LOCK_PUB, "password is wrong")
        #temp_password(lock)

def Activate_Temp(lock):
    Temp_Activated = True
    lock.publish(MQTT_TOPIC_LOCK_PUB, "temp pw activated")
    

def Dectivate_temp():
    Temp_Activated = False

def use_temp_pw_to_unlock(lock, strmsg):
    str_message_pass = strmsg.split(": ", 1)
    #str message is an array with [request, password]
    user_temp_password = str_message_pass[1]
    if user_temp_password == TEMP_PASSWORD and Temp_Activated:
        unlock_door()
        Dectivate_temp()
    else:
        lock.publish(MQTT_TOPIC_LOCK_PUB, "password is wrong or temp pw not activated")

# def send_notification(lock):
#     # Implement your notification logic here
#     lock.publish(MQTT_TOPIC_LOCK_PUB, "WARNING: Lock has been broken into")

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
        check_password(client, strmsg, MQTT_TOPIC_LOCK_SUB)
    elif strmsg == ("Request to Lock"):
        lock_door(client)
    elif strtopic == TOPIC_ACTIVATE_TEMP_SUB:
        print("Hello")
        check_password(client, strmsg, TOPIC_ACTIVATE_TEMP_SUB)
    elif strtopic == TOPIC_UNLOCK_WITH_TEMP_SUB:
        use_temp_pw_to_unlock(client, strmsg)
    elif strtopic == TOPIC_BREAK:
        print("simulating broken lock")
        simulate_broken_lock(client)
    else:
        exit()

# def break_lock(lock):
#     print("Lock broken")
#     lock.disconnet()


def main():
    lock = mqtt.Client(CLIENTID)
    lock.on_connect = on_connect
    start_smartlock(lock)
    lock.loop_start()
    lock.on_message = on_message
    time.sleep(40)
    #LWT
    # lock.break_lock(lock)
    lock.disconnect()
    lock.loop_stop()

main()