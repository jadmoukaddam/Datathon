def mrz_check(client):
    flags = True
    if (flags == True) and (client['passport']['last_name'].upper() not in client['passport']['passport_mrz'][0] or client['passport']['first_name'].upper() not in client['passport']['passport_mrz'][0] or client['passport']['middle_name'].upper() not in client['passport']['passport_mrz'][0] or client['passport']['country_code'].upper() not in client['passport']['passport_mrz'][0]):
        flags = False
    if (flags == True) and ((len(client['passport']['middle_name']) == 0) and not (client['passport']['passport_mrz'][0].index(client['passport']['country_code'].upper()) < client['passport']['passport_mrz'][0].index(client['passport']['last_name'].upper()))): #no middle name
        flags = False
    if (flags == True) and ((len(client['passport']['middle_name']) != 0) and not (client['passport']['passport_mrz'][0].index(client['passport']['country_code'].upper()) < client['passport']['passport_mrz'][0].index(client['passport']['last_name'].upper()) < client['passport']['passport_mrz'][0].index(client['passport']['middle_name'].upper()))):
        flags = False
    if (flags == True) and (client['passport']['passport_number']+client['passport']['country_code']+client['passport']['birth_date'].replace('-','')[2:] not in client['passport']['passport_mrz'][1]):
        flags = False
    return flags

def currency_match(client):
    flags = True
    if client['account_form']['currency'] != client['client_profile']['currency']:
        flags = False
    return flags

def no_mandate(client):
    flags = True
    if client['client_profile']['type_of_mandate'] == '':
        flags = False
    return flags