from dash import Dash, html, dcc, page_container, page_registry

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in page_registry.values()
    ]),
    page_container
])

if __name__ == '__main__':
    app.run(debug=True)
