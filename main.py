import streamlit as st
import time
from functs import grafico,prepro,prepro2,districtfloors,run_query,loaded_model,searchID,prepro3

import pandas as pd

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

option = st.sidebar.selectbox('Home',['HOME','Districts Visualizer','Floor Sniper','Price Estimator','Neighboring Parcels'])
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
    st.image('gotchistats.png',width=600)
    pred = []
    BRS = int(st.number_input('Enter BRS'))
    mit2x = st.selectbox('Does your gotchi have 2x myth eyes?',('YES','NO'))
    if mit2x == 'YES':
        mit2x = 1
    else:
        mit2x = 0
    KIN = int(st.number_input('Kinship Level'))
    EXP = int(st.number_input('Experience Level'))
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
    PID = int(st.number_input('Enter your Parcel ID#'))
    try:
        searchID(dfparcels,PID)
    except:
        st.error('Invalid Parcel ID')
