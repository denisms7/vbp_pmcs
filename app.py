import dash
from dash import html, dcc
from dash.dependencies import Input, Output


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




app = dash.Dash(__name__)
server = app.server


df = pd.DataFrame(pd.read_excel('base_vbp.xlsx'))

df_cultura = df['Cultura'].value_counts().to_frame().reset_index().drop('Cultura', axis=1)
df_cidades = df['Município'].value_counts().to_frame().reset_index().drop('Município', axis=1)



# =========  Layout  =========== #
app.layout = html.Div(children=[

    dcc.Dropdown(
        ['New York City', 'Montreal', 'San Francisco'],
        ['Montreal', 'San Francisco'],
        multi=True, id='id_cidade'
),

        html.Div([html.Div([dcc.Graph(id='fig_vbp_geral')], className='')]),



])
# =========  Callback  =========== #
@app.callback([
        Output('fig_vbp_geral', 'figure'),
    ],
    [
        Input('id_cidade', 'value'),
    ])

def renderizar_graficos(id_cidade):

    fig_vbp_geral = px.bar(df_cidades, x='City', y=check_agrupador, color='City')
    fig_vbp_geral.update_layout(template='plotly_dark', height=250, transition={"duration": 400})


    return fig_vbp_geral

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)