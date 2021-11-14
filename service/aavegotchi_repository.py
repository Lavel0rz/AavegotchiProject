import pandas as pd

from querys import query, query8
from service.functs import execute_query, prepro


class AavegotchiRepository(object):

    @staticmethod
    def get_district_visualizer_data_frame():
        result = execute_query(query)
        result8 = execute_query(query8)
        df8 = prepro(result8)
        df = prepro(result)
        return pd.concat([df, df8])
