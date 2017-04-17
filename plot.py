#! /usr/bin/env python2
#-*- coding:utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import random
import re


def plot_line_chart(ydata, ylabel, xlabel, title, draw_avg=False,
                                 x_range=None, ymax=None, ymin=None):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)

    t = np.arange(x_range[0], x_range[1], 1) if x_range else np.arange(1, len(ydata)+1, 1)
    s = ydata

    plt.plot(t, s)

    if ymin: plt.gca().set_ylim(bottom = ymin)
    else: plt.gca().set_ylim(bottom=0)

    if ymax: plt.gca().set_ylim(top=ymax)

    avg = sum(ydata)/len(ydata)
    if draw_avg: plt.axhline(avg, ls='--', color='red')

    filename = re.sub(r'[\\/]+', '_', title)
    plt.savefig('%s.png' %filename)
    return '%s.png' %filename


def plot_req_time(times, title='req_time', **kwargs):
    ydata = [sec*1000 for sec in times]

    if 'ymax' in kwargs: kwargs['ymax'] *= 1000
    if 'ymin' in kwargs: kwargs['ymin'] *= 1000

    return plot_line_chart(ydata, 'Tims/ms', 'Count', title, **kwargs)
