# Starcraft II Build Order Classification

## Contents

- [Proposal](/Proposal.md)
- [Data Visualization](/Dataset%20Visualization.ipynb)
    - [spawningtool extracted data](https://github.com/StoicLoofah/spawningtool/wiki/Diving-into-the-Data): Discrete action list of units, structures, and upgrades produced. Unfortunately does not make available game-level resource information such as minerals available or supply utilization.
    - sc2reader parsing helper functions adapted from [IBM/starcraft2-replay-analysis](https://github.com/IBM/starcraft2-replay-analysis) under Apache 2.0 License. sc2reader helps us with the extraction of resource information. In particular, we are interested in the distribution of resources across the 3 classes \{economy, army, technology\} as the game progresses.
- [Feature Extraction](/Feature%20Extraction.ipynb)

## Purpose

Automate clustering of replays into different types of Build Orders in an **unsupervised** and possibly **online** fashion.

## Resources

Dataset: [1979 Replays (Patch >= 5.0.2 BU)](https://drive.google.com/file/d/1x9dl1W6j4HRwdGaar-KQnLNYN8OHt7ct/view?usp=sharing)
- Pro-players, non-AI games

Curated Icon set: [Structure,Unit,Upgrades Icon Set + File mapping](https://drive.google.com/file/d/1C78kzDM_g9ii4KGc5pYSowfBbBZH06R3/view?usp=sharing)
- Just unzip into same directory as the notebooks and it should work
- Python data stuctures used for mapping, *will update to more portable .json format at a later time*
- All copyrights belong to **Blizzard Entertainment Inc.**, fair usage for purposes of scientific publication/educational use in this project.