# CSE515T Bayesian Machine Learning Final Project Proposal

*Note:* Originally conceived as a class' final project.

## Intro & Motivation

Interest in Starcraft II (SCII) in the AI/ML community has increased dramatically after the release of DeepMind's AlphaStar bot which was first demonstrated against a [professional player in Janurary 2019](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii) then subsequently released onto the [public ladder for the Fall 2019 season](https://news.blizzard.com/en-us/starcraft2/22933138/deepmind-research-on-ladder).

One interesting observation made by professional casters and commentators is that the strategies employed by AlphaStar were static and inflexible in nature. In particular, the build order or sequence of structures and unit composition remained constrained to a small set of possibilities. *From examination of referenced games played by AlphaStar on the ladder as identified by the community* [(link)](https://www.reddit.com/r/MachineLearning/comments/d13yex/r_deepmind_starcraft_2_update_alphastar_is/). The most recent version of AlphaStar made known to the public is performing at the GrandMaster level (top 0.2% of players) but *fails to beat professional players consistently* (top \~100-200 players).

I take it that the training architecture of AlphaStar was able to refine the execution of particular strategies and exploit the predominant winning strategies employed during the current ladder season but fails to respond to novel strategies employed by human players in the wild. In essense, AlphaStar's *tactics* were impeccable but it lacks *strategy* discovery. To my limited understanding, the different strategies learnt by AlphaStar were mainly driven by *exploiter agents* in what appears to be an adversarial fashion [(DeepMind Blog, Figure 1)](https://deepmind.com/blog/article/AlphaStar-Grandmaster-level-in-StarCraft-II-using-multi-agent-reinforcement-learning).

One interesting development is the proposal of [*informed MCTS* (Santiago Ontanon, 2016)](https://ieeexplore.ieee.org/document/7860394). It is not clear whether AlphaStar utilized this approach as the author has since joined the Google Research team after the publishing of this paper. In traditional MCTS, the tree-policy is informed with UCB1 which does not make assumptions or attempt to exploit prior knowledge of the opponent's actions (Santiago, 2016). The bayesian approach introduced here is to inform exploration with a distribution of opponent actions.

## Project Scope

The framework setup for training agents in the SCII environment would be out-of-scope for this semester's small project. However, a crucial step towards eventually reaching the *informed MCTS* approach to SCII would be to learn a posterior distribution of opponent actions. **A possible first step in this direction would be to explore the different actions as a time-sequence that the player takes to make predictions at to what the player would do next. Furthermore, it would also be interesting to classify the existing strategies in an unsupervised manner to visualize patterns in the current ladder season.**

Therefore, the proposed scope of my semester project for CSE515T Bayesian ML is as follows in order:
1. Employ unsupervised classification on the existing build-orders with EM clustering.
    - Perhaps this could also serve to inform a prior distribution of possible actions
2. Employ Bayesian time-series prediction to SCII build-order dataset to predict possible distribution of future events.
    - I anticipate this task to be much harder and may be incomplete by the end of this semseter
    
As an immediate result of this research project, contributions may be made to the *spawningtool* python package directly:
> Currently, spawningtool offers a basic parser for extracting build orders from replays. Our goal is to incorporate more sophisticated techniques from Artificial Intelligence to understand and classify these build orders.

## Dataset

[lotv.spawningtool.com](lotv.spawningtool.com) has a vast collection of community uploaded replays and some basic labeling of general starting strategies as well as unit compositions (mixture of units to built) which are hand-labeled by the (human) community.

Furthermore, we have community tools for parsing such replays readily available such as [sc2reader](https://pypi.org/project/sc2reader/), [spawningtool](https://pypi.org/project/spawningtool/), and [Zephyrus Replay Parser](https://github.com/ZephyrBlu/zephyrus-sc2-parser). Each extracts information at different level of detail. I have preliminarily picked *spawningtool* for the broad sketch of what actions are taken by players within a match as demonstrated in the Short Demo section below.

Initially, the exploration done in this study will focus on matches among professional players who are in the top 1% of the ranked ladder. In this population, build order mistakes would be rare and can serve as a low-noise environment to test candidate models before widening to a broader set of replays.

2001 replays are extracted since the last major balance patch (where unit strengths and building costs are adjusted - therefore also potentially drastically changing strategies employed). From:
> https://lotv.spawningtool.com/zip/?pro_only=on&patch=150&query=&order_by=play&coop=n&after_played_on=8%2F14%2F20&before_played_on=3%2F14%2F21&before_time=15&after_time=&p=1.

This will form the set of data for exploration in my project.

The same dataset can be extracted by running the bash script `./dl.sh` to queue a download of 80 zip folders (2001 replays extracted).

### Sanitization

19 of the replays are matches played against AI players rather than among human players, furthermore, there is 1 replay with only a single player practicing a build order (likely against Zerg). These replays are omitted from training but may be prototypical cases of noiseless build order executions (which we can use to verify our classification). Lastly, 2 replays uploaded had differing filenames but contains the same game information (detected via sanitizing the filenames). Thus, a total of **1979** games are utilized for this study. Sanitization was done on the filenames of these replays to conform to the unique format `{matchup}_{timestamp}_{playerOneUID-playerTwoUID}.SC2Replay` where matchups are amongst the 9 possible combinations of the 3 races `{P, T, Z}`. The timestamp and player UID pairs alone should uniquely fingerprint all games. The matchup is to help with classifying either by matchup or by race alone.

The sanitized dataset is currently hosted publically at: [GDriveLink](https://drive.google.com/file/d/1x9dl1W6j4HRwdGaar-KQnLNYN8OHt7ct/view?usp=sharing) with plans to find it a more suitable home once this project is in better shape.

## LIMITATIONS

This study does not take into consideration the map that the game was played on nor the starting locations of the players. The slight asymmetry between starting locations and map layout may influence unit movement and position of buildings but should not influence the build order, granted that different build orders may be utilized based on the different maps. However, including map information into our classification may result in it weighted too heavily if it were the case.

Furthermore, the replays are played by professional players which reduces the rate of mechanical mistakes (cannot execute build order correctly due to unfamilarity with unit management, game interface, time management etc.). In a wider population of replays, additional noise will be introduced and the timings for when certain structures and units are produced will have increased variance.