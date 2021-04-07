import spawningtool.parser
from collections import defaultdict

# To map different langauges into English
race_fix_mapping = {
    'П': 'P',
    'З': 'Z',
    'Т': 'T',
    '星': 'P',
    '神': 'P',
    '人': 'T',
    '异': 'Z',
    '蟲': 'Z',
    '프': 'P',
    '테': 'T',
    '저': 'Z',
    'P': 'P',
    'T': 'T',
    'Z': 'Z',
}

class SC2SpawningtoolData(object):

    @classmethod
    def parse_replay(cls, replay=None, replay_file=None):
        if (replay is not None):
            replay_data = cls(replay)
        elif (replay_file is not None):
            replay = spawningtool.parser.parse_replay(replay_file)
            replay_data = cls(replay)
        else:
            print("Error! No valid replay or replay_file given")
            return None
        return replay_data

    def extract_player_hash(self, player):
        return f"{self.timestamp}_{player['uid']}"

    def as_dict(self):
        return self.players
        
    def __init__(self, replay):
        self.replay = replay
        self.timestamp = replay['unix_timestamp']
        self.matchup = 'v'.join(sorted([race_fix_mapping[p['race'][0]] for p in replay['players'].values()]))
        self.players = {self.extract_player_hash(p): {
                            'race': race_fix_mapping[p['race'][0]],
                            'matchup': self.matchup,
                            'data': p['buildOrder'],
                        } for p in replay['players'].values()} # Extracted Build Order information
        self.winners = [self.extract_player_hash(p) for p in replay['players'].values() if p['is_winner']]
        self.winners = [self.extract_player_hash(p) for p in replay['players'].values() if not p['is_winner']]
        self.frames_per_second = replay['frames_per_second']