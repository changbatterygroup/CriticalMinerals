from dash import html, dcc
import App.constants as c


layout = html.Div([
    html.H1("Critical Minerals Assessments"),
    html.P("This is a placeholder description"),
    
    html.Div([
        html.Div([
            html.Label("Porosity %: ", style={
                'font-weight': 'bold',
                'display': 'inline-block',
                'padding-right': '10px'
                }),
            dcc.Input(id=c.P_INPUT_ID, 
                      type='number', 
                      placeholder='Enter Porosity', 
                      min=0, 
                      max=100
            )
        ], id=c.P_INPUT_ID+'-container'),
        html.Br(), 
        html.Button("Submit",id=c.BUTTON_ID, name="Submit")
    ],  id="form-box"),
    html.Br(), 
    
    html.Div([
        html.H3("Reserves"),
        html.Label("Select a plot to view:"),
        dcc.Dropdown(
            id=c.DROPDOWN_ID,
            options=[
                {'label': 'NMC Cathodes', 'value': c.DropDownOptions.NMC.value},
                {'label': 'LIB Cathodes', 'value': c.DropDownOptions.LIB.value},
                {'label': 'Reserve Map',  'value': c.DropDownOptions.RESERVES_MAP.value}
            ],
            value=c.DropDownOptions.NMC.value,
            clearable=False
        ),
        html.Div(id=c.BODY_ID)
    ])
])