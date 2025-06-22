import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go




# Load data
# df = pd.read_csv("lged_2021-2022.csv")
df1 = pd.read_csv('enrollment_2021-2022.csv')
df2 = pd.read_csv('completion_2021-2022.csv')
df3 = pd.read_csv('repeat_2021-2022.csv')
df4 = pd.read_csv('retention_2021-2022.csv')
df5 = pd.read_csv('shgbv_2021-2022.csv')

# =================================================================================================================
# search items
search_items = [
    "All Counties", "Bomi", "Montserrado", "ECE", "PE", "JSE", "SSE", "AE", "TVET",
    "Education", "GPI", "Completion", "Retention", "Repeats", "SGB Cases", "home",
    "Project 1", "Project 2", "Activity 1", "Activity 2", "Activity 3",
    "Teachers", "Students", "Dashboard", "Search", "Gender Parity", "Gender Parity Index"
]

# =======================List of categories enrollment, gpi, completion, repeat, rention =========================== 

# 1. Education categories for enrollment
education_categories = ['ece', 'pe', 'jse', 'sse', 'ae', 'tvet']
formatted_categories = [cat.upper() for cat in education_categories]

# 2. completion categories
completion_categories = ['ece', 'pe', 'jse', 'sse', 'ae', 'tvet']
formatted_categories = [cat.upper() for cat in completion_categories]

# 3. repeat categories
repeat_categories = ['ece', 'pe', 'jse', 'sse', 'ae', 'tvet']
formatted_categories = [cat.upper() for cat in repeat_categories]

# 4. retention categories
retention_categories = ['ece', 'pe', 'jse', 'sse', 'ae', 'tvet']
formatted_categories = [cat.upper() for cat in retention_categories]

# ==============================dropdown options for counties df1, df2, df3, df4, df5 ================================

# 1. Dropdown options for enrollment
county_options = [{'label': 'All Counties', 'value': 'all'}] + \
                 [{'label': county, 'value': county} for county in df1['county'].unique()]

# 2. Dropdown options for completion
county_options2 = [{'label': 'All Counties', 'value': 'all'}] + \
                 [{'label': county, 'value': county} for county in df2['county'].unique()]

# 3. Dropdown options for repeats
county_options3 = [{'label': 'All Counties', 'value': 'all'}] + \
                 [{'label': county, 'value': county} for county in df3['county'].unique()]

# 4. Dropdown options for retention
county_options4 = [{'label': 'All Counties', 'value': 'all'}] + \
                 [{'label': county, 'value': county} for county in df4['county'].unique()]

# 5. Dropdown options for sexual harrassment and gender-based violence (shgbv)
county_options5 = [{'label': 'All Counties', 'value': 'all'}] + \
                 [{'label': county, 'value': county} for county in df5['county'].unique()]
# ==========================================================================================================================

# Initialize Dash app with suppress_callback_exceptions=True
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Sidebar

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    # "background-color": "#f8f9fa", #1d1a1a
    "background": "#051cad",
    "color": "#fff",
    
    "-webkit-transition": "all .3s",
    "-o-transition": "all .3s",
    "transition": "all .3s",
    "height": "100vh",
    "z-index": "9",
}

