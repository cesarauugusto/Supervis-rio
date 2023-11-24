#!/usr/bin/env python3

from pyModbusTCP.client import ModbusClient
import time

def connect_modbustcp():
    global i
    #realiz a conexão com o device modbus
    global client
    try:
        client = ModbusClient(
            host="localhost",
            port=502,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )
        print("Conectado ao dispositivo modbus")
        i=1
    except Exception as erro:
        print(erro) 
    return i 

def red_tags():
    #ler as tags do CLP
    emergencia = client.read_discrete_inputs(0)
    motor = client.read_discrete_inputs(1)
    sensor = client.read_discrete_inputs(2)
    start_sinal = client.read_discrete_inputs(3)
    stop_sinal = client.read_discrete_inputs(4)

    print('eme=',emergencia,'motor=',motor,'sensor=',sensor,'start=',start_sinal,'stop=',stop_sinal)
    return(emergencia,motor,sensor,start_sinal,stop_sinal)

def write_start():
    #escreve nas tags
    start_memoria = client.write_single_coil(0, True)
    time.sleep(1)
    start_memoria = client.write_single_coil(0,False)

def write_stop():
    #desliga o processo
    stop_memoria = client.write_single_coil(1,True)
    time.sleep(1)
    stop_memoria =  client.write_singlecoil(1,False)

def write_emergenciastart():
    #Liga a emergencia
    emergencia = client.write_single_coil(1,True)

def write_emergenciastop():
    #Liga a emergencia
    emergencia = client.write_singlecoil(1,False)


    

        