"""
Hearthstone is a popular online collectible card game (CCG). One of its play modes, Ranked, features
a monthly progression where users earn "stars" and advance up a ladder of "ranks," usually striving
to reach the ultimate rank, Legend. Winning a game nets you a star, while losing a game usually
results in losing a star. Winning several games in a row generally merits an extra star.

This program simulates how many games a player needs to play in order to reach Legend, given a
particular average win rate. Other configuration variables can be specified as well, although the
defaults match Hearthstone's standard implementation.
"""
from collections import OrderedDict
import math
import random
import statistics


def build_star_map():
    """
    The star map is a dictionary that translates how many total stars you have into a rank.
    """
    # total number of stars: rank
    d = OrderedDict()
    ranks = range(1, 26)  # The range [1, 25]; i.e. the numbers 1 to 25, inclusive.
    ranks.reverse()
    num_stars = 0
    stars_per_rank = 2
    d[0] = 25
    for current_rank in ranks:
        # At rank 20, 15, and 10, the number of stars per rank increases by 1.
        if current_rank in [20, 15, 10]:
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


DEFAULT_RANK_FLOORS = (25, 20, 15, 10, 5)


def climb_to_legend(
        win_rate,
        start_stars=0,
        no_streaks_above_rank=5,
        rank_floors=DEFAULT_RANK_FLOORS
):
    """
    Use a random number generator to simulate how many games are needed to reach Legend.

    :param win_rate: How likely the player is to win an individual game.
    :param start_stars: How many stars the player begins with.
    :param no_streaks_above_rank: The rank at which players no longer receive an extra star for a
    win streak.
    :param rank_floors: Once a player passes one of these ranks, they cannot fall back below it,
    even with multiple losses.
    :return: The number of simulated games played.
    :rtype: int
    """
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


def simulate(n, *args, **kwargs):
    average = statistics.mean(climb_to_legend(*args, **kwargs) for _ in xrange(n))
    return average


if __name__ == "__main__":
    print("Welcome to the Hearthstone Legend Climb Simulator!")
    while True:
        win_rate = input("What is your average win rate? (Example: 0.5) ")
        avg = int(math.ceil(simulate(100, win_rate)))
        print("With a win rate of {}, it will take an average of {} games to reach Legend.".format(
            win_rate, avg
        ))
