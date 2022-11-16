import dash
import dash as dash
from dash.dependencies import Input, Output
from dash import dcc, dash_table
from dash import html
import plotly.express as px
import pandas as pd

df = pd.read_csv("Monkey_Pox_Cases_Worldwide.csv")

monkeypox_deprecated_df = pd.read_csv("Worldwide_Case_Detection_Timeline.csv", dtype=str)
temp_df = pd.DataFrame(monkeypox_deprecated_df['Symptoms'].value_counts()).reset_index()
temp_df = temp_df.append(
    pd.DataFrame({'index': 'multiple or other', 'Symptoms': temp_df.loc[temp_df['Symptoms'] < 5]['Symptoms'].sum()},
                 index=[0]))
temp_df = temp_df.loc[temp_df['Symptoms'] > 4]
df_daily = pd.read_csv("Daily_Country_Wise_Confirmed_Cases.csv")
new_daily = df_daily.melt(id_vars=["Country"], var_name="Date", value_name="Value")
app = dash.Dash(__name__)
server=app.server
app.layout = html.Div([
    html.H1("MONKEY-POX Dashboard", style={"textAlign": "center"}),  # Website Tittle
    html.Hr(),  # A separating line function
    html.H1(" Type Of Cases vs Countries", style={"textAlign": "center"}),  # Graph tittle
    html.Div(id="output_cases", children=[]),
    html.Label('Select type of case'),  # Dropdown label
    dcc.Dropdown(id="y_case_type", clearable=False,
                 value='Confirmed_Cases',
                 options=[{'label': y, 'value': y} for y in df[:2]],
                 style={'width': '50%'}),
    dcc.Graph(id='bar_graph', figure={}),
    html.Hr(),  # A separating line function
    html.H1(" Travel History vs Confirmed Cases", style={"textAlign": "center"}),  # Graph tittle
    dcc.Graph(id='scatter_plot_graph', figure={}),

    html.Hr(),  # A separating line function
    html.H1('Distribution of symptoms', style={"textAlign": "center"}),

    dcc.Graph(id='graph', figure={}),

    html.Hr(),  # A separating line function

    html.H4('Daily cases '),
    dcc.Graph(id="line_graph"),

])


@app.callback(
    [Output(component_id='bar_graph', component_property='figure'),
     Output(component_id='scatter_plot_graph', component_property='figure'),
     Output(component_id='graph', component_property='figure'),
     Output(component_id='line_graph', component_property='figure')
     ],

    Input(component_id='y_case_type', component_property='value'),

)
# The function return bar graph to output1, and scatter_plot graph to output2

def interactive_graph(y_axis):
    bar_graph_fig = px.histogram(data_frame=df, x='Country', y=y_axis, hover_name='Country', color='Country')
    scatter_plot_fig = px.scatter(df, x='Travel_History_Yes', y='Confirmed_Cases',
                                  hover_name='Country')
    fig = px.pie(data_frame=temp_df, names='index', values='Symptoms',
                 color_discrete_sequence=px.colors.sequential.Plasma, hole=0.5)

    fig_line = px.line(new_daily,
                       x='Date',
                       y='Value',
                       markers=True,
                       title='Global number of Confirmed Cases',
                       color_discrete_sequence=px.colors.sequential.Blugrn
                       )

    fig_line['data'][0]['line']['color'] = '#38cae0'
    fig_line['data'][0]['line']['width'] = 2

    fig_line.update_xaxes(title='Date confirmed')
    return bar_graph_fig, scatter_plot_fig, fig, fig_line


if __name__ == '__main__':
    app.run_server(port=4050)
