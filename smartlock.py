import time
from paho.mqtt import client as mqtt

MQTT_TOPIC_LOCK_SUB= "Mobile"
MQTT_TOPIC_LOCK_PUB= "Smartlock"
FINAL_PASSWORD = 'QWERTY123'
TEMP_PASSWORD = "12345678"
Temp_Activated = False

CLIENTID = "SmartLock"
BROKER = "localhost"
PORT = 1883

def start_smartlock():
    """
    takes in password and lock and unlock
    subscribe to mobile
    """
    lock = mqtt.Client(CLIENTID)
    lock.connect(BROKER, PORT)
    lock.subscribe(MQTT_TOPIC_LOCK_SUB)
    # lock.will_set("Break", "Lock is Broken!")
    return lock

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

def check_password(lock, strmessage):
    """
    Check password with final password 
    """
    str_message_pass = strmessage.split(": ", 1)
    #str message is an array with [request, password]
    password = str_message_pass[1]
    print(password)
    if FINAL_PASSWORD == password:
        unlock_door(lock)
        lock.loop_forever(10.0)
        #lock door for saftey after 10 secondsß
        lock_door(lock)
        # if strmessage.startswith("Request to activate temp password:"):
        #     Activate_Temp(lock, password)
    else:
        lock.publish(MQTT_TOPIC_LOCK_PUB, "password is wrong")
        #temp_password(lock)

# def Activate_Temp():
#      Temp_Activated = True
    
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    """
    Anytime a message is published to server this runs
    """
    strmsg = (msg.payload).decode()
    print("log", strmsg)
    if strmsg.startswith("Request to Unlock"):
        check_password(client, strmsg)
    elif strmsg == ("Request to Lock"):
        lock_door(client)
    elif strmsg.startswith("Request to activate temp password"):
        check_password(client, strmsg)
    else:
        exit()

# def break_lock(lock):
#     print("Lock broken")
#     lock.disconnet()


def main():
    lock = start_smartlock()
    lock.loop_start()
    lock.on_message = on_message
    time.sleep(40)
    #LWT
    # lock.break_lock(lock)
    lock.disconnect()
    lock.loop_stop()

main()