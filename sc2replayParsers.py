import sc2reader
from sc2reader.events import (
    PlayerStatsEvent,
    UnitBornEvent,
    UnitDiedEvent,
    UnitDoneEvent,
    UnitTypeChangeEvent,
    UpgradeCompleteEvent,
)
from lotv_constants import (
    VESPENE_UNITS,
    SUPPLY_UNITS,
    WORKER_UNITS,
    BASE_UNITS,
    GROUND_UNITS,
    AIR_UNITS,
    TECH_UNITS,
    STATIC_UNITS,
    ARMY_UNITS,
    ARMY_AIR,
    ARMY_GROUND,
    MAP_SPEED,
)
from collections import defaultdict

# Establish our event parsers

def handle_count(caller, event, key, add_value, start_val=0):
    if len(caller.players[event.unit.owner.pid][key]) == 0:
        caller.players[event.unit.owner.pid][key].append((0, start_val)) # minor fix: We start with 1 expansion building?
    # Get the last value
    last_val = caller.players[event.unit.owner.pid][key][-1][1]
    caller.players[event.unit.owner.pid][key].append((event.frame, last_val + add_value))


def handle_expansion_events(caller, event):
    if type(event) is UnitDoneEvent:
        unit = str(event.unit).split()[0]
        if unit in BASE_UNITS:
            caller.players[event.unit.owner.pid]["expansion_event"].append((event.frame, "+", unit))
            handle_count(caller, event, "expansion_buildings", 1, start_val=1)
    elif type(event) is UnitDiedEvent:
        unit = str(event.unit).split()[0]
        if unit in BASE_UNITS:
            caller.players[event.unit.owner.pid]["expansion_event"].append((event.frame, "-", unit))
            handle_count(caller, event, "expansion_buildings", -1, start_val=1)
    elif type(event) is UnitTypeChangeEvent:
        if event.unit.name in BASE_UNITS:
            caller.players[event.unit.owner.pid]["expansion_event"].append((event.frame, "*", event.unit.name))


def handle_worker_events(caller, event):
    if type(event) is PlayerStatsEvent:
        caller.players[event.pid]["workers_active"].append((event.frame, event.workers_active_count))
    elif type(event) is UnitBornEvent:
        unit = str(event.unit).split()[0]
        if unit in WORKER_UNITS:
            caller.players[event.control_pid]["worker_event"].append((event.frame, "+", unit))
    elif type(event) is UnitDiedEvent:
        unit = str(event.unit).split()[0]
        if unit in WORKER_UNITS:
            caller.players[event.unit.owner.pid]["worker_event"].append((event.frame, "-", unit))


def handle_supply_events(caller, event):
    if type(event) is PlayerStatsEvent:
        caller.players[event.pid]["supply_available"].append((event.frame, int(event.food_made)))
        caller.players[event.pid]["supply_consumed"].append((event.frame, int(event.food_used)))
        utilization = 0 if event.food_made == 0 else event.food_used / event.food_made
        caller.players[event.pid]["supply_utilization"].append((event.frame, utilization))
        worker_ratio = 0 if event.food_used == 0 else event.workers_active_count / event.food_used
        caller.players[event.pid]["worker_supply_ratio"].append((event.frame, worker_ratio))
    elif type(event) is UnitDoneEvent:
        unit = str(event.unit).split()[0]
        if unit in SUPPLY_UNITS:
            caller.players[event.unit.owner.pid]["supply_event"].append((event.frame, "+", unit))
    elif type(event) is UnitBornEvent:
        # Specifically for Overlord
        unit = str(event.unit).split()[0]
        if unit == "Overlord":
            caller.players[event.control_pid]["supply_event"].append((event.frame, "+", unit))
    elif type(event) is UnitDiedEvent:
        # Buildings/ Overlord/Overseer
        unit = str(event.unit).split()[0]
        if unit in SUPPLY_UNITS:
            caller.players[event.unit.owner.pid]["supply_event"].append((event.frame, "-", unit))
    elif type(event) is UnitTypeChangeEvent:
        if event.unit_type_name == "Overseer":
            caller.players[event.unit.owner.pid]["supply_event"].append((event.frame, "*", event.unit_type_name))


