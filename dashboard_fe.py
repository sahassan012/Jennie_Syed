import dash
import dash_html_components as html
import dash_core_components as dcc
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
                html.Table(id='update-table', children=[
                    html.Thead([
                        html.Tr([html.Th("name"), html.Th("phone"), html.Th("email"), html.Th("university")])
                    ]),
                    html.Tbody([
                        html.Tr([
                            html.Td(['asd']) for i in range(0,NUM_ATTRIBUTES)
                        ]) for j in range(0, NUM_PROFESSORS)
                    ])
                ]),
                html.Button(id='professor-update-button', children='Add Professor')
            ],
            style={'display': 'inline-block', 'width': '500px', 'vertical-align': 'top'}),

            html.Div([
                html.H1(children='Delete Professor'),
                dcc.Dropdown(
                            id='delete-dropdown',  
                            options=[{'label': name, 'value': name}
                                    for name in faculty_names],
                                    value='New York'
                ),
                html.Button(id='professor-delete-button', children='Delete Professor')
            ],
            style={'display': 'inline-block', 'width': '500px', 'vertical-align': 'top'})
        ]),
        html.Div([
            # Top 10 professors by # of publications
            html.Div([
                html.H1(children='Top 10 Professors by Publications'),
                # dcc.Dropdown(
                #             id='geo-dropdown', 
                #             options=[{'label': name, 'value': name}
                #                     for name in faculty_names],
                #                     value='New York'
                # ),
                # html.P(id='professor-name', children='Name:', style={'color': 'red'}),
                # html.P(id='professor-position', children='Position:', style={'color': 'red'}),
                # html.P(id='professor-interest', children='Interest:', style={'color': 'red'}),
                # html.P(id='professor-email', children='Email:', style={'color': 'red'}),
                # html.P(id='professor-phone', children='Phone:', style={'color': 'red'}),
                # html.P(id='professor-url', children='Url:', style={'color': 'red'}),
                # html.P(id='professor-affiliation', children='Affiliation:', style={'color': 'red'})
            ],
            style={'display': 'inline-block', 'width': '550px', 'vertical-align': 'top'}),

            html.Div([
                html.H1(children='Top 10 Professors by Keywords'),
                # dcc.Dropdown(
                #             id='update-professor-dropdown', 
                #             options=[{'label': name, 'value': name}
                #                     for name in faculty_names],
                #                     value='New York'
                # ),
                # html.Table(id='update-table', children=[
                #     html.Thead([
                #         html.Tr([html.Th("name"), html.Th("phone"), html.Th("email"), html.Th("university")])
                #     ]),
                #     html.Tbody([
                #         html.Tr([
                #             html.Td(['asd']) for i in range(0,NUM_ATTRIBUTES)
                #         ]) for j in range(0, NUM_PROFESSORS)
                #     ])
                # ]),
                # html.Button(id='professor-update-button', children='Add Professor')
            ],
            style={'display': 'inline-block', 'width': '500px', 'vertical-align': 'top'}),

            html.Div([
                html.H1(children='Top 10 Professors by Citations'),
                # dcc.Dropdown(
                #             id='delete-dropdown',  
                #             options=[{'label': name, 'value': name}
                #                     for name in faculty_names],
                #                     value='New York'
                # ),
                # html.Button(id='professor-delete-button', children='Delete Professor')
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
    Output(component_id='update-table', component_property='children'),
    Input(component_id='professor-update-button', component_property='value')
)
def render_myprofessor_table(selected_professor):
    print("updating " + selected_professor)
    professor = update_my_table(selected_professor)
    return html.P(professor['affiliation'])

@app.callback(
    Output(component_id='price-graph-2', component_property='figure'),
    Input(component_id='geo-dropdown-2', component_property='value')
)
def render_graph2(selected_geography):
    filtered_avocado = avocado[avocado['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                       x='date',
                       y='average_price',
                       color='type',
                       title=f'Avocado Prices in {selected_geography}')
    return line_fig


@app.callback(
    State(component_id='delete-dropdown', component_property='value'),
    Input(component_id='professor-delete-button', component_property='value')
)
def render_delete(selected_professor):
    print('deleting ' + selected_professor)
    #professor = find_professor(selected_professor)
    #return html.P(children='Url:' + professor['photoUrl'])

if __name__ == '__main__':
    app.run_server(debug=True)