# Starcraft II Build Order Classification

## Contents

- [Proposal](/Proposal.md)
- [Data Visualization](/Dataset%20Visualization.ipynb)
    - sc2reader parsing helper functions adapted from [IBM/starcraft2-replay-analysis](https://github.com/IBM/starcraft2-replay-analysis) under Apache 2.0 License.
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