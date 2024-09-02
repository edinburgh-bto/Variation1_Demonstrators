import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm, t
from numpy.random import normal
from IPython.display import display
from matplotlib.patches import ConnectionPatch
from ipywidgets import FloatSlider, Button, Layout, widgets
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


class slider_props:
    def __init__(self, minv, maxv, step, init):
        """set a slider's properties"""
        self.minv = minv
        self.maxv = maxv
        self.step = step
        self.init = init


class Sample_size:
    def __init__(self):
        def pars_key(x):
            return round(10*x)

        # declare slider for sample size
        s_prop = slider_props(10, 228, 10, 10)
        slider = FloatSlider(min=s_prop.minv, max=s_prop.maxv, step=s_prop.step, value=s_prop.init,
                             readout_format='d', layout={'width': '60%'},
                             style={'description_width': 'initial'}, description='Sample size $n$:')

        display(slider)

        def update_slider(slider_value):
            """update distibution on slider change"""
            for a in h[pars_key(slider_value.old)]:
                a.set_visible(False)
            for a in h[pars_key(slider_value.new)]:
                a.set_visible(True)
            ax.set_title(
                f'Distribution of masses of {slider_value.new:.0f} Alaskan sockeye salmon')

        # initialise interactive observation of slider
        slider.observe(update_slider, 'value')

        # Initialise figure
        fig = plt.figure()
        ax = fig.add_subplot()

        # Add traces and store in a dictionary keyed to integerised slider values
        # All traces are initially invisible
        salmon = pd.read_csv('Datasets/alaskan salmon.csv')
        h = {}
        for n in range(s_prop.minv, s_prop.maxv+s_prop.step, s_prop.step):
            # calculate a histogram of the first n salmon and return the list of Rectangles that make up this histogram
            rects = ax.hist(salmon.iloc[:n], bins=np.arange(1, 4, 0.2), color='C0')[2].patches
            # set their status to invisible
            for r in rects:
                r.set_visible(False)
            h[pars_key(n)] = rects

        # Show initial trace
        for a in h[pars_key(s_prop.init)]:
            a.set_visible(True)
        ax.set_title(f'Distribution of masses of {s_prop.init:d} Alaskan sockeye salmon')

        # Set up figure layout
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        ax.set_xlabel('Mass (kg)')
        ax.set_ylabel('Number of salmon')
        plt.ion()


