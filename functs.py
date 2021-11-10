import requests
import pandas as pd
import plotly.express as px
import streamlit as st
import pickle
import math
#load model
loaded_model = pickle.load(open('final.pkl', 'rb'))
allparcels = pd.read_csv('ALLparcels.csv')
Bazaarparcels = pd.read_csv('BazaarParcels3.csv')
allparcels['ParcelID'] = allparcels['ParcelID'].astype(int)
allparcels['CoorX'] = allparcels['CoorX'].astype(int)
allparcels['CoorY'] = allparcels['CoorY'].astype(int)
Bazaarparcels['CoorX'] = Bazaarparcels['CoorX'].astype(int)
Bazaarparcels['CoorY'] = Bazaarparcels['CoorY'].astype(int)
x = Bazaarparcels['CoorX'].values
y = Bazaarparcels['CoorY'].values
geocords = []
z = 0
for i in x:
    geocords.append([i,y[z]])
    z = z +1
Bazaarparcels['Geo']=geocords

def grafico(df,district):
    df['distrito']=df['distrito'].astype(int)
    df['tamaño']=df['tamaño'].astype(int)
    df['tamaño']=df['tamaño'].apply(sizer)
    df2 = df[df['distrito']==district]
    total = len(df2)
    primer = df2.groupby('tamaño')['precio'].mean()
    fig = px.bar(primer, x=primer.index, title=f'Average Prices of Sold Parcels in district {district}', y='precio', width=600, height=400,
                 labels={  # replaces default labels by column name
                     "precio": "Mean Price", 'tamaño': 'Parcel Size'
                 })
    return st.plotly_chart(fig),st.text(f'Total number of parcels sold in this district: {total}')


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

def prepro2(data):
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
        new4.append(i.get('id'))
    df = pd.DataFrame({'precio':new,
                 'distrito':new2,
                 'tamaño':new3,
                 'BazaarID':new4})
    df['precio']=df['precio'].astype(float)
    df['precio'] = df['precio'].apply(lambda x: x/1000000000000000000)
    return df
def prepro3(data):
    newdic = data.get('data',0)
    newdic2 = newdic.get('erc721Listings')
    nuevos = []
    new = []
    new2 = []
    new3 = []
    new4 = []
    new5 = []
    new6 = []
    new7= []
    for i in newdic2:
        nuevos.append(i)
    for i in nuevos:
        new.append(i.get('priceInWei'))
        new2.append(i.get('district'))
        new3.append(i.get('size'))
        new4.append(i.get('id'))
        new5.append(i.get('coordinateX'))
        new6.append(i.get('coordinateY'))
        new7.append(i.get('parcel'))
    df = pd.DataFrame({'precio':new,
                 'distrito':new2,
                 'tamaño':new3,
                 'BazaarID':new4,
                 'CoorX':new5,
                 'CoorY':new6,
                 'ParcelID':new7})
    df['precio']=df['precio'].astype(float)
    df['precio'] = df['precio'].apply(lambda x: x/1000000000000000000)
    df['CoorX'] = df['CoorX'].astype(int)
    df['CoorY'] = df['CoorY'].astype(int)
    x = df['CoorX'].values
    y = df['CoorY'].values
    geocords = []
    z = 0
    for i in x:
        geocords.append([i, y[z]])
        z = z + 1
    df['Geo'] = geocords
    return df

def districtfloors(df2,D,Size):
    if Size == 'Humble':
        Size = 0
    elif Size == 'Reasonable':
        Size = 1
    elif Size == 'Vertical Spacious':
        Size = 2
    else:
        Size = 3

    df2['distrito']=df2['distrito'].astype(int)
    df2['tamaño'] = df2['tamaño'].astype(int)
    df3 = df2[df2['distrito']==D]
    df4 = df3[df3['tamaño']==Size]
    grouped = df4.groupby(['precio'])['BazaarID'].min()
    x = (grouped.values[0])
    y = grouped.index[0]
    url = "https://aavegotchi.com/baazaar/erc721/" + str(x)
    return st.write(f"Current Floor:     {y}$GHST  [" + url + "](" + url + ")")

def run_query(data):
    request = requests.post('https://api.thegraph.com/subgraphs/name/aavegotchi/aavegotchi-core-matic'
                            '',
                            json={'query': data})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, data))
#mapeo
def sizer(num):
    if num == 0:
        return 'Humble'
    elif num == 1:
        return 'Reasonable'
    else:
        return 'Spacious'
def calc_distances(a,b):
    p1 = a
    p2 = b
    print(p2,p1)
    distance = math. sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
    return distance
def searchID(df,ID):


    dfbus = allparcels[allparcels['ParcelID']==ID]

    x = dfbus['CoorX'].values[0]
    y = dfbus['CoorY'].values[0]
    coordejem = [x,y]




    print(df['Geo'].values[0][0])
    distancias = df['Geo'].map(lambda x: calc_distances(coordejem, x))
    df['distances']=distancias
    grouped = df.groupby(['distances'])['BazaarID'].min()
    z=grouped.values[0]

    url = "https://aavegotchi.com/baazaar/erc721/" + str(z)
    return st.write(f"Current Closest Parcel For Sale: [" + url + "](" + url + ")")