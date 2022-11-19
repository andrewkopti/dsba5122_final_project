import streamlit as st
import pandas as pd
import altair as alt

# header
st.header('Non-profit Organizations in the United States')

# sidebar
st.sidebar.header('Size Metric')
st.sidebar.write('How to define an organization\'s size? Select the metric below that\'s most important to you.')
metrics = {
    'Employees': 'TOTEMPLOYEE', 
    'Revenue': 'TOTALREVCURRENT', 
    'Volunteers': 'TOTVOLUNTEERS'}
selected_metric = st.sidebar.radio('Largest organizations by:', options=metrics.keys())

# data
df = pd.read_csv('data.csv')
total_organizations = df.shape[0]
total_revenue = int(df['TOTALREVCURRENT'].sum())
top_10_df = df.nlargest(10, metrics[selected_metric]).sort_values(metrics[selected_metric], ascending=False)
top_10_df['salary_proportion'] = top_10_df['SALARIESCURRENT']/top_10_df['TOTALREVCURRENT']

# tabs
tab1, tab2, tab3 = st.tabs(['Exploring the U.S.', 'Largest Non-profits', 'Non-profit Salaries'])

with tab1:
    st.write('### How big is the non-profit industry in the United States?')
    st.write(f'In 2017, **{total_organizations:,}** non-profit orgnanizations \
        existed in the United States.')
    st.write(f'They reported **${total_revenue:,}** in total revenue.')

    # TODO: map chart

with tab2:
    st.write('### Who are the largest non-profits in the United States?')
    st.write('By revenue, the top 10 non-profit organizations are part of \
        the healthcare industry. Four of the top 10 are located in California.')
    st.write('By employee count, eight of the top 10 are also healthcare \
        organizations. The two exceptions are the YMCA, which provides community \
        services aimed at youths, and the Good Samaritan Society, which provides \
        senior housing services.')
    st.write('By number of volunteers, the organizations in the top 10 have a much \
        more diverse mix of missions.')

    # TODO: bar chart
    bar_chart = alt.Chart(top_10_df).mark_bar().encode(
        x = f'{metrics[selected_metric]}:Q', 
        y = alt.Y(f'NAME:O', sort='-x')
    )
    st.altair_chart(bar_chart, use_container_width=True)
    
    # TODO: map chart

with tab3:
    st.write('### How do the largest non-profits spend their money?')
    st.write('Non-profits with different missions can be expected to spend different \
        proportions of their revenue on salaries versus other expenses.')
    st.write('For example, a hospital system needs to employee a large number \
        of healthcare workers, which can be expensive. Alternatively, healthcare \
        insurance providers are often rated based on the ratio of claims expenses \
        to salaries, which should be a much smaller proportion.')
    st.write('Explor the top 10 organizations and judge for yourself whether their \
        salary percentage seems justified.')

    # TODO: bar chart
    bar_chart = alt.Chart(top_10_df).mark_bar().encode(
        x = f'salary_proportion:Q', 
        y = alt.Y(f'NAME:O', sort='-x')
    )
    st.altair_chart(bar_chart, use_container_width=True)