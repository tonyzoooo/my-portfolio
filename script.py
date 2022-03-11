import pandas as pd
import streamlit as st
from data_handler import DataHandler, DataFormatter, Data
import altair as alt



""" 
# My Portfolio

Hello there! This is a project made to better track the evolution of my personal investments. 
I wanted to have a tool at hand to organize my spendings and I stumbled upon the streamlit 
framework. It seemed to fulfill my needs so I gave it a try!

The application is meant to display the assets currently owned using a *.csv* file. 

## How does it work?

Fill out a *.csv* file with the configuration below or just use the data generator to create a sample.

|   date   | company | product | type   | value | comment |
|----------|---------|---------|--------|-------|---------|
|yyyy-mm-dd|<string> |<string> |<string>|<float>|<string> |
|...       |...      |...      |...     |...    |...      |
|...       |...      |...      |...     |...    |...      |

"""

def inputs():
    st.sidebar.header("Data here :)")
    upload_button = st.sidebar.file_uploader("Input", type=["csv"], accept_multiple_files=False)
    edit_button = st.sidebar.button("Edit data", disabled=True)
    #download_button = st.sidebar.download_button("Save file")
    return upload_button, edit_button, #download_button

def display_evolution(data: Data, formatter: DataFormatter):
        col1, col2, col3 = st.columns(3)
        with col1: 
            value = formatter.get_current_total(data.current_total)
            label = formatter.get_evolution_description("Current assets", data.current_month)
            st.metric(label, value)
        with col2: 
            value = formatter.get_evolution_float(data.first_total, data.current_total)
            delta = formatter.get_evolution_percent(data.first_total, data.current_total)
            label = formatter.get_evolution_description("All-time evolution", data.first_month)
            st.metric(label, value, delta)
        with col3: 
            value = formatter.get_evolution_float(data.last_total, data.current_total)
            delta = formatter.get_evolution_percent(data.last_total, data.current_total)
            label = formatter.get_evolution_description("Monthly evolution", data.last_month)
            st.metric(label, value, delta)

def main():
    input_data, edit = inputs()
    if input_data:
        data = pd.read_csv(input_data)
        data_handler = DataHandler(data)
        data_formatter = DataFormatter()
        
        

        # Stacked area chart with every product
        st.header("Global assets evolution")
        products_df = data_handler.get_overall_df()
        chart = alt.Chart(products_df).mark_area().encode(
            x="date:T", 
            y="value:Q", 
            color="product:N", 
            tooltip=["product:N", "value:Q", "date:T"]).interactive()
        st.altair_chart(chart, use_container_width=True)
        data_info = data_handler.data_structure 
        display_evolution(data_info, data_formatter)

        # Bar chart with every product over the last month
        st.header("Resources partitioning")
        col1, col2 = st.columns(2)
        with col1:
            lines_df = data_handler.select_data_by_date(-1, products_df)
            bars = alt.Chart(lines_df).transform_joinaggregate(
                total_value='sum(value)',
            ).transform_calculate(
                percentage= "datum.value / datum.total_value"
            ).mark_bar().encode(
                x='product:N',
                y=alt.Y('percentage:Q', axis=alt.Axis(format='.0%')),
                color=alt.Color(field="product", type="nominal", legend=None)
            )

            text = bars.mark_text(
                align='center',
                baseline='middle',
                dy=-10  # Nudges text to top so it doesn't appear on the bar
            ).encode(
                text='value:Q'
            ).properties(
                title='by product/company')

            st.altair_chart(bars + text, use_container_width=True)

        # Bar chart for product type
        with col2:
            type_df = data_handler.get_type_df()

            pie = alt.Chart(type_df).encode(
                theta=alt.Theta('value:Q'),
                color=alt.Color(field="type", type="nominal")
            ).mark_arc().properties(
                title='by type')

            st.altair_chart(pie, use_container_width=True)


        # Table containing raw data 
        st.header("Raw numbers")
        st.write(data)


if __name__ == '__main__':
    main()