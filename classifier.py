import sys
import time
import math
import IMU


IMU.detectIMU()
if IMU.BerryIMUversion == 99:
    print("No BerryIMU found... exiting")
    sys.exit()
IMU.initIMU()

while True:
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()

    
    # Calculate the magnitude of the accelerometer readings
    acc_mag = math.sqrt(ACCx ** 2 + ACCy ** 2 + ACCz ** 2)
    gyro_mag = math.sqrt(GYRx ** 2 + GYRy ** 2 + GYRz ** 2)
    print(f"ACCx:{ACCx:.2f}, ACCy:{ACCy:.2f}, ACCz:{ACCz:.2f}, Acc Mag:{acc_mag:.2f}, GYRx:{ACCx:.2f}, GYRy:{ACCy:.2f}, GYRz:{ACCz:.2f}, Gyro Mag:{gyro_mag:.2f}")

    # Classify the activity based on thresholds
    if acc_mag < 4000:
        activity = "Upward Lift"
    else:
        if gyro_mag > 500:
            activity = "Forward Push"
        else:
            activity = "None"
    # Print the classified activity
    print(f"Classified Activity: {activity}")

    # Add a delay to control the loop rate
    time.sleep(0.5)
