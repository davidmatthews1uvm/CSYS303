from collections import Counter
import math
import matplotlib.pyplot as plt
import numpy as np
import shifterator
import time

from book_utils import words_of_book, load_happiness_dict, MOBY_DICK_URL, PRIDE_AND_PREJUDICE_URL, get_twitter_freq_dict

# load word scores
happiness_dict = load_happiness_dict()

# word shift lenses
book_lenses = [(3,7)]
twitter_lenses = [(4,6)]

# Moby Dick
moby_dick_words = words_of_book(MOBY_DICK_URL)
moby_dict_ttl_words = len(moby_dick_words)

moby_dict_part_one = Counter(moby_dick_words[int(0.1*moby_dict_ttl_words): int(0.15*moby_dict_ttl_words)])
moby_dict_part_two = Counter(moby_dick_words[int(0.85*moby_dict_ttl_words): int(0.90*moby_dict_ttl_words)])

shift = shifterator.WeightedAvgShift(moby_dict_part_one, moby_dict_part_two, type2score_1=happiness_dict, stop_lens=book_lenses, reference_value="average")

fig, ax = plt.subplots(figsize=(12,20))
shift.get_shift_graph(ax=ax, detailed=True,
                                system_names=['Moby Dick 10-15%', 'Moby Dick 85-90%'],
                                filename="figs/Assignment_10_MobyDick.pdf", show_plot=False, show_total=True)

# Pride and Prejudice
pride_prejudice_words = words_of_book(PRIDE_AND_PREJUDICE_URL)
pride_prejudice_ttl_words = len(pride_prejudice_words)

pride_prejudice_part_one = Counter(pride_prejudice_words[int(0.68*pride_prejudice_ttl_words): int(0.77*pride_prejudice_ttl_words)])
pride_prejudice_part_two = Counter(pride_prejudice_words[int(0.93*pride_prejudice_ttl_words): int(1.0*pride_prejudice_ttl_words)])

shift = shifterator.WeightedAvgShift(pride_prejudice_part_one, pride_prejudice_part_two, happiness_dict, stop_lens=book_lenses, reference_value="average")

fig, ax = plt.subplots(figsize=(12,20))
shift.get_shift_graph(ax=ax, detailed=True,
                                system_names=[ 'Pride and Prejudice 68-77%', 'Pride and Prejudice 93-100%'],
                                filename="figs/Assignment_10_PridePrejudice.pdf", show_plot=False)


# Twitter COVID 19 
# 2020/03/12 relative to 2020/01/09

twitter_pre_covid = get_twitter_freq_dict(year=2020, month=1, day=9)
twitter_covid = get_twitter_freq_dict(year=2020, month=3, day=12)

twitter_pre_capital_insurrection = get_twitter_freq_dict(year=2020, month=1, day=6)
twitter_capital_insurrection = get_twitter_freq_dict(year=2021, month=1, day=6)

shift = shifterator.WeightedAvgShift(twitter_pre_covid, twitter_covid, happiness_dict, stop_lens=twitter_lenses, reference_value="average")

fig, ax = plt.subplots(figsize=(12,20))
shift.get_shift_graph(ax=ax, detailed=True,
                                system_names=['Pre COVID Twitter\n2020-01-09', 'COVID Twitter\n2020-03-12' ],
                                filename="figs/Assignment_10_COVID_Twitter.pdf", show_plot=False, show_total=True)

shift = shifterator.WeightedAvgShift(twitter_pre_capital_insurrection, twitter_capital_insurrection, happiness_dict, stop_lens=twitter_lenses, reference_value="average")

fig, ax = plt.subplots(figsize=(12,20))
shift.get_shift_graph(ax=ax, detailed=True,
                                system_names=[ 'Pre Capital Insurrection\n2020-01-06', 'Capital Insurrection\n2021-01-06'],
                                filename="figs/Assignment_10_Capital_Insurection_Twitter.pdf", show_plot=False, show_total=True)
