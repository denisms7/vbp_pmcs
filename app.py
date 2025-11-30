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
df['Safra'] = df['Safra'].apply(lambda x: str(x).replace('/','-')).fillna(0)

# =========  Layout  =========== #
app.layout = html.Div(children=[

    html.Div([ # linha 0
        html.Div([
            html.H3(['MUNICÍPIO DE CENTENÁRIO DO SUL – PARANÁ'], className='m-0'),
            html.Hr([], className='m-0'),
            html.P(['Paço Municipal Praça Padre Aurélio Basso, 378 – Centro - Estado do Paraná'], className='m-0'),
            html.P(['www.centenariodosul.pr.gov.br | CNPJ: 75.845.503/0001-67'], className='m-0'),
            html.P(['Fone: (43) 3675-8000 | CEP: 86.630-000 | E-mail: contato@centenariodosul.pr.gov.br'], className='m-0 mb-5'),

        ], className='col-md-12'),
    ], className='row  pt-5 ps-1'), # fim linha 0

    html.Div([ # linha 1
        html.H3('Comparativo entre Cidades'),
        html.Div([
            dcc.Dropdown(df['Município'].value_counts().index.sort_values(ascending=True),'Centenário do Sul', className='form-control', placeholder='Selecione a(s) Cidades', multi=True, id='id_cidade'),
        ], className='col-md-6 p-1'),
        html.Div([
            dcc.RadioItems(['Área (ha)',
            'Rebanho Estático', 'Abate / Comercialização', 'Peso', 'Produção',
            'VBP'],'Área (ha)', id='check_rank', className='m-1', inputStyle={'margin-right': '5px', 'margin-left': '5px'}),
        ], className='col-md-6 p-1'),
    ], className='row'), # fim linha 1

    html.Div([ # linha 2
        html.Div([html.Div([dcc.Graph(id='fig_vbp_geral')], className=''),], className='col-md-6 p-1'),
        html.Div([html.Div([dcc.Graph(id='fig_rank')], className=''),], className='col-md-6 p-1'),
    ], className='row'), # fim linha 2

    html.Div([ # linha 3
        html.H3('Comparativo de Cultura'),
        html.Div([
            dcc.Dropdown(df['Cultura'].value_counts().index.sort_values(ascending=True),className='form-control', placeholder='Selecione a Cultura',  id='id_produto'),
        ], className='col-md-6 p-1'),
        html.Div([
            ], className='col-md-6 p-1'),
    ], className='row'), # fim linha 3

    html.Div([ # linha 4
        html.Div([dcc.RadioItems(['Área (ha)',
           'Rebanho Estático', 'Abate / Comercialização', 'Peso', 'Produção',
           'VBP'],'Área (ha)',  id='check_producao_0', className='m-1', inputStyle={'margin-right': '5px', 'margin-left': '5px'}),
        ], className='col-md-6 p-1'),
        html.Div([dcc.RadioItems(['Área (ha)',
           'Rebanho Estático', 'Abate / Comercialização', 'Peso', 'Produção',
           'VBP'],'VBP',  id='check_producao_1', className='m-1', inputStyle={'margin-right': '5px', 'margin-left': '5px'}),
        ], className='col-md-6 p-1'),
    ], className='row'), # fim linha 4

    html.Div([ # linha 5
        html.Div([html.Div([dcc.Graph(id='fig_an_1')], className=''),], className='col-md-6 p-1'),
        html.Div([html.Div([dcc.Graph(id='fig_an_0')], className=''),], className='col-md-6 p-1'),
    ], className='row'), # fim da linha 5

    html.Div([ # linha 6
        html.H3('Dados Estaduais'),
        html.Div([dcc.RadioItems(['Media', 'Mediana'],'Media' ,  id='check_media', className='m-1', inputStyle={'margin-right': '5px', 'margin-left': '5px'}),], className='col-md-4 p-1'),
        html.Div([], className='col-md-4 p-1'),
        html.Div([dcc.RadioItems(['Minimo', 'Maximo'],'Minimo',  id='check_min_max', className='m-1', inputStyle={'margin-right': '5px', 'margin-left': '5px'}),], className='col-md-4 p-1'),
    ], className='row'), # fim da linha 6

    html.Div([ # linha 7
        html.Div([html.Div([dcc.Graph(id='fig_media')], className=''),], className='col-md-4 p-1'),
        html.Div([html.Div([dcc.Graph(id='fig_min_max')], className=''),], className='col-md-4 p-1'),
        html.Div([html.Div([dcc.Graph(id='fig_total')], className=''),], className='col-md-4 p-1'),
    ], className='row'), # fim da linha 7

    html.Div([ # linha 8
        html.Hr(),
        html.Div([html.P(['Desenvolvido por Denis muniz Silva'],className="text-center"),], className='col-md-12 p-1'),
    ], className='row pt-5'), # fim da linha 8

], className='container-fluid')

