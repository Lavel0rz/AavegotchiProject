import plotly.express as px
import streamlit as st


def plotter(df, param, title):
    df = df
    fig = px.histogram(df, x="Date", y=df['Price'], histfunc=param, title=title,color_discrete_sequence=["purple"])
    fig.update_layout(bargap=0.2)
    return st.plotly_chart(fig)
