import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# css used for highlighting text
highlight_css = """
    <style>
        .highlight {
            background-color: #dbfaf7;
            border-radius: 7px;
            padding: 4px;
            font-weight: 550;
        }
        .title {
            background-color: #1b3652;
            border-radius: 10px;
            padding: 5px;
            color: #ffffff;
            font-weight: 550;
        }
    </style>
"""
st.markdown(highlight_css, unsafe_allow_html=True)

# title
st.write('# <span class=title>Non-profit</span> Organizations in the United States', unsafe_allow_html=True)

# sidebar
st.sidebar.header('Size')
st.sidebar.write('How do you define an organization\'s size? Select the metric below that\'s most important to you.')
metrics = {
    'Employees': 'TOTEMPLOYEE', 
    'Revenue': 'TOTALREVCURRENT', 
    'Volunteers': 'TOTVOLUNTEERS'}
selected_metric = st.sidebar.radio('Largest organizations by:', options=metrics.keys())
n_organizations = st.sidebar.slider('Number of organizations to view:', 3, 25, 10)

# data
df = pd.read_csv('data.csv')
total_organizations = df.shape[0]

# function sourced from https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings/45846841#45846841
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', ' Thousand', ' Million', ' Billion'][magnitude])  

total_revenue = human_format(df['TOTALREVCURRENT'].sum())

# organization count dataframe
count_df = df.groupby(['STATE'])['STATE'].count()
count_df = pd.DataFrame(count_df)
count_df['count'] = count_df['STATE']
count_df = count_df.rename_axis('state').reset_index()

# top 10 organizations
top_orgs_df = df.nlargest(n_organizations, metrics[selected_metric]).sort_values(metrics[selected_metric], ascending=False)
top_orgs_df['salary_proportion'] = top_orgs_df['SALARIESCURRENT']/top_orgs_df['TOTALREVCURRENT']
top_orgs_df['NAME'] = top_orgs_df['NAME'].str.title()

top_orgs_count_df = top_orgs_df.groupby(['STATE'])['STATE'].count()
top_orgs_count_df = pd.DataFrame(top_orgs_count_df)
top_orgs_count_df['count'] = top_orgs_count_df['STATE']
top_orgs_count_df = top_orgs_count_df.rename_axis('state').reset_index()

# tabs
tab1, tab2, tab3 = st.tabs(['Exploring the U.S.', 'Largest Non-profits', 'Non-profit Salaries'])

with tab1:
    # text
    st.header('How big is the non-profit industry in the United States?')
    st.write(f'In 2017, <span class = highlight>{total_organizations:,}</span> non-profit orgnanizations \
        were registered in the United States.', unsafe_allow_html=True)
    st.write(f'They reported <span class = highlight>${total_revenue}</span> in total revenue.', unsafe_allow_html=True)

    # choropleth using plotly (streamlit does not render these from altair)
    count_map = px.choropleth(
        count_df,
        custom_data=['state', 'count'],
        locations='state', 
        locationmode='USA-states', 
        color='count', 
        scope='usa',
        color_continuous_scale=px.colors.sequential.Teal
    )
    count_map.update_traces(
        marker_line_width=0,
        hovertemplate='<br>'.join([
            '<b>%{customdata[0]}</b>'
            '<br>Organizations: %{customdata[1]}',
        ])
    )
    count_map.update_coloraxes(showscale=False)
    st.plotly_chart(count_map)

with tab2:
    # text
    st.header('Who are the largest non-profits in the United States?')
    st.write('By revenue, <span class = highlight>the top 10 non-profit \
        organizations are part of the healthcare industry.</span> \
        Four of the top 10 are located in California.', unsafe_allow_html=True)
    st.write('By employee count, <span class = highlight>eight of the top 10 \
        are also healthcare organizations</span>. The two exceptions are the \
        YMCA, which provides community services aimed at youths, and the Good \
        Samaritan Society, which provides senior housing services.', unsafe_allow_html=True)
    st.write('By number of volunteers, the organizations in the top 10 have a much \
        more diverse mix of missions.')

    # bar chart
    bar_chart = alt.Chart(top_orgs_df).mark_bar().encode(
        x=alt.X(f'{metrics[selected_metric]}:Q', axis=alt.Axis(title=selected_metric)),
        y=alt.Y(f'NAME:O', sort='-x', axis=alt.Axis(title=None)),
        color=alt.Color(metrics[selected_metric], scale=alt.Scale(scheme='tealblues'), legend=None),
        tooltip=alt.Tooltip(f'{metrics[selected_metric]}:Q', format=",.0f")
    ).properties(
        width='container',
        height=350
    ).configure_scale(
        bandPaddingInner=0.25
    ).interactive()
    st.altair_chart(bar_chart, use_container_width=True)
    
    # choropleth using plotly (streamlit does not render these from altair)
    top_orgs_map = colorbar_title = px.choropleth(
        top_orgs_count_df,
        custom_data=['state', 'count'],
        locations='state', 
        locationmode='USA-states', 
        color='count', 
        scope='usa',
        color_continuous_scale=px.colors.sequential.Teal
    )
    top_orgs_map.update_coloraxes(showscale=False)
    top_orgs_map.update_traces(
        marker_line_width=0,
        hovertemplate='<br>'.join([
            '<b>%{customdata[0]}</b>'
            '<br>Organizations: %{customdata[1]}',
        ])
    )
    st.plotly_chart(top_orgs_map)


with tab3:
    # text
    st.header('How do the largest non-profits spend their money?')
    st.write('Non-profits with different missions can be expected to spend different \
        proportions of their revenue on salaries versus other expenses.')
    st.write('For example, a hospital system needs to employ a large number \
        of healthcare workers, which can be expensive. Alternatively, healthcare \
        insurance providers are often rated based on the ratio of claims expenses \
        to salaries, which should be a much smaller proportion.')
    st.write('Explore the top 10 organizations and judge for yourself whether their \
        salary percentage seems justified.')

    # bar chart
    bar_chart = alt.Chart(top_orgs_df).mark_bar().encode(
        x=alt.X('salary_proportion:Q', axis=alt.Axis(format='%', title='Revenue Used for Salaries')),
        y=alt.Y(f'NAME:O', sort='-x', axis=alt.Axis(title=None)),
        color=alt.Color('salary_proportion', scale=alt.Scale(scheme='browns'), legend=None),
        tooltip=alt.Tooltip('salary_proportion:Q', format='.0%')
    ).properties(
        width='container',
        height=350
    ).configure_scale(
        bandPaddingInner=0.25
    )
    st.altair_chart(bar_chart, use_container_width=True)