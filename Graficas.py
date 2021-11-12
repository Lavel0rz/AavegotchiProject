import streamlit as st
import plotly.express as px



def plotter(df,param,title):
    df = df
    fig = px.histogram(df, x="Date",y=df['Price'],histfunc=param,title=title)
    fig.update_layout(bargap=0.2)
    fig1 =st.plotly_chart(fig)
    return fig1