# padding for the page content
CONTENT_STYLE = {
    
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div(
    [
        html.A([
                html.Img(src='/assets/navs.png', alt='', width=70, height=70, className='mx-2'),
                html.Span("Educate HER", className='fs-4', style={'color': 'red'}),
            ], className='d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none', href='/'),
        # html.H2( "HOPE", className="display-4"),
        html.Hr(),
        html.P(
            "Numbers of learners per education level in the project focus area", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Search 🔍", href="/search", style={'color': 'white'})),
                dbc.NavItem(dbc.NavLink("Home 🏠", href="/about", className='text-white', active="exact")),
                dbc.NavItem(dbc.NavLink("Overview 📊", href="/", className='text-white', active="exact")),
                dbc.NavItem(dbc.NavLink("Teachers & Staff 👨‍🏫", href="/teachers", className='text-white', active="exact")),
                
                dbc.DropdownMenu(
                    label="Learners category 🎓", 
                    children=[
                        dbc.DropdownMenuItem("Early Childhood Education (ECE)", href="/ece"),
                        dbc.DropdownMenuItem("Primary Education (PE)", href="/pe"),
                        dbc.DropdownMenuItem("Junior Secondary Education (JSE)", href="/jse"),
                        dbc.DropdownMenuItem("Senior Secondary Education (SSE)", href="/sse"),
                        dbc.DropdownMenuItem("Adult Education (AE)", href="/ae"),
                        dbc.DropdownMenuItem("Technical and Vocational Education (TVET)", href="/tvet"),
                    ],
                   
                ),
                dbc.DropdownMenu(
                    label="Reports & Discussions 📊", 
                    children=[
                        dbc.DropdownMenuItem("Research Policies", href="/ece"),
                        dbc.DropdownMenuItem("Documentory ", href="/pe"),
                        dbc.DropdownMenuItem("Analysis", href="/jse"),
                    ],
                    
                ),
            
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    html.Div(id='page-content', children=[], style=CONTENT_STYLE),



    html.Footer(
    dbc.Container([
        html.Hr(),

        # Title / Paragraph Section
        dbc.Row([
            dbc.Col(html.P(
                "The Educate HER Coalition is led by three women-led organizations with a strong focus on women’s rights, and women’s transformative leadership..",
                style={'color': 'white', 'textAlign': 'center', 'fontSize': '16px'}
            ), width=12)
        ], style={'marginBottom': '20px'}),

        # First Row: Three logos with labels
        dbc.Row([
            dbc.Col([
                html.A([
                    html.Img(src='/assets/hope.png', height="60px"),
                    html.Div("Helping Our People Excel Inc.", style={'color': 'white', 'textAlign': 'center', 'marginTop': '5px'})
                ], href='https://www.liberiawork.com/recruiter/46729', target='_blank')
            ], width=4, className='text-center'),

            dbc.Col([
                html.A([
                    html.Img(src='/assets/HER.png', height="60px"),
                    html.Div("Educate HER - Liberia", style={'color': 'white', 'textAlign': 'center', 'marginTop': '5px'})
                ], href='https://carefund.org/', target='_blank')
            ], width=4, className='text-center'),

            dbc.Col([
                html.A([
                    html.Img(src='/assets/pywi.png', height="60px"),
                    html.Div("Paramount Young Women Initiative", style={'color': 'white', 'textAlign': 'center', 'marginTop': '5px'})
                ], href='https://web.facebook.com/payowiliberia', target='_blank')
            ], width=4, className='text-center')
        ], style={'marginBottom': '30px'}),

        # Centered Heading
        dbc.Row([
            dbc.Col(html.H5("This Project is Sponsored by:", style={'color': 'white', 'textAlign': 'center'}), width=12)
        ], style={'marginBottom': '20px'}),

        # Second Row: Two logos with labels
        dbc.Row([
            dbc.Col([
                html.A([
                    html.Img(src='/assets/oxfarm.png', height="60px"),
                    html.Div("Oxfam Denmark", style={'color': 'white', 'textAlign': 'center', 'marginTop': '5px'})
                ], href='https://oxfam.dk/en', target='_blank')
            ], width=6, className='text-center'),

            dbc.Col([
                html.A([
                    html.Img(src='/assets/educationoutloud.png', height="60px"),
                    html.Div("Education Outloud", style={'color': 'white', 'textAlign': 'center', 'marginTop': '5px'})
                ], href='https://educationoutloud.org/', target='_blank')
            ], width=6, className='text-center')
        ], style={'marginBottom': '30px'}),

        # Existing Social Media and Copyright
        dbc.Row([
            dbc.Col([
                html.A(html.Img(src='/assets/facebook.png', height="40px"), href='https://web.facebook.com/profile.php?id=100082335920417#', target='_blank'),
                html.A(html.Img(src='/assets/linkedin.png', height="40px"), href='https://linkedin.com', target='_blank', style={'marginLeft': '10px'}),
                html.A(html.Img(src='/assets/twitter.avif', height="40px"), href='https://twitter.com', target='_blank', style={'marginLeft': '10px'}),
            ], width='auto', className='d-flex align-items-center'),

            dbc.Col([
                html.P(f"© {pd.Timestamp.now().year} Educate HER Liberia. Designed by RhotelHub. All rights reserved.",
                       style={'textAlign': 'right', 'marginBottom': '0px', 'color': 'white'})
            ], className='d-flex align-items-center justify-content-end')
        ], justify='between', style={'padding': '10px 0'})
    ]),

    style={
           'backgroundColor': 'steelblue', 
           'padding': '2rem 1rem', 
           'marginTop': '30px', 
           "margin-right": "2rem", 
           "margin-left": "18rem",
           }

)

])

# Callback to update main page content
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    
    # Home Page tabs
    if pathname == "/":
        return html.Div([
            html.H3("Welcome to the Educate HER Data Analytics Dashboard", 
                    style={'color': 'white', 'fontSize': '30px', 'backgroundColor': '#0e2be3', 'textAlign': 'center', 'padding': '15px'}),
                    # style={'color': 'blue', 'fontSize': '30px', 'backgroundColor': '#05157d', 'textAlign': 'center', 'padding': '15px'}),
            dcc.Tabs([
                dcc.Tab(label='Enrollment', children=[
                    dcc.Dropdown(id='county-dropdown-education', options=county_options, value='all'),
                    dcc.Graph(id='education-bar'),

                html.A('Data Source: Annual School Census',
                    href='https://ourworldindata.org/life-expectancy',
                    target='_blank',
                    style={'color': 'maroon', 'fontSize': '12px', 'fontStyle': 'italic','fontWeight': 'bold', 'textAlign': 'right', 'display': 'block'}),
                    
                    
                    # Adding paragraph below the graph
                html.P("The following categories represent different levels of education in the country:", 
                       style={'fontSize': '18px', 'fontWeight': 'bold', 'marginTop': '20px'}),
                html.P(
                    "2. Primary Education (PE): Primary education is the first stage of formal education, usually covering children ages 6 to 12. "
                    "It provides the basic skills of literacy, numeracy, and social development.\n\n"
                    ),
                html.P(
                    "3. Junior Secondary Education (JSE): This level follows primary education and usually caters to students aged 12 to 15. "
                    "It focuses on more specialized subjects and prepares students for senior secondary education.\n\n"
                    ),
                html.P(
                    "4. Senior Secondary Education (SSE): Senior secondary education typically includes students aged 15 to 18. "
                    "It is focused on preparing students for higher education or vocational training.\n\n"
                    ),
                html.P(
                    "5. Adult Education (AE): Adult education provides opportunities for adults who did not complete their formal education. "
                    "It focuses on literacy, vocational skills, and basic education for adults.\n\n"
                    ),
                html.P(
                    "6. Technical and Vocational Education and Training (TVET): TVET focuses on providing practical and specialized skills in various trades. "
                    "It prepares students for careers in sectors like construction, technology, and healthcare."
                    ),
                     
                ]),
                dcc.Tab(label='Gender Parity Index', children=[
                    dcc.Dropdown(id='county-dropdown-gpi', options=county_options, value='all'),
                    dcc.Graph(id='gpi-bar'),
                    
                    html.A('Data Source: Annual School Census',
                    href='http://www.moeliberia.com/minister-of-education-launches-the-2024-2025-annual-school-census-in-liberia/',
                    target='_blank',
                    style={'color': 'maroon', 'fontSize': '12px', 'fontStyle': 'italic','fontWeight': 'bold', 'textAlign': 'right', 'display': 'block'}),
                ]),
                
                
                dcc.Tab(label='Completion', children=[
                    dcc.Dropdown(id='county-dropdown-completion', options=county_options2, value='all'),
                    dcc.Graph(id='completion-graph')
                ]),
                dcc.Tab(label='Retention', children=[
                    dcc.Dropdown(id='county-dropdown-retention', options=county_options4, value='all'),
                    dcc.Graph(id='retention-graph')
                ]),
                dcc.Tab(label='Repeats', children=[
                    dcc.Dropdown(id='county-dropdown-repeat', options=county_options3, value='all'),
                    dcc.Graph(id='repeats-graph')
                ]),
                dcc.Tab(label='SGB Case', children=[
                    dcc.Dropdown(id='county-dropdown-shgbv', options=county_options5, value='all'),
                    dcc.Graph(id='shgbv-graph')
                ])
            ])
        ])

    # Teachers Page
    elif pathname == "/teachers":
        return html.H3("Teacher & Staff Information")

    # Contact or Other
    # # elif pathname == "/search":
    # #     return html.H3("Search Feature Coming Soon")

    elif pathname == "/search":
        return html.Div([
            html.H3("Search Dashboard", style={'textAlign': 'center'}),
            html.Label("Enter keyword to search county or education level:"),
            dcc.Input(id='search-input', type='text', placeholder='Search...', debounce=True),
            html.Button('Search', id='search-button', n_clicks=0),  # Add the search button
            html.Div(id='search-results')
        ])


    # Project 1 Page
    elif pathname == "/about":
        return html.Div([
            dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='/assets/top_banner.png', alt='educate HER', className="banner-image"),
                html.Div([
                    html.Br(),
                    html.H5('About Educate HER')
                ], className='alt-text'),
                html.Div([
                    html.H2("Welcome to the Educate HER Dashboard"),
                    # html.P(desc)
                    html.P("Educate HER is a national coalition of institutions and advocates committed to promoting gender equity and equality in education in Liberia. Our key strategies include, research and policy review, awareness and civic participation, capacity building of education stakeholders and key actors, and advocacy and policy engagement. Our Vision: All girls have access to safe, quality education in Liberia. One of the key strategies to achieving gender equity and equality in education is ensuring Sustainable Systems for Evidence- Based Decision Making. Lack of access to information poses a significant challenge to policy implementation and to effective civil society advocacy for this purpose. Improving the availability of and access to disaggregated data on girls education will better inform policy-making and implementation, including school policies and gender-specific programming. Making that data accessible to civil society organizations and the public will increase civic participation as it relates to holding officials accountable for girls education.", )
                ], className='overlay-text')
            ], className='banner-container')
        ]),
        
        dbc.Col([
            # html.Div(html.P(second_desc), className='text-justify'),
            html.Div(html.P("Since 2022, Educate HER has worked closely with the Department of Planning, Research, and Development to conduct quarterly data collection and analysis on girls education. We are committed to expanding that partnership to provide tangible supports that are in line with section 3.1 of the ESP and section 7 of the NPGE. With financial support from Global Partnership for Education (GPE) programs, BACKUP Education through Deutsche Gesellschaft fur Internationale Zusammenarbeit (GIZ) and Education Out Load through Oxfam Danmark, we have partnered with the Ministry of Education to develop and manage the Liberia Girls Education Dashboard. This dashboard is for stakeholders to access (gender-) disaggregated data needed to inform school policies and gender-specific programming and accelerate the National Policy on Girls Education implementation. Educate HER intends to ensure that data related to girls education in Liberia is collected in line with the Girls Education Policy, up to date, and publicly available for education stakeholders to review for program planning, education financing, and policy review."), 
                     className='text-justify'),
            # html.Div(html.P('You can zoom, rotate the virus model in the 3D Viewer to explore the virus.'), className='text-justify'),
            html.Img(src='/assets/db.png', alt='Virus', className="img-fluid"),
            # html.Div([html.I("Front. Virol.")," 1:815388. doi: 10.3389/fviro.2021.815388"], className='ref text-end')
        ]),
    ])
            
        ]),
        

    # Project 2 Page
    elif pathname == "/project-2":
        return html.Div([
            html.H3("Project 2 Details"),
            html.P("Project 2 is focused on improving access to education for marginalized communities, particularly women and children in remote areas. The project includes a variety of activities aimed at addressing barriers to education."),
            html.Ul([
                html.Li("Providing scholarships for women and children to attend school."),
                html.Li("Establishing mobile learning units to reach rural areas."),
                html.Li("Collaborating with local authorities to improve education policies."),
            ]),
            html.P("The expected impact of Project 2 includes:"),
            html.Ul([
                html.Li("Increased school attendance rates among women and children."),
                html.Li("Reduction in gender disparity in education access."),
                html.Li("Enhanced community engagement in educational initiatives."),
            ]),
            dcc.Graph(id='project-2-graph')  # Placeholder for relevant graph related to Project 2
        ])

    # Activity 1 Page
    elif pathname == "/activity-1":
        return html.Div([
            html.H3("Activity 1 Details"),
            html.P("Activity 1 focuses on organizing community events to raise awareness about the importance of education, particularly for girls and women."),
            html.Ul([
                html.Li("Hosting workshops to encourage female enrollment in schools."),
                html.Li("Collaborating with local NGOs to promote education."),
                html.Li("Creating educational campaigns through social media and radio."),
            ]),
            html.P("The impact of Activity 1 is measured through:"),
            html.Ul([
                html.Li("Increased public awareness about the importance of girls' education."),
                html.Li("Higher rates of enrollment of girls in primary and secondary education."),
            ]),
            dcc.Graph(id='activity-1-graph')  # Placeholder for relevant graph related to Activity 1
        ])

    # Activity 2 Page
    elif pathname == "/activity-2":
        return html.Div([
            html.H3("Activity 2 Details"),
            html.P("Activity 2 is focused on improving the learning environment by providing educational tools and materials to schools in underprivileged areas."),
            html.Ul([
                html.Li("Distributing textbooks and educational resources to schools."),
                html.Li("Providing digital tools such as laptops and tablets to teachers and students."),
                html.Li("Establishing library and study centers in remote areas."),
            ]),
            html.P("The key outcomes of Activity 2 include:"),
            html.Ul([
                html.Li("Improved student engagement through the use of modern educational tools."),
                html.Li("Better learning outcomes as a result of more accessible resources."),
            ]),
            dcc.Graph(id='activity-2-graph')  # Placeholder for relevant graph related to Activity 2
        ])

    # Activity 3 Page
    elif pathname == "/activity-3":
        return html.Div([
            html.H3("Activity 3 Details"),
            html.P("Activity 3 focuses on teacher training programs to enhance the pedagogical skills of educators in the targeted counties."),
            html.Ul([
                html.Li("Conducting workshops on modern teaching methods and techniques."),
                html.Li("Training teachers on how to integrate technology into the classroom."),
                html.Li("Establishing mentorship programs for novice teachers."),
            ]),
            html.P("The success of Activity 3 will be measured by:"),
            html.Ul([
                html.Li("Increased teacher satisfaction and engagement."),
                html.Li("Improved teaching quality and student outcomes."),
            ]),
            dcc.Graph(id='activity-3-graph')  # Placeholder for relevant graph related to Activity 3
        ])
    
    elif pathname in ["/about", "/project-2", "/activity-1", "/activity-2", "/activity-3"]:
        return html.H3(f"Details for {pathname.strip('/')}")
    
    # Student Pages (Each category)
    elif pathname.strip('/') in education_categories:
        selected_level = pathname.strip('/').lower()
        title_map = {
            'ece': "Early Childhood Education (ECE)",
            'pe': "Primary Education (PE)",
            'jse': "Junior Secondary Education (JSE)",
            'sse': "Senior Secondary Education (SSE)",
            'ae': "Adult Education (AE)",
            'tvet': "Technical and Vocational Education (TVET)"
        }

        return html.Div([
            html.H3(f"{title_map[selected_level]} Student Data"),
            dcc.Tabs([
                dcc.Tab(label='Enrollment', children=[
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(name='Male', x=df1['county'], y=df1[f'male_{selected_level}'], marker_color='blue'),
                            go.Bar(name='Female', x=df1['county'], y=df1[f'female_{selected_level}'], marker_color='red'),
                        ]).update_layout(
                            barmode='group',
                            xaxis_title='County',
                            yaxis_title='Number of Students',
                            title=f"Male vs Female by County - {title_map[selected_level]}"
                        )
                    )
                ]),
                dcc.Tab(label='Gender Parity Index', children=[
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(x=df1['county'], y=df1[f'{selected_level}_gpi'], marker_color='mediumseagreen')
                        ]).update_layout(
                            xaxis_title='County',
                            yaxis_title='Gender Parity Index (GPI)',
                            title=f"Gender Parity Index (GPI) by County - {title_map[selected_level]}"
                        )
                    )
                ]),

                # Completion datasets graphs
                dcc.Tab(label='Completion', children=[
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(name='Male', x=df2['county'], y=df2[f'male_{selected_level}'], marker_color='blue'),
                            go.Bar(name='Female', x=df2['county'], y=df2[f'female_{selected_level}'], marker_color='red'),
                            go.Bar(name='Total', x=df2['county'], y=df2[f'total_{selected_level}'], marker_color='green'),
                            
                        ]).update_layout(
                            barmode='group',
                            xaxis_title='County',
                            yaxis_title='Number of Students',
                            title=f"Male and Female completion by County - {title_map[selected_level]}"
                        )
                    )
                    
                # Repeats datasets graphs
                ]),
                dcc.Tab(label='Repeats', children=[
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(name='Male', x=df3['county'], y=df3[f'male_{selected_level}'], marker_color='blue'),
                            go.Bar(name='Female', x=df3['county'], y=df3[f'female_{selected_level}'], marker_color='red'),
                            go.Bar(name='Total', x=df3['county'], y=df3[f'total_{selected_level}'], marker_color='green'),        
                        ]).update_layout(
                            barmode='group',
                            xaxis_title='County',
                            yaxis_title='Number of Students',
                            title=f"Male and Female Repeats by County - {title_map[selected_level]}" 
                        )
                    )
                    
                # Retention datasets
                ]),
                dcc.Tab(label='Retention', children=[
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(name='Male', x=df4['county'], y=df4[f'male_{selected_level}'], marker_color='blue'),
                            go.Bar(name='Female', x=df4['county'], y=df4[f'female_{selected_level}'], marker_color='red'),
                            go.Bar(name='Total', x=df4['county'], y=df4[f'total_{selected_level}'], marker_color='green'),
                            
                        ]).update_layout(
                            barmode='group',
                            xaxis_title='County',
                            yaxis_title='Number of Students',
                            title=f"Male and Female completion by County - {title_map[selected_level]}" 
                        )
                    )
            
                ])
            ])
        ])

    # 404 Page
    else:
        return html.H3("Page Not Found")

