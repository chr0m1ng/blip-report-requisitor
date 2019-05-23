from requests import Session
from functools import reduce
from uuid import uuid4
from json import dumps


def percentage(part, whole):
    return round(100 * float(part) / float(whole), 2)


class Requisitor(object):

    def __init__(self, authorization='', token='', bot=''):
        if authorization[0:3].lower() != 'key':
            authorization = 'Key %s' % authorization
        self.Session = Session()
        self.Session.headers.update({'Authorization': authorization})
        self.Token = token
        self.Bot = bot

    def getCustomReport(self, uri, start_date, end_date, take=999999):
        body = {
            'id': str(uuid4()),
            'method': 'get',
            'to': 'postmaster@analytics.msging.net',
            'uri': '%s?startDate=%sT03%%3A00%%3A00.000Z&endDate=%sT03%%3A00%%3A00.000Z&$take=%s' %
            (uri, start_date.strftime('%Y-%m-%d'),
             end_date.strftime('%Y-%m-%d'), take)
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
            'https://api.blip.ai/applications/%s/messages/receivedBy/D/%sT00:00:00.000Z/%sT00:00:00.000Z' %
            (self.Bot, start_date.strftime('%Y-%m-%d'),
             end_date.strftime('%Y-%m-%d')),
            headers={
                'Authorization': 'Bearer %s' % self.Token
            }
        )
        sent_messages = self.Session.get(
            'https://api.blip.ai/applications/%s/messages/sentBy/D/%sT00:00:00.000Z/%sT00:00:00.000Z' %
            (self.Bot, start_date.strftime('%Y-%m-%d'),
             end_date.strftime('%Y-%m-%d')),
            headers={
                'Authorization': 'Bearer %s' % self.Token
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
