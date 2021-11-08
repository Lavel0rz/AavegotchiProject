import streamlit as st
import time
from functs import grafico,prepro,prepro2,districtfloors,run_query

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
result2 = run_query(query2)
result3 = run_query(query3)
result = run_query(query)
df1 = prepro2(result2)
df2 = prepro2(result3)
df3 = pd.concat([df1, df2])
df = prepro(result)
st.set_page_config(page_title="Aavegotchi", page_icon="money", layout='wide', initial_sidebar_state='auto')

option = st.sidebar.selectbox('Home',['Districts Visualizer','Floor Sniper'])
if option == 'Districts Visualizer':
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

