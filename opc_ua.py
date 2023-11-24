from opcua import Client
import time

global i
i=0
def connect_opc():
    global client, i
    client = Client('opc.tcp://localhost:4840')
    try:
        client.connect()
        i=1
        print('Conectado com o servidor')
    except Exception as erro:
        print(erro)
    return(i)    

def disconect_opc():
    global i
    client.disconnect()
    print('Desconectado do Servidor')
    i=0
    return(i)
    
def read_tags():
    
    path_start_sinal = client.get_node('ns=4;s=|var|CODESYS Control Win V3.Application.PLC_PRG.start_sinal')
    start_sinal = path_start_sinal.get_value()
    path_stop_sinal = client.get_node('ns=4;s=|var|CODESYS Control Win V3.Application.PLC_PRG.stop_sinal')
    stop_sinal = path_stop_sinal.get_value()
    path_emergencia = client.get_node('ns=4;s=|var|CODESYS Control Win V3.Application.PLC_PRG.emergencia')
    emergencia = path_emergencia.get_value()
    path_sensor = client.get_node('ns=4;s=|var|CODESYS Control Win V3.Application.PLC_PRG.sensor')
    sensor = path_sensor.get_value()
    path_motor = client.get_node('ns=4;s=|var|CODESYS Control Win V3.Application.PLC_PRG.motor_esteira')
    motor = path_motor.get_value()
    
    return start_sinal,stop_sinal,emergencia,sensor,motor

def write_start():
    path_start_sinal = client.get_node('ns=4;s=|var|CODESYS Control Win V3.Application.PLC_PRG.start_sinal')
    var_type = path_start_sinal.get_data_type_as_variant_type()
    path_start_sinal.set_value(True,var_type)
    time.sleep(1)
    path_start_sinal.set_value(False,var_type)
    
def write_stop():
    path_stop_sinal = client.get_node('ns=4;s=|var|CODESYS Control Win V3.Application.PLC_PRG.stop_sinal')
    var_type = path_stop_sinal.get_data_type_as_variant_type()
    path_stop_sinal.set_value(True,var_type)
    time.sleep(1)
    path_stop_sinal.set_value(False,var_type)
    
                   