def handle_vespene_events(caller, event):
    if type(event) is PlayerStatsEvent:
        caller.players[event.pid]["vespene_available"].append((event.frame, event.vespene_current))
        caller.players[event.pid]["vespene_collection_rate"].append((event.frame, event.vespene_collection_rate))
        vesp_per_worker = 0 if event.workers_active_count == 0 else event.vespene_collection_rate / event.workers_active_count
        caller.players[event.pid]["vespene_per_worker_rate"].append((event.frame, vesp_per_worker))
        caller.players[event.pid]["vespene_cost_active_forces"].append((event.frame, event.vespene_used_active_forces))
        caller.players[event.pid]["vespene_spend"].append((event.frame, event.vespene_used_current))
        caller.players[event.pid]["vespene_value_current_technology"].append((event.frame, event.vespene_used_current_technology))
        caller.players[event.pid]["vespene_value_current_army"].append((event.frame, event.vespene_used_current_army))
        caller.players[event.pid]["vespene_value_current_economic"].append((event.frame, event.vespene_used_current_economy))
        caller.players[event.pid]["vespene_queued"].append((event.frame, event.vespene_used_in_progress))
        caller.players[event.pid]["vespene_queued_technology"].append((event.frame, event.vespene_used_in_progress_technology))
        caller.players[event.pid]["vespene_queued_army"].append((event.frame, event.vespene_used_in_progress_army)) # BUG!!
        caller.players[event.pid]["vespene_queued_economic"].append((event.frame, event.vespene_used_in_progress_economy))
        # Additional partitioned current+queued resources
        caller.players[event.pid]["vespene_total_technology"].append((event.frame, event.vespene_used_current_technology + event.vespene_used_in_progress_technology))
        caller.players[event.pid]["vespene_total_army"].append((event.frame, event.vespene_used_current_army + event.vespene_used_in_progress_army))
        caller.players[event.pid]["vespene_total_economic"].append((event.frame, event.vespene_used_current_economy + event.vespene_used_in_progress_economy))
    elif type(event) is UnitDoneEvent:
        unit = str(event.unit).split()[0]
        if unit in VESPENE_UNITS:
            caller.players[event.unit.owner.pid]["vespene_event"].append((event.frame, "+", unit))
    elif type(event) is UnitDiedEvent:
        unit = str(event.unit).split()[0]
        if unit in VESPENE_UNITS:
            caller.players[event.unit.owner.pid]["vespene_event"].append((event.frame, "-", unit))


def handle_resources_events(caller, event):
    if type(event) is PlayerStatsEvent:
        caller.players[event.pid]["mineral_destruction"].append((event.frame, event.minerals_killed))
        caller.players[event.pid]["mineral_destruction_army"].append((event.frame, event.minerals_killed_army))
        caller.players[event.pid]["mineral_destruction_economic"].append((event.frame, event.minerals_killed_economy))
        caller.players[event.pid]["mineral_destruction_technology"].append((event.frame, event.minerals_killed_technology))
        caller.players[event.pid]["mineral_loss"].append((event.frame, event.minerals_lost))
        caller.players[event.pid]["mineral_loss_army"].append((event.frame, event.minerals_lost_army))
        caller.players[event.pid]["mineral_loss_economic"].append((event.frame, event.minerals_lost_economy))
        caller.players[event.pid]["mineral_loss_technology"].append((event.frame, event.minerals_lost_technology))

        caller.players[event.pid]["vespene_destruction"].append((event.frame, event.vespene_killed))
        caller.players[event.pid]["vespene_destruction_army"].append((event.frame, event.vespene_killed_army))
        caller.players[event.pid]["vespene_destruction_economic"].append((event.frame, event.vespene_killed_economy))
        caller.players[event.pid]["vespene_destruction_technology"].append((event.frame, event.vespene_killed_technology))
        caller.players[event.pid]["vespene_loss"].append((event.frame, event.vespene_lost))
        caller.players[event.pid]["vespene_loss_army"].append((event.frame, event.vespene_lost_army))
        caller.players[event.pid]["vespene_loss_economic"].append((event.frame, event.vespene_lost_economy))
        caller.players[event.pid]["vespene_loss_technology"].append((event.frame, event.vespene_lost_technology))


