def domicile_validator(client):
    return client['account_form']['country_of_domicile'] == client['client_profile']['country_of_domicile']

def address_validator(client):
    return client['account_form']['address'] == client['client_profile']['address']