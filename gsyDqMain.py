# -*- coding: utf-8 -*-
"""
Main script for dynamic visualisation of Clarke and Park Transforms.

Note that DO NOT USE matplotlib 3.0.2. It causes errors.

A working matplotlib version is 2.3.3.

Author : 高斯羽 博士 (Dr. GAO, Siyu)

Version : 0.2.0

Last modified : 2019-02-28

List of functions
------------------

* animate_
* help_on_clicked_
* init_
* load_ffmpeg_on_clicked_
* make_ani_
* video_play_on_clicked_
* video_save_on_clicked_
* video_stop_on_clicked_

Function definitions
----------------------

"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
import tkinter.messagebox as msgbox
import threading
import os
import sys


from numpy import sin, cos
from matplotlib.widgets import Button, TextBox
from tkinter import filedialog

# custom modules
from gsyDqLib import date_time_now
from gsyDqLib import cal_ABDQ
from gsyDqLib import find_pll_direction, find_sequences
from gsyDqLib import set_font_size
from gsyDqLib import collect_tb, load_ffmpeg
from gsyDqLib import check_file_saved, save_animation_to_disk

from gsyIO import save_txt_on_event, search_file_and_start

from gsyINI import read_ini_to_tb, write_ini

# matplotlib font settings
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Times New Roman'
mpl.rcParams['mathtext.fontset'] = 'cm'


# constants
CONST_INI_FILENAME = 'gsy_dq.ini'

CONST_ORANGE = (255/255, 165/255, 0/255)    # color orange

CONST_PURPLE = (204/255, 51/255, 255/255)   # color purple

CONST_WIDTH = 1280

CONST_HEIGHT = 720

CONST_DPI = 100

CONST_STR_DOCT_FILENAME = 'index.html'

CONST_STR_COPYRIGHT = ('\u00a9 $Dr. GAO, \ Siyu. 2017$'                   
                       + '\n' + '$siyu.gao@outlook.com$') 

CONST_STR_VER = '1.1'

CONST_STR_HELP = u'''
This program is intended to visualise the Clarke and Park transforms. 
                  
Written by : Dr. GAO, Siyu
Version : 1.1
                  
Input Harmonic Order : 
This sets the order of harmonic to be analysed. 1st order is the fundamental. This input needs to be a float.

PLL Order : 
This sets the angular velocity of the PLL as multiples of the fundamental frequency. This input needs to be a float.
Positive number means the PLL is rotating anti-clockwise.
Negative number means the PLL is rotating clockwise.

Samples :
This sets how many samples are taken within one fundamental period. This also sets the total frames for the video. 
Increasing this number would make the curves smoother. But the program would consume more resource.

FPS :
This sets the frame rate for saving video. This frame rate is not applied when runing on-the-fly.

Base Freq :
This sets the fundamental frequency.

NOTE : you'd better to stop the video first before changing the above input field settings.

Stop :
This button would stop the video. You can ONLY change the input fields when the video is stopped.

Play :
This button would refresh the video. Any updates made to the input fileds would be applied.

Save video :
This button would trigger the video to be saved. Only limited progress would be displayed 
due to the use of maplotlib's built-in save function. A message would be prompted when the save is finished.
The codec FFmpeg is required. It's free to download and use. The FFmpeg binary (ffmpeg.exe) is required. 
It's usually located in the "bin" folder. The video length equals Samples divided by FPS.

Browse : 
This button would allow you to browse for the FFmpeg binary.
The path would be saved to an INI file and loaded on next program start-up.
'''

print(date_time_now() + 'Started')

# =============================================================================
# <Help figure>
# =============================================================================

fig_help = plt.figure(figsize=(720/CONST_DPI, 640/CONST_DPI), dpi=CONST_DPI, num='Help')

ax_button_save_help = plt.axes([0.85, 0.025, 0.12, 0.06])
    
plt.close(fig_help)

text_help = fig_help.text(0.02, 1, CONST_STR_HELP, va='top')
text_help.set_family('Segoe UI')
text_help.set_fontweight('normal')
text_help.set_fontsize(9)

button_save_help = Button(ax_button_save_help, 'Save as txt', color='gold')
button_save_help.label.set_family('Arial')
button_save_help.label.set_fontweight('bold')
    
button_save_help.on_clicked(lambda x: save_txt_on_event(x, CONST_STR_HELP))

# =============================================================================
# </Help figure>
# =============================================================================


# =============================================================================
# <Main figure>
# =============================================================================

fig_main = plt.figure(figsize=(CONST_WIDTH/CONST_DPI, CONST_HEIGHT/CONST_DPI), 
                      dpi=CONST_DPI, 
                      num='Visualisation of Clarke and Park Transforms')

fig_main.suptitle(r'Clarke and Park Transforms',
                  fontsize=16, fontweight='bold', family='Arial', y = 0.95)

fig_main.text(0.88, 0.95, CONST_STR_COPYRIGHT, va='top')

# -----------------------------------------------------------------------------
# <Main figure interactive controls>
# -----------------------------------------------------------------------------

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# <Interactive, input texts>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# text box, input harmonic order
ax_tb_input_harmonic = plt.axes([0.1, 0.04, 0.03, 0.03])
textbox_input_harmonic = TextBox(ax_tb_input_harmonic, 
                                 'Input \u0020 \n Harmonic Order : ', 
                                 initial='', color='w')

# text box, input PLL order
ax_tb_pll_order = plt.axes([0.1, 0.005, 0.03, 0.03])

textbox_pll_order = TextBox(ax_tb_pll_order, 'Input PLL Order : ', 
                            initial='', color='w')

# text box, sampling points
ax_tb_samples = plt.axes([0.19, 0.04, 0.03, 0.03])
textbox_samples = TextBox(ax_tb_samples, 'Samples : ', 
                          initial='', color='w')

# text box, frames per second (FPS), only truely while in saved video, on the fly animation may not
ax_tb_fps = plt.axes([0.19, 0.005, 0.03, 0.03])
textbox_fps = TextBox(ax_tb_fps, 'FPS : ', initial='', color='w')

# text box, base frequency
ax_tb_base_freq = plt.axes([0.262, 0.04, 0.03, 0.03])
textbox_base_freq = TextBox(ax_tb_base_freq, 'Base \u0020 \n Freq : ', 
                            initial='', color='w')

# text box, FFmpeg binary path
ax_tb_ffmpeg_path = plt.axes([0.6, 0.005, 0.305, 0.03])
textbox_ffmpeg_path = TextBox(ax_tb_ffmpeg_path, 'FFmpeg path :', 
                              initial='', color='w')

# set text boxes' font family and font weight
list_textbox = [textbox_input_harmonic, textbox_pll_order, 
                textbox_samples, textbox_fps, textbox_base_freq,
                textbox_ffmpeg_path]

for item in list_textbox:
    
    item.label.set_family('Arial')
    item.label.set_fontweight('bold')
    
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# </Interactive, input texts>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# <Interactive, buttons>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
# button, stop the video
ax_button_stop = plt.axes([0.315, 0.04, 0.03, 0.03])
button_stop = Button(ax_button_stop, 'Stop', color='pink')

# button, play the video
ax_button_play = plt.axes([0.365, 0.04, 0.03, 0.03])
button_play = Button(ax_button_play, 'Play', color='gold')

# button, save the video
ax_button_save_video = plt.axes([0.315, 0.005, 0.08, 0.03])
button_save_video = Button(ax_button_save_video, 'Save Video', color='grey')
button_save_video.label.set_color('w')

# button, browse for FFmpeg binary
ax_button_browse = plt.axes([0.91, 0.005, 0.05, 0.03])
button_browse = Button(ax_button_browse, 'Browse', color='lightgrey')

# button, display help
ax_button_help = plt.axes([0.4, 0.04, 0.08, 0.03])
button_help = Button(ax_button_help, 'Help', color='lime')
button_help.label.set_fontsize(12)

# button, open documentation
ax_button_doct = plt.axes([0.4, 0.005, 0.08, 0.03])
button_doct = Button(ax_button_doct, 'DOCT', color='skyblue')
button_doct.label.set_fontsize(12)

# set buttons' font family and font weight
list_button = [button_stop, button_play, 
               button_save_video, 
               button_help, button_doct,
               button_browse]

for item in list_button:
    
    item.label.set_family('Arial')
    item.label.set_fontweight('bold')
    
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# </Interactive, buttons>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
# -----------------------------------------------------------------------------
# </Main figure interactive controls>
# -----------------------------------------------------------------------------

# get current work folder path
str_cwd = os.getcwd()

# system independent path join
str_ini_file_path = os.path.join(str_cwd, CONST_INI_FILENAME)

# assign the values stored in the INI file to the textboxes
bool_ini_exist, config = read_ini_to_tb(str_ini_file_path, list_textbox)


# <Condition>
if bool_ini_exist == True:
# if the INI file found, use it, else, use default values
# on exception, use default values
    
    try:
        
        dbl_harmonic_order = float(textbox_input_harmonic.text)
        dbl_harmonic_order = abs(dbl_harmonic_order)
        
        dbl_pll_order = float(textbox_pll_order.text)
        
        dbl_base_freq = float(textbox_base_freq.text)
        dbl_base_freq = abs(dbl_base_freq)
        
        if dbl_base_freq == 0:
            
            dbl_base_freq = 50
            
        else:
            
            dbl_base_freq = dbl_base_freq
        
        dbl_base_period = 1 / dbl_base_freq
                
        int_samples = int(textbox_samples.text)
        int_samples = abs(int_samples)
        
        int_fps = int(textbox_fps.text)
        int_fps = abs(int_fps)
        
        
        str_ffmpeg_path = textbox_ffmpeg_path.text        
        
    except:
        
        # default settings
        dbl_harmonic_order = 1
        dbl_pll_order = 1        
        dbl_base_freq = 50
        dbl_base_period = 1 / dbl_base_freq
        int_samples = 200
        int_fps = 30
        str_ffmpeg_path = ''
    
else:
    
        # default settings
        dbl_base_freq = 50
        dbl_base_period = 1 / dbl_base_freq
        dbl_pll_order = 1
        dbl_harmonic_order = 1
        int_samples = 200
        int_fps = 30
        str_ffmpeg_path = ''
# </Condition>

# make the data
(time, theta, 
 alpha_vector, beta_vector, 
d_vector, q_vector,
d_ax_on_x, d_ax_on_y, 
q_ax_on_x, q_ax_on_y, 
d_vector_on_x, d_vector_on_y, 
q_vector_on_x, q_vector_on_y) = cal_ABDQ(int_samples, dbl_base_freq, 
                                         dbl_harmonic_order, dbl_pll_order)

# get pll frequency info
str_freq_pll = find_pll_direction(dbl_base_freq, dbl_pll_order)

# get sequence info
(str_freq_harmonic, 
 str_freq_clarke, 
 str_freq_park, 
 dbl_period_clarke, 
 dbl_period_park) = find_sequences(dbl_base_freq, dbl_harmonic_order, dbl_pll_order)

# set font size
dbl_font_size = set_font_size(dbl_harmonic_order)

# -----------------------------------------------------------------------------
# <Coordinate 1, the rotating vectors>
# -----------------------------------------------------------------------------

# static, set coordinate axes
ax1 = plt.subplot(1, 2, 1)

# make axes equal
plt.axis('equal')

# axes limits
plt.axis([-3, 3, -3, 3])

# static, grid lines
ax1.grid(visible=True, zorder=0)

# static, unit circle
ax1.plot(cos(theta), sin(theta), linewidth=2, color='k',zorder=3, linestyle=':')

# static, alpha axis
ax1.annotate("",
             xy=(2, 0), xytext=(-2, 0), 
             arrowprops=dict(shrink=0, fc='black', ec='black', lw=0.1))

# static, alpha axis label
ax1.text(2, -0.3, r'$\alpha$', fontsize=15, horizontalalignment='center')

# static, beta axis
ax1.annotate("",
             xy=(0, 2), xytext=(0, -2), 
             arrowprops=dict(shrink=0, fc='black', ec='black', lw=0.1))

# static, beta axis label
ax1.text(0.2, 2, r'$\beta$', fontsize=15, verticalalignment='center')

# static, frequency info
ax1_text_freq_harmonic = ax1.text(-4.07, 2.95, str_freq_harmonic,
                                  zorder=10, fontsize=10.5, 
                                  va='top', ha='left',
                                  bbox=dict(facecolor='white', edgecolor='red', 
                                            boxstyle='round'))

ax1_text_freq_pll = ax1.text(-4.07, 1.5, str_freq_pll, 
                             zorder=10, fontsize=10.5,
                             va='top', ha='left',
                             bbox=dict(facecolor='white', edgecolor='blue', 
                                       boxstyle='round'))

# static, set legend    
# make some empty plots, set the colours and labels and display the legends
# that's why "pseudo"
ax1_pseudo_harmonic, = ax1.plot([], [], label=r'$Input$' + '\n' + r'$harmonic$',
                                color='blue', lw=3)
ax1_pseudo_alpha, = ax1.plot([], [], label=r'$\alpha$', color='red', lw=3)
ax1_pseudo_beta, = ax1.plot([], [], label=r'$\beta$', color='green', lw=3)
ax1_pseudo_d, = ax1.plot([], [], label=r'$d$', color=CONST_ORANGE, lw=3)
ax1_pseudo_q, = ax1.plot([], [], label=r'$q$', color=CONST_PURPLE, lw=3)

ax1.legend(handles=[ax1_pseudo_harmonic, 
                    ax1_pseudo_alpha, ax1_pseudo_beta, 
                    ax1_pseudo_d, ax1_pseudo_q], 
           fontsize=11,
           loc = 'lower left', shadow=True, fancybox=True,
           bbox_to_anchor=(-0.36, -0.01))

# to be animated, info strings
str_time = ''
str_harmonic_theta = ''
str_pll_theta = ''
ax1_text_info = ax1.text(-2.1, -2.8, '',
                        fontsize=15,
                        bbox=dict(facecolor='white', edgecolor='white'))

# to be animated, pll locked/not locked on text
ax1_text_pll_locked = ax1.text(0, 2.7, '',
                               fontsize=12, color='red', ha='center', va='top',
                               bbox=dict(facecolor='white', edgecolor='white'))

# to be animated, ellipse
ax1_ellipse, = ax1.plot([], [], 
                        color='blue', linewidth=3)

# to be animated, d axis
# I am actually combining an arrow and a line here. 
# Because I found that the annotation arrow cannot go to the negative in 
# saved videos. 
# It can be displayedfine in animation, but for some reason, 
# not in saved videos. 
# Therefore, one annotation arrow + one line then.
ax1_d_ax_pos = ax1.annotate('',
                            xy=(0,0), xytext=(0,0), 
                            arrowprops=dict(shrink=0, 
                                            fc='slategrey', ec='slategrey', 
                                            lw=0.1))

ax1_d_ax_neg, = ax1.plot([], [], '', color='slategrey', lw=4)

# to be animated, d axis label
ax1_d_label = ax1.text(0, 0, '', fontsize=15, ha='center')

# to be animated, q axis
ax1_q_ax_pos = ax1.annotate('',
                            xy=(0, 0), xytext=(0, 0), 
                            arrowprops=dict(shrink=0, 
                                            fc='slategrey', ec='slategrey',
                                            lw=0.1))

ax1_q_ax_neg, = ax1.plot([], [], '', color='slategrey', lw=4)

# to be animated, q axis label
ax1_q_label = ax1.text(0, 0, '', fontsize=15, ha='center')    

# to be animated, alpha arrow
ax1_alpha_arrow = ax1.annotate("",
                               xy=(0, 0), xytext=(0, 0),
                               arrowprops=dict(shrink=0, 
                                               fc='red', ec='red', 
                                               lw=0.1))

# to be animated, beta arrow
ax1_beta_arrow = ax1.annotate("",
                              xy=(0, 0), xytext=(0, 0), 
                              arrowprops=dict(shrink=0, 
                                              fc='green', ec='green', 
                                              lw=0.1))

# to be animated, harmonic arrow
ax1_harmonic_arrow = ax1.annotate("",
                                  xy=(0, 0), xytext=(0, 0), 
                                  arrowprops=dict(shrink=0, 
                                                  fc='blue', ec='blue',
                                                  lw=0.1))

# to be animated, d arrow
ax1_d_vector_arrow = ax1.annotate("",
                                  xy=(0, 0), xytext=(0, 0), 
                                  arrowprops=dict(shrink=0, 
                                                  fc=CONST_ORANGE, ec=CONST_ORANGE, 
                                                  lw=0.1))

# to be animated, q arrow
ax1_q_vector_arrow = ax1.annotate("",
                                  xy=(0, 0), xytext=(0, 0), 
                                  arrowprops=dict(shrink=0, 
                                                  fc=CONST_PURPLE, ec=CONST_PURPLE,
                                                  lw=0.1))

# to be animated, helping lines
ax1_help_line_alpha, = ax1.plot([], [], 
                                color='black', linewidth=2, linestyle='--')

ax1_help_line_beta, = ax1.plot([], [], 
                               color='black', linewidth=2, linestyle='--')

ax1_help_line_d, = ax1.plot([], [], 
                            color='blue', linewidth=3, linestyle='--')

ax1_help_line_q, = ax1.plot([], [], 
                            color='blue', linewidth=3, linestyle='--')

# -----------------------------------------------------------------------------
# </Coordinate 1, the rotating vectors>
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# <Coordinate 2, alpha vs time and beta vs time>
# -----------------------------------------------------------------------------

# static, set coordinate
ax2 = plt.subplot(2, 2, 2)

# set x axis limits, 0 to the base period
ax2.set_xlim([0, dbl_base_period])

# set y axis limits
# find the maximum of all data points and add 0.05 to it
ylim_max = (max(max(alpha_vector), max(beta_vector), max(d_vector), max(q_vector)) 
            + 0.05)

ylim_min = -1 * ylim_max

ax2.set_ylim([ylim_min, ylim_max])

# static, horizontal middle line
ax2.axhline(y=0, color='k', lw=3)

# static, grid lines
ax2.grid(True)

# to be animated, period helping lines (auxiliary lines) and text
ax2_period_lines = []
ax2_period_text = []

# <for-loop, make 100 ax2 helping lines>
# 100 because I need to dynamically update them and 100 should be more than needed
# dynamic update mainly due to the refreshing the animate according to new
# user config, not because animating itself
for item in np.arange(0, 100, 1):
    temp_plot, = ax2.plot([], [], linestyle='--', linewidth=1.5, color='k')
    
    ax2_period_lines.append(temp_plot)
    
    temp_text = ax2.text(0, 0, '',
                         ha='right', va='top', 
                         family='Arial', fontsize=dbl_font_size, fontweight='bold')
    
    ax2_period_text.append(temp_text)
# </for-loop, make 100 ax2 helping lines>
 
# to be animated, alpha line
ax2_alpha_vs_time, = ax2.plot([], [], label = r'$\alpha$',
                              color='r', linewidth=3)
    
# to be animated, beta line
ax2_beta_vs_time, = ax2.plot([], [], label = r'$\beta$', 
                             color='g', linewidth=3)

# to be animated, alpha helping line
ax2_alpha_help_line, = ax2.plot([], [], 
                                color='black', linewidth=1.5, linestyle='--')

# to be animated, beta helping line
ax2_beta_help_line, = ax2.plot([], [], 
                                color='black', linewidth=1.5, linestyle='--')

# static, set legend    
ax2Legend = plt.legend(handles=[ax2_alpha_vs_time, ax2_beta_vs_time], 
                       title=str_freq_clarke,
                       loc = 'upper right', shadow=True, fancybox=True, 
                       bbox_to_anchor=(1.28, 1))

# set legend title font size
ax2Legend.get_title().set_fontsize('10')

# set legend text font size
plt.setp(plt.gca().get_legend().get_texts(), fontsize='10')

# -----------------------------------------------------------------------------
# </Coordinate 2, alpha vs time and beta vs time>
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# <Coordinate 3, d vs time and q vs time>
# -----------------------------------------------------------------------------
# the codes here are similar to Coordinate 2

# static, set coordinate
ax3 = plt.subplot(2, 2, 4)

ax3.set_xlim([0, dbl_base_period])

ax3.set_ylim([ylim_min, ylim_max])

# static, horizontal middle line
ax3.axhline(y=0, color='k', lw=3)

# static, grid lines
ax3.grid(True)
        
# to be animated, period helping lines and text
ax3_period_lines = []
ax3_period_text = []

for item in np.arange(0, 100, 1):
    
    temp_plot, = ax3.plot([], [], linestyle='--', linewidth=1.5, color='k')
    
    ax3_period_lines.append(temp_plot)
    
    temp_text = ax3.text(0, 0, '',
                         ha='right', va='top', color='blue',
                         family='Arial', fontsize=dbl_font_size, fontweight='bold')
    
    ax3_period_text.append(temp_text)

# to be animated, pll locked/not locked on text
ax3_text_pll_locked = ax3.text(0.01, -0.375, '',
                               fontsize=15, color='red', ha='center', va='top',
                               bbox=dict(facecolor='white', edgecolor='white'))        

# to be animated, d line
ax3_d_vs_time, = ax3.plot([], [], label = r'$d$',
                          color=CONST_ORANGE, linewidth=3)

# to be animated, q line
ax3_q_vs_time, = ax3.plot([], [], label = r'$q$', 
                          color=CONST_PURPLE, linewidth=3)
            
# static, set legend
ax3Legend = plt.legend(handles=[ax3_d_vs_time, ax3_q_vs_time], 
                       title=str_freq_park,
                       loc = 'upper right', shadow=True, fancybox=True,
                       bbox_to_anchor=(1.28, 1))

ax3Legend.get_title().set_fontsize('9')
plt.setp(plt.gca().get_legend().get_texts(), fontsize='10')

# static, set x label
ax3.set_xlabel(r'Time (s)', fontweight='bold', fontsize=12, family='Arial')

# to be animated, d helping line
ax3_d_help_line, = ax3.plot([], [], 
                            color='blue', linewidth=1.5, linestyle='--')

# to be animated, q helping line
ax3_q_help_line, = ax3.plot([], [], 
                            color='blue', linewidth=1.5, linestyle='--')

# -----------------------------------------------------------------------------
# </Coordinate 3, d vs time and q vs time>
# -----------------------------------------------------------------------------

# =============================================================================
# </Main figure>
# =============================================================================


# =============================================================================
# <Function: initialisation for animation>
# =============================================================================

def init():   
    """
    .. _init :
        
    matplotlib's documentation:
    https://matplotlib.org/api/animation_api.html
    
    This function initialise the animation.

    Parameters
    ----------
    None

    Returns
    -------
