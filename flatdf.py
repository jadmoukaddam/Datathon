def data_to_df(full_data:list):
    dfs = []
    for client in full_data:
        keep = [
            ['gender', 'country_code', 'nationality', 'birth_date'],
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