def handle_ground_events(caller, event):
    if type(event) is UnitDoneEvent:
        unit = str(event.unit).split()[0]
        if unit in GROUND_UNITS:
            count_name = "_".join(["building", unit, "count"])
            caller.players[event.unit.owner.pid]["ground_building"].append((event.frame, "+", unit))
            handle_count(caller, event, count_name, 1)
    elif type(event) is UnitDiedEvent:
        unit = str(event.unit).split()[0]
        if unit in GROUND_UNITS:
            count_name = "_".join(["building", unit, "count"])
            caller.players[event.unit.owner.pid]["ground_building"].append((event.frame, "-", unit))
            handle_count(caller, event, count_name, -1)
    elif type(event) is UnitTypeChangeEvent:
        if event.unit_type_name == "LurkerDen":
            count_name = "_".join(["building", event.unit_type_name, "count"])
            caller.players[event.unit.owner.pid]["ground_building"].append((event.frame, "*", event.unit_type_name))
            handle_count(caller, event, count_name, 1)


def handle_air_events(caller, event):
    if type(event) is UnitDoneEvent:
        unit = str(event.unit).split()[0]
        if unit in AIR_UNITS:
            count_name = "_".join(["building", unit, "count"])
            caller.players[event.unit.owner.pid]["air_building"].append((event.frame, "+", unit))
            handle_count(caller, event, count_name, 1)
    elif type(event) is UnitDiedEvent:
        unit = str(event.unit).split()[0]
        if unit in AIR_UNITS:
            count_name = "_".join(["building", unit, "count"])
            caller.players[event.unit.owner.pid]["air_building"].append((event.frame, "-", unit))
            handle_count(caller, event, count_name, -1)
    elif type(event) is UnitTypeChangeEvent:
        if event.unit_type_name == "GreaterSpire":
            count_name = "_".join(["building", event.unit_type_name, "count"])
            caller.players[event.unit.owner.pid]["air_building"].append((event.frame, "*", event.unit_type_name))
            handle_count(caller, event, count_name, 1)


def handle_unit_events(caller, event):
    if type(event) is UnitBornEvent:
        unit = event.unit_type_name
        if unit in ARMY_UNITS:
            unit_count_name = "_".join(["unit", unit, "count"])
            caller.players[event.control_pid]["army_event"].append((event.frame, "+", unit))
            handle_count(caller, event, unit_count_name, 1)
            if unit in ARMY_AIR:
                handle_count(caller, event, "army_air", 1)
            elif unit in ARMY_GROUND:
                handle_count(caller, event, "army_ground", 1)
            handle_count(caller, event, "army_count", 1)
    elif type(event) is UnitDoneEvent:
        unit = str(event.unit).split()[0]
        if unit in ARMY_UNITS:
            unit_count_name = "_".join(["unit", unit, "count"])
            caller.players[event.unit.owner.pid]["army_event"].append((event.frame, "+", unit))
            handle_count(caller, event, unit_count_name, 1)
            if unit in ARMY_AIR:
                handle_count(caller, event, "army_air", 1)
            elif unit in ARMY_GROUND:
                handle_count(caller, event, "army_air", 1)
            handle_count(caller, event, "army_count", 1)
    elif type(event) is UnitDiedEvent:
        unit = str(event.unit).split()[0]
        if unit in ARMY_UNITS:
            unit_count_name = "_".join(["unit", unit, "count"])
            caller.players[event.unit.owner.pid]["army_event"].append((event.frame, "-", unit))
            if unit in ARMY_AIR:
                handle_count(caller, event, "army_air", -1)
            elif unit in ARMY_GROUND:
                handle_count(caller, event, "army_ground", -1)
            handle_count(caller, event, unit_count_name, -1)
            handle_count(caller, event, "army_count", -1)
    elif type(event) is UnitTypeChangeEvent:
        unit = str(event.unit).split()[0]
        if event.unit_type_name in ARMY_UNITS:
            unit_count_name = "_".join(["unit", event.unit_type_name, "count"])

            caller.players[event.unit.owner.pid]["army_event"].append((event.frame, "*", unit))

            handle_count(caller, event, unit_count_name, 1)