class Normal_rule:
    def __init__(self):
        def pars_key(x):
            """return key of 10x and rounded to nearest int"""
            return round(10*x)

        # declare slider for number st. dev. from mean
        s_prop = slider_props(0.5, 3.0, 0.1, 1.0)
        slider = FloatSlider(min=s_prop.minv, max=s_prop.maxv, step=s_prop.step, value=s_prop.init,
                             readout_format='.1f', layout={'width': '60%'},
                             style={'description_width': 'initial'},
                             description='Number of standard deviations from the mean:')

        display(slider)

        def update_slider(slider_value):
            """update distibution on slider change"""
            for a in h[pars_key(slider_value.old)]:
                a.set_visible(False)
            for a in h[pars_key(slider_value.new)]:
                a.set_visible(True)

        # initialise interactive observation of slider
        slider.observe(update_slider, 'value')

        # Initialise figure
        fig = plt.figure()
        ax = fig.add_subplot()

        # Add traces and store in a dictionary keyed to integerised slider values
        # All traces are initially invisible
        h = {}
        for nsd in np.arange(s_prop.minv, s_prop.maxv+s_prop.step, s_prop.step):
            x1 = np.linspace(-3.5, -nsd, 50)
            x2 = np.linspace(-nsd, nsd, 50)
            x3 = np.linspace(nsd, 3.5, 50)
            a = norm.cdf(nsd)-norm.cdf(-nsd)
            b = (1-a)/2

            # list of all elements to display in this trace
            h[pars_key(nsd)] = []

            # the histograms
            h[pars_key(nsd)].append(ax.fill_between(
                x1, 0, norm.pdf(x1), color='C0', visible=False))
            h[pars_key(nsd)].append(ax.fill_between(
                x2, 0, norm.pdf(x2), color='C1', visible=False))
            h[pars_key(nsd)].append(ax.fill_between(
                x3, 0, norm.pdf(x3), color='C0', visible=False))

            # the annotations
            h[pars_key(nsd)].append(ax.annotate(
                f'{b:.1%}', xy=(-(3.5+nsd)/2, 0.01), xytext=(-2.5, 0.15), arrowprops={}, ha='center', size=12, visible=False))
            h[pars_key(nsd)].append(ax.annotate(f'{b:.1%}', xy=(
                (3.5+nsd)/2, 0.01), xytext=(2.5, 0.15), arrowprops={}, ha='center', size=12, visible=False))
            h[pars_key(nsd)].append(ax.text(
                0, 0.05, f'{a:.1%} of the\ndata lie\nwithin this\norange\nregion', color='w', ha='center', size=12, visible=False))
            h[pars_key(nsd)].append(ax.text(
                0, 0.42, f'{b:.1%} + {a:.1%} + {b:.1%} = 100%', ha='center', visible=False))

        # Show initial trace
        for a in h[pars_key(s_prop.init)]:
            a.set_visible(True)

        # Set up figure layout
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_xticks(ticks=range(-3, 4), labels=[ f'$\\bar{{x}}{i:+.2g}s$' if i else '$\\bar{{x}}$' for i in range(-3, 4)])
        plt.ion()


class Normal_distribution:
    def __init__(self):
        def pars_key(m, s):
            """return key tuple of m and s x 10 and rounded to nearest int"""
            return round(10*m), round(10*s)

        # declare sliders for mean and st. dev.
        mp = slider_props(155, 175, 0.5, 164)
        sp = slider_props(2, 20, 0.5, 6.5)
        slider_mean = FloatSlider(min=mp.minv, max=mp.maxv, step=mp.step, value=mp.init,
                                  readout_format='.1f', layout={'width': '60%'}, style={'description_width': 'initial'}, description='mean height (cm):')
        slider_sd = FloatSlider(min=sp.minv, max=sp.maxv, step=sp.step, value=sp.init,
                                readout_format='.1f', layout={'width': '60%'}, style={'description_width': 'initial'}, description='st. dev. height (cm):')

        # display sliders
        display(slider_mean)
        display(slider_sd)

        def update_mean(mean):
            """update distibution mean on slider change"""
            h[pars_key(mean.old, slider_sd.value)].set_visible(False)
            h[pars_key(mean.new, slider_sd.value)].set_visible(True)

        def update_sd(sd):
            """update distibution st dev on slider change"""
            h[pars_key(slider_mean.value, sd.old)].set_visible(False)
            h[pars_key(slider_mean.value, sd.new)].set_visible(True)

        # initialise interactive observation of sliders
        slider_mean.observe(update_mean, 'value')
        slider_sd.observe(update_sd, 'value')

        # Initialise figure
        fig = plt.figure()
        ax = fig.add_subplot()

        # Add traces and store in a dictionary keyed to integerised slider values
        # All traces are initially invisible
        h = {}
        for mean in np.arange(mp.minv, mp.maxv+mp.step, mp.step):
            for sd in np.arange(sp.minv, sp.maxv+sp.step, sp.step):
                x = np.linspace(mean-3*sd, mean+3*sd, 50)
                y = norm.pdf(x, mean, sd)
                h[pars_key(mean, sd)] = ax.fill_between(x, 0, y, color='C0', visible=False)

        # Show initial trace
        h[pars_key(mp.init, sp.init)].set_visible(True)

        # Set up figure layout
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_xlabel('Height (cm)')
        plt.ion()


