import streamlit as st
import time
from functs import grafico,prepro,prepro2,districtfloors,run_query,loaded_model,searchID,prepro3,districtfloorswalls,districtfloorswalls1
from Graficas import plotter
from querys import query,query2,query3,query4,query5,query6,query7,query8,query9

import pandas as pd
dfventas = pd.read_csv('FechaVentas.csv')
dfghost = pd.read_csv('GHSTPRICE.csv')
root_path = "https://thegraph.com/hosted-service/subgraph/aavegotchi/aavegotchi-core-matic?Aavegotchi?id:1!"
result9 = run_query(query9)
result8 = run_query(query8)
result7 = run_query(query7)
result6 = run_query(query6)
result5 = run_query(query5)
result4 = run_query(query4)
result2 = run_query(query2)
result3 = run_query(query3)
result = run_query(query)
df7 = prepro2(result7)
df6 = prepro3(result6)
df5 = prepro3(result5)
df4 = prepro3(result4)
df1 = prepro2(result2)
df2 = prepro2(result3)
df3 = pd.concat([df1, df2])
df3 = pd.concat([df3,df7])
df8 = prepro(result8)
df = prepro(result)
df10 = prepro(result9)
df9 = pd.concat([df,df8])

dfparcels = pd.concat([df4,df5,df6])

st.set_page_config(page_title="Aavegotchi", page_icon="money", layout='wide', initial_sidebar_state='auto')

option = st.sidebar.selectbox('Home',['HOME','Districts Visualizer','Floor Sniper','Price Estimator','Neighboring Parcels','Bazaar Stats'])
if option == 'HOME':
    st.header('WELCOME TO THE GOTCHIVERSE')
    st.image('citadelimage.png')
if option == 'Districts Visualizer':
    st.image('districts.jpg',width = 450)
    st.title('Aavegotchi Parcels Average Bazaar Prices By District')

    district = st.select_slider('Select District', [1,2,3,4,5,14,15,16,17,18,19,20,21,22,39,40,41,42,43])

    grafico(df9,district)
    time.sleep(2)

if option == 'Floor Sniper':
    D = st.selectbox('Choose District',(1,2,3,4,5,14,15,16,17,18,19,20,21,22,39,40,41,42,43))
    Size = st.selectbox('Choose Size',('Humble','Reasonable','Vertical Spacious','Horizontal Spacious'))
    try:
        districtfloors(df3,D,Size)
        time.sleep(2)
    except:st.error('No parcels found!')
    if D == 1:
        x = st.checkbox('You are in D1!, check for the most inner walls if you wish')
        if x:
            try:
                districtfloorswalls1(df3,D,Size)
                st.image('wallz.png', width=650)
            except:
                st.error('No inner wall parcels found!')
    else:
        y = st.checkbox('Check for main Inner walls Parcels too!')
        if y:
            try:
                districtfloorswalls(df3,D,Size)
                st.image('wallz.png',width=650)
            except:
                st.error('No inner wall parcels found!')



if option == 'Price Estimator':
    st.write("Here's a little price estimator fueled by Machine Learning! Keep in mind the model is not perfect and it seems to not weight Kinship/EXP, take the estimation with a grain of salt")
    col1, mid, col2 = st.columns([1, 1, 2])
    with col1:
        st.image('gotchistats.png', width=500)
    with col2:
        st.image('features.png')
    pred = []
    BRS = int(st.number_input('Enter BRS',value=450,min_value=324,max_value=600,step=1))
    mit2x = st.selectbox('Does your gotchi have 2x myth eyes?',('YES','NO'))
    if mit2x == 'YES':
        mit2x = 1
    else:
        mit2x = 0
    KIN = int(st.number_input('Kinship Level',value=50,min_value=0,max_value=100000,step=1))
    EXP = int(st.number_input('Experience Level',value=50,min_value=0,max_value=100000,step=1))
    HAUNT = int(st.radio('Haunt',(1,2)))
    pred.append(BRS)
    pred.append(mit2x)
    pred.append(KIN)
    pred.append(EXP)
    pred.append(HAUNT)
    prediccion = loaded_model.predict([pred])
    st.markdown(f"""Estimation : {int(prediccion)}$GHST""")

if option == 'Neighboring Parcels':
    st.title('Search for neighboring parcels near yours')
    st.text('This little widget will look for listed parcels in the bazaar and pull the closest one to the one you input through your parcel#ID')
    PID = int(st.number_input('Enter your Parcel ID#',value=1,min_value=1,max_value=100000,step=1))
    try:
        searchID(dfparcels,PID)
    except:
        st.error('Invalid Parcel ID')
if option == 'Bazaar Stats':
    st.title('Some Bazaar Stats as of 12th November 2021')
    col1, mid, col2 = st.columns([1, 1, 2])
    with col1:
        plotter(dfventas,'avg',title = 'Average Gotchi Weekly Sales in $GHST')
    with col2:
        plotter(dfventas,None,title = 'Volume Gotchi Weekly Sales in $GHST')

    col3, mid2, col4 = st.columns([1, 1, 2])
    with col3:
        plotter(dfventas, 'min', title='Floor Gotchi Weekly Prices in $GHST')
    with col4:
        plotter(dfghost, 'avg', title='$GHST Monthly Average Price')


