import streamlit as st
import time
from functs import grafico,prepro,prepro2,districtfloors,run_query,loaded_model,searchID,prepro3
from Graficas import plotter

import pandas as pd
dfventas = pd.read_csv('FechaVentas.csv')
root_path = "https://thegraph.com/hosted-service/subgraph/aavegotchi/aavegotchi-core-matic?Aavegotchi?id:1!"


query = '''
{
  erc721Listings (orderBy:district,first:1000,where:{category:4,timePurchased_gt:0,cancelled:false}) {
 		category
    priceInWei
    size
    timePurchased
    district
    parcel {
 			  id
 			}
  }
}



'''
query2= '''
{
  erc721Listings (orderBy:tokenId,first:1000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    parcel {
               id 
             }
  }
}



'''
query3 = '''
{
  erc721Listings (orderBy:tokenId,first:1000,skip:1000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    parcel {
               id 
             }
  }
}

'''
query4 = '''
{
  erc721Listings (orderBy:tokenId,first:1000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    coordinateX
    coordinateY
    parcel {
               id 
             }
  }
}

'''
query5 = '''
{
  erc721Listings (orderBy:tokenId,first:1000,skip:1000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    coordinateX
    coordinateY
    parcel {
               id 
             }
  }
}

'''
query6 = '''
{
  erc721Listings (orderBy:tokenId,first:1000,skip:2000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    coordinateX
    coordinateY
    parcel {
               id 
             }
  }
}

'''

result6 = run_query(query6)
result5 = run_query(query5)
result4 = run_query(query4)
result2 = run_query(query2)
result3 = run_query(query3)
result = run_query(query)

df6 = prepro3(result6)
df5 = prepro3(result5)
df4 = prepro3(result4)
df1 = prepro2(result2)
df2 = prepro2(result3)
df3 = pd.concat([df1, df2])
df = prepro(result)
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

    grafico(df,district)
    time.sleep(2)

if option == 'Floor Sniper':
    D = st.selectbox('Choose District',(1,2,3,4,5,14,15,16,17,18,19,20,21,22,39,40,41,42,43))
    Size = st.selectbox('Choose Size',('Humble','Reasonable','Vertical Spacious','Horizontal Spacious'))
    print(df3)
    districtfloors(df3,D,Size)
    time.sleep(2)

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
    col1, mid, col2 = st.columns([1, 1, 2])
    with col1:
        plotter(dfventas,'avg',title = 'Average Gotchi Weekly Sales in $GHST')
    with col2:
        plotter(dfventas,None,title = 'Volume Gotchi Weekly Sales in $GHST')

    plotter(dfventas, 'min', title='Floor Gotchi Weekly Prices in $GHST')

