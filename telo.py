import djitellopy
import time
import cv2



drone = djitellopy.Tello()
drone.connect()
print(drone.get_battery())


drone.takeoff()

drone.streamon()
time.sleep(1)



try:

    frame = drone.get_frame_read().frame
    cv2.imwrite("tst.jpg", frame)
    # frame.imwrite("tst.jpg")

except Exception as e:
    print('er', e)


    
drone.land()

