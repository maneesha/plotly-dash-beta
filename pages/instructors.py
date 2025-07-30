import dash
from dash import html, dash_table, dcc 
from utils.build_pages import get_json_from_query_number,create_country_bar_chart  
import pandas as pd

# Initialize page 
# dash.register_page(__name__, title="Instructors")

# # Load in instructors data as json and df 
# instructors_json = get_json_from_query_number(776)
# instructors_df = pd.DataFrame(instructors_json)

# # Create country counts df 
# instructors_country_counts_df = instructors_df['country'].value_counts().reset_index()

# # Create country counts bar chart 
# chart = create_country_bar_chart(instructors_country_counts_df)

# # Set up page layout
# layout = html.Div([
#     # Page heading
#     html.H1('These are our Instructors'),
#     # Page intro text 
#     html.Div("Something about Instructors. They teach DC, LC, SWC workshops."),
#     html.Br(),
#     # Display table
#     dash_table.DataTable(
#         data=instructors_json, 
#         # Add sort feature to table
#         sort_action='native',
#         # Set number of rows to display
#         page_size=20,
#     ),
#     # Display bar plot
#     html.H2('Plot Instructors by country'),
#     dcc.Graph(figure=chart)

# ]) # close outer html.Div 