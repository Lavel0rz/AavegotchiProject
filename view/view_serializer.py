import time

import pandas as pd

from graphics import plotter
from service.aavegotchi_repository import AavegotchiRepository
from service.functs import grafico, districtfloors, districtfloorswalls1, districtfloorswalls, loaded_model, search_id, floorwearables

SALES_DF = pd.read_csv('src/dfs/FechaVentas.csv')
GHOST_DF = pd.read_csv('src/dfs/GHSTPRICE.csv')

#clases
class ViewSerializer(object):

    def __init__(self, stream_lit):
        self.stream_lit = stream_lit

    def render_home(self):
        self.stream_lit.header('WELCOME TO THE GOTCHIVERSE')
        self.stream_lit.image('src/imgs/citadelimage.png')

    def render_district_visualizer(self):
        self.stream_lit.image('src/imgs/districts.jpg', width=450)
        self.stream_lit.title('Aavegotchi Parcels Average Bazaar Prices By District')

        district = self.stream_lit.select_slider('Select District',
                                                 [1, 2, 3, 4, 5, 14, 15, 16, 17, 18, 19, 20, 21, 22, 39, 40, 41, 42,
                                                  43])

        grafico(AavegotchiRepository.get_district_visualizer_data_frame(), district)
        time.sleep(0.5)

    def render_floor_sniper(self):
        df = AavegotchiRepository.get_floor_sniper_df()
        available_districts = self.stream_lit.selectbox('Choose District',
                                                        (1, 2, 3, 4, 5, 14, 15, 16, 17, 18, 19, 20, 21, 22, 39, 40, 41,
                                                         42, 43))
        size = self.stream_lit.selectbox('Choose Size',
                                         ('Humble', 'Reasonable', 'Vertical Spacious', 'Horizontal Spacious'))
        try:
            districtfloors(df, available_districts, size)
            time.sleep(0.5)
        except:
            self.stream_lit.error('No parcels found!')
        if available_districts == 1:
            x = self.stream_lit.checkbox('You are in D1!, check for the most inner walls if you wish')
            if x:
                try:
                    districtfloorswalls1(df, available_districts, size)
                    self.stream_lit.image('src/imgs/wallz.png', width=650)
                except:
                    self.stream_lit.error('No inner wall parcels found!')
        else:
            y = self.stream_lit.checkbox('Check for main Inner walls Parcels too!')
            if y:
                try:
                    districtfloorswalls(df, available_districts, size)
                    self.stream_lit.image('src/imgs/wallz.png', width=650)
                except:
                    self.stream_lit.error('No inner wall parcels found!')

    def render_price_estimator(self):
        self.stream_lit.write(
            "Here's a little price estimator fueled by Machine Learning! Keep in mind the model is not perfect and it "
            "seems to not weight Kinship/EXP, take the estimation with a grain of salt")
        col1, mid, col2 = self.stream_lit.columns([1, 1, 2])
        with col1:
            self.stream_lit.image('src/imgs/gotchistats.png', width=500)
        with col2:
            self.stream_lit.image('src/imgs/features.png')
        prediction = loaded_model.predict([self.populate_prediction_values()])
        self.stream_lit.markdown(f"""Estimation : {int(prediction)}$GHST""")

    def populate_prediction_values(self):
        prediction_values = []
        BRS = int(self.stream_lit.number_input('Enter BRS', value=450, min_value=324, max_value=600, step=1))
        mit2x = self.stream_lit.selectbox('Does your gotchi have 2x myth eyes?', ('YES', 'NO'))
        if mit2x == 'YES':
            mit2x = 1
        else:
            mit2x = 0
        KIN = int(self.stream_lit.number_input('Kinship Level', value=50, min_value=0, max_value=100000, step=1))
        EXP = int(self.stream_lit.number_input('Experience Level', value=50, min_value=0, max_value=100000, step=1))
        HAUNT = int(self.stream_lit.radio('Haunt', (1, 2)))
        prediction_values.append(BRS)
        prediction_values.append(mit2x)
        prediction_values.append(KIN)
        prediction_values.append(EXP)
        prediction_values.append(HAUNT)
        return prediction_values

    def render_neighbour_parcels(self):
        df_parcels = AavegotchiRepository.get_neighbouring_parcels_df()
        self.stream_lit.title('Search for neighboring parcels near yours')
        self.stream_lit.text(
            'This little widget will look for listed parcels in the bazaar and pull the closest one to the one you '
            'input through your parcel#ID')
        PID = int(self.stream_lit.number_input('Enter your Parcel ID#', value=1, min_value=1, max_value=100000, step=1))
        try:
            search_id(df_parcels, PID)
        except:
            self.stream_lit.error('Invalid Parcel ID')

    def render_bazaar_stats(self):
        self.stream_lit.title('Some Bazaar Stats as of 12th November 2021')
        col1, mid, col2 = self.stream_lit.columns([1, 1, 2])

        with col1:
            plotter(SALES_DF, 'avg', title='Average Gotchi Weekly Sales in $GHST')
        with col2:
            plotter(SALES_DF, None, title='Volume Gotchi Weekly Sales in $GHST')

        col3, mid2, col4 = self.stream_lit.columns([1, 1, 2])
        with col3:
            plotter(SALES_DF, 'min', title='Floor Gotchi Weekly Prices in $GHST')
        with col4:
            plotter(GHOST_DF, 'avg', title='$GHST Monthly Average Price')

    def render_floor_sniper_wearables(self):
        self.stream_lit.title('Floor Prices for Wearables')
        name = self.stream_lit.sidebar.selectbox('Wearable Floors',
                                            ['Common', 'Uncommon', 'Rare', 'Legendary',
                                             'Mythical',
                                             'Godlike'])
        df = AavegotchiRepository.get_wearables_floor_df()
        return floorwearables(df, name)

