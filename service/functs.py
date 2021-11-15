import math
import pickle

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# load model
loaded_model = pickle.load(open('final.pkl', 'rb'))
allparcels = pd.read_csv('src/dfs/ALLparcels.csv')

allparcels['ParcelID'] = allparcels['ParcelID'].astype(int)
allparcels['CoorX'] = allparcels['CoorX'].astype(int)
allparcels['CoorY'] = allparcels['CoorY'].astype(int)


def grafico(df, district):
    df['distrito'] = df['distrito'].astype(int)
    df['tamaño'] = df['tamaño'].astype(int)
    df['tamaño'] = df['tamaño'].apply(sizer)
    df2 = df[df['distrito'] == district]
    total = len(df2)
    primer = df2.groupby('tamaño')['precio'].mean()
    fig = px.bar(primer, x=primer.index, title=f'Average Prices of Sold Parcels in district {district}', y='precio',
                 width=600, height=400,
                 labels={  # replaces default labels by column name
                     "precio": "Mean Price", 'tamaño': 'Parcel Size'
                 })
    return st.plotly_chart(fig), st.text(f'Total number of parcels sold in this district: {total}')


def prepro(data):
    newdic = data.get('data', 0)
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
    df = pd.DataFrame({'precio': new,
                       'distrito': new2,
                       'tamaño': new3,
                       'parcelaid': new4})
    df['precio'] = df['precio'].astype(float)
    df['precio'] = df['precio'].apply(lambda x: x / 1000000000000000000)
    return df


def prepro2(data):
    newdic = data.get('data', 0)
    newdic2 = newdic.get('erc721Listings')
    nuevos = []
    new = []
    new2 = []
    new3 = []
    new4 = []
    new5 = []
    new6 = []
    for i in newdic2:
        nuevos.append(i)
    for i in nuevos:
        new.append(i.get('priceInWei'))
        new2.append(i.get('district'))
        new3.append(i.get('size'))
        new4.append(i.get('id'))
        new5.append(i.get('coordinateX'))
        new6.append(i.get('coordinateY'))
    df = pd.DataFrame({'precio': new,
                       'distrito': new2,
                       'tamaño': new3,
                       'BazaarID': new4, 'CoorX': new5,
                       'CoorY': new6})
    df['CoorX'] = df['CoorX'].astype(int)
    df['CoorY'] = df['CoorY'].astype(int)
    df['precio'] = df['precio'].astype(float)
    df['precio'] = df['precio'].apply(lambda x: x / 1000000000000000000)
    return df
def preprowear(data):
    newdic = data.get('data',0)
    newdic2 = newdic.get('erc1155Listings')
    nuevos = []
    new = []
    new2 = []
    new3 = []
    new4 = []
    for i in newdic2:
        nuevos.append(i)
    for i in nuevos:
        new.append(i.get('priceInWei'))
        new2.append(i.get('erc1155TypeId'))
        new3.append(i.get('rarityLevel'))
        new4.append(i.get('id'))
    df = pd.DataFrame({'Price':new,
                 'ID':new2,
                 'Rarity':new3,
                 'BazaarID':new4})
    df['Price']=df['Price'].astype(float)
    df['Price'] = df['Price'].apply(lambda x: x/1000000000000000000)
    df['BazaarID']=df['BazaarID'].astype(int)

    df['BazaarID'] = df['BazaarID'].apply(lambda x: 'https://aavegotchi.com/baazaar/erc1155/' + str(x))

    return df

def prepro3(data):
    newdic = data.get('data', 0)
    newdic2 = newdic.get('erc721Listings')
    nuevos = []
    new = []
    new2 = []
    new3 = []
    new4 = []
    new5 = []
    new6 = []
    new7 = []
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
    df = pd.DataFrame({'precio': new,
                       'distrito': new2,
                       'tamaño': new3,
                       'BazaarID': new4,
                       'CoorX': new5,
                       'CoorY': new6,
                       'ParcelID': new7})
    df['precio'] = df['precio'].astype(float)
    df['precio'] = df['precio'].apply(lambda x: x / 1000000000000000000)
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


def districtfloors(df2, D, Size):
    if Size == 'Humble':
        Size = 0
    elif Size == 'Reasonable':
        Size = 1
    elif Size == 'Vertical Spacious':
        Size = 2
    else:
        Size = 3

    df2['distrito'] = df2['distrito'].astype(int)
    df2['tamaño'] = df2['tamaño'].astype(int)
    df3 = df2[df2['distrito'] == D]
    df4 = df3[df3['tamaño'] == Size]
    grouped = df4.groupby(['precio'])['BazaarID'].min()
    x = (grouped.values[0])
    y = grouped.index[0]
    url = "https://aavegotchi.com/baazaar/erc721/" + str(x)
    return st.write(f"Current Floor:     {y}$GHST  [" + url + "](" + url + ")")


def districtfloorswalls(df2, D, Size):
    if Size == 'Humble':
        Size = 0
    elif Size == 'Reasonable':
        Size = 1
    elif Size == 'Vertical Spacious':
        Size = 2
    else:
        Size = 3
    df2['CoorX'] = df2['CoorX'].astype(int)
    df2['CoorY'] = df2['CoorY'].astype(int)
    df2['distrito'] = df2['distrito'].astype(int)
    df2['tamaño'] = df2['tamaño'].astype(int)
    df3 = df2[df2['distrito'] == D]
    df4 = df3[df3['tamaño'] == Size]
    df4 = df4[(df4['CoorX'] >= 2448)]
    df4 = df4[(df4['CoorY'] >= 1544)]
    df4 = df4[(df4['CoorY'] <= 4736)]
    grouped = df4.groupby(['precio'])['BazaarID'].min()
    x = (grouped.values[0])
    y = grouped.index[0]
    url = "https://aavegotchi.com/baazaar/erc721/" + str(x)
    return st.write(f"Current Floor:     {y}$GHST  [" + url + "](" + url + ")")


