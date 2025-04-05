import pickle
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
from load_updated_data import load_clients
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timedelta

full_data = load_clients("clients.pkl")

def data_to_df(full_data:list):
    dfs = []
    for client in full_data:
        keep = [
            ['gender', 'country_code', 'birth_date'],
            ['country_of_domicile', 'nationality', 'marital_status',
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

df = data_to_df(full_data)

country_code_encoder = LabelEncoder()
country_dom_encoder = LabelEncoder()
marital_status_encoder = LabelEncoder()
investment_experience_encoder = LabelEncoder()
currency_encoder = LabelEncoder()
gender_encoder = LabelEncoder()
nationality_encoder = LabelEncoder()
irp_encoder = LabelEncoder()
ih_encoder = LabelEncoder()
mandate_encoder = LabelEncoder()
pref_markets_encoder=MultiLabelBinarizer()

def encode_gender(df:pd.DataFrame,encoder:LabelEncoder)-> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['gender'])
    df['gender'] = encoder.transform(df['gender'])
    return df, encoder

def encode_nationality(df:pd.DataFrame,encoder:LabelEncoder)-> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['nationality'])
    df['nationality'] = encoder.transform(df['nationality'])
    return df, encoder

def encode_irp(df:pd.DataFrame,encoder:LabelEncoder)-> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['investment_risk_profile'])
    df['investment_risk_profile'] = encoder.transform(df['investment_risk_profile'])
    return df, encoder

def encode_ih(df:pd.DataFrame,encoder:LabelEncoder)-> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['investment_horizon'])
    df['investment_horizon'] = encoder.transform(df['investment_horizon'])
    return df, encoder

def encode_mandate(df:pd.DataFrame,encoder:LabelEncoder)-> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['type_of_mandate'])
    df['type_of_mandate'] = encoder.transform(df['type_of_mandate'])
    return df, encoder

def encode_pref_markets(df:pd.DataFrame,encoder:MultiLabelBinarizer)-> tuple[pd.DataFrame, LabelEncoder]:
    encoded=encoder.fit_transform(df['preferred_markets'].to_list())
    temp_df = pd.DataFrame.from_records(encoded)
    temp_df.rename(columns = {i: f'pref_markets_{i}' for i in range(temp_df.shape[1])},inplace=True)
    return pd.concat([df,temp_df],axis=1), encoder

def encode_country_code(df: pd.DataFrame,encoder:LabelEncoder) -> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['country_code'])
    df['country_code'] = encoder.transform(df['country_code'])
    return df, encoder

def get_age(birth_date: str) -> int:
    try:
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        age = (datetime.now()-timedelta(5) - birth_date).days // 365
        return age
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return None

def encode_age(df: pd.DataFrame) -> pd.DataFrame:
    df['age'] = df['birth_date'].apply(get_age)
    return df

def encode_country_of_domicile(df: pd.DataFrame,encoder:LabelEncoder) -> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['country_of_domicile'])
    df['country_of_domicile'] = encoder.transform(df['country_of_domicile'])
    return df, encoder

def encode_marital_status(df: pd.DataFrame,encoder:LabelEncoder) -> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['marital_status'])
    df['marital_status'] = encoder.transform(df['marital_status'])
    return df, encoder

def encode_investment_experience(df: pd.DataFrame,encoder:LabelEncoder) -> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['investment_experience'])
    df['investment_experience'] = encoder.transform(df['investment_experience'])
    return df, encoder

def encode_currency(df: pd.DataFrame,encoder:LabelEncoder) -> tuple[pd.DataFrame, LabelEncoder]:
    encoder.fit(df['currency'])
    df['currency'] = encoder.transform(df['currency'])
    return df, encoder

def get_higher_ed(higher_ed: list) -> int:
    if higher_ed is None or len(higher_ed) == 0:
        return 0
    else:
        return 1

def encode_higher_education(df: pd.DataFrame) -> pd.DataFrame:
    df['higher_education'] = df['higher_education'].apply(get_higher_ed)
    return df

df,gender_encoder = encode_gender(df,gender_encoder)
df,nationality_encoder = encode_nationality(df,nationality_encoder)
df,irp_encoder = encode_irp(df,irp_encoder)
df, ih_encoder = encode_ih(df, ih_encoder)
df, mandate_encoder = encode_mandate(df,mandate_encoder)
df, pref_markets_encoder = encode_pref_markets(df, pref_markets_encoder)
df,country_code_encoder = encode_country_code(df,country_code_encoder)
df = encode_age(df)
df, country_dom_encoder = encode_country_of_domicile(df,country_dom_encoder)
df,marital_status_encoder = encode_marital_status(df,marital_status_encoder)
df, investment_experience_encoder = encode_investment_experience(df, investment_experience_encoder)
df,currency_encoder = encode_currency(df,currency_encoder)
df = encode_higher_education(df)