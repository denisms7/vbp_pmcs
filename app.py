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
    html.H1('VPB'),
    html.H2('Comparativo entre cidades'),
    html.Div([
        dcc.Dropdown(df['Município'].value_counts().index, className='form-control', placeholder='Selecione a(s) Cidades', multi=True, id='id_cidade'),
        html.Div([dcc.Graph(id='fig_vbp_geral')], className=''),
    ], className='col-sm-6 p-2'),

    html.Div([
        dcc.Dropdown(df['Cultura'].value_counts().index,className='form-control', placeholder='Selecione a Cultura',  id='id_produto'),
        html.Div([dcc.Graph(id='fig_produto')], className=''),
    ], className='col-sm-6 p-2'),

    html.H2('Media e Mediana de VPB Total'),
        html.Div([
            dcc.Dropdown(df['Município'].value_counts().index, className='form-control', placeholder='Selecione aCidades para comparar', id='id_media'),
            html.Div([dcc.Graph(id='fig_media')], className=''),
        ], className='col-sm-6 p-2'),


    html.H2('Maiores Produtores'),

], className='row'),
], className='container-fluid p-5')
# =========  Callback  =========== #
@app.callback([
        Output('fig_vbp_geral', 'figure'),
        Output('fig_produto', 'figure'),
        Output('fig_media', 'figure'),
    ],
    [
        Input('id_cidade', 'value'),
        Input('id_produto', 'value'),
        Input('id_media', 'value'),
    ])

def renderizar_graficos(id_cidade, id_produto, id_media):
    df_filtro_cidade = df[df['Município'].isin(pd.Series(id_cidade))]

    # df_media_cidade = df[[id_media, 'Safra','VBP']].groupby(by=['Safra']).mean().reset_index()
    df_media = df[['Safra','VBP']].groupby(by=['Safra'])['VBP'].mean().reset_index()
    # df_media = df_media.rename(columns={'VBP': 'Media'})

    df_mediana = df[['Safra','VBP']].groupby(by=['Safra'])['VBP'].median().reset_index()
    # df_mediana = df_mediana.rename(columns={'VBP': 'Mediana'})

    df_statistico = pd.concat([df_media, df_mediana], axis='0')
    print(df_media.head())

    graf_linha = df_filtro_cidade.groupby(by=['Município', 'Safra'])['VBP'].apply(np.sum).to_frame().reset_index()
    fig_vbp_geral = px.line(graf_linha, x='Safra', y='VBP', color='Município', text='VBP', title="VBP Bruto Anual")

    graf_produto = df_filtro_cidade[df_filtro_cidade['Cultura'].isin(pd.Series(id_produto))]
    fig_produto = px.bar(graf_produto, x='Safra', y='Produção', color='Município', title=f"{id_produto} Comparação entre Municípios (exeto animais)")


    fig_media = px.line(df_statistico, x=0, y=0, title="Medias")

    fig_vbp_geral.update_layout(template='plotly_dark', transition={"duration": 400})
    fig_produto.update_layout(template='plotly_dark', transition={"duration": 400}, barmode='group')

    return fig_vbp_geral, fig_produto, fig_media

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)
