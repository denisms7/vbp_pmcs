import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go





app = dash.Dash(__name__)
server = app.server

pd.set_option('float_format','{:.3f}'.format)

df = pd.DataFrame(pd.read_excel('base_vbp.xlsx'))
df['Área (ha)'] = df['Área (ha)'].apply(lambda x: str(x).replace(' ',''))


# =========  Layout  =========== #
app.layout = html.Div(children=[
html.Div([
    html.H1('VBP'),
    html.H2('Comparativo entre Cidades'),
    html.Div([
        html.Div([
            dcc.Dropdown(df['Município'].value_counts().index.sort_values(ascending=True),'Centenário do Sul', className='form-control', placeholder='Selecione a(s) Cidades', multi=True, id='id_cidade'),
            html.Div([dcc.Graph(id='fig_vbp_geral')], className=''),
        ], className='col-md-6 p-1'),

        html.Div([
            dcc.Dropdown(df['Cultura'].value_counts().index.sort_values(ascending=True),className='form-control', placeholder='Selecione a Cultura',  id='id_produto'),
            html.Div([dcc.Graph(id='fig_produto')], className=''),
        ], className='col-md-6 p-1'),

        html.Div([
            html.Div([dcc.Graph(id='fig_area')], className=''),
        ], className='col-md-6 p-1'),

    ], className='row'),


    html.H2('Análise Estadual'),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='fig_media')], className=''),
        ], className='col-md-4 p-1'),

            html.Div([
            html.Div([dcc.Graph(id='fig_min_max')], className=''),
        ], className='col-md-4 p-1'),

        html.Div([
            html.Div([dcc.Graph(id='fig_total')], className=''),
        ], className='col-md-4 p-1'),
    ], className='row'),



], className='row p-2'),
], className='container-fluid')
# =========  Callback  =========== #
@app.callback([
        Output('fig_vbp_geral', 'figure'),
        Output('fig_produto', 'figure'),
        Output('fig_media', 'figure'),
        Output('fig_min_max', 'figure'),
        Output('fig_total', 'figure'),
        Output('fig_area', 'figure'),
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

    df_total = df.groupby(by=['Safra'])['VBP'].sum().reset_index()
    df_total = df_total.rename(columns={'VBP': 'Total'}).set_index('Safra')

    df_statistico = pd.concat([df_media, df_mediana, df_maximo,df_minimo, df_total], axis=1).reset_index()



    graf_linha = df_filtro_cidade.groupby(by=['Município', 'Safra'])['VBP'].apply(np.sum).to_frame().reset_index()
    fig_vbp_geral = px.line(graf_linha, x='Safra', y='VBP', color='Município')

    graf_produto = df_filtro_cidade[df_filtro_cidade['Cultura'].isin(pd.Series(id_produto))]
    fig_produto = px.bar(graf_produto, x='Safra', y='Produção', color='Município')

    # graf_area = df_filtro_cidade[df_filtro_cidade['Cultura'].isin(pd.Series(id_produto))]
    fig_area = px.bar(graf_produto, x='Safra', y='Área (ha)', color='Município')

    fig_media = go.Figure()
    fig_media.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Media'],text='Media', name='Media'))
    fig_media.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Mediana'],text='Mediana', name='Mediana'))

    fig_min_max = go.Figure()
    fig_min_max.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Min'],text='Min', name='Minima'))
    fig_min_max.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Max'],text='Max', name='Maximo'))

    fig_total = px.bar(df_statistico, x='Safra', y='Total')



    fig_vbp_geral.update_layout(template='plotly_dark', transition={"duration": 400}, title="VBP Bruto Anual")
    fig_produto.update_layout(template='plotly_dark', transition={"duration": 400}, barmode='group', title=f"{id_produto} Comparação entre Municípios (exeto animais)")
    fig_area.update_layout(template='plotly_dark', transition={"duration": 400}, barmode='group', title="Comparação por Area")
    fig_media.update_layout(template='plotly_dark',height=300, transition={"duration": 400}, title='Media e Mediana - VBP por Safra')
    fig_min_max.update_layout(template='plotly_dark',height=300, transition={"duration": 400}, title='Minimo e Maxima - VBP por Safra')
    fig_total.update_layout(template='plotly_dark',height=300 , transition={"duration": 400}, title="Total - VBP por Safra")

    return fig_vbp_geral, fig_produto, fig_media, fig_min_max, fig_total, fig_area

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)
