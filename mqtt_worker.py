import paho.mqtt.client as mqtt
import xlwt
import xlrd
from typing import List

style0 = xlwt.easyxf(num_format_str='#,##0.00')
client = mqtt.Client()
client.connect('localhost', 1883)

aq_lists = xlwt.Workbook()


def init_lists():
    size = xlrd.open_workbook("DataTable.xls").sheet_by_index(0).nrows
    for i in range(size):
        aq_lists.add_sheet(f"Aquarium_{i} Info")
    aq_lists.add_sheet('Errors')



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('tanks/#')
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    m_s_type = f"{msg.topic}".split('/')[1]
    if m_s_type.split('_')[0] == "tank":
        s_index = int(m_s_type.split('_')[1])
        l_b = aq_lists.get_sheet(f"Aquarium_{s_index} Info")
        s_inf = f"{msg.payload.decode()}".split('__')
        l_b.write(len(l_b.__getattribute__('_Worksheet__rows')), 0, s_inf[0])
        l_b.write(len(l_b.__getattribute__('_Worksheet__rows'))-1, 1, s_inf[1])
        aq_lists.save(f"Aquariums_Info_Sim.xls")
    elif m_s_type.split('_')[0] == "error":
        s_index = int(m_s_type.split('_')[1])
        l_b = aq_lists.get_sheet("Errors")
        s_inf = f"{msg.payload.decode()}".split('__')
        l_b.write(len(l_b.__getattribute__('_Worksheet__rows')), 0, s_inf[0])
        l_b.write(len(l_b.__getattribute__('_Worksheet__rows')) - 1, 1, s_inf[1])
        aq_lists.save(f"Aquariums_Info_Sim.xls")



init_lists()
while True:
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
