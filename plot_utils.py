import numpy as np
import matplotlib.pyplot as plt
import pathlib

def plot_ZIPF_unsorted(samples, title="", xlabel="", ylabel="", save=None):
    Y = np.array(sorted(samples, reverse=True))
    return plt_ZIPF(Y, **kwargs)

def plot_ZIPF(Y, title="", xlabel="", ylabel="", save=None):
    assert isinstance(Y, np.ndarray)
    N = Y.shape[0]
    X = np.arange(1, N+1)
    fig, ax = plt.subplots(1, figsize=(8,8))
    ax.scatter(X, Y, c="k")
    
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(xlabel, fontsize=18)
    ax.set_ylabel(ylabel, fontsize=18)
    ax.set_title(title, fontsize=24)

    if save is not None:
        if not isinstance(save, list):
            save = [save]
        for fname in save:
            save_folder = pathlib.Path(fname).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(fname)

    return fig, ax