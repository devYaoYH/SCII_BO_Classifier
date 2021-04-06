STRUCTURES = set([
    'Armory',
    'Assimilator',
    'BanelingNest',
    'Barracks',
    'BarracksReactor',
    'BarracksTechLab',
    'Bunker',
    'CommandCenter',
    'Creeptumor',
    'CyberneticsCore',
    'DarkShrine',
    'EngineeringBay',
    'EvolutionChamber',
    'Extractor',
    'Factory',
    'FactoryReactor',
    'FactoryTechLab',
    'FleetBeacon',
    'Forge',
    'FusionCore',
    'Gateway',
    'GhostAcademy',
    'GreaterSpire',
    'Hatchery',
    'Hive',
    'HydraliskDen',
    'InfestationPit',
    'Lair',
    'LurkerDen',
    'MissileTurret',
    'Nexus',
    'NydusCanal',
    'NydusNetwork',
    'NydusWorm',
    'OrbitalCommand',
    'PhotonCannon',
    'PlanetaryFortress',
    'Pylon',
    'Reactor',
    'Refinery',
    'RoachWarren',
    'RoboticsBay',
    'RoboticsFacility',
    'SensorTower',
    'ShieldBattery',
    'SpawningPool',
    'SpineCrawler',
    'Spire',
    'SporeCrawler',
    'Stargate',
    'Starport',
    'StarportReactor',
    'StarportTechLab',
    'SupplyDepot',
    'TechLab',
    'TemplarArchive',
    'TwilightCouncil',
    'UltraliskCavern',
    'WarpGate',
])
UNITS = set([
    'Adept',
    'Archon',
    'Baneling',
    'Banshee',
    'BattleHellion',
    'Battlecruiser',
    'BroodLord',
    'Carrier',
    'Colossus',
    'Corruptor',
    'Cyclone',
    'DarkTemplar',
    'Disruptor',
    'Drone',
    'Ghost',
    'Hellbat',
    'Hellion',
    'HighTemplar',
    'Hydralisk',
    'Immortal',
    'Infestor',
    'Liberator',
    'Lurker',
    'LurkerMPEgg',
    'Marauder',
    'Marine',
    'Medivac',
    'Mothership',
    'MothershipCore',
    'MULE',
    'Mutalisk',
    'Nuke',
    'Observer',
    'Oracle',
    'Overlord',
    'Overseer',
    'Phoenix',
    'Probe',
    'Queen',
    'Ravager',
    'RavagerCocoon',
    'Raven',
    'Reaper',
    'Roach',
    'SCV',
    'Sentry',
    'SiegeTank',
    'Stalker',
    'SwarmHost',
    'Tempest',
    'Thor',
    'Ultralisk',
    'Viking',
    'VikingAssault',
    'VikingFighter',
    'Viper',
    'VoidRay',
    'WarpPrism',
    'WidowMine',
    'Zealot',
    'Zergling',
])
UPGRADES = set([
    'AdeptPiercingAttack',
    'AdeptShieldUpgrade',
    'AnabolicSynthesis',
    'BansheeCloak',
    'BansheeSpeed',
    'BattlecruiserBehemothReactor',
    'BattlecruiserEnableSpecializations',
    'Blink',
    'Burrow',
    'CarrierLaunchSpeedUpgrade',
    'CentrificalHooks',
    'Charge',
    'ChitinousPlating',
    'CycloneAirUpgrade',
    'CycloneLockOnDamageUpgrade',
    'CycloneLockOnRangeUpgrade',
    'CycloneRapidFireLaunchers',
    'DarkTemplarBlinkUpgrade',
    'DiggingClaws',
    'DrillClaws',
    'DurableMaterials',
    'EnhancedShockwaves',
    'EvolveGroovedSpines',
    'EvolveMuscularAugments',
    'ExtendedThermalLance',
    'FlyingLocusts',
    'GhostMoebiusReactor',
    'GlialReconstitution',
    'GraviticDrive',
    'HiSecAutoTracking',
    'HighCapacityBarrels',
    'HydraliskSpeedUpgrade',
    'HyperflightRotors',
    'InfestorEnergyUpgrade',
    'LiberatorAGRangeUpgrade',
    'LocustLifetimeIncrease',
    'LurkerRange',
    'MagFieldLaunchers',
    'MedivacCaduceusReactor',
    'MedivacIncreaseSpeedBoost',
    'MicrobialShroud',
    'NeosteelFrame',
    'NeuralParasite',
    'ObserverGraviticBooster',
    'PersonalCloaking',
    'PhoenixRangeUpgrade',
    'ProtossAirArmorsLevel1',
    'ProtossAirArmorsLevel2',
    'ProtossAirArmorsLevel3',
    'ProtossAirWeaponsLevel1',
    'ProtossAirWeaponsLevel2',
    'ProtossAirWeaponsLevel3',
    'ProtossGroundArmorsLevel1',
    'ProtossGroundArmorsLevel2',
    'ProtossGroundArmorsLevel3',
    'ProtossGroundWeaponsLevel1',
    'ProtossGroundWeaponsLevel2',
    'ProtossGroundWeaponsLevel3',
    'ProtossShieldsLevel1',
    'ProtossShieldsLevel2',
    'ProtossShieldsLevel3',
    'PsiStormTech',
    'PunisherGrenades',
    'RavenCorvidReactor',
    'RavenDamageUpgrade',
    'RavenEnhancedMunitions',
    'RavenRecalibratedExplosives',
    'ShieldWall',
    'SmartServos',
    'Stimpack',
    'StrikeCannons',
    'TerranBuildingArmor',
    'TerranInfantryArmorsLevel1',
    'TerranInfantryArmorsLevel2',
    'TerranInfantryArmorsLevel3',
    'TerranInfantryWeaponsLevel1',
    'TerranInfantryWeaponsLevel2',
    'TerranInfantryWeaponsLevel3',
    'TerranShipArmorsLevel1',
    'TerranShipArmorsLevel2',
    'TerranShipArmorsLevel3',
    'TerranShipWeaponsLevel1',
    'TerranShipWeaponsLevel2',
    'TerranShipWeaponsLevel3',
    'TerranVehicleAndShipArmorsLevel1',
    'TerranVehicleAndShipArmorsLevel2',
    'TerranVehicleAndShipArmorsLevel3',
    'TerranVehicleAndShipWeaponsLevel1',
    'TerranVehicleAndShipWeaponsLevel2',
    'TerranVehicleAndShipWeaponsLevel3',
    'TerranVehicleArmorsLevel1',
    'TerranVehicleArmorsLevel2',
    'TerranVehicleArmorsLevel3',
    'TerranVehicleWeaponsLevel1',
    'TerranVehicleWeaponsLevel2',
    'TerranVehicleWeaponsLevel3',
    'TransformationServos',
    'TunnelingClaws',
    'VoidRaySpeedUpgrade',
    'WarpGateResearch',
    'ZergFlyerArmorsLevel1',
    'ZergFlyerArmorsLevel2',
    'ZergFlyerArmorsLevel3',
    'ZergFlyerWeaponsLevel1',
    'ZergFlyerWeaponsLevel2',
    'ZergFlyerWeaponsLevel3',
    'ZergGroundArmorsLevel1',
    'ZergGroundArmorsLevel2',
    'ZergGroundArmorsLevel3',
    'ZergMeleeWeaponsLevel1',
    'ZergMeleeWeaponsLevel2',
    'ZergMeleeWeaponsLevel3',
    'ZergMissileWeaponsLevel1',
    'ZergMissileWeaponsLevel2',
    'ZergMissileWeaponsLevel3',
    'hydraliskspeed',
    'overlordspeed',
    'overlordtransport',
    'zerglingattackspeed',
    'zerglingmovementspeed',
])