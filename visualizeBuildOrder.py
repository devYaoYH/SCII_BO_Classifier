import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from lotv_constants import (
    STRUCTURES, UNITS, UPGRADES
)
from icon_mapping import ICON_MAP
ICON_DIR = 'icons'

# Memoized plt imgs
mem_icons = dict()

BUILD_ORDER_TIME_CUTOFF = 300
FILLER_TIME_THRESHOLD = 3
FILLER_DUMMY_NAME = 'FILLER'

# cutoff None renders entire game
def build_visual_sequence(raw_buildOrder, cutoff=BUILD_ORDER_TIME_CUTOFF):
    visual_buildOrder = []
    for event in raw_buildOrder:
        # Convert time to seconds
        t_min, t_sec = list(map(int, event['time'].split(':')))
        t_event = t_min*60+t_sec
        # Break after 5min
        if (cutoff is not None and t_event >= cutoff):
            break
        cur_event = dict(event)
        cur_event['time'] = t_event
        # Check if there is a gap longer than 1 second between this event and the last
        t_delta = cur_event['time'] - visual_buildOrder[-1]['time'] if len(visual_buildOrder) > 0 else 0
        if (t_delta > FILLER_TIME_THRESHOLD):
            # Insert dummy event(s) with time gap
            for i in range(t_delta//FILLER_TIME_THRESHOLD):
                visual_buildOrder.append({
                    'icon': None,
                    'time': t_delta,
                    'name': FILLER_DUMMY_NAME,
                })
        # Add mapping of visual icon
        event_name = event['name'].strip().replace(' ','') # Clean up name
        cur_event['name'] = event_name
        cur_event['icon'] = ICON_MAP[event_name]
        # Add event back into list
        visual_buildOrder.append(cur_event)
    return visual_buildOrder

def plot_game_series(data, save_file=None, show=True):
    fig, ax = plt.subplots(4, len(data), figsize=(len(data), 8), dpi=64)
    for i, event in enumerate(data):
        for j in range(4):
            ax[j][i].axis('off')
        if (event['icon'] is None):
            continue
        rank = 1
        if (event['name'] in STRUCTURES):
            rank = 1
        elif (event['name'] in UNITS):
            rank = 2
        elif (event['name'] in UPGRADES):
            rank = 3
        else:
            print(f"ERROR: {event['name']} not found!")
        ax[0][i].text(0.3,0,f"{event['time']//60}:{event['time']%60:02}")
        if (event['icon'] in mem_icons):
            ax[rank][i].imshow(mem_icons[event['icon']])
        else:
            img = mpimg.imread(os.path.join(ICON_DIR,event['icon']))
            mem_icons[event['icon']] = img
            ax[rank][i].imshow(img)
    plt.tight_layout()
    if (save_file is not None):
        fig.savefig(f"{save_file}.png")
    if (show):
        plt.show()