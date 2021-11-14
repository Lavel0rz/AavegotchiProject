import pandas as pd

from querys import query, query8, query3, query2, query7, query6, query5, query4
from service.functs import execute_query, prepro, prepro2, prepro3


class AavegotchiRepository(object):

    @staticmethod
    def get_district_visualizer_data_frame():
        result = execute_query(query)
        result8 = execute_query(query8)
        df8 = prepro(result8)
        df = prepro(result)
        return pd.concat([df, df8])

    @staticmethod
    def get_floor_sniper_df():
        result2 = execute_query(query2)
        result3 = execute_query(query3)
        result7 = execute_query(query7)
        df1 = prepro2(result2)
        df2 = prepro2(result3)
        df7 = prepro2(result7)
        floor_sniping_data = pd.concat([df1, df2])
        floor_sniping_data = pd.concat([floor_sniping_data, df7])
        return floor_sniping_data

    @staticmethod
    def get_neighbouring_parcels_df():
        result6 = execute_query(query6)
        result5 = execute_query(query5)
        result4 = execute_query(query4)
        df6 = prepro3(result6)
        df5 = prepro3(result5)
        df4 = prepro3(result4)
        df_parcels = pd.concat([df4, df5, df6])
        return df_parcels
