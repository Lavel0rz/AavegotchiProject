
import pandas as pd
import plotly.express as px
import streamlit as st


def grafico(df,district):
    df['distrito']=df['distrito'].astype(int)
    df2 = df[df['distrito']==district]
    total = 'Total sales',len(df2)
    primer = df2.groupby('tamaño')['precio'].mean()
    fig = px.bar(primer, x=primer.index, title='Average Prices of Sold Parcels', y='precio', width=600, height=400,
                 labels={  # replaces default labels by column name
                     "precio": "Mean Price", 'tamaño': 'Parcel Size'
                 })
    return st.plotly_chart(fig),st.text(total)

def prepro(data):
    newdic = data.get('data',0)
    newdic2 = newdic.get('erc721Listings')
    nuevos = []
    new = []
    new2 = []
    new3 = []
    new4 = []
    for i in newdic2:
        nuevos.append(i)
    for i in nuevos:
        new.append(i.get('priceInWei'))
        new2.append(i.get('district'))
        new3.append(i.get('size'))
        new4.append(i.get('parcel'))
    df = pd.DataFrame({'precio':new,
                 'distrito':new2,
                 'tamaño':new3,
                 'parcelaid':new4})
    df['precio']=df['precio'].astype(float)
    df['precio'] = df['precio'].apply(lambda x: x/1000000000000000000)
    return df