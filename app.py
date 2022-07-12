import dash
from dash import html, dcc
from dash.dependencies import Input, Output


import pandas as pd
import openpyxl
import plotly.express as px
import plotly.graph_objects as go

df = pd.DataFrame(pd.read_excel('base_vbp.xlsx'))

df_cidades = df['Município'].value_counts().index
df_produto = df['Cultura'].value_counts().index


app = dash.Dash(__name__)
server = app.server




# =========  Layout  =========== #
app.layout = html.Div(children=[
    html.Div([
        dcc.Dropdown(df_cidades,'Centenário do Sul', multi=True, id='id_cidade'),
        dcc.Dropdown(df_produto, multi=True, id='id_produto')
    ], className=''),

    html.Div([dcc.Graph(id='fig_vbp_geral')], className=''),
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
    df_filtro_cidade = df[df['Município'].isin([id_cidade])]
    graf_linha = df_filtro_cidade.groupby(by=['Município', 'Safra'])['VBP'].sum().to_frame().reset_index()

    print(df_filtro_cidade)

    fig_vbp_geral = px.line(graf_linha, x="Safra", y="VBP", color='Município', text="VBP")
    fig_produto = px.bar(df_filtro_cidade, x='Safra', y='Produção')

    fig_vbp_geral.update_layout(template='plotly_dark', height=500, transition={"duration": 400})
    fig_produto.update_layout(template='plotly_dark', height=250, transition={"duration": 400})

    return fig_vbp_geral, fig_produto

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)