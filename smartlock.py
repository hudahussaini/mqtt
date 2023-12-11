import time
from paho.mqtt import client as mqtt

MQTT_TOPIC_LOCK = "Smartlock"
FINAL_PASSWORD = "QWERTY123"
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
    lock.subscribe(MQTT_TOPIC_LOCK)
    return lock

def lock_door(lock):
    """
    If this was real we would call a function to actually lock the door
    Send signal back to mobile saying door is locked
    """
    print("Yay you were able to lock the door")
    lock.publish(MQTT_TOPIC_LOCK, "Locking Door")

def unlock_door(lock):
    """
    If this was real we would call a function to actually unlock the door
    Send signal back to mobile saying door is unlocked
    """
    print("Yay you were able to unlock the door")
    lock.publish(MQTT_TOPIC_LOCK, "*click* *click* the door has been unlocked")

def check_password(lock, password):
    """
    Check password with final password 
    """
    if FINAL_PASSWORD == password:
        unlock_door(lock)
        lock.loop_forever(10.0)
        #lock door for saftey after 10 secondsß
        lock_door(lock)
    else:
        lock.publish(MQTT_TOPIC_LOCK, "password is wrong")
        temp_password()

def temp_password(lock):
    lock.publish(MQTT_TOPIC_LOCK, f"Temp Password is {TEMP_PASSWORD}")
    
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def main():
    lock = start_smartlock()
    lock.loop_start()
    lock.on_message = on_message

    time.sleep(40)
    lock.disconnect()
    lock.loop_stop()

main()