# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plot_module as pm
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

# create the layout of our app....this is where we add the routes!
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Aircraft Tracking", className="mb-2"))
        ]),
        dbc.Row([
            dbc.Col(html.H6(children="Florida Tech Capstone Design Project with Embraer", className="mb-4"))
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Plant View',
                                    className= "text-center text-light bg-dark"), body=True, color="dark"),
                    className="mb-4")
        ])
    
    ]),    
    dcc.Graph(figure=pm.fig)
   
])


# hide labels and show the plot
#fig.show()

def main():
    app.run_server(debug=True, port=5000)