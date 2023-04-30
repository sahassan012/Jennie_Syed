import dash
from dash import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from MongoDB_utils import find_professor, get_all_professor_names
from Mysql_utils import  create_my_table, update_my_table, delete_my_table, create_top10_professors_by_school, create_top10_professors_by_keywords
from Neo4j_utils import create_top10_professors_by_publications

avocado = pd.read_csv('avocado-updated-2020.csv')
app = dash.Dash()

faculty_names = get_all_professor_names()
professor = {}
NUM_PROFESSORS = 10
NUM_ATTRIBUTES = 4
#print(faculty)
app.layout = html.Div(
    children=[
        html.Div([
            # Find professor widget
            html.Div([
                html.H1(children='Find Professor'),
                dcc.Dropdown(
                            id='geo-dropdown', 
                            options=[{'label': name, 'value': name}
                                    for name in faculty_names],
                                    value='New York'
                ),
                html.P(id='professor-name', children='Name:', style={'color': 'red'}),
                html.P(id='professor-position', children='Position:', style={'color': 'red'}),
                html.P(id='professor-interest', children='Interest:', style={'color': 'red'}),
                html.P(id='professor-email', children='Email:', style={'color': 'red'}),
                html.P(id='professor-phone', children='Phone:', style={'color': 'red'}),
                html.P(id='professor-url', children='Url:', style={'color': 'red'}),
                html.P(id='professor-affiliation', children='Affiliation:', style={'color': 'red'})
            ],
            style={'display': 'inline-block', 'width': '550px', 'vertical-align': 'top'}),

            html.Div([
                html.H1(children='Update Professor'),
                dcc.Dropdown(
                            id='update-professor-dropdown', 
                            options=[{'label': name, 'value': name}
                                    for name in faculty_names],
                                    value='New York'
                ),
                dash_table.DataTable(id='update-table'),
                dbc.Button(id='professor-update-button', children='Add Professor'),
            ],

            style={'display': 'inline-block', 'width': '500px', 'vertical-align': 'top'}),
            html.Div([
                html.H1(children='Delete Professor'),
                dcc.Dropdown(
                            id='delete-professor-dropdown', 
                            options=[{'label': name, 'value': name}
                                    for name in faculty_names],
                                    value='New York'
                ),
                dash_table.DataTable(id='delete-table'),
                dbc.Button(id='professor-delete-button', children='Delete Professor'),
            ],
            style={'display': 'inline-block', 'width': '500px', 'vertical-align': 'top'}),


        ]),
        html.Div([
            # Top 10 professors by # of publications
            html.Div([
                html.H1(children='Top 10 Professors by Publications'),
            ],
            style={'display': 'inline-block', 'width': '550px', 'vertical-align': 'top'}),

            html.Div([
                html.H1(children='Top 10 Professors by Keywords'),
            ],
            style={'display': 'inline-block', 'width': '500px', 'vertical-align': 'top'}),

            html.Div([
                html.H1(children='Top 10 Professors by Citations'),
            ],
            style={'display': 'inline-block', 'width': '500px', 'vertical-align': 'top'})
        ])
    ]
)

# START callbacks for find my professor elements
@app.callback(
    Output(component_id='professor-name', component_property='children'),
    Input(component_id='geo-dropdown', component_property='value')
)
def render_name(selected_professor):
    professor = find_professor(selected_professor)
    return html.P(children='Name:' + professor['name'])

@app.callback(
    Output(component_id='professor-position', component_property='children'),
    Input(component_id='geo-dropdown', component_property='value')
)
def render_position(selected_professor):
    professor = find_professor(selected_professor)
    return html.P(children='Position:' + professor['position'])

@app.callback(
    Output(component_id='professor-interest', component_property='children'),
    Input(component_id='geo-dropdown', component_property='value')
)
def render_position(selected_professor):
    professor = find_professor(selected_professor)
    return html.P(children='Interest:' + (professor['researchInterest'] if professor['researchInterest'] else 'None'))

@app.callback(
    Output(component_id='professor-email', component_property='children'),
    Input(component_id='geo-dropdown', component_property='value')
)
def render_email(selected_professor):
    professor = find_professor(selected_professor)
    return html.P(children='Email:' + professor['email'])

@app.callback(
    Output(component_id='professor-phone', component_property='children'),
    Input(component_id='geo-dropdown', component_property='value')
)
def render_phone(selected_professor):
    professor = find_professor(selected_professor)
    return html.P(children='Phone:' + professor['phone'])

@app.callback(
    Output(component_id='professor-url', component_property='children'),
    Input(component_id='geo-dropdown', component_property='value')
)
def render_url(selected_professor):
    professor = find_professor(selected_professor)
    return html.P(children='Url:' + professor['photoUrl'])

@app.callback(
    Output(component_id='professor-affiliation', component_property='children'),
    Input(component_id='geo-dropdown', component_property='value')
)
def render_affiliation(selected_professor):
    professor = find_professor(selected_professor)
    return html.P(children='Affiliation:' + (professor['affiliation'] if professor['affiliation'] else 'None'))
# END callbacks for find my professor elements

@app.callback(
    Output('update-table', 'children'),
    [Input('professor-update-button', 'n_clicks')],
    Input('update-table', 'active_cell'),
    [dash.dependencies.State('update-professor-dropdown', 'value')]
)
def update_professor(n_clicks, selected_value):
    if n_clicks is None:
        return html.P('')
    professors = update_my_table(selected_value)
    df = pd.read_json(professors)
    print(df)
    return 'asd'


@app.callback(
    Output('delete-table', 'children'),
    [Input('professor-delete-button', 'n_clicks')],
    [dash.dependencies.State('delete-professor-dropdown', 'value')]
)
def delete_professor(n_clicks, selected_value):
    print('deleting ' + selected_value)
    if n_clicks is None:
        return html.P('')
    professors = delete_my_table(selected_value)
    df = pd.read_json(professors)
    print(df)
    return 'deleted'


if __name__ == '__main__':
    app.run_server(debug=True)