# Callback for Education Bar chart on Home Page
@app.callback(
    Output('education-bar', 'figure'),
    Input('county-dropdown-education', 'value')
)
def update_education_chart(selected_county):
    if selected_county == 'all':
        data_subset = df1.sum(numeric_only=True)
    else:
        data_subset = df1[df1['county'] == selected_county].iloc[0]

    categories = ['ECE', 'PE', 'JSE', 'SSE', 'AE', 'TVET']
    male_counts = [data_subset[f'male_{cat.lower()}'] for cat in categories]
    female_counts = [data_subset[f'female_{cat.lower()}'] for cat in categories]

    fig = go.Figure(data=[
        go.Bar(name='Male', x=categories, y=male_counts, marker_color='blue'),
        go.Bar(name='Female', x=categories, y=female_counts, marker_color='red')
    ])

    fig.update_layout(
        barmode='group',
        xaxis_title='Education Category 2021-2022',
        yaxis_title='Number of Students',
        title=f"Male vs Female Participation - {'All Counties' if selected_county == 'all' else selected_county}"
    )

    return fig

# Callback for GPI Bar chart on Home Page
@app.callback(
    Output('gpi-bar', 'figure'),
    Input('county-dropdown-gpi', 'value')
)
def update_gpi_chart(selected_county):
    if selected_county == 'all':
        data_subset = df1.mean(numeric_only=True)
    else:
        data_subset = df1[df1['county'] == selected_county].iloc[0]

    gpi_categories = ['ECE', 'PE', 'JSE', 'SSE', 'AE', 'TVET']
    gpi_values = [data_subset[f'{cat.lower()}_gpi'] for cat in gpi_categories]

    fig = go.Figure(data=[
        go.Bar(x=gpi_categories, y=gpi_values, marker_color='mediumseagreen')
    ])

    fig.update_layout(
        xaxis_title='Education Category 2021-2022',
        yaxis_title='Gender Parity Index (GPI)',
        title=f"Gender Parity Index by Education Category - {'All Counties' if selected_county == 'all' else selected_county}"
    )

    return fig
    
