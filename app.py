import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

caminho ='base_vbp.xlsx'
df = pd.DataFrame(pd.read_excel(caminho))

df_cultura = df['Cultura'].value_counts().to_frame().reset_index().drop('Cultura', axis=1)
df_cidades = df['Município'].value_counts().to_frame().reset_index().drop('Município', axis=1)




app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(children=[
    dcc.Dropdown(df_cidades, multi=True, placeholder="Selecione a(s) Cidade"),
    dcc.Dropdown(df_cultura, multi=True, placeholder="Selecione a(s) Cultura"),
])

# =========  Callback  =========== #



if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)