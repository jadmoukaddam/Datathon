import pandas as pd
#import encoding from pytorch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder

country_code_encoder = LabelEncoder()

def data_to_df(full_data:list):
    dfs = []
    for client in full_data:
        keep = [
            ['gender', 'country_code', 'nationality', 'birth_date'],
            ['country_of_domicile', 'marital_status',
             'higher_education', 'employment_history', 'aum', 'inheritance_details',
             'real_estate_details', 'investment_risk_profile', 'investment_horizon', 'investment_experience',
             'type_of_mandate', 'preferred_markets', 'currency'],
            [],
            [],
            ['label']
                ]
        keys=client.keys()
        res={}
        for key, subkeys in zip(keys, keep):
            d = {subkey: client[key][subkey] for subkey in subkeys }
            res = res|d
        dfs.append(res)
    return pd.DataFrame.from_records(dfs)


X = data_to_df(full_data)


def encode_country_code(df: pd.DataFrame) -> pd.DataFrame:
    country_code_encoder.fit(df['country_code'])
    df['country_code'] = country_code_encoder.transform(df['country_code'])
    return df

X = encode_country_code(X)
print(X["country_code"])