::      
    tuple(ax2_period_lines) : a tuple of a list of matplotlib plot object
    tuple(ax2_period_text)  : a tuple of a list of matplotlib plot object
    tuple(ax3_period_lines) : a tuple of a list of matplotlib plot object
    tuple(ax3_period_text)  : a tuple of a list of matplotlib plot object
    ax1_text_info           : matplotlib text object
    ax1_text_pll_locked     : matplotlib text object
    ax1_d_ax_pos            : matplotlib annotatiton object
    ax1_d_ax_neg            : matplotlib annotatiton object
    ax1_d_label             : matplotlib text object
    ax1_q_ax_pos            : matplotlib annotatiton object
    ax1_q_ax_neg            : matplotlib annotatiton object
    ax1_q_label             : matplotlib text object
    ax1_alpha_arrow         : matplotlib annotatiton object
    ax1_beta_arrow          : matplotlib annotatiton object
    ax1_harmonic_arrow      : matplotlib annotatiton object
    ax1_d_vector_arrow      : matplotlib annotatiton object
    ax1_q_vector_arrow      : matplotlib annotatiton object
    ax1_help_line_alpha     : matplotlib plot object
    ax1_help_line_beta      : matplotlib plot object
    ax1_help_line_d         : matplotlib plot object
    ax1_ellipse             : matplotlib plot object
    ax2_alpha_vs_time       : matplotlib plot object
    ax2_beta_vs_time        : matplotlib plot object
    ax2_alpha_help_line     : matplotlib plot object
    ax2_beta_help_line      : matplotlib plot object
    ax3_d_vs_time           : matplotlib plot object
    ax3_q_vs_time           : matplotlib plot object
    ax3_d_help_line         : matplotlib plot object
    ax3_q_help_line         : matplotlib plot object
    ax3_text_pll_locked     : matplotlib text object

    Examples
    --------
    
    .. code:: python
    
        animation.FuncAnimation(locFig, animate, np.arange(0, locInt_samples, 1), interval=1/locInt_fps*1e3, blit=True, init_func=init)
    """         
    # ax1 info strings
    ax1_text_info.set_text('')
    
    ax1_text_pll_locked.set_text('')

    # ax1 d axis   
    ax1_d_ax_pos.xy = (0, 0)
    ax1_d_ax_pos.xytext = (0, 0)
    
    ax1_d_ax_neg.set_xdata([])
    ax1_d_ax_neg.set_ydata([])
    
    # ax1 d axis label
    ax1_d_label = ax1.text(0, 0, '')
    
    # ax1 q axis
    ax1_q_ax_pos = ax1.annotate('',
                                xy=(0, 0), xytext=(0, 0), 
                                arrowprops=dict(shrink=0, 
                                                fc='slategrey', 
                                                ec='slategrey', 
                                                lw=0.1))
    
    ax1_q_ax_neg.set_xdata([])
    ax1_q_ax_neg.set_ydata([])
    
    # ax1 q axis label
    ax1_q_label = ax1.text(0, 0, '')    
    
    # ax1 arrows
    ax1_alpha_arrow = ax1.annotate('',
                                   xy=(0, 0), xytext=(0, 0), 
                                   arrowprops=dict(shrink=0, 
                                                   fc='r', ec='r', 
                                                   lw=0.1))
    
    
    ax1_beta_arrow = ax1.annotate("",
                                  xy=(0, 0), xytext=(0, 0), 
                                  arrowprops=dict(shrink=0, 
                                                  fc='green', ec='green', 
                                                  lw=0.1))
    
    
    ax1_harmonic_arrow = ax1.annotate("",
                                      xy=(0, 0), xytext=(0, 0), 
                                      arrowprops=dict(shrink=0, 
                                                      fc='blue', ec='blue', 
                                                      lw=0.1))
    
    ax1_d_vector_arrow = ax1.annotate("",
                                      xy=(0, 0), xytext=(0, 0), 
                                      arrowprops=dict(shrink=0, 
                                                      fc=CONST_ORANGE, ec=CONST_ORANGE,
                                                      lw=0.1))
    
    ax1_q_vector_arrow = ax1.annotate("",
                                      xy=(0, 0), xytext=(0, 0), 
                                      arrowprops=dict(shrink=0, 
                                                      fc=CONST_PURPLE, ec=CONST_PURPLE, 
                                                      lw=0.1))
    
    # ax1 helping lines
    ax1_help_line_alpha.set_xdata([])
    ax1_help_line_alpha.set_ydata([])
    
    ax1_help_line_beta.set_xdata([])
    ax1_help_line_beta.set_ydata([])
    
    ax1_help_line_d.set_xdata([])
    ax1_help_line_d.set_ydata([])
    
    ax1_help_line_q.set_xdata([])
    ax1_help_line_q.set_ydata([])
    
    # for interharmonics
    ax1_ellipse, = ax1.plot([], [], 
                            color='pink', linewidth=3, linestyle=':')
    
    # ax2 period helping lines
    for item in ax2_period_lines:
        item.set_xdata([])
        item.set_ydata([])

    # ax2 period text        
    for item in ax2_period_text:
        item.set_text('')
            
    # ax2 alpha and beta lines
    ax2_alpha_vs_time.set_xdata([])
    ax2_alpha_vs_time.set_ydata([])
    
    ax2_beta_vs_time.set_xdata([])
    ax2_beta_vs_time.set_ydata([])
    
    # ax2 alpha and beta helping lines
    ax2_alpha_help_line.set_xdata([])
    ax2_alpha_help_line.set_ydata([])
    
    ax2_beta_help_line.set_xdata([])
    ax2_beta_help_line.set_ydata([])
    
    # ax3 period helping lines
    for item in ax3_period_lines:
        item.set_xdata([])
        item.set_ydata([])

    # ax3 period text        
    for item in ax3_period_text:
        item.set_text('')
    
    # ax3 d and q lines
    ax3_d_vs_time.set_xdata([])
    ax3_d_vs_time.set_ydata([])
    
    ax3_q_vs_time.set_xdata([])
    ax3_q_vs_time.set_ydata([])
    
    # ax3 d and q helping lines
    ax3_d_help_line.set_xdata([])
    ax3_d_help_line.set_ydata([])
    
    ax3_q_help_line.set_xdata([])
    ax3_q_help_line.set_ydata([])
    
    ax3_text_pll_locked.set_text('')
    
    # to return a list of objects for animation, you need "tuple"
    return  (tuple(ax2_period_lines) 
             + tuple(ax2_period_text) 
             + tuple(ax3_period_lines) 
             + tuple(ax3_period_text) 
             + (ax1_text_info, ax1_text_pll_locked,
                ax1_d_ax_pos,
                ax1_d_ax_neg, ax1_d_label,
                ax1_q_ax_pos, ax1_q_ax_neg, ax1_q_label,
                ax1_alpha_arrow, ax1_beta_arrow, ax1_harmonic_arrow,
                ax1_d_vector_arrow, ax1_q_vector_arrow,
                ax1_help_line_alpha, ax1_help_line_beta, ax1_help_line_d,
                ax1_ellipse,
                ax2_alpha_vs_time, ax2_beta_vs_time,            
                ax2_alpha_help_line, ax2_beta_help_line,
                ax3_d_vs_time, ax3_q_vs_time,
                ax3_d_help_line, ax3_q_help_line,
                ax3_text_pll_locked))
    
# =============================================================================
# </Function: initialisation for animation>    
# =============================================================================


# =============================================================================
# <Function: updates for animation>    
# =============================================================================
    
def animate(item):
    """
    .. _animate :
        
    matplotlib's documentation:
    https://matplotlib.org/api/animation_api.html
    
    This function updates the animation.

    Parameters
    ----------
    item : int
        This parameter is used as a frame number to update the animation.
            
    Returns
    -------
