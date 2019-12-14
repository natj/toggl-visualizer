
from read_toggl_reports import read_toggl_reports
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
from matplotlib import colorbar

from datetime import datetime
from datetime import timedelta


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
        ]

#own projects
deep_work_labels = [
        'organize/reflect',
        'RadTurb',
        'runko',
        'toggl-visz',
        ]


#collaboration projects
collaboration_work_labels = [
        'corrugation',
        'ML-dynamos',
        'sheets',
        'shocks',
        ]


project_info = {
        #shallow
        'emails'           :{ 'idn':1,  'mode':'shallow'},
        'misc'             :{ 'idn':2,  'mode':'shallow'},
        'meetings'         :{ 'idn':3,  'mode':'shallow'},
        'talks'            :{ 'idn':4,  'mode':'shallow'},
        #deep 
        'organize/reflect' :{ 'idn':5,  'mode':'deep'},
        'RadTurb'          :{ 'idn':6,  'mode':'deep'},
        'runko'            :{ 'idn':7,  'mode':'deep'},
        'toggl-visz'       :{ 'idn':8,  'mode':'deep'},
        #collaborative
        'corrugation'      :{ 'idn':9,  'mode':'coll'},
        'ML-dynamos'       :{ 'idn':10, 'mode':'coll'},
        'sheets'           :{ 'idn':11, 'mode':'coll'},
        'shocks'           :{ 'idn':12, 'mode':'coll'},
        }


def plot_duration_hist(reports):

    projs = {}

    durations = []
    durations_shallow = []
    durations_deep = []
    durations_coll = []

    for r in reports:
        tlen = r['duration']/60.0 #duration in minutes
        durations.append(tlen)

        if not(r['project'] in projs.keys()):
            projs[r['project']] = 1
        else:
            projs[r['project']] += 1


        #deep work
        if r['project'] in deep_work_labels:
            durations_deep.append(tlen)

        #shallow work
        if r['project'] in shallow_work_labels:
            durations_shallow.append(tlen)

        #collaborative work
        if r['project'] in collaboration_work_labels:
            durations_coll.append(tlen)

    print(projs)



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
    print("samples (shallows):", len(durations_shallow))
    print("samples (collaborative):",  len(durations_coll))
    bins = np.linspace(0.0, 100.0, 50)


    #hist, bins = np.histogram(durations, bins=100)
    hist, bins = np.histogram(durations, bins=bins)
    axs[0].plot(bins[:-1], hist, 'k')

    hist2, bins = np.histogram(durations_deep, bins=bins)
    axs[0].plot(bins[:-1], hist2, "r-")

    hist2, bins = np.histogram(durations_shallow, bins=bins)
    axs[0].plot(bins[:-1], hist2, "b-")

    hist3, bins = np.histogram(durations_coll, bins=bins)
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


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def plot_day_hist(reports):

    N = 100
    bins = np.linspace(0.0, 24.0, N)

    hist = np.zeros(N) #all
    hist_deep = np.zeros(N) #deep work
    hist_shallow  = np.zeros(N) #shallow work
    hist_coll = np.zeros(N) #collaborative


    for r in reports:

        tstart = r['start']
        tstop =  r['end']
        t0 = tstart.hour + tstart.minute/60.0
        t1 = tstop.hour + tstop.minute/60.0

        idx = find_nearest(bins, t0)
        while True:
            if bins[idx] < t1:

                #all
                hist[idx] += 1

                #deep work
                if r['project'] in deep_work_labels:
                    hist_deep[idx] += 1

                #shallow work
                if r['project'] in shallow_work_labels:
                    hist_shallow[idx] += 1

                #collaborative
                if r['project'] in collaboration_work_labels:
                    hist_coll[idx] += 1

                idx += 1
            else:
                break


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

    axs[0].plot(bins, hist, 'k')
    axs[0].plot(bins, hist_deep, 'r-')
    axs[0].plot(bins, hist_shallow, 'b-')
    axs[0].plot(bins, hist_coll, 'g-')



    axs[0].set_xlabel('Hour of the day')
    axs[0].set_ylabel('N')
    axs[0].set_xlim((0, 24))

    axs[0].axvline(x=12.0, linestyle='dashed', color='black')



    axleft    = 0.18
    axbottom  = 0.16
    axright   = 0.96
    axtop     = 0.95
    fig.subplots_adjust(left=axleft, bottom=axbottom, right=axright, top=axtop)
    fig.savefig('day.pdf')