class t_distribution:
    def __init__(self):
        def pars_key(x):
            """return key of 10x and rounded to nearest int"""
            return round(10*x)

        # declare slider for number st. dev. from mean
        s_prop = slider_props(1, 17, 1, 1)
        slider = FloatSlider(min=s_prop.minv, max=s_prop.maxv, step=s_prop.step, value=s_prop.init,
                             readout_format='.0f', description='ν:')

        display(slider)

        def update_slider(slider_value):
            """update distibution on slider change"""
            for lines in h[pars_key(slider_value.old)]:
                for line in lines:
                    line.set_visible(False)
            for lines in h[pars_key(slider_value.new)]:
                for line in lines:
                    line.set_visible(True)

        # initialise interactive observation of slider
        slider.observe(update_slider, 'value')

        # Initialise figure
        fig = plt.figure()
        ax = fig.add_subplot()

        # Add traces and store in a dictionary keyed to integerised slider values
        # All traces are initially invisible
        h = {}
        for nu in np.arange(s_prop.minv, s_prop.maxv+s_prop.step, s_prop.step):
            x = np.arange(-5, 5, 0.1)

            # list of all elements to display in this trace
            h[pars_key(nu)] = []

            if nu == s_prop.minv:
                legend1 = 'Normal distribution $\mu=0$, $\sigma=1$'
                legend2 = 't-distribution'
            else:
                legend1 = ''
                legend2 = ''
            # the histograms
            h[pars_key(nu)].append(ax.plot(x, norm.pdf(x), color='C1', label=legend1, visible=False))
            h[pars_key(nu)].append(ax.plot(x, t.pdf(x, nu), color='C0', label=legend2, visible=False))

        # Show initial trace
        for lines in h[pars_key(s_prop.init)]:
            for line in lines:
                line.set_visible(True)

        # Set up figure layout
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[:2], labels[:2])
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_title('Comparison of $t$ and Normal distributions')
        ax.legend(bbox_to_anchor=(0.55, 1.0))
        plt.ion()
   
        
