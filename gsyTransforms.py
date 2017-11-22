# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 09:50:56 2017

@author: 212612902
"""

import numpy as np

from numpy import sqrt, sin, cos

# =============================================================================
# <Function: calculate the symmetrical components (Fortescue)>
# =============================================================================
def cal_symm(a, b, c):
    
    # 120 degree rotator
    ALPHA = np.exp(1j * 2/3 * np.pi)
        
    # positive sequence
    a_pos = 1/3 * ( a + b * ALPHA + c * (ALPHA ** 2) )
    
    b_pos = 1/3 * ( a * (ALPHA ** 2) + b + c * ALPHA )
    
    c_pos = 1/3 * ( a * ALPHA + b * (ALPHA ** 2) + c )
    
    # negative sequence
    a_neg = 1/3 * ( a + b * (ALPHA ** 2) + c * ALPHA )
    
    b_neg = 1/3 * ( a * ALPHA + b + c * (ALPHA ** 2) )
    
    c_neg = 1/3 * ( a * (ALPHA ** 2) + b * ALPHA + c )
    
    # zero sequence
    zero = 1/3 * (a + b + c)
    
    return a_pos, b_pos, c_pos, a_neg, b_neg, c_neg, zero

# =============================================================================
# </Function: calculate the symmetrical components (Fortescue)>
# =============================================================================


# =============================================================================
# <Function: calculate the amplitude invariant Clarke Transform>
# =============================================================================
def cal_clarke(a, b, c):
    
    alpha = 2/3 * ( a - 1/2 * (b + c) )
    
    beta = 2/3 * ( sqrt(3)/2 * (b - c) )
    
    zero = 2/3 * 1/2 * (a + b + c)
    
    return alpha, beta, zero
# =============================================================================
# </Function: calculate the amplitude invariant Clarke Transform>
# =============================================================================


# =============================================================================
# <Function: calculate the symmetrical components for the amplitude invariant Clarke Transform>
# =============================================================================
def cal_clarke_symm(a, b, c):
    
    # based on the DSOGI 
    
    QUAD = np.exp(-1j * np.pi/2)
    
    # calculate the Clarke components
    alpha, beta, zero = cal_clarke(a, b, c)
    
    # positive alpha and beta
    alpha_pos = 1/2 * ( alpha - beta * QUAD )
    
    beta_pos = 1/2 * ( alpha * QUAD + beta )
    
    # negative alpha and beta
    alpha_neg = 1/2 * ( alpha + beta * QUAD )
    
    beta_neg = 1/2 ( -1 * alpha * QUAD + beta )
    
    return alpha_pos, beta_pos, alpha_neg, beta_neg, zero
# =============================================================================
# </Function: calculate the symmetrical components for the amplitude invariant Clarke Transform>
# =============================================================================    


# =============================================================================
# <Function: calculate the Park Transform>
# =============================================================================
def cal_park(theta, alpha, beta, zero):
    
    # Park transform
    
    length_theta = len(theta)
    
    length_alpha = len(alpha)
    
    length_beta = len(beta)
    
    length_zero = len(zero)
    
    if all( x == length_theta for x in (length_theta, length_alpha, length_beta, length_zero) ):
        
        pass
    
    else:
        
        raise ValueError('Element length mismatch.'
                         + 'The length of theta, alpha, beta and zero must be all the same')    
    
    d = cos(theta) * alpha + sin(theta) * beta
    
    q = -sin(theta) * alpha + cos(theta) * beta
    
    zero = zero
    
    return d, q, zero
# =============================================================================
# </Function: calculate the Park Transform>
# =============================================================================
    

# =============================================================================
# def draw_clarke(dbl_har_order, dbl_base_freq=50, dbl_cycle=4, 
#                 mag_a=1, mag_b=1, mag_c=1,
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
#     # base phases of the 3-phase inputs, note, base phases only
#     phase_a = omega * time
#     phase_b = omega * time - (2 / 3 * pi)
#     phase_c = omega * time + (2 / 3 * pi)
#     
#     # 3-phase inputs
#     input_a = mag_a * cos(dbl_har_order * phase_a)
#     input_b = mag_b * cos(dbl_har_order * phase_b)
#     input_c = mag_c * cos(dbl_har_order * phase_c)
#     
#     # amplitude invariant Clarke transform
#     alpha, beta, zero = cal_clarke(input_a, input_b, input_c)
#     
#     # legend labels for the 3-phase inputs
#     str_a_lbl = r'$a = cos(' + str(dbl_har_order) + r'\cdot \omega t)$'
#     str_b_lbl = r'$b = cos[' + str(dbl_har_order) + r'\cdot (\omega t - \frac{2}{3}\pi)]$'
#     str_c_lbl = r'$c = cos[' + str(dbl_har_order) + r'\cdot (\omega t + \frac{2}{3}\pi)]$'
#     
#     # legend labels for the Clarke transform
#     str_alpha_lbl = r'$\alpha = \frac{2}{3} (a - \frac{1}{2} b - \frac{1}{2} c)$'                 
#     
#     str_beta_lbl = r'$\beta = \frac{2}{3} ( 0 + \frac{\sqrt{3}}{2} b - \frac{\sqrt{3}}{2} c)$' 
#                         
#     str_zero_lbl = r'$Zero = \frac{2}{3} (\frac{1}{2} a + \frac{1}{2} b + \frac{1}{2} c)$' 
#     
#     # condition, coordinate 1 title
#     if all( x == mag_a for x in (mag_a, mag_b, mag_c) ):
#      
#         if int_remainder == 1:
#         
#             str_ax1_title = ( r'$\textbf{Three-Phase Inputs, } \omega =2 \pi \times' 
#                              + str(dbl_har_order) + r'\times' + str(dbl_base_freq) 
#                              + r'\textbf{ (positive sequence)}$' )
#             
#         elif int_remainder == 2:
#             
#             str_ax1_title = ( r'$\textbf{Three-Phase Inputs, } \omega =2 \pi \times' 
#                              + str(dbl_har_order) + r'\times' + str(dbl_base_freq) 
#                              + r'\textbf{ (negative sequence)}$' )
#             
#         elif int_remainder == 0:
#             
#             str_ax1_title = ( r'$\textbf{Three-Phase Inputs, } \omega =2 \pi \times' 
#                              + str(dbl_har_order) + r'\times' + str(dbl_base_freq) 
#                              + r'\textbf{ (zero sequence)}$' )
#             
#         else:
#                 
#             str_ax1_title = ( r'$\textbf{Three-Phase Inputs, } \omega =2 \pi \times' 
#                              + str(dbl_har_order) + r'\times' + str(dbl_base_freq) 
#                              + r'$' )    
#             
#     else:
#         
#         str_ax1_title = ( r'$\textbf{Three-Phase Inputs, } \omega =2 \pi \times' 
#                              + str(dbl_har_order) + r'\times' + str(dbl_base_freq) 
#                              + r'$' )  
#         
#     # coordinate 2 title
#     str_ax2_title = r'$\textbf{Outputs of the General Amplitude Invariant Clarke Transform}$'        
#     # =============================================================================
#     # </Make data, titles, legends>    
#     # =============================================================================
#     
#     
#     # =============================================================================
#     # <Main figure setup>
#     # =============================================================================
#     # make main figure
#     fig = plt.figure(figsize=(900.0/100.0, 600.0/100.0), dpi = 100.0)
#     
#     # adjust spacing between subplots
#     fig.subplots_adjust(hspace=0.5)
#     
#     # <coordnate 1> =============================================================================
#     # make coordinate 1
#     ax1 = plt.subplot(2, 1, 1)
#     
#     # set coordinate 1 title
#     ax1.set_title(str_ax1_title, fontsize=14, fontweight='bold', y=1.2)
#     
#     # set coordinate 1 horizontal line
#     ax1.axhline(y=0, color='k', lw=3)
#     
#     # plot 3-phase inputs
#     ax1_input_a, = plt.plot(time, input_a, color='r', lw=2, label=str_a_lbl)
#     ax1_input_b, = plt.plot(time, input_b, color='g', lw=2, label=str_b_lbl)
#     ax1_input_c, = plt.plot(time, input_c, color='b', lw=2, label=str_c_lbl)
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
#     ax1_lgd.get_frame().set_alpha(1.0)
#     
#     # set y label
#     ax1.set_ylabel(r'\textbf{Amplitude}', fontweight='bold', fontsize=12)    
#     # </coordnate 1> =============================================================================
#     
#     # <coordnate 2> =============================================================================
#     # make coordinate 2
#     ax2 = plt.subplot(2, 1, 2)
#     
#     # set coordinate 2 title
#     ax2.set_title(str_ax2_title, fontsize=14, fontweight='bold', y=1.23)
#     
#     # plot coordinate 2 horizontal line
#     ax2.axhline(y=0, color='k', lw=3)
#     
#     # plot Clarke transform components
#     ax2_alpha, = plt.plot(time, alpha, color='r', lw=2, label=str_alpha_lbl)
#     ax2_beta, = plt.plot(time, beta, color='g', lw=2, label=str_beta_lbl)
#     ax2_zero, = plt.plot(time, zero, color='b', lw=2, label=str_zero_lbl)
#     
#     # get automatic y limits
# #    y_min, y_max = ax2.get_ylim()
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
#     ax2_lgd.get_frame().set_alpha(1.0)
#     
#     # set labels
#     ax2.set_xlabel(r'\textbf{Time (s)}', fontweight='bold', fontsize=12)
#     ax2.set_ylabel(r'\textbf{Amplitude}', fontweight='bold', fontsize=12)
#     # </coordnate 2> =============================================================================
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
# draw_clarke(1, mag_a=0.7, mag_b=1.2, mag_c=0.6)
# =============================================================================
    
# =============================================================================
# 
# import numpy as np
# import os
# 
# for item in (1.7, 2.4, 5.6):
#     
#     path = r'J:\_Clarke & Park\Figures\Clarke_unbalanced'
#     
#     path = os.path.join(path, str(item) + '.png')
#     
#     draw_clarke(item, bool_savefig=True, str_fig_path=path)
# =============================================================================