# Callback for Completion Bar chart on Home Page
@app.callback(
    Output('completion-graph', 'figure'),
    Input('county-dropdown-completion', 'value')
)
def update_completion_graph(selected_county):
    if selected_county == 'all':
        data_subset = df2.sum(numeric_only=True)
    else:
        data_subset = df2[df2['county'] == selected_county].iloc[0]

    completion_categories = ['ECE', 'PE', 'JSE', 'SSE', 'AE', 'TVET']
    male_counts = [data_subset[f'male_{cat.lower()}'] for cat in completion_categories]
    female_counts = [data_subset[f'female_{cat.lower()}'] for cat in completion_categories]
    total_counts = [data_subset[f'total_{cat.lower()}'] for cat in completion_categories]

    fig = go.Figure(data=[
        go.Bar(name='Male', x=completion_categories, y=male_counts, marker_color='blue'),
        go.Bar(name='Female', x=completion_categories, y=female_counts, marker_color='red'),
        go.Bar(name='Total', x=completion_categories, y=total_counts, marker_color='green')
    ])

    fig.update_layout(
        barmode='group',
        xaxis_title='Completion Category 2021-2022',
        yaxis_title='Number of Students',
        title=f"Male vs Female Completion- {'All Counties' if selected_county == 'all' else selected_county}"
    )
    return fig

