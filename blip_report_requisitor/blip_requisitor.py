from requests import Session
from functools import reduce
from uuid import uuid4
from json import dumps
from urllib.parse import quote

def percentage(part, whole):
    return round(100 * float(part) / float(whole), 2)


class Requisitor(object):

    def __init__(self, authorization='', token='', bot=''):
        if authorization[0:3].lower() != 'key':
            authorization = f'Key {authorization}'
        self.Session = Session()
        self.Session.headers.update({'Authorization': authorization})
        self.Token = token
        self.Bot = bot

    def getAllReportsOfAllCategories(self, start_date, end_date, take=999999):    
        ret = []
        for category in self.getAllCategories() :
            ret.append({category: self.getCustomReport(category,start_date,end_date)})
        return ret

    def getAllCategories(self, take=999999):
        body = {
            'id': str(uuid4()),
            'method': 'get',
            'to': 'postmaster@analytics.msging.net',
            'uri': f'/event-track?$take={take}',
        }

        command = self.Session.post('https://msging.net/commands', json=body)
        command = command.json()
        
        report = [tracking['category'] for tracking in command['resource']['items']]

        return report

    def getCustomReport(self, category, start_date, end_date, take=999999):
        category = f'/event-track/{quote(category)}'
        a = f'normal{category} ne ta'
        body = {
            'id': str(uuid4()),
            'method': 'get',
            'to': 'postmaster@analytics.msging.net',
            'uri': f'{category}?startDate={start_date.strftime("%Y-%m-%d")}T03%3A00%3A00.000Z&endDate={end_date.strftime("%Y-%m-%d")}T03%3A00%3A00.000Z&$take={take}'
        }
        command = self.Session.post(
            'https://msging.net/commands',
            json=body
        )
        command = command.json()
        itemType = command['resource']['itemType']
        report = []
        if itemType == 'application/vnd.iris.eventTrack+json':
            report = Requisitor.getEventTrackValues(command['resource'])
        elif itemType == 'application/vnd.iris.analytics.metric-identity+json':
            report = Requisitor.getMetricsValue(command['resource'])

        return report

    def getTrafficMessagesReport(self, start_date, end_date):
        recv_messages = self.Session.get(
            f'https://api.blip.ai/applications/{self.Bot}/messages/receivedBy/D/{start_date.strftime("%Y-%m-%d")}T00:00:00.000Z/{end_date.strftime("%Y-%m-%d")}T00:00:00.000Z',
            headers={
                'Authorization': f'Bearer {self.Token}'
            }
        )
        sent_messages = self.Session.get(
            f'https://api.blip.ai/applications/{self.Bot}/messages/sentBy/D/{start_date.strftime("%Y-%m-%d")}T00:00:00.000Z/{end_date.strftime("%Y-%m-%d")}T00:00:00.000Z' ,
            headers={
                'Authorization': f'Bearer {self.Token}'
            }
        )

        recv_messages = reduce(
            lambda x, y: x + y,
            [x['count'] for x in recv_messages.json()]
        )
        sent_messages = reduce(
            lambda x, y: x + y,
            [x['count'] for x in sent_messages.json()]
        )

        return recv_messages + sent_messages

    @staticmethod
    def getMessagesCount(messages):
        return reduce(
            lambda x, y: x + y,
            [x['count'] for x in messages]
        )

    @staticmethod
    def getMetricsValue(resource):
        return reduce(
            lambda x, y: x + y,
            [x['count'] for x in resource['items']]
        )

    @staticmethod
    def getEventTrackValues(resource):
        tracks = Requisitor.mergeTracks(resource['items'])
        if len(tracks) == 1:
            return tracks[0]['total']

        if len(tracks) == 0:
            return 0
        total = reduce(
            lambda x, y: x + y,
            [x['total'] for x in tracks]
        )
        for t in tracks:
            t['%'] = percentage(t['total'], total)
        return tracks

    @staticmethod
    def mergeTracks(tracks):
        merged = []
        for t in tracks:
            track_pos = Requisitor.getTrackPosByActionOrDefault(
                t['action'],
                merged
            )
            if track_pos is None:
                merged.append(
                    {
                        'acao': t['action'],
                        'total': int(t['count'])
                    }
                )
            else:
                merged[track_pos]['total'] += int(t['count'])
        return merged

    @staticmethod
    def getTrackPosByActionOrDefault(action, tracks, default=None):
        for i, track in enumerate(tracks):
            if track['acao'] == action:
                return i
        return default