def plot_day_heatmap(reports):

    #find first and last day

    #find smallest and largest days
    d1 = datetime.now() - timedelta(days=1000)
    d0 = datetime.now()
    for r in reports:
        day = r['day']

        if day < d0:
            d0 = day
        if day > d1:
            d1 = day

    Ndays = (d1-d0).days + 10
    print("sample days", Ndays)
    print("start:", d0)
    print("end:  ", d1)

    #------------------
    # build heatmap data

    N = 48
    bins = np.linspace(0.0, 24.0, N)

    hist         = np.zeros((N, Ndays)) #all
    hist_deep    = np.zeros((N, Ndays)) #deep work
    hist_shallow = np.zeros((N, Ndays)) #shallow work
    hist_coll    = np.zeros((N, Ndays)) #collaborative


    for r in reports:
        day = r['day']
        tstart = r['start']
        tstop =  r['end']
        t0 = tstart.hour + tstart.minute/60.0
        t1 = tstop.hour + tstop.minute/60.0

        idd = (day - d0).days


        idx = find_nearest(bins, t0)
        while True:
            if bins[idx] < t1:

                #all
                hist[idx, idd] += 1

                #deep work
                if r['project'] in deep_work_labels:
                    hist_deep[idx,idd] += 1

                #shallow work
                if r['project'] in shallow_work_labels:
                    hist_shallow[idx,idd] += 1

                #collaborative
                if r['project'] in collaboration_work_labels:
                    hist_coll[idx,idd] += 1

                idx += 1
            else:
                break

    #----------------------------
    #setup figure
    fig = plt.figure(1, figsize=(7.0, 3.5))
    gs = plt.GridSpec(1, 1)
    gs.update(hspace=0.0)

    axs = []
    axs.append(plt.subplot(gs[0, 0]))

    for ax in axs:
        ax.minorticks_on()
    #----------------------------

    extent = [ 0, Ndays, 0.0, 24.0 ]

    #hist = np.ma.masked_where(hist_deep == 0, hist_deep)
    #hist = np.ma.masked_where(hist_shallow == 0, hist_shallow)

    hist = np.ma.masked_where(hist == 0, hist)
    axs[0].imshow(hist, 
            extent=extent,
            origin='lower',
            cmap='Reds',
            interpolation='nearest',
            aspect='auto',
            vmin = 0,
            vmax = 3,
            )


    #parse mondays
    for idd in range(Ndays):
        day = d0 + timedelta(days=idd)

        #monday
        if day.weekday() == 0:
            axs[0].axvline(idd, linestyle='dotted',alpha=0.15)

        #first day of month
        if day.day == 1:
            axs[0].axvline(idd, linestyle='dashed',alpha=0.2)


    #visualize start & end time of days
    #duration of work 
    #real duration spent working/at rest

    #efficiency measurements:
    # ratio of real to start-to-end time
    # -number of sessions per day
    # -minutes of deep work



    #----------------------------
    axleft    = 0.18
    axbottom  = 0.16
    axright   = 0.96
    axtop     = 0.95
    fig.subplots_adjust(left=axleft, bottom=axbottom, right=axright, top=axtop)
    fig.savefig('day_heatmap.pdf')

    #----------------------------


