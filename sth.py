import json
import requests 

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


class GetSchedule():
    def __init__(self, leauge):
        self.leauge = leauge
        self.teams = teams
        leauge_keys = {
            'LEC': 100001483,
            'LCS': 100001486
        }
        self.url_schedule = f'https://api.sportsdata.io/v3/lol/scores/json/Schedule/{leauge_keys[leauge]}?key=2bf56a8d446f40b7b6a86f5e438bb5f2'


    def get_data(self):
        schedule = requests.get(self.url_schedule).json() 
        output = []
        for element in schedule: 
            new_element = { 
                'gameId': element['GameId'],
                'firstTeam': { 
                    'id': element['TeamAKey'],
                    'team_id': element['TeamAId'],
                    'name': element['TeamAName'],
                    'src': self.teams[element['TeamAKey']]
                }, 
                'secondTeam': { 
                    'id': element['TeamBKey'],
                    'team_id': element['TeamBId'],
                    'name': element['TeamBName'],
                    'src': self.teams[element['TeamBKey']]
                }, 
                'datetime': element['DateTime'],
                'week': element['Week'],
                'winner': self.get_result(element['GameId'])
            } 
            output.append(new_element) 
        return output

    def get_result(self, gameid):
        self.url_results = f'https://api.sportsdata.io/v3/lol/stats/json/BoxScore/{gameid}?key=2bf56a8d446f40b7b6a86f5e438bb5f2'
        results = requests.get(self.url_results).json()
        try: 
            winner_id = results[0]['Matches'][0]['WinningTeamId']
        except:
            winner_id = ''
        return winner_id

    def weeks_to_txt(self):
        output = self.get_data()
        maxWeek = max(output, key=lambda x:x['week'])['week']
        for n in range(1, maxWeek+1):
            temp = [x for x in output if x['week'] == n]
            text = json.dumps(temp, indent = 2)
            with open(f'OUTPUT/ {self.leauge} week{n}.txt', 'w') as f:
                f.write(text)

GetSchedule('LCS').weeks_to_txt()
