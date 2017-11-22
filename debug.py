# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 16:03:51 2017

@author: BachDesktop
"""

import numpy as np
import matplotlib as mpl

#import cmath

import matplotlib.pyplot as plt

from gsyTransforms import cal_symm, cal_clarke, cal_park

from numpy import pi, sin, cos, sqrt

# matplotlib setup
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['text.usetex'] = True
#mpl.rcParams['text.latex.preview'] = True
mpl.rcParams['text.latex.preamble'] = [r'\boldmath']
mpl.rcParams['font.weight'] = 'bold'

time_end = 0.08

time = np.linspace( 0, time_end, (10 ** 5) )

# angular freq
omega = 2 * np.pi * 50

theta = omega * time

n = 1.3

phase_a = n * (theta) 
phase_b = n * (theta - (2 / 3 * pi)) 
phase_c = n * (theta + (2 / 3 * pi)) 

a = ( cos(phase_a) + 1j * sin(phase_a) ) * 1.7

b = ( cos(phase_b) + 1j * sin(phase_b) ) * 1.2

c = ( cos(phase_c) + 1j * sin(phase_c) ) * 2.8

a_pos, b_pos, c_pos, a_neg, b_neg, c_neg, zero = cal_symm(a, b, c)

plt.subplot(411)

plt.plot(time, a, color='r')
plt.plot(time, b, color='g')
plt.plot(time, c, color='b')

ylim_max =  3
ylim_min = -1 * ylim_max


plt.xlim([0, time_end])
plt.ylim([ylim_min, ylim_max])

plt.grid(True)

plt.subplot(412)

plt.plot(time, a_pos, color='r')
plt.plot(time, b_pos, color='g')
plt.plot(time, c_pos, color='b')

plt.xlim([0, time_end])
plt.ylim([ylim_min, ylim_max])

plt.grid(True)

plt.subplot(413)

plt.plot(time, a_neg, color='r')
plt.plot(time, b_neg, color='g')
plt.plot(time, c_neg, color='b')

plt.xlim([0, time_end])
plt.ylim([ylim_min, ylim_max])

plt.grid(True)

plt.subplot(414)

plt.plot(time, zero)

plt.xlim([0, time_end])
plt.ylim([ylim_min, ylim_max])

plt.grid(True)

plt.show()

# =============================================================================
# quad = np.exp(-1j * np.pi/2)
# 
# alpha, beta, zero = cal_clarke(a, b, c)
# 
# d, q, zero = cal_park(theta, alpha, beta, zero)
# 
# alpha_pos = 1/2 * (alpha - beta * quad)
# 
# beta_pos = 1/2 * (alpha * quad + beta)
# 
# alpha_neg = 1/2 * (alpha + beta * quad)
# 
# beta_neg = 1/2 * (-alpha * quad + beta)
# 
# d_pos = cos(theta) * alpha_pos + sin(theta) * beta_pos
# 
# q_pos = -sin(theta) * alpha_pos + cos(theta) * beta_pos
# 
# d_neg = cos(theta) * alpha_neg + sin(theta) * beta_neg
# 
# q_neg = -sin(theta) * alpha_neg + cos(theta) * beta_neg
# 
# mod_alpha = abs(alpha)[0]
# 
# mod_beta = abs(beta)[0]
# 
# mod_zero = abs(zero)[0]
# 
# fig = plt.figure(figsize=(900.0/100.0, 900.0/100.0), dpi = 100.0)
# 
# ax = plt.subplot(111, projection='polar')
# 
# ax.plot(theta, abs(alpha), lw=3, color='r', 
#         label=(r'$\alpha, \ ' + 'Magnitude = ' + '{0:.4f}'.format(mod_alpha) + '$'))
# 
# ax.plot(theta, abs(beta), lw=3, color='g', 
#         label=(r'$\beta, \ ' + 'Magnitude = ' + '{0:.4f}'.format(mod_beta) + '$'))
# 
# ax.plot(theta, abs(zero), lw=3, color='b', 
#         label=(r'$Zero, \ ' + 'Magnitude = ' + '{0:.4f}'.format(mod_zero) + '$'))
# 
# ax.set_rmax(1.2)
# 
# ax.set_rticks(np.arange(0.2, 1.6, 0.2))
# 
# ax.set_rlabel_position(-90)
# 
# ax.set_thetagrids(np.arange(0, 360, 45), frac=2.0)
# 
# ax.tick_params(axis='both', which='major', labelsize=15, pad=12)
# 
# ax.legend(loc='upper right', fontsize=12, bbox_to_anchor=(1.1,1.12))
# =============================================================================

#plt.show()

#plt.polar(theta, abs(d), lw=5, color='k')

# =============================================================================
# plt.figure
# 
# plt.polar(theta, abs(d_pos), lw=5, color='r')
#  
# plt.polar(theta, abs(q_pos), lw=2, color='g')
#  
# plt.polar(theta, abs(d_neg), lw=1, color='pink')
#  
# plt.polar(theta, abs(q_neg), lw=1, color='lime')
# 
# =============================================================================
#plt.figure
#
#plt.plot(time, d, color='k', lw=5)
#
#plt.plot(time, d_pos, color='r')
#plt.plot(time, d_neg, color='g')

# =============================================================================
# plt.polar(theta, abs(alpha_pos), lw=5, color='r')
# 
# plt.polar(theta, abs(beta_pos), lw=2, color='g')
# 
# plt.polar(theta, abs(alpha_neg), lw=5, color='pink')
# 
# plt.polar(theta, abs(beta_neg), lw=2, color='lime')
# =============================================================================

#plt.plot(time, alpha, time, beta)
#
#plt.plot(beta.real, beta.imag)

#plt.plot(v_pos.real, v_pos.imag, lw=2, color='red')
#
#plt.plot(v_neg.real, v_neg.imag, lw=2, color='g')


# =============================================================================
# # base phases of the 3-phase inputs, note, base phases only
# phase_a = theta
# phase_b = theta - (2 / 3 * pi)
# phase_c = theta + (2 / 3 * pi)
# 
# # 3-phase inputs
# input_a = cos(3.7 * phase_a)
# input_b = cos(3.7 * phase_b)
# input_c = cos(3.7 * phase_c)
# 
# # amplitude invariant Clarke transform
# alpha, beta, zero = cal_clarke(input_a, input_b, input_c)
# 
# r = sqrt(alpha**2 + beta**2)
# 
# plt.polar(omega*time, r, lw=5)
# =============================================================================

#import numpy as np
#import matplotlib.pyplot as plt

# =============================================================================
# from gsyTransforms import cal_clarke, cal_park
# 
# def draw_park(dbl_har_order, dbl_pll_order=1, dbl_base_freq=50, dbl_cycle=4, 
#                 bool_savefig=False, int_dpi=600, str_fig_path=''):
#     
#     # import modules
#     import matplotlib as mpl
#     import matplotlib.pyplot as plt
#     import numpy as np
#     import os
#     
#     from numpy import pi, cos
#     from gsyDqLib import date_time_now
#     
#     # matplotlib setup
#     mpl.rcParams['font.family'] = 'serif'
#     mpl.rcParams['text.usetex'] = True
#     mpl.rcParams['text.latex.preview'] = True
#     mpl.rcParams['text.latex.preamble'] = [r'\boldmath']
#     mpl.rcParams['font.weight'] = 'bold'
#     
# 
#     # =============================================================================
#     # <Process input arguments>    
#     # =============================================================================
#     # process input harmonic order
#     try:
#         
#         dbl_har_order = float(dbl_har_order)    
#         
#         if dbl_har_order != 0:
#             
#             dbl_har_order = abs(dbl_har_order)
#             
#         else:
#             
#             dbl_har_order = 1
#             
#             print(date_time_now() + ' Invalid harmoinc order. Harmonic order set to 1')
#             
#     except:
#         
#         dbl_har_order = 1
#         
#         print(date_time_now() + ' Invalid harmoinc order. Harmonic order set to 1')
#         
#         pass
#     
#     # process PLL order
#     try:
#         
#         dbl_pll_order = float(dbl_pll_order)
#         
#     except:
#         
#         dbl_pll_order = 1.0
#         
#         print(date_time_now() + ' Invalid PLL order. PLL order set to 1')
#         
#         pass
#     
#     # process base frequency
#     try:
#         
#         dbl_base_freq = float(dbl_base_freq)
#         
#         if dbl_base_freq != 0:
#             
#             dbl_base_freq = abs(dbl_base_freq)
#             
#         else:
#             
#             dbl_base_freq = 50.0
#             
#             print(date_time_now() + ' Invalid base frequency. Base frequency set to 50')        
#     
#     except:
#         
#         dbl_base_freq = 50.0
#             
#         print(date_time_now() + ' Invalid base frequency. Base frequency set to 50') 
#         
#         pass
#     
#     # process how many cycles to display
#     try:
#         
#         dbl_cycle = float(dbl_cycle)
#         
#         if dbl_cycle != 0:
#             
#             dbl_cycle = abs(dbl_cycle)
#             
#         else:
#             
#             dbl_cycle = 4
#             
#             print(date_time_now() + ' Invalid display cycles. Set display cycles to 4')        
#         
#     except:
#         
#         dbl_cycle = 4
#             
#         print(date_time_now() + ' Invalid display cycles. Set display cycles to 4')        
#         
#         pass
#     
#     # process whether to save the figure
#     try:
#         
#         bool_savefig = bool(bool_savefig)
#         
#     except:
#         
#         bool_savefig = False
#             
#         pass
#     
#     # process dpi
#     try:
#         
#         int_dpi = int(int_dpi)
#         
#         if int_dpi != 0:
#             
#             int_dpi = int_dpi
#             
#         else:
#             
#             int_dpi = 600
#             
#             print(date_time_now() + ' Invalid dpi. Set dpi to 600') 
#         
#     except:
#         
#         int_dpi = 600
#             
#         print(date_time_now() + ' Invalid dpi. Set dpi to 600') 
#         
#         pass
#     
#     # process figure path
#     try:
#     
#         str_fig_path = str(str_fig_path)
#         
#         if bool_savefig == True:
#             
#             if len(str_fig_path) == 0:
#                 
#                 str_fig_path = 'Figure_' + str( int(np.random.rand() * 1e6) ) + '.png'
#                 
#                 str_fig_path = os.path.join(os.getcwd(), str_fig_path)
#                 
#             else:
#                 
#                 pass
#                 
#         else:
#             
#             pass
#         
#     except:
#         
#         str_fig_path = 'Figure_' + str( int(np.random.rand() * 1e6) ) + '.png'
#                 
#         str_fig_path = os.path.join(os.getcwd(), str_fig_path)
#         
#         print(date_time_now() + ' Invalid figure path. Set figure path to "' + str_fig_path + '"') 
#         
#         pass
#     # =============================================================================
#     # </Process input arguments>
#     # =============================================================================
#     
#     
#     # =============================================================================
#     # <Make data, titles, legends>    
#     # =============================================================================
#     int_remainder = np.mod(dbl_har_order, 3)
#     
#     dbl_base_period = 1 / dbl_base_freq
#         
#     time_end = dbl_base_period / dbl_har_order * dbl_cycle
#     
#     # time vector
#     time = np.linspace( 0, time_end, (10 ** 5) )
#     
#     # angular freq
#     omega = 2 * np.pi * dbl_base_freq
#     
#     theta = omega * time
#     
#     # base phases of the 3-phase inputs, note, base phases only
#     phase_a = theta
#     phase_b = theta - (2 / 3 * pi)
#     phase_c = theta + (2 / 3 * pi)
#     
#     # 3-phase inputs
#     input_a = cos(dbl_har_order * phase_a)
#     input_b = cos(dbl_har_order * phase_b)
#     input_c = cos(dbl_har_order * phase_c)
#     
#     # amplitude invariant Clarke transform
#     alpha, beta, zero = cal_clarke(input_a, input_b, input_c)
#     
#     # Park transform
#     d, q, zero = cal_park(theta * dbl_pll_order, alpha, beta, zero)
#     
#      # condition, coordinate 1 title
#     if int_remainder == 1:  # positive sequence
#     
#         str_ax1_title = ( r'$\textbf{Three-Phase Inputs, } \omega =2 \pi \times' 
#                          + str(dbl_har_order) + r'\times' + str(dbl_base_freq) 
#                          + r'\textbf{ (positive sequence)}$' )
#         
#     elif int_remainder == 2: # negative sequence
#         
#         str_ax1_title = ( r'$\textbf{Three-Phase Inputs, } \omega =2 \pi \times' 
#                          + str(dbl_har_order) + r'\times' + str(dbl_base_freq) 
#                          + r'\textbf{ (negative sequence)}$' )
#         
#     elif int_remainder == 0: # zero sequence
#         
#         str_ax1_title = ( r'$\textbf{Three-Phase Inputs, } \omega =2 \pi \times' 
#                          + str(dbl_har_order) + r'\times' + str(dbl_base_freq) 
#                          + r'\textbf{ (zero sequence)}$' )
#         
#     else:
#             
#         str_ax1_title = ( r'$\textbf{Three-Phase Inputs, } \omega =2 \pi \times' 
#                          + str(dbl_har_order) + r'\times' + str(dbl_base_freq) 
#                          + r'$' )    
#         
#     # coordinate 2 title
#     str_ax2_title = r'$\textbf{Outputs of the General Amplitude Invariant Clarke Transform}$'  
#     
#     if int_remainder == 1: # positive sequence
#         
#         str_ax2_title = (str_ax2_title 
#                          + r'$\textbf{\ (}$' 
#                          + r'$\alpha \textbf{ leads } \beta' 
#                          + r'\textbf{ by } 90^{\circ} \textbf{)}$')
#         
#     elif int_remainder == 2: # negative sequence
#         
#         str_ax2_title = (str_ax2_title 
#                          + r'$\textbf{\ (}$' 
#                          + r'$\alpha \textbf{ lags } \beta' 
#                          + r'\textbf{ by } 90^{\circ} \textbf{)}$')
#         
#     elif int_remainder == 0: # zero sequence
#         
#         str_ax2_title = str_ax2_title + r'$\ (\alpha = 0, \beta = 0)$'
#         
#     else:
#         
#         str_ax2_title = str_ax2_title
# 
#     # coordinate 3 title
#     str_ax3_title = r'\textbf{Outputs of the General Park Transform}'
#     
#     if int_remainder == 1: # positive sequence        
#         
#         if ( dbl_har_order - dbl_pll_order ) >= 0:
#             
#             str_ax3_title = (str_ax3_title 
#                              + r'$\textbf{\ (}$' 
#                              + r'$d \textbf{ leads } q' 
#                              + r'\textbf{ by } 90^{\circ}' 
#                              + r'\textbf{)}$,' 
#                              + '\n' + r'$\textbf{PLL is locked to (}' 
#                              + str(dbl_pll_order) 
#                              + r'\times' 
#                              + str(dbl_base_freq) 
#                              + r'\textbf{ Hz), } f_{dq}=' 
#                              + str(dbl_har_order - dbl_pll_order) 
#                              + r'\times 50 \textbf{ Hz}' 
#                              + r'$')
#                              
#         elif ( dbl_har_order - dbl_pll_order ) <= 0:
#             
#             str_ax3_title = (str_ax3_title 
#                              + r'$\textbf{\ (}$' 
#                              + r'$d \textbf{ lags } q' 
#                              + r'\textbf{ by } 90^{\circ}' 
#                              + r'\textbf{)}$,' 
#                              + '\n' + r'$\textbf{PLL is locked to (}' 
#                              + str(dbl_pll_order) 
#                              + r'\times' 
#                              + str(dbl_base_freq) 
#                              + r'\textbf{ Hz)}$')
#             
#         else:
#             
#             str_ax3_title = str_ax3_title
#         
#     elif int_remainder == 2: # negative sequence
#         
#         if ( dbl_har_order + dbl_pll_order ) >= 0:
#         
#             str_ax3_title = (str_ax3_title 
#                              + r'$\textbf{\ (}$' 
#                              + r'$d \textbf{ lags } q' 
#                              + r'\textbf{ by } 90^{\circ}' 
#                              + r'\textbf{)}$,' 
#                              + '\n' + r'$\textbf{PLL is locked to (}' 
#                              + str(dbl_pll_order) 
#                              + r'\times' 
#                              + str(dbl_base_freq) 
#                              + r'\textbf{ Hz), } f_{dq}=' 
#                              + str(dbl_har_order + dbl_pll_order) 
#                              + r'\times 50 \textbf{ Hz}' 
#                              + r'$')
#                              
#         elif ( dbl_har_order + dbl_pll_order ) <= 0:
#             
#             str_ax3_title = (str_ax3_title 
#                              + r'$\textbf{\ (}$' 
#                              + r'$d \textbf{ leads } q' 
#                              + r'\textbf{ by } 90^{\circ}' 
#                              + r'\textbf{)}$,' 
#                              + '\n' + r'$\textbf{PLL is locked to (}' 
#                              + str(dbl_pll_order) 
#                              + r'\times' 
#                              + str(dbl_base_freq) 
#                              + r'\textbf{ Hz), } f_{dq}=' 
#                              + str(dbl_har_order + dbl_pll_order) 
#                              + r'\times 50 \textbf{ Hz}' 
#                              + r'$')
#                              
#         else:
#             
#             str_ax3_title = str_ax3_title
#         
#     elif int_remainder == 0: # zero sequence
#         
#         str_ax3_title = str_ax3_title + r'$\ (d = 0, q = 0)$'
#         
#     else:
#         
#         str_ax3_title = str_ax3_title
#     
#     # legend labels for coordinate 1, 3-phase inputs
#     str_a_lbl = r'$a = cos(' + str(dbl_har_order) + r'\cdot \omega t)$'
#     str_b_lbl = r'$b = cos[' + str(dbl_har_order) + r'\cdot (\omega t - \frac{2}{3}\pi)]$'
#     str_c_lbl = r'$c = cos[' + str(dbl_har_order) + r'\cdot (\omega t + \frac{2}{3}\pi)]$'
#     
#     # legend labels for coordinate 2, Clarke transform
#     str_alpha_lbl = r'$\alpha = \frac{2}{3} (a - \frac{1}{2} b - \frac{1}{2} c)$'                 
#     
#     str_beta_lbl = r'$\beta = \frac{2}{3} ( 0 + \frac{\sqrt{3}}{2} b - \frac{\sqrt{3}}{2} c)$' 
#                         
#     str_zero_lbl = r'$Zero = \frac{2}{3} (\frac{1}{2} a + \frac{1}{2} b + \frac{1}{2} c)$' 
#     
#     # legend labels for coordinate 3, Park transform
#     str_d_lbl = r'$d = cos\theta \cdot \alpha - sin\theta \cdot \beta$'
#     
#     str_q_lbl = r'$q = -sin\theta \cdot \alpha + cos\theta \cdot \beta$'
#     # =============================================================================
#     # </Make data, titles, legends>    
#     # =============================================================================
#     
#     
#     # =============================================================================
#     # <Main figure setup>
#     # =============================================================================
#     # make main figure
#     fig = plt.figure(figsize=(900.0/100.0, 900.0/100.0), dpi = 100.0)
#     
#     # adjust spacing between subplots
#     fig.subplots_adjust(hspace=0.7)
#     
#     # <coordnate 1> =============================================================================
#     # make coordinate 1
#     ax1 = plt.subplot(3, 1, 1)
#     
#     # set coordinate 1 title
#     ax1.set_title(str_ax1_title, fontsize=14, fontweight='bold', y=1.2)
#     
#     # set coordinate 1 horizontal line
#     ax1.axhline(y=0, color='k', lw=3)
#     
#     # plot 3-phase inputs
#     ax1_input_a, = ax1.plot(time, input_a, color='r', lw=2, label=str_a_lbl)
#     ax1_input_b, = ax1.plot(time, input_b, color='g', lw=2, label=str_b_lbl)
#     ax1_input_c, = ax1.plot(time, input_c, color='b', lw=2, label=str_c_lbl)
#     
#     # get automatic y limits
#     y_min, y_max = ax1.get_ylim()
#     
#     # set limits and grid lines
#     plt.xlim([0, time_end])
#     plt.ylim([y_min, y_max])
#     plt.grid(True)
#     
#     # range arguments for ploting period helping lines
#     rng_start = dbl_base_period / dbl_har_order
#     rng_stop = time_end + rng_start
#     rng_step = rng_start
#     
#     # plot period helping lines
#     for item in np.arange(rng_start, rng_stop, rng_step):
#         
#         plt.plot([item, item], [y_min, y_max], 
#                  linestyle='--', linewidth=2, color='k')
#     
#     # set legend
#     ax1_lgd = plt.legend(handles=[ax1_input_a, ax1_input_b, ax1_input_c], 
#                          loc='upper center', fontsize=11, bbox_to_anchor=(0.5, 1.25), 
#                          shadow=False, fancybox=True, ncol=3)
#     
#     # set legend transparence
#     ax1_lgd.get_frame().set_alpha(0.9)
#     
#     # set y label
#     ax1.set_ylabel(r'\textbf{Amplitude}', fontweight='bold', fontsize=12)    
#     # </coordnate 1> =============================================================================
#     
#     # <coordnate 2> =============================================================================
#     # make coordinate 2
#     ax2 = plt.subplot(3, 1, 2)
#     
#     # set coordinate 2 title
#     ax2.set_title(str_ax2_title, fontsize=14, fontweight='bold', y=1.23)
#     
#     # plot coordinate 2 horizontal line
#     ax2.axhline(y=0, color='k', lw=3)
#     
#     # plot Clarke transform components
#     ax2_alpha, = ax2.plot(time, alpha, color='r', lw=2, label=str_alpha_lbl)
#     ax2_beta, = ax2.plot(time, beta, color='g', lw=2, label=str_beta_lbl)
#     ax2_zero, = ax2.plot(time, zero, color='b', lw=2, label=str_zero_lbl)
#     
#     # get automatic y limits
#     y_min, y_max = ax2.get_ylim()
#     
#     # set coordinate 2 limits
#     plt.xlim([0, time_end])
#     plt.ylim([y_min, y_max])
#     plt.grid(True)
#     
#     # plot period helping lines
#     for item in np.arange(rng_start, rng_stop, rng_step):
#         
#         plt.plot([item, item], [y_min, y_max], linestyle='--', linewidth=2, color='k')
#     
#     # set coordinate 2 legend
#     ax2_lgd = plt.legend(handles=[ax2_alpha, ax2_beta, ax2_zero], loc='upper center', 
#                          fontsize=11, bbox_to_anchor=(0.5, 1.27), 
#                          shadow=False, fancybox=True, ncol=3)
#     
#     # set legend transparence
#     ax2_lgd.get_frame().set_alpha(0.9)
#     
#     # set labels
#     ax2.set_ylabel(r'\textbf{Amplitude}', fontweight='bold', fontsize=12)
#     # </coordnate 2> =============================================================================
#     
#     # <coordnate 3> =============================================================================
#     ax3 = plt.subplot(3, 1, 3)
#     
#     # plot coordinate 3 horizontal line
#     ax3.axhline(y=0, color='k', lw=3)
#     
#     # set coordinate 3 title
#     ax3.set_title(str_ax3_title, fontsize=14, fontweight='bold', y=1.23)
#     
#     # plot Park transform components
#     ax3_d, = ax3.plot( time, d, color='orange', lw=2, label=str_d_lbl )
#     ax3_q, = ax3.plot( time, q, color='darkviolet', lw=2,label=str_q_lbl )
#     ax3_zero, = ax3.plot( time, zero, color='b', lw=2, label=str_zero_lbl )
#     
#     # get automatic y limits
#     y_min, y_max = ax3.get_ylim()
#     
#     # set coordinate 3 limits
#     plt.xlim([0, time_end])
#     plt.ylim([y_min, y_max])
#     plt.grid(True)
#     
#     # range arguments for ploting period helping lines
#     if int_remainder == 1:  # positive sequence
#                     
#         if (dbl_har_order - dbl_pll_order) != 0:
#                         
#             rng_start = dbl_base_period / (dbl_har_order - dbl_pll_order)
#             rng_stop = time_end + rng_start
#             rng_step = rng_start
#             
#         else:
#             
#             rng_start = 0
#             rng_stop = 0
#             rng_step = 0
#                         
#     elif int_remainder == 2: # negative sequence
#         
#         if (dbl_har_order + dbl_pll_order) != 0:
#         
#             rng_start = dbl_base_period / abs(dbl_har_order + dbl_pll_order)
#             rng_stop = time_end + rng_start
#             rng_step = rng_start
#             
#         else:
#             
#             rng_start = 0
#             rng_stop = 0
#             rng_step = 0
#         
#     elif int_remainder == 0: # zero sequence
#         
#         rng_start = 0
#         rng_stop = 0
#         rng_step = 0
#         
#     else:
#         
#         rng_start = 0
#         rng_stop = 0
#         rng_step = 0
#         
#         
#     # plot period helping lines
#     if all(x == 0 for x in (rng_start, rng_stop, rng_step)):
#         
#         pass
#     
#     else:
#     
#         for item in np.arange(rng_start, rng_stop, rng_step):
#             
#             plt.plot([item, item], [y_min, y_max], linestyle='--', linewidth=2, color='k')
#     
#     # set coordinate 3 legend
#     ax3_lgd = plt.legend(handles=[ax3_d, ax3_q, ax3_zero], loc='upper center', 
#                          fontsize=11, bbox_to_anchor=(0.5, 1.27), 
#                          shadow=False, fancybox=True, ncol=3)
#     
#     # set legend transparence
#     ax3_lgd.get_frame().set_alpha(0.9)
#     
#     # set xy labels
#     ax3.set_xlabel(r'\textbf{Time (s)}', fontweight='bold', fontsize=12)
#     ax3.set_ylabel(r'\textbf{Amplitude}', fontweight='bold', fontsize=12)    
#     # </coordnate 3> =============================================================================
#     
#     plt.show()
#     # =============================================================================
#     # </Main figure setup>
#     # =============================================================================
#     
#     
#     # =============================================================================
#     # <Condition, save figure>    
#     # =============================================================================
#     if bool_savefig == True:
#         
#         plt.tight_layout()
#         
#         fig.savefig(str_fig_path, dpi=int_dpi)
#         
#         plt.tight_layout()
#         
#         print( date_time_now() + 'Figure saved as:"' + str_fig_path + '"' ) 
#         
#         plt.close()
#         
#         
#     else:
#                 
#         pass    
#     # =============================================================================
#     # </Condition, save figure>    
#     # =============================================================================
#     
#     
#     
# draw_park(1.1, dbl_pll_order=1.1)
# =============================================================================

#time_end = 0.02
#    
## time vector
#time = np.linspace( 0, time_end, (10 ** 5) )
#
## angular freq
#omega = 2 * np.pi * 50.0
#
#theta = omega * time
#
## base phases of the 3-phase inputs, note, base phases only
#phase_a = theta
#phase_b = theta - (2 / 3 * np.pi)
#phase_c = theta + (2 / 3 * np.pi)
#
## 3-phase inputs
#input_a = np.cos(1.1 * phase_a)
#input_b = np.cos(1.1 * phase_b)
#input_c = np.cos(1.1 * phase_c)
#
## amplitude invariant Clarke transform
#alpha, beta, zero = cal_clarke(input_a, input_b, input_c)
#
#r= np.sqrt(alpha**2 + beta**2)
#
#plt.plot(r*np.cos(1.1*theta), r*np.sin(1.1*theta))
#
#plt.show()