# Bibliotecas
from dash import dash, dcc, html, Input, Output # acrescentando os módulos
import dash_bootstrap_components as dbc # estilização do bootstrap
# from Modbus import connect_modbustcp,write_emergenciastart,write_emergenciastop,write_start,write_stop,red_tags
from opc_ua import connect_opc, write_start,disconect_opc,read_tags,write_stop

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
        html.Label('Sinalizador Ligado', id='sinalizador_start'),
        html.Label('Sinalizador Desligado', id='sinalizador_stop'),
        dbc.Button('Emergência Desligada',id='emergenciabtn'),
    ], id='div_sinaiscima'),
    
     html.Div([
        dbc.Button('Ligar Motor', id='aciona_btn',n_clicks=0),
        html.Label('Estado do Motor', id='estado_motor'),
        html.Label('Sensor', id='estado_sensor'),
    ], id='div_sinaisbaixo'),
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
            return f'Servidor Conectado', {'background-color': 'green'}
    else:
        if inputoff >= 1:
            i = disconect_opc()
            return f'Servidor Desconectado', {'background-color': 'red'}
        
#Callvac acionamento
@app.callback(
    Output('aciona_btn','children'),
    [Input('aciona_btn','n_clicks')]
)
def update_output_acionamento(input):
    if input%2 == 0:
        write_start()
        print('Ligando Motor...')
        return f'Ligar Motor'
    else:
        write_stop()
        print('Parando motor...')
        return f'Desligar Motor'
    
# Executa o app em servidor
if __name__ == '__main__':
    app.run_server(debug=True)