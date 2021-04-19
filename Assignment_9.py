import urllib.request
import hashlib
import re

import numpy as np
import tqdm
import matplotlib.pyplot as plt
import taichi as ti
import time

ti.init(arch=ti.gpu)



PRIDE_AND_PREJUDICE_URL = "https://www.gutenberg.org/ebooks/42671.txt.utf-8"
MOBY_DICK_URL = "https://www.gutenberg.org/files/2701/2701-0.txt"

words_file_str = "../data/data_labMT_labMTwords-english-covid.csv"
scores_file_str = "../data/data_labMT_labMTscores-english-covid.csv"


def words_of_book(url, force_lower_case=False, debug=False):
    """Download the given book from Project Gutenberg. Return a list of
    words. Punctuation has been removed. Upper-case letters have been
    replaced with lower-case if force_lower_case is True.
    """

    cache_file = "{}.txt".format("../data/{}".format(hashlib.sha1(url.encode("utf-8")).hexdigest()))
    # try to read the book from a file.
    try:
        with open(cache_file, "r") as f:
            all_chars =  f.read()
    except:
        # else downlaoad book.

        req = urllib.request.urlopen(url)
        charset = req.headers.get_content_charset()
        if charset is None:
            charset = 'utf-8'
        all_chars = req.read().decode(charset)
        with open(cache_file, "w") as f:
            f.write(all_chars)


    r = re.search(r"(\*+)?(.+)?START OF THE PROJECT GUTENBERG EBOOK(.+)?(\*+)?", all_chars)
    book_begin_idx = r.end()

    pride_prejudice_search = "_Engraved for No. 72 of La Belle Assemblee 1^{st} July 1815_]"
    second_book_begin_idx = all_chars.find(pride_prejudice_search)
    if second_book_begin_idx != -1:
        book_begin_idx = max(book_begin_idx, second_book_begin_idx + len(pride_prejudice_search))

    r = re.search(r"(\*+)?(.+)?END OF THE PROJECT GUTENBERG EBOOK(.+)?(\*+)?", all_chars)
    book_end_idx = r.start()

    r = re.search(r"(\s+)(\*(\s+))+(\s+)?Transcriber's note:", all_chars)
    if r is not None:
        book_end_idx = min(book_end_idx, r.start())
    
    book_chars = all_chars[book_begin_idx:book_end_idx]
    book = re.sub(r'[^\w\s]', '', book_chars) # remove punctuation
    book = re.sub(r'\s+', ' ', book) # remove extra white space
    if force_lower_case:
        book = book.lower()
    book = book.split()
    if debug:
        print("BEGIN", book[:100], "END", book[-100:])
    return book

def load_happiness_dict():
    with open(words_file_str, "r") as f:
        words = [word.strip() for word in f.readlines()]

    with open(scores_file_str, "r") as f:
        scores = [float(score.strip()) for score in f.readlines()]

    return dict(zip(words, scores))

@ti.func
def isnan(x):
    return not (x < 0 or 0 < x or x == 0)

@ti.kernel
def clear():
    for i in book_happiness_avg_ti:
        book_happiness_avg_ti[i] = 0
@ti.kernel
def compute_rolling_avg(N: ti.i32, book_length: ti.i32, lens_min: ti.f32, lens_max: ti.f32):
    for idx in range(book_length):
        if idx < book_length - N:
            summed_score = 0.0
            words_in_filter = 0
            for jdx in range(N):
                word_value = book_happiness_ti[idx+jdx]
                is_nan = isnan(word_value)
                if not is_nan and (word_value <= lens_min or word_value >= lens_max):
                    summed_score += word_value
                    words_in_filter += 1
            book_happiness_avg_ti[idx] = summed_score/words_in_filter



moby_dick_book = words_of_book(MOBY_DICK_URL, force_lower_case=True)
pride_prejucide_book = words_of_book(PRIDE_AND_PREJUDICE_URL, force_lower_case=True)
happiness_dict = load_happiness_dict()

max_words = max(len(moby_dick_book), len(pride_prejucide_book))
book_happiness = np.zeros(max_words, dtype=np.float32)

book_happiness_ti = ti.field(ti.f32, (max_words))
book_happiness_avg_ti = ti.field(ti.f32, (max_words))

for book, name in [(moby_dick_book, "Moby Dick"), (pride_prejucide_book, "Pride and Prejudice")]:
    book_happiness[:] = 0
    curr_book_len = len(book)
    
    for idx in range(curr_book_len):
        word = book[idx]
        book_happiness[idx] = happiness_dict[word] if word in happiness_dict else np.nan
    

    book_happiness_ti.from_numpy(book_happiness)
    gfig, gax = plt.subplots()
    for N in [1000, 3200, 10000]:
        tmp_fig, tmp_ax = plt.subplots()

        clear()
        t0 = time.time()
        compute_rolling_avg(N, curr_book_len, 3, 7)
        t1 = time.time()
        print("Window size N: {} for {} took: {:.3f}".format(N, name, t1-t0))
        book_happiness_avg = book_happiness_avg_ti.to_numpy()
        
        # plot on the global figure
        gax.plot(np.arange(N//2, curr_book_len - N//2)*1/curr_book_len, book_happiness_avg[:curr_book_len-N], label=f"Window of {N} words", alpha=0.7)
        
        # plot on the tmp figure
        tmp_ax.plot(np.arange(N//2, curr_book_len - N//2)*1/curr_book_len, book_happiness_avg[:curr_book_len-N], label=f"Window of {N} words")
        tmp_ax.legend()
        tmp_ax.set_title("Happiness Timeseries of {}".format(name))
        tmp_ax.set_xlabel("Fraction of Book")
        tmp_ax.set_ylabel("Happiness Score")
        tmp_fig.savefig("figs/Assignment_9_{}_Window_{}.pdf".format(name.replace(" ","_"), N))

    gax.legend()
    gax.set_title("Happiness Timeseries of {}".format(name))
    gax.set_xlabel("Fraction of Book")
    gax.set_ylabel("Happiness Score")
    gfig.savefig("figs/Assignment_9_{}.pdf".format(name.replace(" ", "_")))
    gfig.show()