# Callbacks for the graphs repeats
@app.callback(
    Output('repeats-graph', 'figure'),
    Input('county-dropdown-repeat', 'value')
)
def update_repeats_graph(selected_county):
    if selected_county == 'all':
        data_subset = df3.sum(numeric_only=True)
    else:
        data_subset = df3[df3['county'] == selected_county].iloc[0]

    repeat_categories = ['ECE', 'PE', 'JSE', 'SSE', 'AE', 'TVET']
    male_counts = [data_subset[f'male_{cat.lower()}'] for cat in repeat_categories]
    female_counts = [data_subset[f'female_{cat.lower()}'] for cat in repeat_categories]
    total_counts = [data_subset[f'total_{cat.lower()}'] for cat in repeat_categories]

    fig = go.Figure(data=[
        go.Bar(name='Male', x=repeat_categories, y=male_counts, marker_color='blue'),
        go.Bar(name='Female', x=repeat_categories, y=female_counts, marker_color='red'),
        go.Bar(name='Total', x=repeat_categories, y=total_counts, marker_color='green')
    ])

    fig.update_layout(
        barmode='group',
        xaxis_title='Repeats Category 2021-2022',
        yaxis_title='Number of Students',
        title=f"Male VS Female Repeats - {'All Counties' if selected_county == 'all' else selected_county}"
    )
    return fig

