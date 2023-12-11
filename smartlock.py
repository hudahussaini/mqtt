import time
from paho.mqtt import client as mqtt

MQTT_TOPIC_LOCK_SUB= "Mobile"
MQTT_TOPIC_LOCK_PUB= "Smartlock"
FINAL_PASSWORD = "b'QWERTY123'"
TEMP_PASSWORD = "12345678"

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
    return lock

def lock_door(lock):
    """
    If this was real we would call a function to actually lock the door
    Send signal back to mobile saying door is locked
    """
    print("lock")
    lock.publish(MQTT_TOPIC_LOCK_PUB, "Locking Door")

def unlock_door(lock):
    """
    If this was real we would call a function to actually unlock the door
    Send signal back to mobile saying door is unlocked
    """
    print("unlock")
    lock.publish(MQTT_TOPIC_LOCK_PUB, "*click* *click* the door has been unlocked")

def check_password(lock, password):
    """
    Check password with final password 
    """
    print("hellofff")
    if FINAL_PASSWORD == password:
        unlock_door(lock)
        lock.loop_forever(10.0)
        #lock door for saftey after 10 secondsß
        lock_door(lock)
    else:
        lock.publish(MQTT_TOPIC_LOCK_PUB, "password is wrong")
        #temp_password(lock)

def temp_password(lock):
    lock.publish(MQTT_TOPIC_LOCK_PUB, f"Temp Password is {TEMP_PASSWORD}")
    
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    """
    Anytime a message is published to server this runs
    """
    check_password(client, str(msg.payload))

def main():
    lock = start_smartlock()
    lock.loop_start()
    lock.on_message = on_message

    time.sleep(40)
    lock.disconnect()
    lock.loop_stop()

main()