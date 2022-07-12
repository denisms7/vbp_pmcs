import dash
from dash import html, dcc
from dash.dependencies import Input, Output


import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go





app = dash.Dash(__name__)
server = app.server

df = pd.DataFrame(pd.read_excel('base_vbp.xlsx'))


# =========  Layout  =========== #
app.layout = html.Div(children=[
html.Div([
    html.H1('VPB'),
    html.H2('Comparativo entre Cidades'),
    html.Div([
        dcc.Dropdown(df['Município'].value_counts().index, className='form-control', placeholder='Selecione a(s) Cidades', multi=True, id='id_cidade'),
        html.Div([dcc.Graph(id='fig_vbp_geral')], className=''),
    ], className='col-sm-6 p-2'),

    html.Div([
        dcc.Dropdown(df['Cultura'].value_counts().index,className='form-control', placeholder='Selecione a Cultura',  id='id_produto'),
        html.Div([dcc.Graph(id='fig_produto')], className=''),
    ], className='col-sm-6 p-2'),

    html.H2('Análise global'),
        html.Div([
            html.Div([dcc.Graph(id='fig_media')], className=''),
        ], className='col-sm-6 p-2'),
            html.Div([
            html.Div([dcc.Graph(id='fig_min_max')], className=''),
        ], className='col-sm-6 p-2'),


    html.H2('Maiores Produtores'),

], className='row'),
], className='container-fluid p-5')
# =========  Callback  =========== #
@app.callback([
        Output('fig_vbp_geral', 'figure'),
        Output('fig_produto', 'figure'),
        Output('fig_media', 'figure'),
        Output('fig_min_max', 'figure'),
    ],
    [
        Input('id_cidade', 'value'),
        Input('id_produto', 'value'),
    ])

def renderizar_graficos(id_cidade, id_produto):
    df_filtro_cidade = df[df['Município'].isin(pd.Series(id_cidade))]


    df_media = df.groupby(by=['Safra'])['VBP'].mean().reset_index()
    df_media = df_media.rename(columns={'VBP': 'Media'}).set_index('Safra')

    df_mediana = df.groupby(by=['Safra'])['VBP'].median().reset_index()
    df_mediana = df_mediana.rename(columns={'VBP': 'Mediana'}).set_index('Safra')

    df_minimo = df.groupby(by=['Safra'])['VBP'].min().reset_index()
    df_minimo = df_minimo.rename(columns={'VBP': 'Min'}).set_index('Safra')

    df_maximo = df.groupby(by=['Safra'])['VBP'].max().reset_index()
    df_maximo = df_maximo.rename(columns={'VBP': 'Max'}).set_index('Safra')

    df_statistico = pd.concat([df_media, df_mediana, df_maximo,df_minimo], axis=1).reset_index()



    graf_linha = df_filtro_cidade.groupby(by=['Município', 'Safra'])['VBP'].apply(np.sum).to_frame().reset_index()
    fig_vbp_geral = px.line(graf_linha, x='Safra', y='VBP', color='Município', text='VBP', title="VBP Bruto Anual")

    graf_produto = df_filtro_cidade[df_filtro_cidade['Cultura'].isin(pd.Series(id_produto))]
    fig_produto = px.bar(graf_produto, x='Safra', y='Produção', color='Município', title=f"{id_produto} Comparação entre Municípios (exeto animais)")

    fig_media = go.Figure()
    fig_media.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Media'], name='Media'))
    fig_media.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Mediana'], name='Mediana'))

    fig_min_max = go.Figure()
    fig_min_max.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Min'], name='Minima'))
    fig_min_max.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Max'], name='Maximo'))


    fig_vbp_geral.update_layout(template='plotly_dark', transition={"duration": 400})
    fig_produto.update_layout(template='plotly_dark', transition={"duration": 400}, barmode='group')
    fig_media.update_layout(template='plotly_dark', transition={"duration": 400}, title='Media e Mediana VBP por Safra')
    fig_min_max.update_layout(template='plotly_dark', transition={"duration": 400}, title='Minimo e Maxima VBP por Safra')

    return fig_vbp_geral, fig_produto, fig_media, fig_min_max

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)
