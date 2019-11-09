from django.shortcuts import render
from openpyxl import Workbook

import requests
import json

# Create your views here.

# Herberts Token: 23bbb528dc93cc6ca0a1a828b3a99195a77dbfad
# Bradleys Token: 848e37043e042ae16a97145c194d3d06cdb95572


def establish_wobo_connection(model='team', identifier=None):
    print('Establishing connection...')
    
    # Here we are establishing a HTTP GET connection to WorkBoard's REST API. To keep this dynamic we allow two
    # variables: model, which is the kind of data model we want to pull and identifier, which is to specify certain
    # items we might want to pull from the API.
    # The 'Authorization' header is necessary as we need to prove our identity to WorkBoard.
    req = requests.get(url='https://www.myworkboard.com/wb/apis/{}/{}'.format(model, identifier),
                       headers={'Authorization': "bearer 848e37043e042ae16a97145c194d3d06cdb95572"},
                       )
    
    return req


def build_teams(identifier=None):
    # Here we are using the 'establish_wobo_connection' method to fetch data from WorkBoard's API, specifically for all
    # teams which the API key owner is a part of.
    response = establish_wobo_connection(model='team')
    
    # If we get a valid connection (HTTP status 200) we proceed with reading the data as JSON format.
    if response.status_code == 200:
        data = json.loads(response.text)
        
        wb = Workbook()
        ws = wb.active
        
        # This part allows us to extract relevant data from the HTTP response we got from WoBo.
        teams = data['data']['team']
        
        # here we define all column names through putting them into a list. Before doing so we convert the keys into a
        # list. The asterisk extracts the values from the 'dict_values'.
        column_names = [*teams[0].keys()]
        ws.append(column_names)
        
        # We create a a row for every team returned by WoBo. Instead of using the keys we extract the values here.
        for team in teams:
            ws.append([*team.values()])
            
        # Here we save our workbook to an actual XLSX file.
        wb.save('text.xlsx')
       
    else:
        raise BrokenPipeError("You fucked up. Your request was invalid....")


if __name__ == '__main__':
    build_teams()

