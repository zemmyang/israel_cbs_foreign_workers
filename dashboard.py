import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

dfs = pd.read_excel("compiled.xlsx", sheet_name=None, usecols=lambda c: not c.startswith('Unnamed:'), index_col=0)
all_countries = set([country for df in dfs.values() for country in df.index])

st.write("dashboard for the thingy that lead you here")

st.markdown("by [zemmy ang](https://zemmyang.com/)")

thousands, men_pct, age_pct, df_tab, misc = st.tabs(["in thousands", "pct men", "pct age", "dataframe display", "misc + credits"])

with df_tab:
    st.write("raw data. nothing too cool here but here it is regardless")

    year_option = st.selectbox(
        'Select year',
        dfs.keys(),
        key="year"
        )

    st.dataframe(dfs[year_option])

# pie chart representing the age ranges per country with a selectable time

with age_pct:
    st.write("i like pie... charts")

    st.write("pie chart representing the age ranges per country with a selectable time")

    year_option_pie = st.selectbox(
        'Select year',
        dfs.keys(),
        key="year_pie"
        )

    countries = dfs[str(year_option_pie)].index
    age_headers =  dfs[str(year_option_pie)].columns[1:9]

    country_option_pie = st.selectbox(
        'Select country',
        countries,
        key="country_pie"
    )

    sizes = dfs[str(year_option_pie)][age_headers].loc[country_option_pie]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=sizes.index, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)

# bar chart representing the number of people per country over time

with men_pct:
    st.write("the line will be drawn here. this far. no further.")

    st.write("shows the percentage of men per country over time")

    country_option_menpct = st.multiselect(
        'Countries to show',
        all_countries,
        ['Africa - total', 'America-Oceania - total', "Asia - total", "Europe - total"],
        key="country_menpct"
        )

    data = {year: dfs[str(year)]["% Male"] for year in dfs.keys()}

    st.line_chart(pd.DataFrame(data).T[country_option_menpct])

# get the data here
    
with misc:
    st.markdown('''
    raw data obtained from the [Israeli Central Bureau of Statistics](https://www.cbs.gov.il/en/Pages/search/yearly.aspx)
    
    data cleaning + code for this dashboard in this github repo: https://github.com/zemmyang/israel_cbs_foreign_workers
                    
    dashboard powered by [streamlit](https://streamlit.io/) and streamlit cloud

    want the raw data? [here you go](https://github.com/zemmyang/israel_cbs_foreign_workers/raw/main/compiled.xlsx) (would appreciate credit but you dont have to)
        ''')

with thousands:
    
    st.write("raw number of workers (in thousands) per country given a specific year")

    year_option_raw = st.selectbox(
        'Select year',
        dfs.keys(),
        key="year_raw"
        )
    
    countries_without_totals = [i for i in dfs[year_option_raw]["Total in thousands"].index if "total" not in i.lower()]

    st.bar_chart(dfs[year_option_raw]["Total in thousands"].loc[countries_without_totals])

    if (year_option_raw == "2021") | (year_option_raw == "2020") | (year_option_raw == "2022"):
        st.write("remember when covid was a thing? pepperidge farm remembers")
