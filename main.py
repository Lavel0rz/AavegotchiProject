import pandas as pd
import streamlit as stream_lit

from querys import query, query2, query3, query4, query5, query6, query7, query8, query9
from service.functs import prepro, prepro2, execute_query, prepro3
from view.view_serializer import ViewSerializer

ROOT_PATH = "https://thegraph.com/hosted-service/subgraph/aavegotchi/aavegotchi-core-matic?Aavegotchi?id:1!"

result9 = execute_query(query9)
result8 = execute_query(query8)
result7 = execute_query(query7)
result6 = execute_query(query6)
result5 = execute_query(query5)
result4 = execute_query(query4)
result2 = execute_query(query2)
result3 = execute_query(query3)
result = execute_query(query)
df7 = prepro2(result7)
df6 = prepro3(result6)
df5 = prepro3(result5)
df4 = prepro3(result4)
df1 = prepro2(result2)
df2 = prepro2(result3)
floor_sniping_data = pd.concat([df1, df2])
floor_sniping_data = pd.concat([floor_sniping_data, df7])
df8 = prepro(result8)
df = prepro(result)
df10 = prepro(result9)
districts_visualizer_data = pd.concat([df, df8])

df_parcels = pd.concat([df4, df5, df6])

stream_lit.set_page_config(page_title="Aavegotchi", page_icon="money", layout='wide', initial_sidebar_state='auto')

option = stream_lit.sidebar.selectbox('Home',
                                      ['HOME', 'Districts Visualizer', 'Floor Sniper', 'Price Estimator',
                                       'Neighbour Parcels',
                                       'Bazaar Stats'])

view_serializer = ViewSerializer(stream_lit)

if option == 'HOME':
    view_serializer.render_home()

if option == 'Districts Visualizer':
    view_serializer.render_district_visualizer(districts_visualizer_data)

if option == 'Floor Sniper':
    view_serializer.render_floor_sniper(floor_sniping_data)

if option == 'Price Estimator':
    view_serializer.render_price_estimator()

if option == 'Neighbour Parcels':
    view_serializer.render_neighbour_parcels(df_parcels)

if option == 'Bazaar Stats':
    view_serializer.render_bazaar_stats()
