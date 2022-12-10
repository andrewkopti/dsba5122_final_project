# Introduction
This application attempts to provide visuals to help users better understand the non-profit industry in the United States. It shows how non-profit organizations are are distributed throughout the country, who the largest non-profit organizations are based on different metrics, and how the largest non-profit organizations spend their revenue.

# Data Design
The IRS 990 dataset was retrieved from Snowflake and very little preprocessing was necessary. Charts were developed by grouping organizations by state or ranking and filtering based on number of employees, revenue, or number of volunteers.

Bar charts were developed using Altair and choropleth (map) charts were developed using Plotly.

# Future Work
The application could be enhanced by adding organization categories. This would allow a user to see whether an organization is a health insurance provider or a hospital system, for example. Another enhancement could be adding additional years to the dataset. Finally, the revenue sources for organizations could be included as an additional chart.

# Link
The application can be found on [Streamlit](https://final-project-andrewkopti.streamlit.app/).
