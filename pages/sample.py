import dash_ag_grid as dag
import pandas as pd
from dash import register_page, html 

# Initialize page 
register_page(__name__, title="Sample")

# Sample data
data = pd.DataFrame({
    'Country': ['USA', 'USA', 'Canada', 'Canada', 'Mexico'],
    'City': ['New York', 'Los Angeles', 'Toronto', 'Vancouver', 'Mexico City'],
    'Population': [8_000_000, 4_000_000, 3_000_000, 2_000_000, 9_000_000]
})

grid = dag.AgGrid(
    rowData=data.to_dict('records'),
    columnDefs=[
        {"field": "Country", "rowGroup": True, "hide": True}, # Group by Country, but hide the original column
        {"field": "City", "cellRenderer": "agGroupCellRenderer", "showRowGroup": 'Country'}, # Display Country groups in City column
        {"field": "Population", "aggFunc": "sum"}, # Sum population within groups
    ],
    columnSize="sizeToFit",
    defaultColDef={"resizable": True, "sortable": True},
    dashGridOptions={"groupDisplayType": "custom"}, # Customize group display
)


layout = html.Div([grid])