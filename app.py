import dash
from dash import html, dcc
from dash.dependencies import Input, Output


import pandas as pd
import numpy as np
import openpyxl
import plotly.express as px
import plotly.graph_objects as go




app = dash.Dash(__name__)
server = app.server

df = pd.DataFrame(pd.read_excel('base_vbp.xlsx'))


# =========  Layout  =========== #
app.layout = html.Div(children=[
    html.Div([
        dcc.Dropdown(df['Município'].value_counts().index, multi=True, id='id_cidade'),
        html.Div([dcc.Graph(id='fig_vbp_geral')], className=''),

    ], className=''),

    dcc.Dropdown(df['Cultura'].value_counts().index,  id='id_produto'),
    html.Div([dcc.Graph(id='fig_produto')], className=''),


])
# =========  Callback  =========== #
@app.callback([
        Output('fig_vbp_geral', 'figure'),
        Output('fig_produto', 'figure'),
    ],
    [
        Input('id_cidade', 'value'),
        Input('id_produto', 'value'),
    ])

def renderizar_graficos(id_cidade, id_produto):
    df_filtro_cidade = df[df['Município'].isin(pd.Series(id_cidade))]


    graf_linha = df_filtro_cidade.groupby(by=['Município', 'Safra'])['VBP'].apply(np.sum).to_frame().reset_index()
    fig_vbp_geral = px.line(graf_linha, x='Safra', y='VBP', color='Município', text='VBP', title="VBP Bruto Anual")

    graf_produto = df_filtro_cidade[df_filtro_cidade['Cultura'].isin(pd.Series(id_produto))]
    fig_produto = px.bar(graf_produto, x='Safra', y='Produção', color='Município', title=f"{id_produto} Comparação entre Municípios (exeto animais)")

    fig_vbp_geral.update_layout(template='plotly_dark', height=400, transition={"duration": 400})
    fig_produto.update_layout(template='plotly_dark', height=400, transition={"duration": 400}, barmode='group')

    return fig_vbp_geral, fig_produto

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)