def plot_timeline(reports):

    #find smallest and largest days
    d1 = datetime.now() - timedelta(days=1000)
    d0 = datetime.now()
    for r in reports:
        day = r['day']

        if day < d0:
            d0 = day
        if day > d1:
            d1 = day

    Ndays = (d1-d0).days + 10

    #------------------
    # build time line data

    N = 24*120 #min resolution
    bins = np.linspace(0.0, 24.0, N)

    hist         = np.zeros((N, Ndays)) #all

    #parse different projects
    for r in reports:
        day = r['day']
        tstart = r['start']
        tstop =  r['end']
        t0 = tstart.hour + tstart.minute/60.0 + tstart.second/3600.0
        t1 = tstop.hour  + tstop.minute/60.0  + tstop.second/3600.0

        idd = (day - d0).days
        idx = find_nearest(bins, t0)
        while True:
            if bins[idx] <= t1:
                col = project_info[r['project']]['idn']
                hist[idx, idd] = col

                idx += 1
            else:
                break


    #parse day start and end
    days = range(Ndays)
    day_starts = np.zeros(Ndays)
    day_stops  = np.zeros(Ndays)
    day_real_len  = np.zeros(Ndays)
    for r in reports:
        day = r['day']
        tstart = r['start']
        tstop =  r['end']
        t0 = tstart.hour + tstart.minute/60.0 + tstart.second/3600.0
        t1 = tstop.hour  + tstop.minute/60.0  + tstop.second/3600.0

        idd = (day - d0).days
        #idx0 = find_nearest(bins, t0)
        #idx1 = find_nearest(bins, t1)

        day_real_len[idd] += r['duration']/3600 #duration in hours

        #check if array is empty
        if day_starts[idd] == 0.0:
            day_starts[idd] = t0
        elif day_starts[idd] > t0:
            day_starts[idd] = t0

        if day_stops[idd] == 0.0:
            day_stops[idd] = t1
        elif day_stops[idd] < t1:
            day_stops[idd] = t1

    #superficial duration
    day_len = day_stops-day_starts


    #----------------------------
    #setup figure
    fig = plt.figure(1, figsize=(7.0, 4.5))
    gs = plt.GridSpec(4, 1)
    gs.update(hspace=0.0)

    axs = []
    axs.append(plt.subplot(gs[0:2, 0]))
    axs.append(plt.subplot(gs[2, 0]))
    axs.append(plt.subplot(gs[3, 0]))

    for ax in axs:
        ax.minorticks_on()
        ax.set_xlim((0, Ndays))

    axs[1].set_ylim((0.0, 20.0))
    axs[2].set_ylim((0.0, 1.0))

    axs[0].set_ylabel('Hour of day')
    axs[1].set_ylabel('Duration (h)')
    axs[2].set_ylabel('Efficiency')


    #----------------------------

    extent = [ 0, Ndays, 0.0, 24.0 ]
    hist = np.ma.masked_where(hist == 0, hist)

    axs[0].imshow(hist, 
            extent=extent,
            origin='lower',
            cmap='Spectral',
            interpolation='nearest',
            aspect='auto',
            vmin = 0,
            vmax = 12,
            )


    #remove zero days
    day_starts = np.ma.masked_where(day_starts == 0, day_starts)
    day_stops  = np.ma.masked_where(day_stops  == 0, day_stops)


    #filter out days with <1hr duration
    day_starts = np.ma.masked_where(day_real_len <= 1.0, day_starts)
    day_stops  = np.ma.masked_where(day_real_len <= 1.0, day_stops)

    axs[0].plot(days, day_starts, color='k', alpha=0.2, linestyle='steps-post')
    axs[0].plot(days, day_stops,  color='k', alpha=0.2, linestyle='steps-post')



    #parse mondays
    for idd in range(Ndays):
        day = d0 + timedelta(days=idd)

        #monday
        if day.weekday() == 0:
            axs[0].axvline(idd, linestyle='dotted',alpha=0.15)

        #first day of month
        if day.day == 1:
            axs[0].axvline(idd, linestyle='dashed',alpha=0.2)


    #visualize start & end time of days
    #duration of work 
    #real duration spent working/at rest

    #efficiency measurements:
    # ratio of real to start-to-end time
    # -number of sessions per day
    # -minutes of deep work

    #real duration done work
    axs[1].plot(days, day_real_len, 'k-', linestyle='steps-post')

    #from start to end duration
    axs[1].plot(days, day_len, 'b-', linestyle='steps-post')
    

    #efficiency
    axs[2].plot(days, day_real_len/day_len, 'k-', linestyle='steps-post')


    #----------------------------
    axleft    = 0.12
    axbottom  = 0.16
    axright   = 0.96
    axtop     = 0.95
    fig.subplots_adjust(left=axleft, bottom=axbottom, right=axright, top=axtop)
    fig.savefig('timeline.pdf')


    #----------------------------


if __name__ == "__main__":

    plt.rc("font", family="sans-serif")
    # plt.rc('text',  usetex=True)
    plt.rc("xtick", labelsize=8)
    plt.rc("ytick", labelsize=8)
    plt.rc("axes", labelsize=8)


    #read
    reports = read_toggl_reports()

    #visualize
    #plot_duration_hist(reports)
    #plot_day_hist(reports)
    #plot_day_heatmap(reports)
    plot_timeline(reports)