::
    tuple(ax2_period_lines) : a tuple of a list of matplotlib plot object
    tuple(ax2_period_text)  : a tuple of a list of matplotlib plot object
    tuple(ax3_period_lines) : a tuple of a list of matplotlib plot object
    tuple(ax3_period_text)  : a tuple of a list of matplotlib plot object
    ax1_text_info           : matplotlib text object
    ax1_text_pll_locked     : matplotlib text object
    ax1_d_ax_pos            : matplotlib annotatiton object
    ax1_d_ax_neg            : matplotlib annotatiton object
    ax1_d_label             : matplotlib text object
    ax1_q_ax_pos            : matplotlib annotatiton object
    ax1_q_ax_neg            : matplotlib annotatiton object
    ax1_q_label             : matplotlib text object
    ax1_alpha_arrow         : matplotlib annotatiton object
    ax1_beta_arrow          : matplotlib annotatiton object
    ax1_harmonic_arrow      : matplotlib annotatiton object
    ax1_d_vector_arrow      : matplotlib annotatiton object
    ax1_q_vector_arrow      : matplotlib annotatiton object
    ax1_help_line_alpha     : matplotlib plot object
    ax1_help_line_beta      : matplotlib plot object
    ax1_help_line_d         : matplotlib plot object
    ax1_ellipse             : matplotlib plot object
    ax2_alpha_vs_time       : matplotlib plot object
    ax2_beta_vs_time        : matplotlib plot object
    ax2_alpha_help_line     : matplotlib plot object
    ax2_beta_help_line      : matplotlib plot object
    ax3_d_vs_time           : matplotlib plot object
    ax3_q_vs_time           : matplotlib plot object
    ax3_d_help_line         : matplotlib plot object
    ax3_q_help_line         : matplotlib plot object
    ax3_text_pll_locked     : matplotlib text object

    Examples
    --------
    .. code:: python
    
        animation.FuncAnimation(locFig, animate, np.arange(0, locInt_samples, 1), interval=1/locInt_fps*1e3, blit=True, init_func=init)
    """
        
    # update ax1 info strings    
    str_time = r'$t = {:0.5f}'.format(time[item]) + '\ s$'
    
    str_harmonic_theta = (r'$\theta_{Harmonic} = $' 
                          + ('${:0.3f}'
                             .format(2 * 180 
                                     * dbl_harmonic_order 
                                     * dbl_base_freq 
                                     * time[item])) 
                          + '^{\circ}$')
    
    str_pll_theta = (r'$\theta_{PLL} = $' 
                     + ('${:0.3f}'
                        .format(2 * 180 
                                * dbl_pll_order 
                                * dbl_base_freq 
                                * time[item]))
                     + '^{\circ}$')
    
    ax1_text_info.set_text(str_time 
                          + '\n' + str_harmonic_theta 
                          + '\n' + str_pll_theta)
    
    # update ax1 d axis
    ax1_d_ax_pos.xy = (2 * d_ax_on_x[item], 2 * d_ax_on_y[item])
    
    ax1_d_ax_neg.set_xdata([0, -2 * d_ax_on_x[item]])
    ax1_d_ax_neg.set_ydata([0, -2 * d_ax_on_y[item]])
    
    # update ax1 d axis label
    ax1_d_label.set_x(2.1 * d_ax_on_x[item])
    ax1_d_label.set_y(2.1 * d_ax_on_y[item])
    
    if d_ax_on_y[item] > 0:          
        
        ax1_d_label.set_va('bottom')
        
    elif d_ax_on_y[item] < 0:
        
        ax1_d_label.set_va('top')
            
    ax1_d_label.set_text('$d$')
        
    # update ax1 q axis
    ax1_q_ax_pos.xy=(2 * q_ax_on_x[item], 2 * q_ax_on_y[item])
    
    ax1_q_ax_neg.set_xdata([0, -2 * q_ax_on_x[item]])
    ax1_q_ax_neg.set_ydata([0, -2 * q_ax_on_y[item]])
    
    # update ax1 q axis label
    ax1_q_label.set_x(2.1 * q_ax_on_x[item])
    ax1_q_label.set_y(2.1 * q_ax_on_y[item])
    
    if q_ax_on_y[item] > 0:      
        
        ax1_q_label.set_va('bottom')
        
    elif q_ax_on_y[item] < 0:
        
        ax1_q_label.set_va('top')
            
    ax1_q_label.set_text('$q$')
    
    # update ax1 alpha and beta helping lines (so they are under the arrows)
    ax1_help_line_alpha.set_xdata([alpha_vector[item], alpha_vector[item]])
    ax1_help_line_alpha.set_ydata([0, beta_vector[item]])
    
    ax1_help_line_beta.set_xdata([0, alpha_vector[item]])
    ax1_help_line_beta.set_ydata([beta_vector[item], beta_vector[item]])
    
    ax1_help_line_d.set_xdata([d_vector_on_x[item], alpha_vector[item]])
    ax1_help_line_d.set_ydata([d_vector_on_y[item], beta_vector[item]])
    
    ax1_help_line_q.set_xdata([q_vector_on_x[item], alpha_vector[item]])
    ax1_help_line_q.set_ydata([q_vector_on_y[item], beta_vector[item]])
    
    # update ax1 arrows        
    ax1_alpha_arrow.xy = (alpha_vector[item], 0)    
    ax1_alpha_arrow.xytext = (0, 0)
    
    
    ax1_beta_arrow.xy = (0, beta_vector[item])
    ax1_beta_arrow.xytext = (0, 0)
    
    
    ax1_harmonic_arrow.xy = (alpha_vector[item], beta_vector[item])
    ax1_harmonic_arrow.xytext = (0, 0)
    
    
    ax1_d_vector_arrow.xy = (d_vector_on_x[item], d_vector_on_y[item])
    ax1_d_vector_arrow.xytext = (0, 0)
    
    
    ax1_q_vector_arrow.xy=(q_vector_on_x[item], q_vector_on_y[item])
    ax1_q_vector_arrow.xytext=(0, 0)
    
    # update ax1 origin dot
    ax1_origin = ax1.scatter(0, 0, marker='o', color='black', lw=4)
    
    # update the ellipse                    
    ax1_ellipse.set_xdata(alpha_vector[0:item])
    ax1_ellipse.set_ydata(beta_vector[0:item])
    
    # update ax2 period helping lines    
    if (dbl_period_clarke != 0):
        
        # clear all lines
        for j in ax2_period_lines:
        
            j.set_xdata([])
            j.set_ydata([])
        
        # draw all lines
        for j in np.arange(0, round(dbl_base_period/dbl_period_clarke), 1):
            
            ax2_period_lines[j].set_xdata([(j+1)*dbl_period_clarke, (j+1)*dbl_period_clarke])
            ax2_period_lines[j].set_ydata([ylim_min, ylim_max])
            
    else:
        
        # clear all lines
        for j in ax2_period_lines:
        
            j.set_xdata([])
            j.set_ydata([])
        
    dbl_font_size = set_font_size(dbl_harmonic_order)
    
    # update ax2 period helping text
    if (dbl_period_clarke != 0):
                
        # clear all text
        for k in ax2_period_text:
        
            k.set_text('')
        
        # set all text
        for k in np.arange(0, round(dbl_base_period/dbl_period_clarke), 1):
            
            ax2_period_text[k].set_x((k+1)*dbl_period_clarke - 0.02e-2)
            ax2_period_text[k].set_y(-0.1)
            
            ax2_period_text[k].set_fontsize(dbl_font_size)
            
            ax2_period_text[k].set_text(r'Period' + '\n' + str(k+1))
            
        if dbl_font_size < 4:
            
            # clear all text
            for k in ax2_period_text:
            
                k.set_text('')
            
    else:
        
        # clear all text
        for k in ax2_period_text:
        
            k.set_text('')

        
    # update ax2 plots
    ax2_alpha_vs_time.set_xdata(time[0:item])
    
    ax2_alpha_vs_time.set_ydata(alpha_vector[0:item])
    
    ax2_beta_vs_time.set_xdata(time[0:item])
    
    ax2_beta_vs_time.set_ydata(beta_vector[0:item])
    
    # update ax2 helping lines
    ax2_alpha_help_line.set_xdata([0, time[item]])
    ax2_alpha_help_line.set_ydata([alpha_vector[item], alpha_vector[item]])
    
    ax2_beta_help_line.set_xdata([0, time[item]])
    ax2_beta_help_line.set_ydata([beta_vector[item], beta_vector[item]])

    # update ax3 period helping lines    
    if (dbl_period_park != 0):
        # clear all lines
        for j in ax3_period_lines:
        
            j.set_xdata([])
            j.set_ydata([])
        
        # draw all lines
        for j in np.arange(0, round(dbl_base_period/dbl_period_park), 1):
            
            ax3_period_lines[j].set_xdata([(j+1)*dbl_period_park, (j+1)*dbl_period_park])
            ax3_period_lines[j].set_ydata([ylim_min, ylim_max])
            
    else:
        # clear all lines
        for j in ax3_period_lines:
        
            j.set_xdata([])
            j.set_ydata([])
            
    # update ax3 period helping text
    if (dbl_period_park != 0):
        
        # clear all text
        for k in ax3_period_text:
        
            k.set_text('')
        
        # set all text
        for k in np.arange(0, round(dbl_base_period/dbl_period_park), 1):
            
            ax3_period_text[k].set_x((k+1)*dbl_period_park - 0.02e-2)
            ax3_period_text[k].set_y(-0.1)
            
            ax3_period_text[k].set_fontsize(dbl_font_size)
            
            ax3_period_text[k].set_text(r'Period' + '\n' + str(k+1))
            
        if dbl_font_size < 4:
            
            # clear all text
            for k in ax3_period_text:
            
                k.set_text('')
            
    else:
        # clear all text
        for k in ax3_period_text:
        
            k.set_text('')
           
    # update ax3 plots
    ax3_d_vs_time.set_xdata(time[0:item])
    
    ax3_d_vs_time.set_ydata(d_vector[0:item])
    
    ax3_q_vs_time.set_xdata(time[0:item])
    
    ax3_q_vs_time.set_ydata(q_vector[0:item])
    
    # update ax3 helping lines    
    int_remainder = np.mod(dbl_harmonic_order, 3)
    
    str_ax1_pll_locked_on = (r'$The \ PLL \ is \ locked \ on,$'
                             + '\n' 
                             + (r'$thus \ the \ d \ axis \ is \ aligned \ with' 
                                + '\ the \ input \ harmonic$'))
    
    str_ax3_pll_locked_on = (r'$The \ PLL \ is \ locked \ on,$'
                             + '\n' 
                             + r'$thus \ the \ d \ and \ q \ components \ are \ DC$')
    
    # if positive sequences and PLL locked on
    if (int_remainder == 1) and ((dbl_harmonic_order - dbl_pll_order) == 0):
        ax3_d_help_line.set_xdata(0)
        ax3_d_help_line.set_ydata(0)
        
        ax3_q_help_line.set_xdata(0)
        ax3_q_help_line.set_ydata(0)
        
        ax1_text_pll_locked.set_text(str_ax1_pll_locked_on)
        ax3_text_pll_locked.set_text(str_ax3_pll_locked_on)
        
    # if negative sequnces and PLL locked on
    elif (int_remainder == 2) and ((dbl_harmonic_order + dbl_pll_order) == 0):
        ax3_d_help_line.set_xdata(0)
        ax3_d_help_line.set_ydata(0)
        
        ax3_q_help_line.set_xdata(0)
        ax3_q_help_line.set_ydata(0)
        
        ax1_text_pll_locked.set_text(str_ax1_pll_locked_on)
        ax3_text_pll_locked.set_text(str_ax3_pll_locked_on)   
        
    # if zero sequence
    elif (int_remainder == 0):
        ax3_d_help_line.set_xdata(0)
        ax3_d_help_line.set_ydata(0)
        
        ax3_q_help_line.set_xdata(0)
        ax3_q_help_line.set_ydata(0)
        
        ax1_text_pll_locked.set_text('')
        ax3_text_pll_locked.set_text('')
        
    # if other conditions (not locked on and not zero sequences)
    else:
        ax3_d_help_line.set_xdata([0, time[item]])
        ax3_d_help_line.set_ydata([d_vector[item], d_vector[item]])
        
        ax3_q_help_line.set_xdata([0, time[item]])
        ax3_q_help_line.set_ydata([q_vector[item], q_vector[item]])
        
        ax1_text_pll_locked.set_text('')
        ax3_text_pll_locked.set_text('')
    
    # return, the order of return affects the layers
    return (
            tuple(ax2_period_lines) 
            + 
            tuple(ax2_period_text) 
            + tuple(ax3_period_lines) 
            + tuple(ax3_period_text) 
            + (ax1_text_info, ax1_text_pll_locked,
               ax1_d_ax_pos,
               ax1_d_ax_neg, ax1_d_label,
               ax1_q_ax_pos, ax1_q_ax_neg, ax1_q_label,
               ax1_help_line_alpha, ax1_help_line_beta, 
               ax1_help_line_d, ax1_help_line_q,
               ax1_ellipse,
               ax1_alpha_arrow, 
               ax1_beta_arrow, 
               ax1_harmonic_arrow,
               ax1_d_vector_arrow, ax1_q_vector_arrow,
               ax1_origin, 
               ax2_alpha_vs_time, ax2_beta_vs_time,             
               ax2_alpha_help_line, ax2_beta_help_line,
               ax3_d_vs_time, ax3_q_vs_time,
               ax3_d_help_line, ax3_q_help_line,
               ax3_text_pll_locked))
    
# =============================================================================
# </Function: updates for animation>    
# =============================================================================


# =============================================================================
# <Function: make the animation>
# =============================================================================
    
def make_ani(locFig, locInt_samples, locInt_fps):
    """
    .. _make_ani :
    
    This function is a wrapper for matplotlib's "animation.FuncAnimation".
    
    Reference for using "lambda" : https://goo.gl/zDmGPR

    Parameters
    ----------
    locFig : matplotlib figure object
        The matplotlib figure object to be animated.
        
    locInt_samples : int
        The total number of samples. Equal to the total frames of the animation.    
        
    locInt_fps : int
        The frame per second for the anmation. Note that higher frame may not be
        realised due to intense computation in real time.
            
    Returns
    -------
    locAnim : matplotlib animation object
        The animation object return by "animation.FuncAnimation".

    Examples
    --------
    
    .. code:: python
    
        ani = make_ani(fig_main, int_samples, int_fps)
    """
    
    try:
        
        locInt_samples = round(locInt_samples)
        
        locInt_samples = abs(locInt_samples)
        
        if locInt_samples <=0:
            
            locInt_samples = 1
            
        else:
            
            locInt_samples = locInt_samples
            
    except:
        
        locInt_samples = 1
        
        pass
                
    
    try:
        
        locInt_fps = round(locInt_fps)
    
        locInt_fps = abs(locInt_fps)
    
        if locInt_fps <= 0:
        
            locInt_fps = 30
        
        else:
        
            locInt_fps = locInt_fps
            
    except:
        
        locInt_fps = 30
        
        pass
    
    locAnim = animation.FuncAnimation(locFig, animate, np.arange(0, locInt_samples, 1), 
                              interval=1/locInt_fps*1e3, blit=True, init_func=init)

    return locAnim

# =============================================================================
# </Function: make the animation>
# =============================================================================


ani = make_ani(fig_main, int_samples, int_fps)


# =============================================================================
# <Function: "Play" button on_clicked event handler>
# =============================================================================

def video_play_on_clicked(event):
    
    """
    .. _video_play_on_clicked :
    
    This function refresh the animation according to current user configurations.
    
    Reference for using "lambda" : https://goo.gl/zDmGPR

    Parameters
    ----------
    event : event
        The event that trigger this function.
                
    Returns
    -------
    None

    Examples
    --------
    
    .. code:: python
    
        button_play.on_clicked(video_play_on_clicked)
    """
    
    # I know globals are not good but I haven't found other ways to update the
    # animation
    global str_ini_file_path
    
    global dbl_base_freq, dbl_base_period
    global int_samples, dbl_harmonic_order, dbl_pll_order, int_fps
    
    global time, theta
    global alpha_vector, beta_vector
    global d_vector, q_vector
    global d_ax_on_x, d_ax_on_y
    global q_ax_on_x, q_ax_on_y
    global d_vector_on_x, d_vector_on_y
    global q_vector_on_x, q_vector_on_y
    
    global str_freq_harmonic
    global str_freq_clarke 
    global str_freq_park 
    global dbl_period_clarke
    global dbl_period_park
    
    global str_freq_pll
    
    global ylim_min, ylim_max
    
    global ax2
    global ax3
    
    global fig_main
    global ani
    
    global list_textbox
    global textbox_input_harmonic, textbox_pll_order
    global textbox_samples, textbox_fps, textbox_base_freq, textbox_ffmpeg_path
    
    # stop the animation
    ani.event_source.stop()
    
    
    try:
        
        dbl_harmonic_order = float(textbox_input_harmonic.text)
    
        dbl_harmonic_order = abs(dbl_harmonic_order)
        
    except ValueError:  
        
        locRoot = tk.Tk()
    
        locRoot.withdraw()
        
        msgbox.showerror('Not a float', 
                         r'This input must be a float.' 
                         + '\n' 
                         + r'Absolute values are taken for negative numbers')
        
        locRoot.destroy()
        
        textbox_input_harmonic.set_val('')
                
        return None
    
    if np.mod(dbl_harmonic_order, 3) == 0:
        
        locRoot = tk.Tk()
    
        locRoot.withdraw()
        
        msgbox.showerror('Zero sequences need 3D coordinates', 
                         'You have selected a zero sequence,' 
                         + '\n' 
                         + 'whose alpha, beta, d and q components' 
                         + '\n' 
                         + 'are zero.')
        
        locRoot.destroy()
        
        return None
    
    try:
       
        dbl_pll_order = float(textbox_pll_order.text)   
        
    except ValueError:
        
        locRoot = tk.Tk()
    
        locRoot.withdraw()
        
        msgbox.showerror('Not a float', 
                         'This input must be a float')
        
        locRoot.destroy()
        
        textbox_pll_order.set_val('')
                        
        return None
    
    try:
        
        int_samples = int(textbox_samples.text)
        
    except:
        
        print(date_time_now() + 'Sampling points exception')
        
        int_samples = 200
                
        pass
    
    try:
        
        int_fps = int(textbox_fps.text)
        
    except:
        
        print(date_time_now() + 'FPS exception')
        
        int_fps = 30
        
        pass
    
    
    try:
        
        dbl_base_freq = float(textbox_base_freq.text)
        
        dbl_base_freq = abs(dbl_base_freq)
        
        if dbl_base_freq <= 0:
            
            dbl_base_freq = 50
            
        else:
            
            dbl_base_freq = dbl_base_freq
            
        dbl_base_period = 1 / dbl_base_freq
        
    except:
        
        dbl_base_freq = 50
        
        dbl_base_period = 1 / dbl_base_freq
        
        pass
            
    # make the data again
    (time, theta, 
     alpha_vector, beta_vector, 
    d_vector, q_vector,
    d_ax_on_x, d_ax_on_y, 
    q_ax_on_x, q_ax_on_y, 
    d_vector_on_x, d_vector_on_y, 
    q_vector_on_x, q_vector_on_y) = cal_ABDQ(int_samples, dbl_base_freq, 
                                                dbl_harmonic_order, 
                                                dbl_pll_order)
    
    (str_freq_harmonic, 
     str_freq_clarke, 
     str_freq_park, 
     dbl_period_clarke, 
     dbl_period_park) = find_sequences(dbl_base_freq, dbl_harmonic_order, dbl_pll_order)
    
    # find the maximum of all data points
    ylim_max = max(max(alpha_vector), max(beta_vector), max(d_vector), max(q_vector)) + 0.05
    
    ylim_min = -1 * ylim_max
    
    str_freq_pll = find_pll_direction(dbl_base_freq, dbl_pll_order)
    
    ax1_text_freq_harmonic.set_text(str_freq_harmonic)
    
    ax1_text_freq_pll.set_text(str_freq_pll)
      
    ax2.set_xlim([0, dbl_base_period])
    ax2.set_ylim([ylim_min, ylim_max])
    
    ax2Legend.set_title(str_freq_clarke)
    
    ax3.set_xlim([0, dbl_base_period])
    ax3.set_ylim([ylim_min, ylim_max])
    
    ax3Legend.set_title(str_freq_park)
    
    ani = make_ani(fig_main, int_samples, int_fps)    
    
    # play the animate
    ani.event_source.start()
    ani.event_source.stop()
    plt.pause(0.5)  # allow time to update
    ani.event_source.start()
        
    # save user configurations
    locStr_ini = collect_tb(list_textbox)   # collect all the content of the text boxes
    
    locStr_ini = '[User configurations]\n' + locStr_ini
    
    write_ini(str_ini_file_path, locStr_ini)    # write them to INI file
    
# =============================================================================
# </Function: "Play" button on_clicked event handler>
# =============================================================================


# =============================================================================
# <Function: "Stop" button on_clicked event handler>
# =============================================================================

def video_stop_on_clicked(event, locObj_animation):

    """
    .. _video_stop_on_clicked :
    
    This function stops the animation.
    
    Reference for using "lambda" : https://goo.gl/zDmGPR

    Parameters
    ----------
    event : event
        The event that triggers this function.
        
    locObj_animation : matplotlib animation object
        The animation to be stopped.
            
    Returns
    -------
    None

    Examples
    --------
    
    .. code:: python
    
        # Ref : https://goo.gl/zDmGPR         

        button_stop.on_clicked(lambda x: video_stop_on_clicked(x, ani))
    """
    # stop the animate
    locObj_animation.event_source.stop()

# =============================================================================
# </Function: "Stop" button on_clicked event handler>
# =============================================================================

    
# =============================================================================
# <Function: "Save video" button on_clicked event handler>    
# =============================================================================

def video_save_on_clicked(event, locObj_animation, 
               locTextbox_fps, locTextbox_ffmpeg_path, 
               locList_textbox, locList_button, locIni_file_path):
    
    """
    .. _video_save_on_clicked :
    
    This function saves the animation to the harddrive.
    
    If the given FFmpeg's path is not valid, a file dialogue would prompted to 
    allow the user to select the FFmpeg's exectuable binary.
    
    A file dialogue would be prompted to allow user to save the video.
    
    The animation object's figure would be closed during save. Limited saving
    progress info would be printed to the console.
    
    After the video is saved, the script would try to restart if it is run in 
    "python.exe" (run rom terminal or cmd). If this script is run in IDLE 
    (run by "pythonw.exe"), then you need to manually restart the script 
    (otherwise the kernel is very likely to crash).
    
    Reference for using "lambda" : https://goo.gl/zDmGPR

    Parameters
    ----------
    event : event
        The event that triggers this function.
        
    locObj_animation : matplotlib animation object
        The animation to be saved.
        
    locTextbox_fps : int
        The frame per second for the anmation. This parameter would be passed
        to the video writer.
        
    locTextbox_ffmpeg_path : str
        Path of FFmepg executable binary.
    
    locList_textbox : list of matplotlib textbox objects
        These textboxes would be hidden.
    
    locList_button : list of matplotlib button objects
        These buttons would be hidden.
    
    locIni_file_path : str
        The INI file path to be used to save user configurations.
            
    Returns
    -------
    None.

    Examples
    --------
    
    .. code:: python
    
        button_save_video.on_clicked(lambda x: video_save_on_clicked(x, 
                                                                     ani, 
                                                                     textbox_fps,
                                                                     textbox_ffmpeg_path, 
                                                                     list_textbox, 
                                                                     list_button, 
                                                                     str_ini_file_path))
    """
     
    # prompt save video message box, yes/no
    
    locStr_message = ('Do you want to save the video?' 
                      + '\n' + 'This will take a while.'
                      + '\n' + 'Only limited progress info will be printed to the console.'
                      + '\n' + 'You have to wait.'
                      + '\n' 
                      + '\n' + 'You will get a message when finished.'
                      + '\n' 
                      + '\n' + 'Also, you may need to restart the script afterwards.')
    
    locRoot = tk.Tk()
    
    locRoot.withdraw()
    
    locBool_save = msgbox.askyesno('Save video', locStr_message)
    
    locRoot.destroy()
        
    # if yes, save the video
    if locBool_save == True:
                
        try:
            
            locInt_fps = int(locTextbox_fps.text)
            
            locInt_fps = abs(locInt_fps)
            
            if locInt_fps <= 0:
                
                locInt_fps = 30
                
            else:
                
                pass
            
        except:
            
            print(date_time_now() + 'FPS exception')
            
            locInt_fps = 30
            
            pass
        
        locStr_ffmpeg_path = locTextbox_ffmpeg_path.text
        
        if os.path.isfile(locStr_ffmpeg_path) == False:
            
            locRoot = tk.Tk()
            
            locRoot.withdraw()
            
            locStr_ffmpeg_path = load_ffmpeg()
            
            locRoot.destroy()
        
            locTextbox_ffmpeg_path.set_val(locStr_ffmpeg_path)
            
        
        if os.path.isfile(locStr_ffmpeg_path) == False:
            
            locRoot = tk.Tk()
    
            locRoot.withdraw()
            
            msgbox.showerror('Cannot find "ffmpeg.exe"', 'ffmpeg.exe NOT found')
            
            locRoot.destroy()
                                    
            return None
                
        plt.rcParams['animation.ffmpeg_path'] = locStr_ffmpeg_path
        
        locFFwriter = animation.FFMpegWriter(fps=locInt_fps, extra_args=['-vcodec', 'libx264'])
        
        # save user configurations
        locStr_ini = collect_tb(locList_textbox)   # collect all the content of the text boxes
        
        locStr_ini = '[User configurations]\n' + locStr_ini
        
        # write them to INI file
        write_ini(locIni_file_path, locStr_ini)   
        
        # hide text box       
        for item in locList_textbox:
            
            print(date_time_now() + 'Hiding textboxes')
            
            item.ax.patch.set_visible(False)
            item.text_disp.set_visible(False)
            item.label.set_visible(False)
            item.ax.axis('off')
        
        # hide buttons        
        for item in locList_button:
            
            print(date_time_now() + 'Hiding buttons')
            
            item.ax.patch.set_visible(False)
            item.label.set_visible(False)
            item.ax.axis('off')
        
        plt.close(locObj_animation._fig)
        
        # save the animate
        locRoot = tk.Tk()
        
        locRoot.withdraw()
        
        locStr_video_path = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                         title="Save video as",
                                                         filetypes = (("Mpeg 4 files","*.mp4"),
                                                                      ("all files","*.*")))
        
        locRoot.destroy()
        
        # if cancelled
        if len(locStr_video_path) == 0:
            
            print(date_time_now() + 'Save cancelled')
            
            return None
        
        if (locStr_video_path.endswith('.mp4') == True) or (locStr_video_path.endswith('.MP4') == True):
            
            pass
            
        else:
            
            locStr_video_path = locStr_video_path + '.mp4'
            
        locStr_video_temp_path = (locStr_video_path + '_temp_'
                                  + str(int(np.random.rand() * 1e12)) 
                                  + '.mp4')
        
        # this thread checks whether the video is saved or not
        thread_checker = threading.Thread(target=check_file_saved, 
                                          args=(locStr_video_path,))
        
        try:
            
            print(date_time_now() + 'Start saving video')
            
            thread_checker.start()
            
            save_animation_to_disk(locObj_animation, 
                                   locStr_video_temp_path,
                                   locStr_video_path,
                                   locFFwriter)
            
        except:
            
            locRoot = tk.Tk()
    
            locRoot.withdraw()
            
            msgbox.showerror('Fatal error', 'Fatal error while trying to save video')
            
            locRoot.destroy()
                       
            return None
        
        
        # get the absolute path of the executable binary for the Python interpreter
        locTemp_py_terminal = sys.executable
        
        # get the index of the last system path separator, i.e., on Windows, it's "\"; on Linux, it's '/'
        locTemp_index = locTemp_py_terminal.rfind(os.sep)
        
        # get the Python interpreter executable binary's file name
        locTemp_py_terminal = locTemp_py_terminal[(locTemp_index + 1):]
        
        # if running in IDLE or similar, do not restart, because the kernel would die
        if locTemp_py_terminal == 'pythonw.exe':
            
            print(date_time_now() + 'Ended. To restart, rerun the script.')
        
        # if running in terminal, try to restart (this is only guess work)
        else:
            
            print(date_time_now() + 'Trying to restart script')
            
            locTemp_python = sys.executable
            
            os.execl(locTemp_python, locTemp_python, * sys.argv)
        
                
    # if no, resume playing        
    else:
        
        locObj_animation.event_source.start()       

# =============================================================================
# </Function: "Save video" button on_clicked event handler>    
# =============================================================================


# =============================================================================
# <Function: "Help" button on_clicked event handler>
# =============================================================================

def help_on_clicked(event, locFig_help):
    
    """
    .. _help_on_clicked :
    
    This function triggers the help figure to be displayed.
    
    Reference for using "lambda" : https://goo.gl/zDmGPR

    Parameters
    ----------
    event : event
        The event that triggers this function.
        
    locFig_help : matplotlib figure
        The figure to be display. This is bascially a simple hack. 
        I put a serise of strings into a maplotlib textbox and put that textbox
        into the help figure. When this help figure is displayed, the user would
        see the help text.
            
    Returns
    -------
    None.

    Examples
    --------
    
    .. code:: python
    
        button_help.on_clicked(lambda x: help_on_clicked(x, fig_help))
    """
    
    locFig_help.show()

# =============================================================================
# </Function: "Help" button on_clicked event handler>      
# =============================================================================
    
# =============================================================================
# <Function: "DOCT" button on_clicked event handler>
# =============================================================================

def doct_on_clicked(event, locStr_doct_filename):
    
    """
    .. _doct_on_clicked :
    
    This function calls the function "search_file_and_start" to try to open the 
    documentation file.
    
    Reference for using "lambda" : https://goo.gl/zDmGPR

    Parameters
    ----------
    event : event
        The event that triggers this function.
        
    locStr_doct_filename : str
        The documentation filename (with extension)
            
    Returns
    -------
    bool
        Returns True if documentation file found. Returns False if documentation
        file not found.

    Examples
    --------
    
    .. code:: python
    
        button_doct.on_clicked(lambda x: doct_on_clicked(x, CONST_STR_DOCT_FILENAME))
    """
    
    print(date_time_now() + 'The documentation file is "' + locStr_doct_filename + '"')
    
    int_index = locStr_doct_filename.rfind('.')
        
    if int_index != (-1):
        
        str_extent = locStr_doct_filename[(int_index + 1):]
        
        str_pattern = '.' + os.sep + '**' + os.sep + '*.' + str_extent
        
    else:
        
        str_pattern = '.' + os.sep + '**' + os.sep + '*.*'

    print(date_time_now() + 'Looking for the documentation')
    
    bool_found = search_file_and_start(str_pattern, locStr_doct_filename)
    
    if bool_found == True:
        
        print(date_time_now() + 'Documentation found')
        
        return True
        
    else:
            
        locRoot = tk.Tk()
         
        locRoot.withdraw()
         
        msgbox.showerror('File not found', 'Documentation file not found')
         
        locRoot.destroy()  
         
        print(date_time_now() + 'Documentation not found')
         
        return False
    
# =============================================================================
# </Function: "DOCT" button on_clicked event handler>      
# =============================================================================

        
# =============================================================================
# <Function: "Browse" button on_clicked event handler>
# =============================================================================

def load_ffmpeg_on_clicked(event, locObj_animation, locTextbox):
    
    """
    .. _load_ffmpeg_on_clicked :
    
    This function calls the "load_ffmpeg" function to load the FFmpeg exectuable
    binary.
    
    Reference for using "lambda" : https://goo.gl/zDmGPR

    Parameters
    ----------
    event : event
        The event that triggers this function.
        
    locObj_animation : matplotlib animation object
        Used to stop/start the animation.
        
    locTextbox :  matplotlib textbox object
        Textbox used to display the FFmpeg exectutable binary's path.
            
    Returns
    -------
    None.

    Examples
    --------
    
    .. code:: python
    
        button_browse.on_clicked(lambda x: load_ffmpeg_on_clicked(x, ani,
                                                                  textbox_ffmpeg_path))
    """
    
    locObj_animation.event_source.stop()

    locStr_ffmpeg_path = load_ffmpeg()
    
    locTextbox.set_val(locStr_ffmpeg_path)
    
    locObj_animation.event_source.start()    

# =============================================================================
# </Function: "Browse" button on_clicked event handler>
# =============================================================================


# =============================================================================
# <Button on_clicked event definitions>
# =============================================================================

# https://goo.gl/zDmGPR         
       
button_play.on_clicked(video_play_on_clicked)

button_stop.on_clicked(lambda x: video_stop_on_clicked(x, ani)) 

button_save_video.on_clicked(lambda x: video_save_on_clicked(x,
                                                             ani,
                                                             textbox_fps,
                                                             textbox_ffmpeg_path, 
                                                             list_textbox, list_button, 
                                                             str_ini_file_path))

button_help.on_clicked(lambda x: help_on_clicked(x, fig_help))

button_doct.on_clicked(lambda x: doct_on_clicked(x, CONST_STR_DOCT_FILENAME))

button_browse.on_clicked(lambda x: load_ffmpeg_on_clicked(x, ani,                                                            
                                                          textbox_ffmpeg_path))

# =============================================================================
# </Button on_clicked event definitions>
# =============================================================================


# this needs to be the last line
plt.show()