def districtfloorswalls1(df2, D, size):
    if size == 'Humble':
        size = 0
    elif size == 'Reasonable':
        size = 1
    elif size == 'Vertical Spacious':
        size = 2
    else:
        size = 3
    df2['CoorX'] = df2['CoorX'].astype(int)
    df2['CoorY'] = df2['CoorY'].astype(int)
    df2['distrito'] = df2['distrito'].astype(int)
    df2['tamaño'] = df2['tamaño'].astype(int)
    df3 = df2[df2['distrito'] == D]
    df4 = df3[df3['tamaño'] == size]

    df4 = df4[(df4['CoorX'] >= 3880)]
    df4 = df4[(df4['CoorY'] >= 2408)]
    df4 = df4[(df4['CoorY'] <= 3880)]
    grouped = df4.groupby(['precio'])['BazaarID'].min()
    x1 = (grouped.values[0])
    y1 = grouped.index[0]
    url1 = "https://aavegotchi.com/baazaar/erc721/" + str(x1)
    return st.write(f"Current Floor:     {y1}$GHST  [" + url1 + "](" + url1 + ")")


def execute_query(data):
    request = requests.post('https://api.thegraph.com/subgraphs/name/aavegotchi/aavegotchi-core-matic'
                            '',
                            json={'query': data})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, data))


# mapeo
def sizer(num):
    if num == 0:
        return 'Humble'
    elif num == 1:
        return 'Reasonable'
    else:
        return 'Spacious'


def calc_distances(a, b):
    p1 = a
    p2 = b
    distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
    return distance


def search_id(df, parcel_id):
    df_bus = allparcels[allparcels['ParcelID'] == parcel_id]

    x = df_bus['CoorX'].values[0]
    y = df_bus['CoorY'].values[0]
    coordinates = [x, y]

    distances = df['Geo'].map(lambda x: calc_distances(coordinates, x))
    df['distances'] = distances
    grouped = df.groupby(['distances'])['BazaarID'].min()

    closer_values = grouped.values[0]

    url = "https://aavegotchi.com/baazaar/erc721/" + str(closer_values)
    return st.write(f"Current Closest Parcel For Sale: [" + url + "](" + url + ")")

def floorwearables(rarity,name):


    if name == 'Common':
        rarity = rarity[rarity['Rarity'] == 0]
        rarity = rarity.sort_values(by='Price')
        rarity['Names'] = rarity['Names'].drop_duplicates(keep='first')
        floors = rarity.dropna()
        floors = floors.reset_index()
        floors.drop('ID', axis=1, inplace=True)
        floors.drop('index', axis=1, inplace=True)
        floors.drop('Rarity', axis=1, inplace=True)
        return st.dataframe(floors)
    elif name == 'Uncommon':
        rarity = rarity[rarity['Rarity'] == 1]
        rarity = rarity.sort_values(by='Price')
        rarity['Names'] = rarity['Names'].drop_duplicates(keep='first')
        floors = rarity.dropna()
        floors = floors.reset_index()
        floors.drop('ID', axis=1, inplace=True)
        floors.drop('index', axis=1, inplace=True)
        floors.drop('Rarity', axis=1, inplace=True)
        return st.dataframe(floors)
    elif name == 'Rare':
        rarity = rarity[rarity['Rarity'] == 2]
        rarity = rarity.sort_values(by='Price')
        rarity['Names'] = rarity['Names'].drop_duplicates(keep='first')
        floors = rarity.dropna()
        floors = floors.reset_index()
        floors.drop('ID', axis=1, inplace=True)
        floors.drop('index', axis=1, inplace=True)
        floors.drop('Rarity', axis=1, inplace=True)
        return st.dataframe(floors)
    elif name == 'Legendary':
        rarity = rarity[rarity['Rarity'] == 3]
        rarity = rarity.sort_values(by='Price')
        rarity['Names'] = rarity['Names'].drop_duplicates(keep='first')
        floors = rarity.dropna()
        floors = floors.reset_index()
        floors.drop('ID', axis=1, inplace=True)
        floors.drop('index', axis=1, inplace=True)
        floors.drop('Rarity', axis=1, inplace=True)
        return st.dataframe(floors)
    elif name == 'Mythical':
        rarity = rarity[rarity['Rarity'] == 4]
        rarity = rarity.sort_values(by='Price')
        rarity['Names'] = rarity['Names'].drop_duplicates(keep='first')
        floors = rarity.dropna()
        floors = floors.reset_index()
        floors.drop('ID', axis=1, inplace=True)
        floors.drop('index', axis=1, inplace=True)
        floors.drop('Rarity', axis=1, inplace=True)
        return st.dataframe(floors)
    elif name == 'Godlike':
        rarity = rarity[rarity['Rarity'] == 5]
        rarity = rarity.sort_values(by='Price')
        rarity['Names'] = rarity['Names'].drop_duplicates(keep='first')
        floors = rarity.dropna()
        floors = floors.reset_index()
        floors.drop('ID', axis=1, inplace=True)
        floors.drop('index', axis=1, inplace=True)
        floors.drop('Rarity', axis=1, inplace=True)
        return st.dataframe(floors)






