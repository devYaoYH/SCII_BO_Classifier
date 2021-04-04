import os
import sys
import spawningtool.parser
from collections import defaultdict

# Where replays are located
replay_dir = "replays"
# Where we should copy over the sanitized replays
output_dir = "sanitized_replays"

class PlayersMetadata(object):
    def __init__(self, players):
        self.valid = True
        self.ai_match = False
        self.reason = ""
        if (len(players) != 2):
            self.valid = False
            self.reason = "Not 2-player match"
        else:
            self.uid = (players[1]['uid'], players[2]['uid'])
            self.race = (players[1]['race'], players[2]['race'])
            self.uidPair = f"{self.uid[0]}-{self.uid[1]}"
            self.matchup = f"{self.race[0][0]}v{self.race[1][0]}"
            if (not (players[1]['is_human'] and players[2]['is_human'])):
                if (players[1]['is_human'] == players[2]['is_human'] and not players[1]['is_human']):
                    self.valid = False
                    self.reason = "No human players"
                else:
                    self.ai_match = True
                    self.humanPlayer = 1 if players[1]['is_human'] else 2

class GameMetadata(object):
    def __init__(self, game):
        self.timestamp = game['unix_timestamp']
        self.map_hash = game['map_hash']
        self.players = PlayersMetadata(game['players'])
        self.valid = self.players.valid
        self.reject_reason = self.players.reason
        self.hashCode = None

    def __str__(self):
        if (self.hashCode is None and self.valid):
            self.hashCode = f"{self.players.matchup}_{self.timestamp}_{self.players.uidPair}{'_AI' if self.players.ai_match else ''}"
        return self.hashCode

# Scan through replays and sanitize replays
replay_codedFilename = dict()
replay_errList = []
replay_rejected = dict()

sanitized_filename_overlaps = defaultdict(set)

counter = 314

# Copy over sanitized & annonymized filenames (simultaneously)
from shutil import copy

for (dirpath, dirnames, filenames) in os.walk(replay_dir):
    for filename in filenames[counter:]:
        game = spawningtool.parser.parse_replay(os.path.join(replay_dir, filename))
        try:
            metadata = GameMetadata(game)
        except Exception as e:
            print(e)
            print(f"Error parsing: {filename}")
            print(f"    info: {game.keys()}")
            print(f"    players: {game['players']}")
            replay_errList.append(filename)
            continue

        if (not metadata.valid):
            print(f"Replay: {filename} NOT VALID")
            print(f"    Reason: {metadata.reject_reason}")
            replay_rejected[filename] = metadata.reject_reason
        else:
            print(f"Replay [{counter}] {filename}: {metadata}")
            sanitized_filename = str(metadata)
            sanitized_filename_overlaps[sanitized_filename].add(filename)
            if (len(sanitized_filename_overlaps[sanitized_filename]) > 1):
                sanitized_filename += f"_{len(sanitized_filename_overlaps[sanitized_filename])}"
            replay_codedFilename[filename] = sanitized_filename
            copy(os.path.join(replay_dir, filename), os.path.join(output_dir, sanitized_filename+".SC2Replay"))
        counter += 1
    break

print(replay_errList)
for fname, reason in replay_rejected.items():
    print(f"{fname}: {reason}")
for s_fname, files in sanitized_filename_overlaps.items():
    if (len(files) > 1):
        print(f"WARN - BAD_HASH: unique_filename:{s_fname} was generated more than once!!")
        print(files)

with open("sanitize.log", "w+") as fout:
    for fname in replay_errList:
        fout.write(fname)
        fout.write("\n")
    for fname, reason in replay_rejected.items():
        fout.write(f"{fname}: {reason}")
        fout.write("\n")

