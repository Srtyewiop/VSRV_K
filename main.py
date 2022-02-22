import datetime
import sched
import threading
import time
from threading import Timer
import xlrd
import paho.mqtt.client as mqtt
from typing import List
from sensors import *

loc = "DataTable.xls"
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_name('Tanks')
sheet2 = wb.sheet_by_name('Aquariums')
client = mqtt.Client()
client.connect('localhost', 1883)
aquariums: List[Aquarium] = []
global_time = datetime.datetime(year=2000, day=1, month=1, hour=0, minute=0, second=0)
curr_day = 0
time_increase_ms = 1000


def create_all(count):
    for i in range(count):
        aq = Aquarium()
        aq.set_index(i)
        aq.set_state(False)
        aq.first_time = datetime.timedelta(hours=sheet2.cell_value(i, 0), milliseconds=0)
        aq.second_time = datetime.timedelta(hours=sheet2.cell_value(i, 1), milliseconds=0)
        aq.third_time = datetime.timedelta(hours=sheet2.cell_value(i, 2), milliseconds=0)
        aq.check_errors()
        aquariums.append(aq)


def refill_tanks():
    for i in range(len(aquariums)):
        aquariums[i].set_mass(float(sheet.cell_value(i, 0)))
        if not aquariums[i].isError:
            msg_inf = global_time.strftime("%Y-%m-%d %H:%M:%S:") + str(global_time.microsecond*0.001) + '__' + str(aquariums[i].get_mass())
            print(f"tank {i} refilled successfully!")
        else:
            msg_inf = global_time.strftime("%Y-%m-%d %H:%M:%S:") + str(global_time.microsecond*0.001) + '__' + '-1'
        client.publish(f"tanks/tank_{i}", msg_inf)


def start_simulation():
    simulation()
    threading.Timer(0.001, start_simulation).start()


def simulation():
    global global_time
    global curr_day
    global time_increase_ms
    if global_time.minute == 0 and global_time.second == 0 and global_time.microsecond == 0:
        print(global_time)
    if global_time.day != curr_day:
        curr_day = global_time.day
        print(f"new day {curr_day}")
        refill_tanks()
    global_time_s = datetime.timedelta(hours=global_time.hour, minutes=global_time.minute, seconds=global_time.second)
    for i in range(len(aquariums)):
        aquariums[i].check_time(global_time_s)
        if aquariums[i].isError:
            msg_inf = global_time.strftime("%Y-%m-%d %H:%M:%S:") + str(global_time.microsecond*0.001) + '__' + 'aquarium_' + str(i)
            client.publish(f"tanks/error_{i}", msg_inf)
        if aquariums[i].check_state_and_decrease_mass((float(sheet.cell_value(i, 0))), time_increase_ms * 0.001):
            msg_inf = global_time.strftime("%Y-%m-%d %H:%M:%S:") + str(global_time.microsecond*0.001) + '__' + str(aquariums[i].get_mass())
            client.publish(f"tanks/tank_{i}", msg_inf)
    global_time += datetime.timedelta(milliseconds=time_increase_ms)


create_all(sheet.nrows)
print('created aquariums successfully!')
start_simulation()
