from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

api_key = '2bf56a8d446f40b7b6a86f5e438bb5f2'
teams = {
    'MSF': 'assets/img/MFS.png',
    'XL': 'assets/img/XLL.png',
    'FNC': 'assets/img/FNC.png',
    'AST': 'assets/img/AST.png',
    'SK': 'assets/img/SK.png',
    'G2': 'assets/img/G2.png',
    'VIT': 'assets/img/VIT.png',
    'BDS': 'assets/img/BDS.png',
    'RGE': 'assets/img/RGE.png',
    'MAD': 'assets/img/MAD.png',
    'TSM': 'nan',
    '100': 'nan',
    'GG': 'nan',
    'C9': 'nan',
    'FLY': 'nan',
    'TL': 'nan',
    'EG': 'nan',
    'IMT': 'nan',
    'CLG': 'nan',
    'DIG': 'nan'
}
leauge_keys = {
    'LEC': 100001483,
    'LCS': 100001486
}

# Create your views here.

@api_view(['GET'])
def schedule(request, leauge_id):
    leauge = leauge_id
    url_schedule = f'https://api.sportsdata.io/v3/lol/scores/json/Schedule/{leauge_keys[leauge]}?key=2bf56a8d446f40b7b6a86f5e438bb5f2'
    def get_result(gameid):
        url_results = f'https://api.sportsdata.io/v3/lol/stats/json/BoxScore/{gameid}?key=2bf56a8d446f40b7b6a86f5e438bb5f2'
        results = requests.get(url_results).json()
        try: 
            winner_id = results[0]['Matches'][0]['WinningTeamId']
        except:
            winner_id = ''
        return winner_id
    def get_data():
        schedule = requests.get(url_schedule).json() 
        output = []
        for element in schedule: 
            new_element = { 
                'gameId': element['GameId'],
                'firstTeam': { 
                    'id': element['TeamAKey'],
                    'team_id': element['TeamAId'],
                    'name': element['TeamAName'],
                    'src': teams[element['TeamAKey']]
                }, 
                'secondTeam': { 
                    'id': element['TeamBKey'],
                    'team_id': element['TeamBId'],
                    'name': element['TeamBName'],
                    'src': teams[element['TeamBKey']]
                }, 
                'datetime': element['DateTime'],
                'week': element['Week'],
                'winner': get_result(element['GameId'])
            } 
            output.append(new_element) 
        return output
    input = get_data()
    return Response(input)