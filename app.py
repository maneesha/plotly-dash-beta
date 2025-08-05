from dash import Dash, html, dcc, page_container, page_registry
import dash_bootstrap_components as dbc


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('The Carpentries Dashboards'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']}", href=page["relative_path"])
        ) for page in page_registry.values()
    ]),
    page_container,
])

if __name__ == '__main__':
    app.run(debug=True)