def handle_tech_events(caller, event):
    if type(event) is UnitDoneEvent:
        unit = str(event.unit).split()[0]
        if unit in TECH_UNITS:
            caller.players[event.unit.owner.pid]["tech_building"].append((event.frame, "+", unit))
    elif type(event) is UnitDiedEvent:
        unit = str(event.unit).split()[0]
        if unit in TECH_UNITS:
            caller.players[event.unit.owner.pid]["tech_building"].append((event.frame, "-", unit))
    elif type(event) is UnitTypeChangeEvent:
        if event.unit_type_name in ["GreaterSpire", "LurkerDen"]:
            caller.players[event.unit.owner.pid]["tech_building"].append((event.frame, "*", event.unit_type_name))


def handle_upgrade_events(caller, event):
    if type(event) is UpgradeCompleteEvent and event.frame > 0:
        if not event.upgrade_type_name.startswith("Spray"):
            caller.players[event.pid]["upgrades"].append((event.frame, event.upgrade_type_name))


def handle_mineral_events(caller, event):
    if type(event) is PlayerStatsEvent:
        caller.players[event.pid]["minerals_available"].append((event.frame, event.minerals_current))
        caller.players[event.pid]["mineral_collection_rate"].append((event.frame, event.minerals_collection_rate,))
        caller.players[event.pid]["mineral_cost_active_forces"].append((event.frame, event.minerals_used_active_forces))
        mins_per_worker = 0 if event.workers_active_count == 0 else event.minerals_collection_rate / event.workers_active_count
        caller.players[event.pid]["mineral_per_worker_rate"].append((event.frame, mins_per_worker))
        caller.players[event.pid]["mineral_spend"].append((event.frame, event.minerals_used_current))
        caller.players[event.pid]["mineral_value_current_technology"].append((event.frame, event.minerals_used_current_technology))
        caller.players[event.pid]["mineral_value_current_army"].append((event.frame, event.minerals_used_current_army))
        caller.players[event.pid]["mineral_value_current_economic"].append((event.frame, event.minerals_used_current_economy))
        caller.players[event.pid]["mineral_queued"].append((event.frame, event.minerals_used_in_progress))
        caller.players[event.pid]["mineral_queued_technology"].append((event.frame, event.minerals_used_in_progress_technology))
        caller.players[event.pid]["mineral_queued_army"].append((event.frame, event.minerals_used_in_progress_army))
        caller.players[event.pid]["mineral_queued_economic"].append((event.frame, event.minerals_used_in_progress_economy))
        # Additional partitioned current+queued resources
        caller.players[event.pid]["mineral_total_technology"].append((event.frame, event.minerals_used_current_technology + event.minerals_used_in_progress_technology))
        caller.players[event.pid]["mineral_total_army"].append((event.frame, event.minerals_used_current_army + event.minerals_used_in_progress_army))
        caller.players[event.pid]["mineral_total_economic"].append((event.frame, event.minerals_used_current_economy + event.minerals_used_in_progress_economy))
        
# Aggregate all of our event parsers for use by our ReplayData class

handlers = [handle_expansion_events, handle_worker_events, handle_supply_events, handle_mineral_events,
            handle_vespene_events, handle_ground_events, handle_air_events, handle_tech_events, handle_upgrade_events,
            handle_unit_events]

