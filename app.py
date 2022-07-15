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
df['Área (ha)'] = df['Área (ha)'].apply(lambda x: str(x).replace(' ','').replace(',','.')).fillna(0).astype(float)


# =========  Layout  =========== #
app.layout = html.Div(children=[
html.Div([
    html.H2('Comparativo entre Cidades'),
    html.Div([
        html.Div([
            dcc.Dropdown(df['Município'].value_counts().index.sort_values(ascending=True),'Centenário do Sul', className='form-control', placeholder='Selecione a(s) Cidades', multi=True, id='id_cidade'),
        ], className='col-md-6 p-1'),
        html.Div([
            dcc.RadioItems(['Área (ha)','Rebanho Estático','Peso','Produção'],  id='check_rank', className='m-1', inputStyle={'margin-right': '5px', 'margin-left': '5px'}),
        ], className='col-md-6 p-1'),

    ], className='row'),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='fig_vbp_geral')], className=''),
        ], className='col-md-6 p-1'),

        html.Div([
            html.Div([dcc.Graph(id='fig_rank')], className=''),
        ], className='col-md-6 p-1'),

    ], className='row'),
html.Div([
        html.Div([
            dcc.Dropdown(df['Cultura'].value_counts().index.sort_values(ascending=True),className='form-control', placeholder='Selecione a Cultura',  id='id_produto'),
        ], className='col-md-6 p-1'),

        html.Div([

        ], className='col-md-6 p-1'),

        html.Div([
            html.Div([dcc.Graph(id='fig_produto')], className=''),
        ], className='col-md-6 p-1'),

        html.Div([
            html.Div([dcc.Graph(id='fig_area')], className=''),
        ], className='col-md-6 p-1'),

    ], className='row'),


    html.H2('Análise Estadual'),
    html.Div([
        html.Div([
            dcc.RadioItems(['Media', 'Mediana'],'Media' ,  id='check_media', className='m-1', inputStyle={'margin-right': '5px', 'margin-left': '5px'}),
        ], className='col-md-4 p-1'),
        html.Div([

        ], className='col-md-4 p-1'),
        html.Div([
            dcc.RadioItems(['Minimo', 'Maximo'],'Minimo' ,  id='check_min_max', className='m-1', inputStyle={'margin-right': '5px', 'margin-left': '5px'}),
        ], className='col-md-4 p-1'),

    ], className='row'),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='fig_media')], className=''),
        ], className='col-md-4 p-1'),

        html.Div([
            html.Div([dcc.Graph(id='fig_total')], className=''),
        ], className='col-md-4 p-1'),

            html.Div([
            html.Div([dcc.Graph(id='fig_min_max')], className=''),
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
        Output('fig_rank', 'figure'),

    ],
    [
        Input('id_cidade', 'value'),
        Input('id_produto', 'value'),
        Input('check_media', 'value'),
        Input('check_min_max', 'value'),
        Input('check_rank', 'value'),

    ])

def renderizar_graficos(id_cidade, id_produto, check_media, check_min_max, check_rank):
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

    fig_rank = go.Figure()
    if check_rank == 'Peso':
        v_lista = []
        for x in df['Safra'].unique().tolist():
            df_rank = df_filtro_cidade.groupby(by=['Safra','Cultura'])['Peso'].sum().reset_index()
            df_rank = df_rank.sort_values(by=['Peso'], axis=0,ascending=False).head(5)
            v_lista.append(df_rank)

        df_rank1 = pd.concat(v_lista)
        fig_rank = px.bar(df_rank1, x='Safra', y='Peso', color='Município', text='Cultura', barmode='group')
        fig_rank.update_layout(template='plotly_dark', transition={"duration": 400})

    elif check_rank == 'Área (ha)':
        v_lista = []
        for x in df['Safra'].unique().tolist():
            df_rank = df_filtro_cidade.groupby(by=['Safra','Município'])['Área (ha)'].sum().reset_index()
            df_rank = df_rank.sort_values(by=['Área (ha)'], axis=0,ascending=False).head(5)
            v_lista.append(df_rank)

        df_rank1 = pd.concat(v_lista)
        fig_rank = px.bar(df_rank1, x='Safra', y='Área (ha)', color='Cultura', text='Cultura', barmode='group')
        fig_rank.update_layout(template='plotly_dark', transition={"duration": 400})

    graf_linha = df_filtro_cidade.groupby(by=['Município', 'Safra'])['VBP'].apply(np.sum).to_frame().reset_index()
    fig_vbp_geral = px.line(graf_linha, x='Safra', y='VBP', color='Município')

    graf_produto = df_filtro_cidade[df_filtro_cidade['Cultura'].isin(pd.Series(id_produto))]
    fig_produto = px.bar(graf_produto, x='Safra', y='Produção', color='Município', text='Produção')

    fig_area = px.bar(graf_produto, x='Safra', y='Área (ha)', color='Município', text='Área (ha)')

    fig_media = go.Figure()
    if check_media == 'Media':
        fig_media.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Media'],text='Media', name='Media'))
        fig_media.update_layout(template='plotly_dark',height=300, transition={"duration": 400}, title='MEDIA - VBP R$')
    else:
        fig_media.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Mediana'],text='Mediana', name='Mediana'))
        fig_media.update_layout(template='plotly_dark',height=300, transition={"duration": 400}, title='MEDIANA - VBP R$')

    fig_min_max = go.Figure()
    if check_min_max == 'Minimo':
        fig_min_max.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Min'],text='Min', name='Minima'))
        fig_min_max.update_layout(template='plotly_dark',height=300, transition={"duration": 400}, title='MINIMO - VBP R$')
    else:
        fig_min_max.add_trace(go.Scatter(x=df_statistico['Safra'], y=df_statistico['Max'],text='Max', name='Maximo'))
        fig_min_max.update_layout(template='plotly_dark',height=300, transition={"duration": 400}, title='MAXIMA - VBP R$')

    fig_total = px.bar(df_statistico, x='Safra', y='Total', text='Total')



    fig_vbp_geral.update_layout(template='plotly_dark', transition={"duration": 400}, title="VBP Bruto Anual")
    fig_produto.update_layout(template='plotly_dark', transition={"duration": 400}, barmode='group', title=f"PRODUÇÃO {id_produto} (exeto animais)")
    fig_area.update_layout(template='plotly_dark', transition={"duration": 400}, barmode='group', title="COMPARAÇÃO POR AREA")
    fig_total.update_layout(template='plotly_dark',height=300 , transition={"duration": 400}, title="TOTAL POR SAFRA - VBP R$")
    fig_rank.update_layout(template='plotly_dark', transition={"duration": 400}, barmode='group')

    return fig_vbp_geral, fig_produto, fig_media, fig_min_max, fig_total, fig_area, fig_rank

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)
