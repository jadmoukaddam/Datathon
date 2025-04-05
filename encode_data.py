import pickle
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
from load_updated_data import load_clients
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

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

def encode_gender(df:pd.DataFrame,encoder:LabelEncoder)-> pd.DataFrame:
    encoder.fit(df['gender'])
    df['gender'] = encoder.transform(df['gender'])
    return df

def encode_nationality(df:pd.DataFrame,encoder:LabelEncoder)-> pd.DataFrame:
    encoder.fit(df['nationality'])
    df['nationality'] = encoder.transform(df['nationality'])
    return df

def encode_irp(df:pd.DataFrame,encoder:LabelEncoder)-> pd.DataFrame:
    encoder.fit(df['investment_risk_profile'])
    df['investment_risk_profile'] = encoder.transform(df['investment_risk_profile'])
    return df

def encode_ih(df:pd.DataFrame,encoder:LabelEncoder)-> pd.DataFrame:
    encoder.fit(df['investment_horizon'])
    df['investment_horizon'] = encoder.transform(df['investment_horizon'])
    return df

def encode_mandate(df:pd.DataFrame,encoder:LabelEncoder)-> pd.DataFrame:
    encoder.fit(df['type_of_mandate'])
    df['type_of_mandate'] = encoder.transform(df['type_of_mandate'])
    return df

def encode_pref_markets(df:pd.DataFrame,encoder:MultiLabelBinarizer)-> pd.DataFrame:
    encoded=encoder.fit_transform(df['preferred_markets'].to_list())
    temp_df = pd.DataFrame.from_records(encoded)
    temp_df.rename(columns = {i: f'pref_markets_{i}' for i in range(temp_df.shape[1])},inplace=True)
    return pd.concat([df,temp_df],axis=1)

def encode_country_code(df: pd.DataFrame,encoder:LabelEncoder) -> pd.DataFrame:
    encoder.fit(df['country_code'])
    df['country_code'] = encoder.transform(df['country_code'])
    return df

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

def encode_country_of_domicile(df: pd.DataFrame,encoder:LabelEncoder) -> pd.DataFrame:
    encoder.fit(df['country_of_domicile'])
    df['country_of_domicile'] = encoder.transform(df['country_of_domicile'])
    return df

def encode_marital_status(df: pd.DataFrame,encoder:LabelEncoder) -> pd.DataFrame:
    encoder.fit(df['marital_status'])
    df['marital_status'] = encoder.transform(df['marital_status'])
    return df

def encode_investment_experience(df: pd.DataFrame,encoder:LabelEncoder) -> pd.DataFrame:
    encoder.fit(df['investment_experience'])
    df['investment_experience'] = encoder.transform(df['investment_experience'])
    return df

def encode_currency(df: pd.DataFrame,encoder:LabelEncoder) -> pd.DataFrame:
    encoder.fit(df['currency'])
    df['currency'] = encoder.transform(df['currency'])
    return df

def get_higher_ed(higher_ed: list) -> int:
    if higher_ed is None or len(higher_ed) == 0:
        return 0
    else:
        return 1

def encode_higher_education(df: pd.DataFrame) -> pd.DataFrame:
    df['higher_education'] = df['higher_education'].apply(get_higher_ed)
    return df

def encode(x:pd.DataFrame)-> pd.DataFrame:
    x= encode_gender(x,gender_encoder)
    x = encode_nationality(x,nationality_encoder)
    x = encode_irp(x,irp_encoder)
    x = encode_ih(x, ih_encoder)
    x = encode_mandate(x,mandate_encoder)
    x = encode_pref_markets(x, pref_markets_encoder)
    x = encode_country_code(x,country_code_encoder)
    x = encode_age(x)
    x = encode_country_of_domicile(x,country_dom_encoder)
    x = encode_marital_status(x,marital_status_encoder)
    x = encode_investment_experience(x, investment_experience_encoder)
    x = encode_currency(x,currency_encoder)
    x = encode_higher_education(x)
    return x


