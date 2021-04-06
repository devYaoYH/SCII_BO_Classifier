import sc2reader
from sc2reader.events import PlayerStatsEvent, UnitBornEvent, UnitDiedEvent, UnitDoneEvent, UnitTypeChangeEvent, UpgradeCompleteEvent

# Adapted from: https://github.com/IBM/starcraft2-replay-analysis/blob/master/notebooks/starcraft2_replay_analysis.ipynb

# Establish some unit and building groups

VESPENE_UNITS = ["Assimilator", "Extractor", "Refinery"]

SUPPLY_UNITS = ["Overlord", "Overseer", "Pylon", "SupplyDepot"]

WORKER_UNITS = ["Drone", "Probe", "SCV", "MULE"]

BASE_UNITS = ["CommandCenter", "Nexus", "Hatchery", "Lair", "Hive", "PlanetaryFortress", "OrbitalCommand"]

GROUND_UNITS = ["Barracks", "Factory", "GhostAcademy", "Armory", "RoboticsBay", "RoboticsFacility", "TemplarArchive",
                "DarkShrine", "WarpGate", "SpawningPool", "RoachWarren", "HydraliskDen", "BanelingNest", "UltraliskCavern",
                "LurkerDen", "InfestationPit",
                "Gateway"] # Additions

AIR_UNITS = ["Starport", "FusionCore", "RoboticsFacility", "Stargate", "FleetBeacon", "Spire", "GreaterSpire"]

TECH_UNITS = ["EngineeringBay", "Armory", "GhostAcademy", "TechLab", "FusionCore", "Forge", "CyberneticsCore",
              "TwilightCouncil", "RoboticsFacility", "RoboticsBay", "FleetBeacon", "TemplarArchive", "DarkShrine",
              "SpawningPool", "RoachWarren", "HydraliskDen", "BanelingNest", "UltraliskCavern", "LurkerDen", "Spire",
              "GreaterSpire", "EvolutionChamber", "InfestationPit",
              "BarracksReactor", "BarracksTechLab", "FactoryReactor", "FactoryTechLab", "StarportReactor", "StarportTechLab", # Additional building-specific addons
              "Reactor"] # Missing addon

STATIC_UNITS = ["NydusWorm", "NydusNetwork", "MissileTurret", "SpineCrawler", "SporeCrawler", "PhotonCannon", "Bunker", "SensorTower", "ShieldBattery"] # Additional static defences

ARMY_UNITS = ["Marine", "Colossus", "InfestorTerran", "Baneling", "Mothership", "MothershipCore", "Changeling", "SiegeTank", "Viking", "Reaper",
              "Ghost", "Marauder", "Thor", "Hellion", "Hellbat", "Cyclone", "Liberator", "Medivac", "Banshee", "Raven", "Battlecruiser", "Nuke", "Zealot",
              "Stalker", "HighTemplar", "Disruptor", "DarkTemplar", "Sentry", "Phoenix", "Carrier", "Oracle", "VoidRay", "Tempest", "WarpPrism", "Observer",
              "Immortal", "Adept", "Zergling", "Overlord", "Hydralisk", "Mutalisk", "Ultralisk", "Roach", "Infestor", "Corruptor",
              "BroodLord", "Queen", "Overseer", "Archon", "Broodling", "InfestedTerran", "Ravager", "Viper", "SwarmHost",
              "WidowMine", "Lurker"] # Additional lotv units

ARMY_AIR = ["Mothership", "MothershipCore", "Viking", "Liberator", "Medivac", "Banshee", "Raven", "Battlecruiser",
            "Viper", "Mutalisk", "Phoenix", "Oracle", "Carrier", "VoidRay", "Tempest", "Observer", "WarpPrism", "BroodLord",
            "Corruptor", "Observer", "Overseer"]

ARMY_GROUND = [k for k in ARMY_UNITS if k not in ARMY_AIR]

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
        caller.players[event.pid]["vespene_queued_army"].append((event.frame, event.vespene_used_in_progress_technology))
        caller.players[event.pid]["vespene_queued_economic"].append((event.frame, event.vespene_used_in_progress_economy))
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
        
# Aggregate all of our event parsers for use by our ReplayData class

handlers = [handle_expansion_events, handle_worker_events, handle_supply_events, handle_mineral_events,
            handle_vespene_events, handle_ground_events, handle_air_events, handle_tech_events, handle_upgrade_events,
            handle_unit_events]