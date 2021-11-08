import streamlit as st
import time
from functs import grafico,prepro
import requests


root_path = "https://thegraph.com/hosted-service/subgraph/aavegotchi/aavegotchi-core-matic?Aavegotchi?id:1!"


def run_query(q):
    request = requests.post('https://api.thegraph.com/subgraphs/name/aavegotchi/aavegotchi-core-matic'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


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
result = run_query(query)
df = prepro(result)
st.set_page_config(page_title="Aavegotchi", page_icon="money", layout='wide', initial_sidebar_state='auto')

option = st.sidebar.selectbox('Home',['Districts Visualizer'])
if option == 'Districts Visualizer':
    st.title('Aavegotchi Parcels Average Bazaar Prices By District')

district = st.select_slider('Select District', [1,2,3,4,5,14,15,16,17,18,19,20,21,22,39,40,41,42,43])

grafico(df,district)
time.sleep(2)