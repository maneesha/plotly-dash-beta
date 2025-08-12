# The Carpentries Data Dashboards

## About the dashboards 

This is a prototype of a set of data dashboards for The Carpentries.

The app builds similar pages for Carpentries workshops, Instructors, and Instructor Trainers. 

Each page includes a table of all data we have consent to share and counts of individuals or events displayed as a table, a bar plot, and a choropleth map. Data can be filtered by country, continent, or active status (for individuals).  The full or filtered data set can be downloaded as csv.

## Run dashboard locally

Source data comes from Redash and depends on secret API keys stored as environment variables.  Ensure you have API keys saved with the name format following `f"REDASH_KEY_QUERY{query_number}"`.

Install dependent packages from `requirements.txt`.

Run `python app.py` and go to http://127.0.0.1:8050/.

## Next steps/to-do

* Currently the aggregate data (country counts) uses the same source data as the full data table.  The aggregate data can include individuals/events without consent.
* Each page follows roughly the same layout.  This can be refactored so we are not duplicating code.  
* General UI upgrades.  Some styling is provided via `dash-bootstrap-components` but as is, it's not very nice to look at. 
* Explore what other data tables or  visualizations may be useful.  This can include ones which would go on a private dashboard.
