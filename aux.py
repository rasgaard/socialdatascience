#Dependencies
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

def haversine_KNN_impute(df, col):
    '''
    Imputes a column of the dataframe using the haversine
    distance matric. 
    '''
    
    valid_idx = np.where(~df[col].isna())[0]
    nan_idx = np.where(df[col].isna())[0]

    X1 = df[['LATITUDE', 'LONGITUDE']].loc[~df[col].isna()].values
    y1 = df[[col]].loc[~df[col].isna()].values

    X2 = df[['LATITUDE', 'LONGITUDE']].loc[ df[col].isna()].values

    #Convert to radians
    X1 = X1 * np.pi/180 
    X2 = X2 * np.pi/180

    #Do the KNN imputation.
    nbrs = NearestNeighbors(n_neighbors=1, metric='haversine')
    nbrs.fit(X1, y1)
    distance, idxs = nbrs.kneighbors(X2)

    y2 = y1[idxs].reshape(-1,)

    imputed = np.zeros(len(df), dtype=object)
    imputed[valid_idx] = y1.reshape(-1,)
    imputed[nan_idx] = y2.reshape(-1,)
    
    dfout = df.copy()
    dfout[col] = imputed
    
    return dfout

def extract_vehicle_types(df):
    '''
    Takes the 5 VEHICLE TYPE CODE ... columns, sort and convert it to a single string.
    '''
    dfout = df.copy()
    
    vehicle_type_columns = [x for x in df.columns if x.startswith('VEHICLE TYPE CODE ')]

    vehicle_type_dict = dict(zip(pd.read_csv('vehicle_types.csv', sep=';', keep_default_na=False, na_values=[''])['from'], 
                                  pd.read_csv('vehicle_types.csv', sep=';', keep_default_na=False, na_values=[''])['to'])) 

    for col in vehicle_type_columns:
        df[col] = df[col].fillna(' ').str.lower().apply(lambda x : vehicle_type_dict[x])

    dfout['VEHICLE TYPES'] = df[vehicle_type_columns].values.tolist()
    dfout['VEHICLE TYPES'] = dfout['VEHICLE TYPES'].apply(lambda x : ', '.join(sorted([y for y in x if y != 'none'])))

    return dfout

def extract_contributing_factors(df):
    '''
    Takes the 5 CONTRIBUTING FACTOR ... columns, sort and convert it to a single string.
    '''
    dfout = df.copy()
    
    contributing_factor_columns = [x for x in df.columns if x.startswith('CONTRIBUTING FACTOR VEHICLE ')]

    contributing_factor_dict = dict(zip(pd.read_csv('contributing_factors.csv', sep=';', keep_default_na=False, na_values=[''])['from'], 
                                        pd.read_csv('contributing_factors.csv', sep=';', keep_default_na=False, na_values=[''])['to'])) 

    for col in contributing_factor_columns:
        df[col] = df[col].fillna('unspecified').str.lower().apply(lambda x : contributing_factor_dict[x])

    dfout['CONTRIBUTING FACTORS'] = df[contributing_factor_columns].values.tolist()
    dfout['CONTRIBUTING FACTORS'] = dfout['CONTRIBUTING FACTORS'].apply(lambda x : ', '.join(sorted([y for y in x if y != 'unspecified'])))

    return dfout