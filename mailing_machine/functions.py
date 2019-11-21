from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from datetime import date, datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import requests
import json

# Create your views here.
# Settings
HERBERT_WOBO = '23bbb528dc93cc6ca0a1a828b3a99195a77dbfad'
BRADLEY_WOBO = '848e37043e042ae16a97145c194d3d06cdb95572'
SENDGRID_API = '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'


def establish_wobo_connection(model='team', identifier='', params=frozenset()):
    # Here we are establishing a HTTP GET connection to WorkBoard's REST API. To keep this dynamic we allow two
    # variables: model, which is the kind of data model we want to pull and identifier, which is to specify certain
    # items we might want to pull from the API.
    # The 'Authorization' header is necessary as we need to prove our identity to WorkBoard.
    url = 'https://www.myworkboard.com/wb/apis/{}/{}'.format(model, identifier)
    print('Connecting to {}. Please wait as we generate the output.'.format(url))
    req = requests.get(url=url,
                       headers={'Authorization': "bearer {}".format(BRADLEY_WOBO)},
                       params=params,
                       )
    
    data = json.loads(req.text)
    
    return {'status_code': req.status_code, 'data': data}


def get_objectives(identifier=None):
    if identifier:
        response = establish_wobo_connection(model='goal', identifier=identifier)
    else:
        response = establish_wobo_connection(model='goal')
    
    if response['status_code'] == 200:
        data = response['data']
        
        return data
    else:
        raise BrokenPipeError('There was an error processing your Objectives request.')


def get_teams(identifier=''):
    if identifier:
        response = establish_wobo_connection(model='team', identifier=identifier)
    else:
        response = establish_wobo_connection(model='team')
    
    if response['status_code'] == 200:
        data = response['data']
        
        return data
    else:
        raise BrokenPipeError('There was an error processing your Teams request.')


def get_key_results(identifier=''):
    if identifier:
        response = establish_wobo_connection(model='metric', identifier=identifier)
    else:
        response = establish_wobo_connection(model='metric')
    
    if response['status_code'] == 200:
        data = response['data']
        
        return data
    else:
        raise BrokenPipeError('There was an error processing your Metrics request.')


def build_data_sheet(team=None):
    '''
    This function unites all partial functions above so that we can fetch all relevant data from WorkBoard's API and
    process it here.
    :param team: The identifier may be used to specify a certain team and their respective stats.
    :return:
    '''
    
    teams = get_teams(identifier=team)['data']
    owners = get_objectives()['data']
    print('Connection successful. All data has been fetched. We are now preparing your export.')
    
    wb = Workbook()
    
    # Create an overview of all teams the user is part of.
    ts = wb.active
    ts.title = 'Teams'
    
    col_names = [*teams['team'][0].keys()]
    ts.append(col_names)
    for team in teams['team']:
        ts.append([*team.values()])
    
    # Create an overview of all objectives the user contributes to.
    os = wb.create_sheet('Objectives')
    col_names = ['Owner ID', 'Owner', 'Objective ID', 'Objective', 'Date created', 'Date modified', 'Start date',
                 'End date', 'Progress', 'Follow up necessary']
    os.append(col_names)
    
    # Create an overview of all key results the user contributes to.
    ks = wb.create_sheet('Key Results')
    col_names = ['Owner ID', 'Owner', 'Objective ID', 'Objective', 'Metric name', 'Progress', 'Date created',
                 'Date modified',
                 'Last update', 'Next update', 'Follow up necessary']
    ks.append(col_names)
    
    for owner in owners['goal']:
        for goal in owner['people_goals']:
            li = [owner['user_id'], owner['user_email']]
            li += [goal['goal_id'], goal['goal_name'],
                   datetime.fromtimestamp(int(goal['goal_create_at'])),
                   datetime.fromtimestamp(int(goal['goal_modified_at'])),
                   datetime.fromtimestamp(int(goal['goal_start_date'])),
                   datetime.fromtimestamp(int(goal['goal_target_date'])),
                   float(goal['goal_progress']), ]
            
            # Determine update-overdue status
            if datetime.now() - timedelta(weeks=2) > datetime.fromtimestamp(int(goal['goal_modified_at'])) and \
                    float(goal['goal_progress']) < 100:
                li += [1]
            else:
                li += [0]
            
            os.append(li)
            
            # Evaluate all key results associated with the objective.
            for metric in goal['goal_metrics']:
                kl = [owner['user_id'], owner['user_email'], goal['goal_id'], goal['goal_name'], metric['metric_name'],
                      float(metric['metric_progress']),
                      datetime.fromtimestamp(int(metric['metric_create_at'])),
                      datetime.fromtimestamp(int(metric['metric_modified_at'])),
                      datetime.fromtimestamp(int(metric['metric_last_update'])),
                      datetime.fromtimestamp(int(metric['metric_next_update']))]
                
                if datetime.now() > datetime.fromtimestamp(int(metric['metric_next_update'])) and float(
                        metric['metric_progress']) < 100:
                    kl += [1]
                else:
                    kl += [0]
                
                ks.append(kl)
    
    # Save the Excel workbook.
    wb.save('wobo_export.xlsx')
    print('Workbook saved! Have fun.')


if __name__ == '__main__':
    build_data_sheet()