class Sampling:
    def getImage(self, image, zoom=1):
        return OffsetImage(image, zoom=zoom)
    
    def generate_population(self):
        """generate the data and image for the finch population
            do this only once so that the pop doesn't change"""

        fig, ax = plt.subplots()
        n = 30
        x, y = [], []
        for xx in np.linspace(-1, 1, n):
            for yy in np.linspace(-1, 1, n):
                if xx**2 + yy**2 < 1:
                    x.append(xx+normal(0, 0.02))
                    y.append(yy+normal(0, 0.02))

        beak = plt.imread('Datasets/finch_clipart.png')

        ax.set_aspect('equal')
        sizes = normal(0.05, 0.01, len(x))
        for x0, y0, zoom in zip(x, y, sizes):
            ab = AnnotationBbox(self.getImage(beak, zoom), (x0, y0), frameon=False, clip_on=False)
            ax.add_artist(ab)

        ax.scatter(x, y, marker='')
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.savefig('Datasets/finch_1976_pop.png', bbox_inches='tight')
        pd.DataFrame({'x':x, 'y':y, 's':sizes}).to_csv('Datasets/finch_1976_pop.csv', index=False)
        
    def __init__(self):
        button1 = Button(description="Next slide", button_style='info', tooltip='Click me', layout=Layout(width='auto'))
        display(button1)

        def new_sample(mu, sigma, n):
            beak_sample = normal(mu, sigma, n)
            xbar = beak_sample.mean()
            s = beak_sample.std()
            return beak_sample, xbar, s
                
        def update_button1(_):
            self.slide_no += 1
            if self.slide_no == 2:
                pop_dist(axs)
            elif self.slide_no == 3:
                sample(axs, pop_data, n)
            elif self.slide_no == 4:
                sample_dist(axs, self.xbar, self.s, self.beak_sample)
            elif self.slide_no == 5:
                estimate(axs, self.xbar, self.s, mu, sigma)
                button1.description = 'Create a new sample'
            else:
                self.beak_sample, self.xbar, self.s = new_sample(mu, sigma, n)
                sample(axs, pop_data, n)
                sample_dist(axs, self.xbar, self.s, self.beak_sample)
                estimate(axs, self.xbar, self.s, mu, sigma)
                    
        button1.on_click(update_button1)

        def beak_pop(axs):
            """Population of beaks"""
            axs['b'].imshow(plt.imread('Datasets/finch_1976_pop.png'))
            axs['a'].annotate(text=
"""A large population of
finches with variable
beak sizes""",
                va='top', ha='center', fontsize=14,
                bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec='none'),
                xytext=(0.5, 0.9), xy=(0.5, -1), xycoords='axes fraction', 
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                fc=(1.0, 0.7, 0.7), ec='none', shrinkA=0)
            )

        def pop_dist(axs):
            """Population distribution"""
            ax = axs['h']
            ax.annotate(text=
"""The population of beak sizes has an
unknown mean $\mu$. Inferential statistics
estimates the mean and its precision
using a single random sample.""",
                va='center', ha='center', fontsize=14, color='w',
                bbox=dict(boxstyle="round", fc='C0', ec='none'),
                xytext=(0.5, -0.1), xy=(0.5, 2), xycoords='axes fraction', 
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                fc='C0', ec='none', shrinkA=0)
            )            

        def sample(axs, pop_data, n):
            ax_pop = axs['b']
            ax_sam = axs['c']
            ax_sam.cla()
            ax_sam.axis('off')

            x = 0.5*np.ones(n)
            y = np.linspace(-1, 1, n)
            beak = plt.imread('Datasets/finch_clipart.png')

            # Select indicies between 0 and the number of birds in the population
            idxs = np.random.choice(list(range(len(pop_data))), size=n, replace=False)
            # Get the coords and size of the birds at these indicies
            s = pop_data.iloc[idxs]
            # Sort in descending y-coord so that arrows do not overlap
            ss = s.sort_values('y', ascending=False).reset_index()
            for y0, idx in zip(y, ss.index):
                beak_data = ss.loc[idx]
                ab = AnnotationBbox(
                    self.getImage(beak, beak_data.s), (0.5, y0), frameon=False)
                ax_sam.add_artist(ab)
                # ax_sam.text(0.505, y0, f'{(beak_data.s-0.05)/0.01+9.5:.2f} mm', va='center', fontsize=6)
                # scale between image coords and position of beak coords
                m = -1/(0.5 - 25/400)
                c = -0.5*m
                con = ConnectionPatch(
                    xyA=((beak_data.x-c)/m, (beak_data.y-c)/m), xyB=(0.497, y0),
                    coordsA='axes fraction', coordsB='data',
                    axesA=ax_pop, axesB=ax_sam,
                    arrowstyle="->", shrinkB=0)
                con.set(color='orange')
                ax_sam.add_artist(con)

            ax_sam.scatter(x, y, marker='')
            ax = axs['e']
            ax.annotate(text=
"""Researchers take
a single random
sample of size $n$
from the population""",
                va='top', ha='center', fontsize=14,
                bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec='none'),
                xytext=(0.5, 0.9), xy=(0.5, -1.3), xycoords='axes fraction', 
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                fc=(1.0, 0.7, 0.7), ec='none', shrinkA=0)
            )            

        def sample_dist(axs, xbar, s, sample):
            ax = axs['d']
            ax.axis('on')
            ax.cla()

            sns.histplot(sample, stat='proportion', ax=ax)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis='x')
            ax.tick_params(axis='y')
            ax.set_xlabel('Beak depth (mm)')
            ax.set_ylabel('Proportion')
            ax.text(0.1, 1, f'$\\bar{{x}} = {xbar:.2f}\,\mathrm{{mm}}$\n$s = {s:.2f}\,\mathrm{{mm}}$', 
                    fontsize=14, transform=ax.transAxes)
            ax = axs['f']
            ax.annotate(text=
"""The sample is visualised
in a histogram and the
sample mean $\\bar{x}$, and
sample standard deviation
$s$, are calculated""",
                va='top', ha='center', fontsize=14,
                bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec='none'),
                xytext=(0.5, 0.9), xy=(0.5, -1.3), xycoords='axes fraction', 
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                fc=(1.0, 0.7, 0.7), ec='none', shrinkA=0)
            )
            return xbar, s
                
        def estimate(axs, xbar, s, mu, sigma):
            ax = axs['i']
            ax.annotate(text=f'$\\bar{{x}}$, $s$ and $n$ are used to\nestimate the population mean:\n$\\widehat{{\\mu}}$ = {xbar:.2f} $\\pm$ {s/np.sqrt(n):.2f}',
                va='center', ha='center', fontsize=14, color='w',
                bbox=dict(boxstyle="round", fc='C2', ec='none'),
                xytext=(1, -0.1), xy=(-0.5, 2), xycoords='axes fraction', 
                arrowprops=None
            )

        mosaic = \
            '''
            .a.ef
            bbb..
            bbbcd
            bbb..
            .h.i.
            '''
        gs_kw = dict(width_ratios=[0.25, 1, 0.25, 1, 1], height_ratios=[0.25, 0.5, 1, 0.5, 0.25])
        fig, axs = plt.subplot_mosaic(mosaic, gridspec_kw=gs_kw, figsize=(9.4, 7))
        plt.subplots_adjust(hspace=0, wspace=0, left=0.05, right=0.99, bottom=0.1, top=1)
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        plt.ion()

        [ax.axis('off') for ax in axs.values()]

        mu = 9.5
        sigma = 1
        n = 20
        self.slide_no = 1
        self.beak_sample, self.xbar, self.s = new_sample(mu, sigma, n)
        pop_data = pd.read_csv('Datasets/finch_1976_pop.csv')

        # run this once to generate population
        # self.generate_population()
        # exit()
        
        beak_pop(axs)