# Callbacks for the graphs retention
@app.callback(
    Output('retention-graph', 'figure'),
    Input('county-dropdown-retention', 'value')
)
def update_retention_graph(selected_county):
    retention_categories = ['ECE', 'PE', 'JSE', 'SSE', 'AE', 'TVET']

    if selected_county == 'all':
        data_subset = df4.sum(numeric_only=True)
    else:
        data_subset = df4[df4['county'] == selected_county].iloc[0]

    male_counts = [data_subset[f'male_{cat.lower()}'] for cat in retention_categories]
    female_counts = [data_subset[f'female_{cat.lower()}'] for cat in retention_categories]
    total_counts = [data_subset[f'total_{cat.lower()}'] for cat in retention_categories]

    fig = go.Figure(data=[
        go.Bar(name='Male', x=retention_categories, y=male_counts, marker_color='blue'),
        go.Bar(name='Female', x=retention_categories, y=female_counts, marker_color='red'),
        go.Bar(name='Total', x=retention_categories, y=total_counts, marker_color='green')
    ])

    fig.update_layout(
        barmode='group',
        xaxis_title='Retention Category 2021-2022',
        yaxis_title='Number of Students',
        title=f"Male vs Female Retention - {'All Counties' if selected_county == 'all' else selected_county}"
    )

    return fig

    

