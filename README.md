# Starcraft II Build Order Classification

## Contents

- [Proposal](/Proposal.md)
    - AlphaStar plays really well (executes actions close to flawlessly), however, the type of strategies it employs are limited and does not adapt to opponent moves especially in the late game.
    - Informed MCTS is an interesting strategy to enable exploitation of possible enemy action distribution.
    - However, we first require some prediction of enemy actions. Here, Bayesian classification and multivariate regression can help.
    - First cluster buildorder sequences to inform priors.
    - Next feed information from clustering into regression for next possible step taken.
- [Data Visualization](/Dataset%20Visualization.ipynb)
    - [spawningtool extracted data](https://github.com/StoicLoofah/spawningtool/wiki/Diving-into-the-Data): Discrete action list of units, structures, and upgrades produced. Unfortunately does not make available game-level resource information such as minerals available or supply utilization.
    - sc2reader parsing helper functions adapted from [IBM/starcraft2-replay-analysis](https://github.com/IBM/starcraft2-replay-analysis) under Apache 2.0 License. sc2reader helps us with the extraction of resource information. In particular, we are interested in the distribution of resources across the 3 classes \{economy, army, technology\} as the game progresses.
- [Feature Extraction](/Feature%20Extraction.ipynb)
    - [Time Series extracted information](/data/timeseries_data.pbz2) is a huge dictionary for each player's statistics in a match and follows the following structured format. The `'data'` field is a pandas dataframe with each column as a distinct feature in this particular instance of a time series (1 game for 1 player).
    ```
    '1597403940_2305463': {
         'race': 'P',
         'matchup': 'PvP',
         'data':      mineral_collection_rate  mineral_per_worker_rate  mineral_queued_army  \
         0                          0                 0.000000                    0   
         1                        293                24.416667                    0   
         2                        671                51.615385                    0   
         3                        671                51.615385                    0   
         4                        755                53.928571                    0   
         ..                       ...                      ...                  ...   
         121                     1903                32.254237                    0   
         122                     1875                31.779661                    0   
         123                     1903                33.982143                    0   
         124                     1903                35.240741                    0   
         125                     1903                35.240741                    0 
    ...
    ```
    - [Action Sequence extracted information](/data/buildOrder_data.pbz2) (pending compression & cleanup) largely follows the same format.
    ```
    '1597403940_2305463': {
         'race': 'P',
         'matchup': 'PvP',
         'data': {
              [...] # Raw spawningtool 'buildOrder' field dictionary for now => can be compressed
         }
    }
    ```
    - As the data is quite large, we use python's (>=3.0) in-built compression tool bzip2 to reduce our footprint (to around 10MB from a 350MB replay pack - of course, we also threw away quite some information along the way). Each set of extracted data can be easily extracted and loaded into a python dictionary using the included `zipUtil` functions:
    ```py
    from zipUtil import zip_write, zip_read
    # Write
    dic = {} # some dictionary
    zip_write('filename', dic)
    # Read
    read_dic = zip_read('filename')
    ```

- [State-Action Generation](/State-Action%20Generation.ipynb)
    - The nearest slice of timeseries information is found for each action taken and put into a (state,action) feature-label pair. In addition to the timeseries information (on economic resources), accumulated actions taken thus far is also extracted as a set of discrete features.

- [Naive Bayes + Baselines](/Naive%20Bayes.ipynb)
    - Baseline: Random Forest Classifier & AdaBoost
    - Naive Bayes: Condition on continuous, discrete, mixture + KDE likelihood estimation
    - Gaussian Process Classification: Binary One-vs-Rest -> softmax
        - Hard to select inducing set, and did not perform above heuristic strategy of picking most frequent actions
    - [Results](/Results%20Visualization.ipynb) are put into a json and plotted here

## Purpose

Automate clustering of replays into different types of Build Orders in an **unsupervised** and possibly **online** fashion.

## Resources

Dataset: [1979 Replays (Patch >= 5.0.2 BU)](https://drive.google.com/file/d/1x9dl1W6j4HRwdGaar-KQnLNYN8OHt7ct/view?usp=sharing)
- Pro-players, non-AI games

Curated Icon set: [Structure,Unit,Upgrades Icon Set + File mapping](https://drive.google.com/file/d/1C78kzDM_g9ii4KGc5pYSowfBbBZH06R3/view?usp=sharing)
- Just unzip into same directory as the notebooks and it should work
- Python data stuctures used for mapping, *will update to more portable .json format at a later time*
- All copyrights belong to **Blizzard Entertainment Inc.**, fair usage for purposes of scientific publication/educational use in this project.