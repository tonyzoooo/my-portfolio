from turtle import color
import pandas as pd
import streamlit as st
from data_handler import DataHandler
import altair as alt

""" 
# My Portfolio

Hello there! This is a project made to better track the evolution of my personal investments. 
I wanted to have a tool at hand to organize my spendings and I stumbled upon the streamlit 
framework. It seemed to fulfill my needs so I gave it a try!

## How does it work?

Feel free to use the data sample to try it out!

"""

def inputs():
    st.sidebar.header("Data here :)")
    upload_button = st.sidebar.file_uploader("Input", type=["csv"], accept_multiple_files=False)
    box = st.sidebar.selectbox("View", ("Overall", "By company", "By product", "By type", "Raw data"))
    edit_button = st.sidebar.button("Edit data", disabled=True)
    #download_button = st.sidebar.download_button("Save file")
    return upload_button, box, edit_button, #download_button

def main():
    input_data, mode, edit = inputs()
    if input_data:
        data = pd.read_csv(input_data)
        data_handler = DataHandler(data)
        if mode == "Raw data":
            st.header("Raw numbers")
            st.write(data)
        elif mode == "Overall":
            st.header("Global assets evolution")
            products_df = data_handler.get_overall_df()
            chart = alt.Chart(products_df).mark_area().encode(
                x="date:T", y="value:Q", color="product:N", tooltip=["product:N", "value:Q", "date:T"]).interactive()
            st.altair_chart(chart, use_container_width=True)
            value = str(data_handler.current_total) + " € (from " + str(data_handler.first_total) + " €)"
            delta = data_handler.delta_total
            st.metric(label="All-time evolution:", value=value, delta=delta)


if __name__ == '__main__':
    main()