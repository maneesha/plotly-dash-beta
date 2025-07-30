import dash
from dash import html, dash_table, dcc 
from utils.build_pages import get_json_from_query_number, create_country_bar_chart  
import pandas as pd 

# Initialize page 
# dash.register_page(__name__, title="Trainers")

# # Load in trainers data as json and df 
# trainers_json = get_json_from_query_number(775)
# trainers_df = pd.DataFrame(trainers_json)

# # Create country counts df 
# trainers_country_counts_df = trainers_df['country'].value_counts().reset_index()

# # Create country counts bar chart 
# chart = create_country_bar_chart(trainers_country_counts_df)

# # Set up page layout
# layout = html.Div([
#     # Page heading
#     html.H1('These are our Trainers'),
#     # Page intro text
#     html.Div("Some text about the Trainers. They teach our future Instructors."),
#     html.Br(),
#     # Display table
#     dash_table.DataTable(
#         data=trainers_json, 
#         # Add sort feature to table
#         sort_action='native',
#         # Set number of rows to display
#         page_size=20,
#     ),
#     # Display bar plot
#     html.H2('Plot Trainers by country'),
#     dcc.Graph(figure=chart)

# ]) # close outer html.Div 
