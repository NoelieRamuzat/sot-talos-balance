'''Test CoM admittance control as described in paper.'''
from sot_talos_balance.utils.run_test_utils import *
from time import sleep

import matplotlib.pyplot as plt
import numpy as np

run_test('appli_dcmCoupledAnkleControl.py')

run_ft_calibration('robot.ftc')
raw_input("Wait before running the test")

# Connect ZMP reference and reset controllers
print('Set controller')
runCommandClient('plug(robot.zmp_estimator.emergencyStop,robot.cm.emergencyStop_zmp)')
runCommandClient('plug(robot.distribute.emergencyStop,robot.cm.emergencyStop_distribute)')
runCommandClient('robot.pitchController.kSum.value = [0.0]')
runCommandClient('robot.pitchController.kDiff.value = [0.0]')
runCommandClient('robot.rollController.kSum.value = [0.0]')
runCommandClient('robot.rollController.kDiff.value =  [0.0]')
runCommandClient('robot.dcm_control.resetDcmIntegralError()')
runCommandClient('robot.dcm_control.Ki.value = Ki_dcm')

c = ask_for_confirmation("Execute a sinusoid?")
if c:
    print("Putting the robot in position...")
    runCommandClient('robot.comTrajGen.move(1,-0.025,1.0)')
    sleep(1.0)
    print("Robot is in position!")

    c2 = ask_for_confirmation("Confirm executing the sinusoid?")
    if c2:
        print("Executing the sinusoid...")
        runCommandClient('robot.comTrajGen.startSinusoid(1,0.025,2.0)')
        print("Sinusoid started!")
    else:
        print("Not executing the sinusoid")

    c3 = ask_for_confirmation("Put the robot back?")
    if c3:
        print("Stopping the robot...")
        runCommandClient('robot.comTrajGen.stop(1)')
        sleep(5.0)
        print("Putting the robot back...")
        runCommandClient('robot.comTrajGen.move(1,0.0,1.0)')
        sleep(1.0)
        print("The robot is back in position!")
    else:
        print("Not putting the robot back")
else:
    print("Not executing the sinusoid")

raw_input("Wait before ending the test")