class Distribution_of_sample_mean:
    def __init__(self):
        def pars_key(x):
            return round(10*x)

        # declare slider for sample size
        s_prop = slider_props(5, 150, 5, 5)
        slider = FloatSlider(min=s_prop.minv, max=s_prop.maxv, step=s_prop.step, value=s_prop.init,
                             readout_format='d', style={'description_width': 'initial'},
                             description='Sample size $n$:', tooltip='drag me')

        display(slider)

        def update_slider(slider_value):
            """update distibution on slider change"""
            for a in h[pars_key(slider_value.old)]:
                a.set_visible(False)
            for a in h[pars_key(slider_value.new)]:
                a.set_visible(True)
            axs[0].set_title(f'Sampling distribution of sample means\nof sample size $n$ = {slider_value.new:.0f} finches')

        # initialise interactive observation of slider
        slider.observe(update_slider, 'value')

        # Initialise figure
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
        # ax = fig.add_subplot()

        # Add traces and store in a dictionary keyed to integerised slider values
        # All traces are initially invisible
        mu = 9.5
        sigma = 1
        n_samp = 100000
        h = {}
        for n in range(s_prop.minv, s_prop.maxv+s_prop.step, s_prop.step):
            ax = axs[0]
            sem = sigma/np.sqrt(n)
            means = normal(mu, sem, n_samp)
            rects = ax.hist(means, bins=np.linspace(mu-4*sem, mu+4*sem, 30), color='C0', alpha=0.5)[2].patches
            # set their status to invisible
            for r in rects:
                r.set_visible(False)
            h[pars_key(n)] = rects

            dx = 8*sem/30
            y = (1 - np.exp(-1)) * n_samp * ( norm.cdf(mu+dx/2, mu, sem) - norm.cdf(mu-dx/2, mu, sem) )
            a = ax.annotate(text='', xy=(mu, y), xytext=(mu+sem, y), visible=False, 
                            arrowprops=dict(arrowstyle='<|-', mutation_scale=10, color='C2'))
            a.set_visible(False)
            h[pars_key(n)].append(a)
            a = ax.text(0.05, 0.6, f'SEM = {sem:.3f} mm', color='C2', transform=ax.transAxes, visible=False)
            h[pars_key(n)].append(a)
            a = ax.axvline(mu, color='C2')
            h[pars_key(n)].append(a)

            ax = axs[1]
            x = range(s_prop.minv, n+s_prop.step, s_prop.step)
            y = sigma/np.sqrt(x)
            h[pars_key(n)].append(ax.scatter(x, y, marker='.', color='C2', visible=False))

        # Show initial trace
        for a in h[pars_key(s_prop.init)]:
            a.set_visible(True)
        axs[0].set_title(f'Sampling distribution of sample means\nof sample size $n$ = {s_prop.init:.0f} finches')
        axs[1].set_title(f'Standard error (SEM) gets smaller\nas sample size increases')

        # Set up figure layout
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        ax = axs[0]
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel('Sample mean beak depth (mm)')
        ax.set_yticks([])
        ax.set_ylabel('Proportion')
        ax = axs[1]
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel('Sample size $n$')
        ax.set_ylabel('Standard error of the mean (mm)')
        ax.set_ylim(0, 0.5)
        plt.ion()