# =========  Callback  =========== #
@app.callback([
        Output('fig_vbp_geral', 'figure'),
        Output('fig_rank', 'figure'),
        Output('fig_an_0', 'figure'),
        Output('fig_an_1', 'figure'),
        Output('fig_media', 'figure'),
        Output('fig_total', 'figure'),
        Output('fig_min_max', 'figure'),

    ],
    [
        Input('id_cidade', 'value'),
        Input('id_produto', 'value'),
        Input('check_media', 'value'),
        Input('check_min_max', 'value'),
        Input('check_rank', 'value'),
        Input('check_producao_1', 'value'),
        Input('check_producao_0', 'value'),
    ])

def renderizar_graficos(id_cidade, id_produto, check_media, check_min_max, check_rank,check_producao_0, check_producao_1):
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

    v_lista = []
    for x in df_filtro_cidade['Município'].unique().tolist():
        for n in df['Safra'].unique().tolist():
            df_filtrado = df[(df['Município'] ==  x) & (df['Safra'] ==  n)].groupby(by=['Município','Safra','Cultura'])[check_rank].sum().reset_index().sort_values(by=[check_rank], axis=0, ascending=False).head(5)
            v_lista.append(df_filtrado)
    df_rank5 = pd.concat(v_lista)

    fig_rank = px.scatter(df_rank5, x='Safra', y=check_rank, size=check_rank , color='Município', hover_data=['Cultura', check_rank])

    graf_linha = df_filtro_cidade.groupby(by=['Município', 'Safra'])['VBP'].apply(np.sum).to_frame().reset_index()
    fig_vbp_geral = px.line(graf_linha, x='Safra', y='VBP', color='Município')

    graf_produto = df_filtro_cidade[df_filtro_cidade['Cultura'].isin(pd.Series(id_produto))]
    fig_an_0 = px.bar(graf_produto, x='Safra', y=check_producao_0, color='Município', text=check_producao_0)
    fig_an_1 = px.bar(graf_produto, x='Safra', y=check_producao_1, color='Município', text=check_producao_1)

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
    fig_rank.update_layout(template='plotly_dark', transition={"duration": 400}, title=f"TOP 5 {check_rank.upper()}")

    fig_an_0.update_layout(template='plotly_dark', transition={"duration": 400}, barmode='group', title=f"COMPARAÇÃO {check_producao_0.upper()}")
    fig_an_1.update_layout(template='plotly_dark', transition={"duration": 400}, barmode='group', title=f"COMPARAÇÃO {check_producao_1.upper()}")

    fig_total.update_layout(template='plotly_dark',height=300, transition={"duration": 400}, title="TOTAL POR SAFRA - VBP R$")

    return fig_vbp_geral, fig_rank, fig_an_0, fig_an_1, fig_media, fig_min_max, fig_total

if __name__ == "__main__":
    app.run(debug=False)
