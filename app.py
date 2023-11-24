# Bibliotecas
from dash import dash, dcc, html, Input, Output # acrescentando os módulos
import dash_bootstrap_components as dbc # estilização do bootstrap
# from Modbus import connect_modbustcp,write_emergenciastart,write_emergenciastop,write_start,write_stop,red_tags
from opc_ua import *

i=0

# Estilização externa
external_stylesheets=[dbc.themes.DARKLY]

# Cria app com dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
     
# Layout do app
app.layout = html.Div([
    
    html.Div([
        html.Div(html.Img(src=app.get_asset_url('logo_ifce.png')), id='logoif'),
        html.H2('Supervisorio da Esteira'),
    ], id='div_titulo'),
    html.Label('Servidor Desconectado',id='label_servidor'),
 
    html.Div([
        dbc.Button('Conectar Servidor', id='servidor_on',n_clicks=0),
        dbc.Button('Desconectar Servidor', id='servidor_off',n_clicks=0),
    ], id='div_botoes_server'),
    
     html.Div([
        html.Label('Aguardando Conexão', id='sinalizador_start'),
        html.Label('Aguardando Conexão', id='sinalizador_stop'),
        dbc.Button('Aguardando Conexão',id='emergenciabtn',n_clicks=0),
    ], id='div_sinaiscima'),
    
     html.Div([
        dbc.Button('Aguardando Conexão', id='aciona_btn',n_clicks=0),
        html.Label('Aguardando Conexão', id='estado_motor'),
        html.Label('Aguardando Conexão', id='estado_sensor'),
    ], id='div_sinaisbaixo'),

    dcc.Interval(interval=2000,n_intervals=0,id='tempo')
])

# Callbacks do app

#Callback Servidor
@app.callback(
    [Output('label_servidor','children'),
    Output('label_servidor', 'style')],
    [Input('servidor_on','n_clicks'),
     Input('servidor_off','n_clicks')]
)
def update_output(inputon,inputoff):
    global i
    if inputon == 0:
        return f'Servidor Desconectado'
    if i == 0:
        if inputon >= 1:
            i = connect_opc()
            return (f'Servidor Conectado', {'background-color': 'green'})
    else:
        if inputoff >= 1:
            i = disconect_opc()
            return (f'Servidor Desconectado', {'background-color': 'red'})
        
#Callback acionamento
@app.callback(
    Output('emergenciabtn','color'),
    [Input('emergenciabtn','n_clicks')]
)
def update_output_emergencia(input):
    global emergencia
    _,_,_,_,emergencia = read_tags()
    
    if input>=1:
        if emergencia == True:
            write_emergencia_start()
        elif emergencia == False:
            write_emergencia_stop()

#Callback acionamento
@app.callback(
    Output('aciona_btn','color'),
    [Input('aciona_btn','n_clicks')]
)
def update_output_acionamento(input):
    
    _,_,_,motor,_ = read_tags()
    
    if input>=1:
        if motor == True:
            write_stop()
        elif motor == False:
            write_start()
    
#Callback de tempo
@app.callback(
    [Output('aciona_btn','children'),
     Output('aciona_btn','style'),
     Output('sinalizador_start','children'),
     Output('sinalizador_start','style'),
     Output('sinalizador_stop','children'),
     Output('sinalizador_stop','style'),
     Output('estado_sensor','children'),
     Output('estado_sensor','style'),
     Output('estado_motor','children'),
     Output('estado_motor','style'),
     Output('emergenciabtn','children'),
     Output('emergenciabtn','style'),],
    [Input('tempo','n_intervals')]
)
def update_output_tempo(tempo):
    global start_sinal,stop_sinal,sensor,motor

    start_sinal,stop_sinal,sensor,motor,emergencia = read_tags()
    print('start:',start_sinal,'stop:',stop_sinal,'sensor:',sensor,'motor:',motor,'emergencia:',emergencia)

    if motor == True:
        children_aciona = 'Desligar Motor'
        style_aciona={'background-color': 'red'}
    elif motor == False:
        children_aciona = 'Ligar Motor'
        style_aciona={'background-color': 'gren'}
    if start_sinal == True:
        children_start = 'Sinalizador Ligado'
        style_start={'background-color': 'green'}
    elif start_sinal == False:
        children_start = 'Sinalizador Desligado'
        style_start={'background-color': 'red'}
    if stop_sinal == True:
        children_stop = 'Sinalizador Ligado'
        style_stop={'background-color': 'green'}
    elif stop_sinal == False:
        children_stop = 'Sinalizador Desligado'
        style_stop={'background-color': 'red'}
    if sensor == True:
        children_sensor = 'Objeto Não Identificado'
        style_sensor={'background-color': 'red'}
    elif sensor == False:
        children_sensor = 'Objeto Identificado'
        style_sensor={'background-color': 'green'}
    if motor == True:
        children_motor = 'Motor Ligado'
        style_motor={'background-color': 'green'}
    elif motor == False:
        children_motor = 'Motor Desligado'
        style_motor={'background-color': 'red'}
    if emergencia == True:
        children_emergencia = 'Emergencia Desligada'
        style_emergencia={'background-color': 'red'}
    elif emergencia == False:
        children_emergencia = 'Emergencia Ligada'
        style_emergencia={'background-color': 'red'}
        children_motor = 'Emergencia Ligada'
        style_motor={'background-color': 'red'}
        children_aciona = 'Emergencia Ligada'
        style_aciona={'background-color': 'red'}

    return(children_aciona,style_aciona,
           children_start,style_start,
           children_stop,style_stop,
           children_sensor,style_sensor,
           children_motor,style_motor,
           children_emergencia,style_emergencia)
    

# Executa o app em servidor
if __name__ == '__main__':
    app.run_server(debug=True)