# Callbacks for the graphs retention
@app.callback(
    Output('shgbv-graph', 'figure'),
    Input('county-dropdown-shgbv', 'value')
)
def update_shgbv_graph(selected_county):
    shgbv_categories = ['shgbv']

    if selected_county == 'all':
        data_subset = df5.sum(numeric_only=True)
    else:
        data_subset = df5[df5['county'] == selected_county].iloc[0]

    reported_counts = [data_subset[f'reported_{cat.lower()}'] for cat in shgbv_categories]
    unreported_counts = [data_subset[f'unreported_{cat.lower()}'] for cat in shgbv_categories]
    total_counts = [data_subset[f'total_{cat.lower()}'] for cat in shgbv_categories]

    fig = go.Figure(data=[
        go.Bar(name='Reported', x=shgbv_categories, y=reported_counts, marker_color='blue'),
        go.Bar(name='Not Reported', x=shgbv_categories, y=unreported_counts, marker_color='red'),
        go.Bar(name='Total', x=shgbv_categories, y=total_counts, marker_color='green')
    ])

    fig.update_layout(
        barmode='group',
        xaxis_title='Sexual Harassment and Gender-Based Violence Category 2021-2022',
        yaxis_title='Number of Students',
        title=f"Reported vs Not Reported SHGBV Cases - {'All Counties' if selected_county == 'all' else selected_county}"
    )

    return fig


@app.callback(
    Output('search-results', 'children'),
    Input('search-input', 'value')
)
def update_search_results(search_value):
    if not search_value:
        return "Type something to search."
    
    search_value = search_value.lower()
    # Search for matches in the predefined search items list
    matches = [item for item in search_items if search_value in item.lower()]
    
    if not matches:
        return "No matches found."
    
    # Creating clickable links for each matched item
    return html.Ul([
        html.Li(
            dcc.Link(
                match, 
                href=f"/{match.lower().replace(' ', '-')}",  # Formatting the URL to match the item
                style={'textDecoration': 'none', 'color': 'blue'}  # Styling the link
            )
        ) for match in matches
    ])

# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8059)