def calculate_effective_experience(jobs: List[Tuple[int, int]]) -> int:
    """
    Calculates effective work experience in years, avoiding double-counting overlapping years.

    Args:
        jobs: List of (start_year, end_year) tuples. None as end_year means the job is current.

    Returns:
        Total number of unique working years across all jobs.
    """
    worked_years = set()
    for start, end in jobs:
        if start is None:
            continue
        end = end if end is not None else 2025
        worked_years.update(range(start, end))
    return len(worked_years)

def extract_numeric_features(full_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Extracts numeric features from a list of client dictionaries.

    Args:
        full_data: List of dictionaries, each representing a client with nested data.

    Returns:
        A pandas DataFrame containing engineered numeric features.
    """

    aum_vec = [np.sum(list(client['client_profile']['aum'].values())) for client in full_data]
    property_value_vec = [client['client_profile']['aum']['real_estate_value'] for client in full_data]
    property_count_vec = [len(client['client_profile']['real_estate_details']) for client in full_data]
    inheritance_vec = [client['client_profile']['aum']['inheritance'] for client in full_data]
    savings_vec = [client['client_profile']['aum']['savings'] for client in full_data]
    job_count_vec = [len(client['client_profile']['employment_history']) for client in full_data]

    # Compute property-to-cash ratio with zero-division handling
    property_to_cash_vec = [
        prop_value / (total_value - prop_value) if (total_value - prop_value) != 0 else -float('inf')
        for prop_value, total_value in zip(property_value_vec, aum_vec)
    ]
    max_ratio = np.max(property_to_cash_vec)
    property_to_cash_vec = [max_ratio if value == -float("inf") else value for value in property_to_cash_vec]

    # Inheritance / (inheritance + savings), safe against zero-division
    inheritance_to_cash_vec = [
        inheritance / (inheritance + saving) if (inheritance + saving) != 0 else 0
        for inheritance, saving in zip(inheritance_vec, savings_vec)
    ]

    # Salary & experience metrics
    current_salary_vec = []
    max_salary_vec = []
    total_work_experience_vec = []
    effective_work_experience_vec = []

    for client in full_data:
        emp_hist = client['client_profile']['employment_history']
        salary = 0
        max_salary = 0

        if len(emp_hist) == 0:
            total_work_experience = 0
            effective_work_experience = 0

        else:
            year_history = []
            min_start = np.inf
            max_end = -np.inf
            for job in emp_hist:
                if max_salary < job['salary']:
                    max_salary = job['salary']

                start, end = job['start_year'], job['end_year']
                year_history.append((start, end))

                if end is None:
                    salary += job['salary']
                    end = 2025

                if start < min_start:
                    min_start = start
                if end > max_end:
                    max_end = end

            total_work_experience = max_end - min_start
            effective_work_experience = calculate_effective_experience(year_history)

        total_work_experience_vec.append(total_work_experience)
        effective_work_experience_vec.append(effective_work_experience)
        current_salary_vec.append(salary)
        max_salary_vec.append(max_salary)

    # Savings per active work year
    saving_per_annum_vec = [
        saving / work_exp if work_exp != 0 else saving
        for saving, work_exp in zip(savings_vec, effective_work_experience_vec)
    ]

    # Current salary compared to max salary seen in career
    salary_to_max_salary_vec = [
        salary / max_salary if max_salary != 0 else 0
        for salary, max_salary in zip(current_salary_vec, max_salary_vec)
    ]

    # Construct final DataFrame
    df_numeric = pd.DataFrame({
        'aum': aum_vec,
        'property_value': property_value_vec,
        'num_properties': property_count_vec,
        'inheritance_value': inheritance_vec,
        'savings_value': savings_vec,
        'num_jobs': job_count_vec,
        'current_salary': current_salary_vec,
        'max_salary': max_salary_vec,
        'property_to_cash_ratio': property_to_cash_vec,
        'inheritance_to_cash_ratio': inheritance_to_cash_vec,
        'total_work_experience': total_work_experience_vec,
        'effective_work_experience': effective_work_experience_vec,
        'saving_per_annum': saving_per_annum_vec,
        'salary_to_max_salary_ratio': salary_to_max_salary_vec
    })

    return df_numeric

def data_for_ML(data:list) -> pd.DataFrame:
    x = extract_numeric_features(data)
    y = encode(data_to_df(data))
    return pd.concat([y,x],axis=1)