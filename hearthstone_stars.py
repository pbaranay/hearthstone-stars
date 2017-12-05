from collections import OrderedDict
import random

def build_star_map():
    # total number of stars: rank
    d = OrderedDict()
    ranks = range(1, 26)
    ranks.reverse()
    num_stars = 0
    stars_per_rank = 2
    d[0] = 25
    for current_rank in ranks:
        if current_rank % 5 == 0 and current_rank not in [25,5]:
            stars_per_rank += 1
        for _ in xrange(stars_per_rank):
            num_stars += 1
            d[num_stars] = current_rank
    d[num_stars+1] = 0  # Legend
    return d


def play_game(win_rate):
    """
    Returns True if win, False otherwise.
    """
    return random.random() < win_rate


def climb_to_legend(win_rate, start_stars=0, no_streaks_above_rank=5, rank_floors=[25, 20, 15, 10, 5]):
    star_map = build_star_map()
    current_stars = start_stars
    star_rank_floors = [min(k for k, v in star_map.items() if v == floor) for floor in rank_floors]
    no_streaks_above = min(k for k, v in star_map.items() if v == no_streaks_above_rank)
    wins_in_row = 0
    games = 0
    legend = star_map.keys()[-1]
    while current_stars < legend and games < 5000:
        games += 1
        if play_game(win_rate):
            wins_in_row += 1
            if wins_in_row >= 3 and current_stars < no_streaks_above:
                current_stars += 2
            else:
                current_stars += 1
        else:
            wins_in_row = 0
            if current_stars not in star_rank_floors:
                current_stars -= 1
    return games
