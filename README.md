# The Carpentries Data Dashboards

## About the dashboards 

This is a prototype of a set of data dashboards for The Carpentries.

The app builds similar pages for Carpentries workshops, Instructors, and Instructor Trainers. 

Each page includes a table of all data we have consent to share and counts of individuals or events displayed as a table, a bar plot, and a choropleth map. Data can be filtered by country, continent, or active status (for individuals).  The full or filtered data set can be downloaded as csv.

## Next steps/to-do

* Currently the aggregate data (country counts) uses the same source data as the full data table.  The aggregate data can include individuals/events without consent.
* Each page follows roughly the same layout.  This can be refactored so we are not duplicating code.  
* General UI upgrades.  Some styling is provided via `dash-bootstrap-components` but as is, it's not very nice to look at. 
* Explore what other data tables or  visualizations may be useful.  This can include ones which would go on a private dashboard.