# Convenience grouping of stats
supply_stats = ('supply_available', 'supply_consumed')
worker_stats = ('workers_active', 'mineral_per_worker_rate')
ratio_stats = ('supply_utilization', 'worker_supply_ratio')
resource_stats = ('mineral_collection_rate', 'vespene_collection_rate')
mineral_stats = ('mineral_value_current_economic', 'mineral_value_current_technology', 'mineral_value_current_army')
vespene_stats = ('vespene_value_current_economic', 'vespene_value_current_technology', 'vespene_value_current_army')
spend_stats = ('mineral_spend', 'vespene_spend')
mineral_queued_stats = ('mineral_queued_economic', 'mineral_queued_technology', 'mineral_queued_army')
vespene_queued_stats = ('vespene_queued_economic', 'vespene_queued_technology', 'vespene_queued_army')
mineral_total_stats = ('mineral_total_economic', 'mineral_total_technology', 'mineral_total_army')
vespene_total_stats = ('vespene_total_economic', 'vespene_total_technology', 'vespene_total_army')

# Alphabetically ordered stats headings
all_stats = sorted(list(set(supply_stats)|set(worker_stats)|set(ratio_stats)|set(resource_stats)|set(mineral_stats)|set(vespene_stats)|set(spend_stats)| \
            set(mineral_queued_stats)|set(vespene_queued_stats)|set(mineral_total_stats)|set(vespene_total_stats)))

# Exposed constant to pick out pertinent statistics
STATS_GROUPS = [supply_stats, worker_stats, ratio_stats, resource_stats, spend_stats, mineral_total_stats, vespene_total_stats]

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

# sc2reader Replay Parser Wrapper Class
class SC2ReplayData(object):
    __parsers__ = handlers
    
    @classmethod
    def parse_replay(cls, replay=None, replay_file=None):
        if (replay is not None):
            replay_data = cls(replay)
        elif (replay_file is not None):
            replay = sc2reader.load_replay(replay_file)
            replay_data = cls(replay)
        else:
            print("Error! No valid replay or replay_file given")
            return None
        
        # Parse events in replay with parsers
        try:
            # Metadata
            replay_data.frames = replay.frames
            for event in replay.events:
                for parser in cls.__parsers__:
                    parser(replay_data, event)
            if replay.winner is not None:
                replay_data.winners = replay.winner.players
                replay_data.losers = [p for p in replay.players if p not in replay.winner.players]
            # Maybe the GAME expansion (version)? e.g. wol/hots/lotv
            replay_data.expansion = replay.expansion
            return replay_data
        except Exception as e:
            print(e)
            return None
        
    def as_dict(self):
        return {
            "replay": self.replay,
            "expansion": self.expansion,
            "frames": self.frames,
            "matchup": 'v'.join(sorted([s.detail_data["race"][0].upper() for s in self.replay.players])),
            "winners": [(s.pid, s.name, s.detail_data["race"]) for s in self.winners],
            "losers": [(s.pid, s.name, s.detail_data["race"]) for s in self.losers],
            "player_names": [str(s) for s in self.replay.players],
            "stats_names": [k for k in self.players[1].keys()], # Player statistic key labels
            "stats": {player: data for player, data in self.players.items()}, # Full dictionary
            "frames_per_second": self.frames_per_second,
        }

    def as_dataframe(self):
        import pandas as pd
        matchup = 'v'.join(sorted([s.detail_data["race"][0].upper() for s in self.replay.players]))
        return {
            # Unique hash for this dataline entry which is similar to replay naming convention
            # Added benefit of pulling out this entry from huge dictionary with replay file information
            f"{self.replay.unix_timestamp}_{p.detail_data['bnet']['uid']}": \
                {
                    "race": p.detail_data["race"][0].upper(), # {P,T,Z}
                    "matchup": matchup, 
                    "data": pd.DataFrame ({
                        # We drop the framenumber for a 1-d array of values per attribute dimension
                        k: [value for (framenumber,value) in self.players[p.pid][k]] \
                        for k in all_stats
                    }, columns=list(all_stats))
                } \
            for p in self.replay.players
        }
        
    def __init__(self, replay):
        self.replay = replay
        self.players = defaultdict(lambda: defaultdict(list)) # Dictionary: {Dictionary: list}
        self.winners = []
        self.losers = []
        self.frames_per_second = replay.game_fps*MAP_SPEED[replay.speed]
        self.expansion = None # ??