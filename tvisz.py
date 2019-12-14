
from read_toggl_reports import read_toggl_reports
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
from matplotlib import colorbar

#global figcounter = 0
#class Fig:
#
#    def __init__(self, width, height):
#
#        self.fig = plt.figure(figcounter, 
#                figsize=(width, height))
#        global figcounter += 1
#        


#shallow/shadow work
shallow_work_labels = [
        'emails',
        'misc',
        'meetings',
        'talks',
        'organize/reflect',
        ]

#own projects
deep_work_labels = [
        'RadTurb',
        'runko',
        'togg-visz',
        ]


#collaboration projects
collaboration_work_labels = [
        'corrugation',
        'ML-dynamos',
        'sheets',
        'shocks',
        ]


def plot_duration_hist(reports):

    projs = {}

    durations = []
    for r in reports:
        tlen = r['duration']/60.0 #duration in minutes
        durations.append(tlen)

        if not(r['project'] in projs.keys()):
            projs[r['project']] = 1
        else:
            projs[r['project']] += 1

    print(projs)



    #same for shallow work filtered out
    durations_deep = []
    for r in reports:
        if r['project'] in shallow_work_labels:
            continue

        tlen = r['duration']/60.0 #duration in minutes
        durations_deep.append(tlen)


    #own projects only
    durations_own = []
    for r in reports:
        if r['project'] in deep_work_labels:
            tlen = r['duration']/60.0 #duration in minutes
            durations_own.append(tlen)

    #----------------------------
    #setup figure
    fig = plt.figure(1, figsize=(3.487, 2.5))
    gs = plt.GridSpec(1, 1)
    gs.update(hspace=0.3)

    axs = []
    axs.append(plt.subplot(gs[0, 0]))

    for ax in axs:
        ax.minorticks_on()
    #----------------------------

    print("samples:", len(durations))
    print("samples (deep):", len(durations_deep))
    print("samples (own):",  len(durations_own))
    bins = np.linspace(0.0, 100.0, 50)


    #hist, bins = np.histogram(durations, bins=100)
    hist, bins = np.histogram(durations, bins=bins)
    axs[0].plot(bins[:-1], hist)

    hist2, bins = np.histogram(durations_deep, bins=bins)
    axs[0].plot(bins[:-1], hist2, "r-")

    hist3, bins = np.histogram(durations_own, bins=bins)
    axs[0].plot(bins[:-1], hist3, "g-")



    axs[0].set_xlabel('Duration (mins)')
    axs[0].set_ylabel('N')

    axs[0].set_yscale('log')

    axs[0].set_xlim((-5, 100.0))

    axleft    = 0.18
    axbottom  = 0.16
    axright   = 0.96
    axtop     = 0.95
    fig.subplots_adjust(left=axleft, bottom=axbottom, right=axright, top=axtop)
    fig.savefig('durations.pdf')



if __name__ == "__main__":

    plt.rc("font", family="sans-serif")
    # plt.rc('text',  usetex=True)
    plt.rc("xtick", labelsize=8)
    plt.rc("ytick", labelsize=8)
    plt.rc("axes", labelsize=8)


    reports = read_toggl_reports()


    plot_duration_hist(reports)