class Null_hypothesis:
    def getImage(self, image, zoom=1):
        return OffsetImage(image, zoom=zoom)
    
    def generate_population(self):
        """generate the data and image for the 1978 finch population
            do this only once so that the pop doesn't change"""

        fig, ax = plt.subplots()
        n = 30
        x, y = [], []
        for xx in np.linspace(-1, 1, n):
            for yy in np.linspace(-1, 1, n):
                if xx**2 + yy**2 < 1:
                    x.append(xx+normal(0, 0.02))
                    y.append(yy+normal(0, 0.02))

        beak = plt.imread('Datasets/finch_clipart.png')

        ax.set_aspect('equal')
        sizes = normal(0.05, 0.01, len(x))
        for x0, y0, zoom in zip(x, y, sizes):
            ab = AnnotationBbox(self.getImage(beak, zoom), (x0, y0), frameon=False, clip_on=False)
            ax.add_artist(ab)

        ax.scatter(x, y, marker='')
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.savefig('Datasets/finch_1978_pop.png', bbox_inches='tight')
        pd.DataFrame({'x':x, 'y':y, 's':sizes}).to_csv('Datasets/finch_1978_pop.csv', index=False)
        
    def __init__(self):
        # button1 = Button(description="Sample populations", button_style='info', tooltip='Click me', layout=Layout(width='auto'))
        # display(button1)

        def new_samples(mu, sigma, n):
            beak_samples = normal(mu, sigma, (n, 2))
            xbars = beak_samples.mean(axis=0)
            return beak_samples, xbars, xbars[1] - xbars[0]

        play = widgets.Play(
            value=1,
            min=1,
            max=1000,
            step=1,
            interval=200,
            description="Press play",
            disabled=False
        )
        slider = widgets.IntSlider()
        widgets.jslink((play, 'value'), (slider, 'value'))
        display(widgets.HBox([play, slider]))

        def update_slider(_):
            """update distibution on slider change"""
            self.beak_samples, self.xbars, d = new_samples(mu, sigma, n)
            d_values.append(d)

            sample(axs, pop_1976_data, pop_1978_data, self.xbars)
            d_statistic(axs, self.xbars, d)
            null_dist(axs, d_values)


        # initialise interactive observation of slider
        slider.observe(update_slider, 'value')
          
        # def update_button1(_):
        #     self.slide_no += 1
        #     if self.slide_no == 2:
        #         sample(axs, pop_1076_data, n)
        #         sample(axs, pop_1078_data, n)
        #     elif self.slide_no == 3:
        #         sample(axs, pop_data, n)
        #     elif self.slide_no == 4:
        #         sample_dist(axs, self.xbar, self.s, self.beak_sample)
        #     elif self.slide_no == 5:
        #         estimate(axs, self.xbar, self.s, mu, sigma)
        #         button1.description = 'Create a new sample'
        #     else:
        #         self.beak_sample, self.xbar, self.s = new_sample(mu, sigma, n)
        #         sample(axs, pop_data, n)
        #         sample_dist(axs, self.xbar, self.s, self.beak_sample)
        #         estimate(axs, self.xbar, self.s, mu, sigma)
                    
        # button1.on_click(update_button1)

        def beak_pop(axs):
            """Population of beaks"""
            axs['a'].imshow(plt.imread('Datasets/finch_1976_pop.png'))
            axs['b'].imshow(plt.imread('Datasets/finch_1978_pop.png'))
            axs['g'].annotate(text=
"""A large population of
1976 finches with variable
beak sizes""",
                va='top', ha='center', fontsize=14,
                bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec='none'),
                xytext=(0.5, 0.9), xy=(0.5, -0.1), xycoords='axes fraction', 
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                fc=(1.0, 0.7, 0.7), ec='none', shrinkA=0)
            )
            axs['h'].annotate(text=
"""A large population of
1978 finches with variable
beak sizes""",
                va='top', ha='center', fontsize=14,
                bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec='none'),
                xytext=(0.5, 0.9), xy=(0.5, -0.1), xycoords='axes fraction', 
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                fc=(1.0, 0.7, 0.7), ec='none', shrinkA=0)
            )
            axs['j'].text(0.5, 0.5,
'''Both populations have 
the same mean $\mu$, and 
standard deviation $\sigma$
''',
                va='center', ha='center', fontsize=14,
                bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec='none')
            )

        def sample(axs, pop_1976_data, pop_1978_data, xbars):
            print(xbars)
            for ax_pop_d, ax_sam_d, pop_data, xi, year in zip('ab', 'cd', (pop_1976_data, pop_1978_data), (0, 1), ('1976', '1978')):
                ax_pop = axs[ax_pop_d]
                ax_sam = axs[ax_sam_d]
                ax_sam.cla()
                ax_sam.axis('off')

                y = 0.5*np.ones(n)
                x = np.linspace(-1, 1, n)
                beak = plt.imread('Datasets/finch_clipart.png')

                idxs = np.random.choice(list(range(len(pop_data))), size=n, replace=False)
                for x0, idx in zip(x, idxs):
                    beak_data = pop_data.iloc[idx]
                    ab = AnnotationBbox(
                        self.getImage(beak, beak_data.s), (x0, 0.5), frameon=False)
                    ax_sam.add_artist(ab)
                    # scale between image coords and position of beak coords
                    m = -1/(0.5 - 25/400)
                    c = -0.5*m
                    con = ConnectionPatch(
                        xyA=((beak_data.x-c)/m, (beak_data.y-c)/m), xyB=(x0, 0.503),
                        coordsA='axes fraction', coordsB='data',
                        axesA=ax_pop, axesB=ax_sam,
                        arrowstyle="->", shrinkB=0)
                    con.set(color='orange')
                    ax_sam.add_artist(con)

                ax_sam.scatter(x, y, marker='')
                ax_sam.text(0.5, 0.3, f'$\\bar{{x}}_\\mathrm{{{year}}}$ = {xbars[xi]:.2f} mm', fontsize=14, ha='center', transform=ax_sam.transAxes)

        def d_statistic(axs, xbars, d):
            ax = axs['e']
            ax.cla()
            ax.axis('off')

            ax.text(0.05, 0.5, 
                f'$d$ = {xbars[1]:.2f} $-$ {xbars[0]:.2f} mm\n' 
                f'$d$ = {d:.2f} mm', ha='left', fontsize=14)
        
        def null_dist(axs, d_values):
            ax = axs['f']
            ax.cla()
            ax.axis('on')
            beak_depth = pd.read_csv('Datasets/finches beak depth.csv')
            xbar_obs = beak_depth.mean()
            d_obs = xbar_obs['1978'] - xbar_obs['1976']

            sns.histplot(d_values, stat='proportion', bins=50, ax=ax)
            ax.set_xlabel('$d$-statistic (mm)')
            # ax.set_title('Null distribution of the $d$-statistic\nassuming null hypothesis were true')
            # ax.axvline(0, color='yellow') # Add a yellow vertical line at d=0
            # ax.set_xlim(-2*d_obs, 2*d_obs) # Fix the x-axis to be between -2*d_obs, 2*d_obs
            # ax.axvline(d_obs, color='magenta') # Add a magenta vertical line at the observed value of d=d_obs
            # ax.axvline(-d_obs, color='magenta') # Add a magenta vertical line at the observed value of d=-d_obs
            # ax.annotate(f'{d_obs:.2f} mm', (d_obs, 0), (270, 55), color='magenta', textcoords='axes points', fontsize=12, arrowprops={'arrowstyle':'-|>', 'color':'magenta'}); # Add an arrow
            # ax.annotate(f'$-${d_obs:.2f} mm', (-d_obs, 0), (15, 55), color='magenta', textcoords='axes points', fontsize=12, arrowprops={'arrowstyle':'-|>', 'color':'magenta'}); # Add an arrow
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_xlim(-1, 1)
            # ax.tick_params(axis='x')
            # ax.tick_params(axis='y')
            # ax.set_xlabel('Beak depth (mm)')
            # ax.set_ylabel('Proportion')
            # ax.text(0.1, 1, f'$\\bar{{x}} = {xbar:.2f}\,\mathrm{{mm}}$\n$s = {s:.2f}\,\mathrm{{mm}}$', 
            #         fontsize=14, transform=ax.transAxes)
            # ax = axs['f']
            # ax.annotate(text=
            #         'The sample is visualised\n'
            #         'in a histogram and the\n'
            #         'sample mean $\\bar{x}$, and\n'
            #         'sample standard deviation\n'
            #         '$s$, are calculated',
            #         va='top', ha='center', fontsize=14,
            #         bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec='none'),
            #         xytext=(0.5, 0.9), xy=(0.5, -1.3), xycoords='axes fraction', 
            #         arrowprops=dict(arrowstyle="wedge,tail_width=1.",
            #         fc=(1.0, 0.7, 0.7), ec='none', shrinkA=0)
            # )
            # return xbar, s
                
        mosaic = \
            '''
            .g...h.
            aaa.bbb
            aaajbbb
            aaa.bbb
            .c.e.d.
            ...f...
            '''
        gs_kw = dict(width_ratios=[0.25, 1, 0.25, 1, 0.25, 1, 0.25], height_ratios=[0.5, 0.25, 1, 0.25, 1, 1])
        fig, axs = plt.subplot_mosaic(mosaic, gridspec_kw=gs_kw, figsize=(9.4, 10))
        plt.subplots_adjust(hspace=0, wspace=0, left=0.05, right=0.99, bottom=0.1, top=1)
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        plt.ion()

        [ax.axis('off') for ax in axs.values()]

        mu = 9.5
        sigma = 1
        n = 20
        self.slide_no = 1
        pop_1976_data = pd.read_csv('Datasets/finch_1976_pop.csv')
        pop_1978_data = pd.read_csv('Datasets/finch_1978_pop.csv')

        # run this once to generate population
        # self.generate_population()
        # exit()
        
        beak_pop(axs)
        d_values = []
        self.beak_samples, self.xbars, d = new_samples(mu, sigma, n)
        d_values.append(d)

        sample(axs, pop_1976_data, pop_1978_data, self.xbars)
        d_statistic(axs, self.xbars, d)
        null_dist(axs, d_values)

