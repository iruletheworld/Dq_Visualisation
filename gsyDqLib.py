# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:19:03 2017

@author: BachDesktop
"""

#import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import sys
import os
import win32api
import win32con
import time

from numpy import sin, cos, pi
from tkinter import filedialog
from time import gmtime, strftime, sleep

# =============================================================================
# <Function: get system time and date>
# =============================================================================
def date_time_now():
    """Return the system date and time as a string.

    Return format: 'yyyy-mm-dd, HH:MM:SS:'

    Parameters
    ----------
        None

    Returns
    -------
    str
        Formatted system date time string in 'yyyy-mm-dd, HH:MM:SS:'. 
        The last colon is intended for print to the console (or making logs).

    Examples
    --------
    >>> date_time_now()
    '2017-11-20, 15:14:42:'
    """
    
    locStr_time_date = strftime('%Y-%m-%d, %H:%M:%S:', gmtime())
    
    return locStr_time_date
# =============================================================================
# </Function: get system time and date>
# =============================================================================
    

# =============================================================================
# <Function: Calculate Clarke and Park transforms>
# =============================================================================
def cal_ABDQ(locInt_Samples, locDbl_base_freq, locDbl_harmonic_order, locDbl_pll_order):
    """Calculates the Clarke Transform (amplitude invariant) and the Park Transform.
    
    Returns the time, theta, Clarke's alpha component, Clarke's beta component,
    Park's d component, Park's q component, 
    the rotating d axis' projection on the x, y axes,
    the rotating q axis' projection on the x, y axes,
    the d component's projection on the x, y axes,
    the q component's projection on the x, y axes.
    

    Parameters
    ----------
    locInt_Samples : int
        The number of samples to be taken during one base period.
        
    locDbl_base_freq : float
        The base frequency of the system, e.g., 50 or 60.
        
    locDbl_harmonic_order : float
        The order of harmonic to be used to calculate Clarke and Park from. 1st harmonic
        is the fundamental. Interharmonics are allowed, e.g., 1.3 order. abs() is applied
        on this parameter.
    
    locDbl_pll_order : float
        The parameter decides the PLL's rotational direction and frequency. The parameter's sign, 
        i.e., positve or negative, decides the rotational direction. Positive means anti-clockwise.
        Negative means clockwise. The absolute value of the parameter decides how many times the base
        frequency that the PLL is rotating.
        
        E.g. : 
            1    means the PLL is rotating anti-clockwise and at 1 times the base frequency.
            2.7  means the PLL is rotating anti-clockwise and at 2.7 times the base frequency.
            -2   means the PLL is rotating clock-wise and at 2 times the base frequency.            
            -3.3 means the PLL is rotating clock-wise and at 3.3 times the base frequency.
    

    Returns
    -------
    locTime : array 
        1d array according to the base frequency and the samples taken within the base period.
        
    locTheta : array
        Angel calculated according to the time array and the base frequency. θ = 2πft.
        
    locAlpha_vector : array
        α component of the amplitude invariant Clarke Transform.
    
    locBeta_vector : array
        β component of the amplitude invariant Clarke Transform.
    
    locD_vector : array
        d component of the Park Transform.
    
    locQ_vector : array
        q component of the Park Transform.
    
    locD_ax_on_x : array
        The rotating d axis' projection on the x axis.
    
    locD_ax_on_y : array
        The rotating d axis' projection on the y axis.
    
    locQ_ax_on_x : array
        The rotating q axis' projection on the x axis.
    
    locQ_ax_on_y : array
        The rotating q axis' projection on the y axis.
    
    locD_vector_on_x : array
        d component's projection on the x axis.
    
    locD_vector_on_y : array
        d component's projection on the y axis.
    
    locQ_vector_on_x : array
        q component's projection on the x axis.
    
    locQ_vector_on_y : array
        q component's projection on the y axis.

    Examples
    --------
    >>> (time, theta, 
     alpha_vector, beta_vector, 
    d_vector, q_vector,
    d_ax_on_x, d_ax_on_y, 
    q_ax_on_x, q_ax_on_y, 
    d_vector_on_x, d_vector_on_y, 
    q_vector_on_x, q_vector_on_y) = cal_ABDQ(200, 50, 1, 1)
    """

    locDbl_harmonic_order = abs(locDbl_harmonic_order)

    # zero division protection        
    try:
        
        if locDbl_base_freq <= 0:
            
            locDbl_base_freq = 50
            
        else:
            
            locDbl_base_freq = locDbl_base_freq
            
            locDbl_base_period = 1 / locDbl_base_freq
            
    except:
        
        locDbl_base_freq = 50
        
        locDbl_base_period = 1 / locDbl_base_freq
        
        pass    
    
    # create the time list according to the base frequency and the samples
    locTime = np.linspace(0, locDbl_base_period, locInt_Samples)
    
    # θ = 2πft
    locTheta = 2 * pi * locDbl_base_freq * locTime
    
    # Clarke Transform, α component
    locAlpha_vector = 2/3 * (cos(locDbl_harmonic_order * locTheta) 
                            - cos(locDbl_harmonic_order * locTheta) 
                            * cos(locDbl_harmonic_order * 2/3 * pi))
    
    # Clarke Transform, β component
    locBeta_vector = 2 * np.sqrt( 3 )/3 * (sin(locDbl_harmonic_order * locTheta) 
                                        * sin(locDbl_harmonic_order * 2/3 * pi))
                  
    # Park Transform, d component                  
    locD_vector = (cos(locDbl_pll_order * locTheta) * locAlpha_vector 
                + sin(locDbl_pll_order * locTheta) * locBeta_vector)
    
    # Park Transform, q component
    locQ_vector = (-1 * sin(locDbl_pll_order * locTheta) * locAlpha_vector 
                   + cos(locDbl_pll_order * locTheta) *  locBeta_vector)
    
    # rotating d axis' projection on x, y axes
    locD_ax_on_x = cos(locDbl_pll_order * locTheta)
    locD_ax_on_y = sin(locDbl_pll_order * locTheta)
    
    # rotating q axis' projection on x, y axes
    locQ_ax_on_x = cos(locDbl_pll_order * locTheta + pi / 2)
    locQ_ax_on_y = sin(locDbl_pll_order * locTheta + pi / 2)
    
    # d component's projection on x, y axes
    locD_vector_on_x = locD_vector * cos(locDbl_pll_order * locTheta)
    locD_vector_on_y = locD_vector * sin(locDbl_pll_order * locTheta)
    
    # q component's projection on x, y axes
    locQ_vector_on_x = locQ_vector * cos(locDbl_pll_order * locTheta + pi / 2)
    locQ_vector_on_y = locQ_vector * sin(locDbl_pll_order * locTheta + pi / 2)
    
    return (locTime, locTheta, 
            locAlpha_vector, locBeta_vector, 
            locD_vector, locQ_vector,
            locD_ax_on_x, locD_ax_on_y, 
            locQ_ax_on_x, locQ_ax_on_y, 
            locD_vector_on_x, locD_vector_on_y, 
            locQ_vector_on_x, locQ_vector_on_y)
# =============================================================================
# </Function: Calculate Clarke and Park transforms>
# =============================================================================
    

# =============================================================================
# <Function: find PLL rotational direction>
# =============================================================================
def find_pll_direction(locDbl_base_freq, locDbl_pll_order):
    """Determin the PLL is rotating anti-clockwise (positive) or clockwise (negative).

    Return is a string.

    Parameters
    ----------
    locDbl_base_freq : float
        The system base frequency.
        
    locDbl_pll_order : float
        The parameter decides the PLL's rotational direction and frequency. The parameter's sign, 
        i.e., positve or negative, decides the rotational direction. Positive means anti-clockwise.
        Negative means clockwise. The absolute value of the parameter decides how many times the base
        frequency that the PLL is rotating.

    Returns
    -------
    locStr_freq_pll : string
        A formatted string descripes the PLL rotational direction and the frequency.

    Examples
    --------
    >>> find_pll_direction(50, 1)
    '$f_{PLL} = 1\\times 50\\ Hz$\\n\$Anti-Clockwise$\\n$Rotating,$\\n$i.e.,$\\n$Positively \\ Rotating $'
    
    >>> find_pll_direction(50, -1)
    '$f_{PLL} = -1\\times 50\\ Hz$\\n$Clockwise \\ Rotating,$\\n$i.e.,$\\n$Negatively \\ Rotating $'
    """
    
    if locDbl_pll_order > 0:
        
        locStr_freq_pll = (r'$f_{PLL} = ' 
                           + str(locDbl_pll_order) 
                           + r'\times ' + str(locDbl_base_freq) + '\ Hz$'
                           + '\n' + r'$Anti-Clockwise$'
                           + '\n' + r'$Rotating,$'
                           + '\n' + r'$i.e.,$'
                           + '\n' + r'$Positively \ Rotating $')
        
    elif locDbl_pll_order < 0:
        
        locStr_freq_pll = (r'$f_{PLL} = ' 
                           + str(locDbl_pll_order) 
                           + r'\times ' + str(locDbl_base_freq) + '\ Hz$'
                           + '\n' + r'$Clockwise \ Rotating,$'
                           + '\n' + r'$i.e.,$'
                           + '\n' + r'$Negatively \ Rotating $')
        
    elif locDbl_pll_order == 0:
        
        locStr_freq_pll = (r'$f_{PLL} = ' 
                           + str(locDbl_pll_order) 
                           + r'\times ' + str(locDbl_base_freq) + '\ Hz$' 
                           + '\n' + r'$Not \ Rotating$')
        
    else:
        
        print(date_time_now() + 'Fatal Error. Source: find_pll_direction()')
        sys.exit('Fatal Error. Source: find_pll_direction()')
        
    return locStr_freq_pll
# =============================================================================
# </Function: find PLL rotational direction>
# =============================================================================
    

# =============================================================================
# <Function: find input Harmonic sequence and the frequencies of Clarke and Park transforms>
# =============================================================================
def find_sequences(locDbl_base_freq, locDbl_harmonic_order, locDbl_pll_order):
    
    
    
    
    locDbl_harmonic_order = abs(locDbl_harmonic_order)
    
    # calculate the sequence
    locInt_remainder = np.mod(locDbl_harmonic_order, 3)
    
    # <Find sequences>
    # Zero sequence, n = 0 + 3k, k = 0, 1, 2, 3...
    if locInt_remainder == 0: 
        
        print(date_time_now()
                + 'Haromnic Order = {}, Zero Sequence'.format(locDbl_harmonic_order) )
        
        sys.exit('You have selected a Zero Sequence whose alpha, beta, d, q are zero')
        
    # Positive sequence, n = 1 + 3k, k = 0, 1, 2, 3...
    elif locInt_remainder == 1: 
        
        print(date_time_now()
                + 'Haromnic Order = {}, Positive Sequence'.format(locDbl_harmonic_order))
        
        locStr_freq_harmonic = (r'$ f_{Harmoic} = \ ' 
                                + str( locDbl_harmonic_order ) 
                                + r'\times ' + str(locDbl_base_freq) + '\ Hz$'
                                + '\n' + r'$Positive-Sequence,$' 
                                + '\n' + r'$Anti-Clockwise$'
                                + '\n' + r'$Rotating, \ i.e.,$'
                                + '\n' + r'$Positively \ Rotating$')
        
        locStr_freq_clarke = (r'$ f_{\alpha\beta} = ' 
                              + str( locDbl_harmonic_order ) 
                              + r'\times ' + str(locDbl_base_freq) + '\  Hz$'
                              + '\n' + r'$\alpha  \  is  \   leading$' 
                              + '\n' + r'$\beta \  by \  90^{\circ}$')
        
        # Park transform frequency. Note that Park changes the frequency while Clarke does not
        if (locDbl_harmonic_order - locDbl_pll_order) == 0:
            
            locStr_freq_park = (r'$f_{dq} = ' 
                                + '{0:.1f}'.format(abs(locDbl_harmonic_order 
                                                       - locDbl_pll_order))
                                + r'\times ' + str(locDbl_base_freq) + '\ Hz$')
            
        elif (locDbl_harmonic_order - locDbl_pll_order) > 0:
            
            # keep 4 decimal places
            locStr_freq_park = (r'$f_{dq} = ' 
                                + '{0:.4f}'.format(abs(locDbl_harmonic_order
                                                       - locDbl_pll_order)) 
                                + r'\times ' + str(locDbl_base_freq) + '\ Hz$'
                                + '\n' + r'$d \ is \ leading$'
                                + '\n' + r'$q \ by \ 90^{\circ}$')
            
        elif (locDbl_harmonic_order - locDbl_pll_order) < 0:
            
            locStr_freq_park = (r'$f_{dq} = ' 
                                + '{0:.4f}'.format(abs(locDbl_harmonic_order 
                                                       - locDbl_pll_order)) 
                                + r'\times ' + str(locDbl_base_freq) + '\ Hz$'
                                + '\n' + r'$d \ is \ lagging$'
                                + '\n' + r'$q \  by \  90^{\circ}$')
        
        if (locDbl_harmonic_order - locDbl_pll_order) == 0:
            
            locDbl_period_park = 0
            
        elif (locDbl_harmonic_order - locDbl_pll_order) != 0:    
            
            locDbl_period_park = 1 / ((locDbl_harmonic_order 
                                       - locDbl_pll_order) * locDbl_base_freq)
            
    # Negative sequence
    elif locInt_remainder == 2: 
        
        print(date_time_now()
                + 'Haromnic Order = {}, Negative Sequence'.format(locDbl_harmonic_order))
        
        locStr_freq_harmonic = (r'$ f_{Harmoic} = \ ' 
                                + str( locDbl_harmonic_order ) 
                                + r'\times ' + str(locDbl_base_freq) + '\ Hz$'
                                + '\n' + r'$Negative-Sequence,$' 
                                + '\n' + r'$Clockwise \ Rotating,$'
                                + '\n' + r'$i.e.,$'
                                + '\n' + r'$Negatively \ Rotating$')
        
        locStr_freq_clarke = (r'$f_{\alpha\beta} = ' 
                              + str( locDbl_harmonic_order ) 
                              + r'\times ' + str(locDbl_base_freq) + '\ Hz$'
                              + '\n' + r'$\alpha \ is \ lagging$'
                              + '\n' + r'$\beta \ by \ 90^{\circ}$')
                
        # Park transform frequency. Note that Park changes the frequency while Clarke does not
        if (locDbl_harmonic_order + locDbl_pll_order) == 0:
            
            locStr_freq_park = (r'$f_{dq} = ' 
                                + '{0:.4f}'.format(abs(locDbl_harmonic_order
                                                       + locDbl_pll_order)) 
                                + r'\times ' + str(locDbl_base_freq) + '\ Hz$')
            
        elif (locDbl_harmonic_order + locDbl_pll_order) > 0:
            
            locStr_freq_park = (r'$f_{dq} = ' 
                                + '{0:.4f}'.format(abs(locDbl_harmonic_order
                                                       + locDbl_pll_order)) 
                                + r'\times ' + str(locDbl_base_freq) + '\ Hz$'
                                + '\n' + r'$d \ is \ lagging$'
                                + '\n' + r'$q \ by \ 90^{\circ}$')
            
        elif (locDbl_harmonic_order + locDbl_pll_order) < 0:
            
            locStr_freq_park = (r'$f_{dq} = ' 
                                + '{0:.4f}'.format(abs(locDbl_harmonic_order
                                                       + locDbl_pll_order)) 
                                + r'\times ' + str(locDbl_base_freq) + '\ Hz$'
                                + '\n' + r'$d \ is \ leading$'
                                + '\n' + r'$q \ by \ 90^{\circ}$')
            
        if (locDbl_harmonic_order + locDbl_pll_order) == 0:
            
            locDbl_period_park = 0
            
        elif (locDbl_harmonic_order + locDbl_pll_order) != 0:            
            
            locDbl_period_park = 1 / ((locDbl_harmonic_order 
                                       + locDbl_pll_order) * locDbl_base_freq)
    
    # Interharmonics
    else:
        
        print(date_time_now() + 'Interharmonic')
        
        locStr_freq_harmonic = (r'$ f_{Harmoic} = \ ' 
                                + str( locDbl_harmonic_order ) 
                                + r'\times ' + str(locDbl_base_freq) + '\ Hz$' 
                                + '\n' + 'Interharmonic')
        
        locStr_freq_clarke = (r'$f_{\alpha\beta} = ' 
                              + str( locDbl_harmonic_order ) 
                              + r'\times ' + str(locDbl_base_freq) + '\ Hz$' 
                              + '\n' + 'Interharmonic')
        
        locStr_freq_park = 'Interharmonic'

        locDbl_period_park = 0
    # </Find sequences>
        
    # Clarke transform period
    if locDbl_harmonic_order != 0:
        
        locDbl_period_clarke = 1 / abs(locDbl_harmonic_order * locDbl_base_freq)
        
    else:
        
        locDbl_period_clarke = 0
        
    return (locStr_freq_harmonic, locStr_freq_clarke, locStr_freq_park, 
            locDbl_period_clarke, locDbl_period_park)
# =============================================================================
# </Function: find input Harmonic sequence and the frequencies of Clarke and Park transforms>
# =============================================================================
    
    
# =============================================================================
# <Function: set period font size>
# =============================================================================
def set_font_size(locDbl_harmonic_order):
    
    # Decrease the font size with increased harmonic order
    locDbl_font_size = -0.5 * abs(locDbl_harmonic_order) + 11    
    
    if locDbl_font_size > 10.0:    
        
        locDbl_font_size = 10.0
        
    elif locDbl_font_size < 4.0:
        
        locDbl_font_size = 4.0
        
    if abs(locDbl_harmonic_order) > 15.0:
        
        locDbl_font_size = 1.0e-6
    
    return locDbl_font_size
# =============================================================================
# </Function: set period font size>
# =============================================================================
    

# =============================================================================
# <Function: read ini file and put the configs to text boxes>
# =============================================================================
def read_ini(locStr_ini_file_path, locList_textbox):
    
    print(date_time_now() + 'Read INI file start')
    
    try:
        
        # open ini file
        locIni_file = open(locStr_ini_file_path, 'r')
        
        # read by lines
        locConfig = locIni_file.readlines()
        
        # get of the line break for each line
        locConfig = [item.strip('\n') for item in locConfig]
        
        locConfig = [item.strip('\r') for item in locConfig]

        # double loop        
        for i in locConfig:
            
            locIndex = i.find('=')
            
            # keep the left of the '='
            locStr_temp_config = i[:locIndex]
            
            for j in locList_textbox:
            
                # strp chars from the labels
                locStr_temp_label = j.label.get_text().replace(' ', '').replace('\n', '').replace('\r', '').replace(':', '')
                                
                if locStr_temp_config == locStr_temp_label:
                    
                    # get the right part of the '=' and assgin it to the text boxes
                    j.set_val(i[(locIndex+1):])
                    
                    print(date_time_now() + 'Setting config : ' + i)
                    
                    break
                    
                else:
                    
                    pass
            
        print(date_time_now() + 'Read INI file complete')
            
        return True
            
    except:
        
        print(date_time_now() + 'INI file read failed')
        
        return False
# =============================================================================
# </Function: read ini file and put the configs to text boxes>
# =============================================================================


# =============================================================================
# <Function: collect text boxes for write ini later>
# =============================================================================
def collect_tb(locList_textbox):
    
    print(date_time_now() + 'Collecting text from text boxes')
    
    locStr_textbox = ''
    
    for item in locList_textbox:
        
        locStr_textbox = (locStr_textbox 
                          + item.label.get_text().replace(' ', '')
                          .replace('\n', '').replace('\r', '').replace(':', '=') 
                          + item.text + '\n')
        
    print(date_time_now() + 'Collection complete')    
    
    return locStr_textbox
# =============================================================================
# </Function: collect text boxes for write ini later>
# =============================================================================


# =============================================================================
# <Function: write ini file>
# =============================================================================
def write_ini(locStr_ini_file_path, locStr_ini):
    
    print(date_time_now() + 'INI file save start')
    
    try:
        
        locStr_ini = '[User configurations]\n' + locStr_ini
        
        locIni_file = open(locStr_ini_file_path, 'w')
        
        locIni_file.write(locStr_ini)
        
        locIni_file.close()
        
        print(date_time_now() + 'INI file save complete')
        
    except:
        
        print(date_time_now() + 'INI file save failed')
        
        pass
# =============================================================================
# </Function: write ini file>
# =============================================================================
        
    
# =============================================================================
# <Function: load ffmpeg.exe>
# =============================================================================
def load_ffmpeg():
    
    # tk main window
    locRoot = tk.Tk()
        
    # hide tk main window
    locRoot.withdraw()
    
    # open file dialogue
    locStr_ffmpeg_path = filedialog.askopenfilename(title=('Please select "ffmpeg.exe",' 
                                                    + ' you might need to install it'),
                                                    filetypes=(('ffmpeg.exe', 'ffmpeg.exe'), 
                                                               ('all files', '*.*')))
    # destroy tk main window
    locRoot.destroy()   
    
    return locStr_ffmpeg_path
# =============================================================================
# </Function: load ffmpeg.exe>
# =============================================================================


# =============================================================================
# <Function: check whther the file exists periodically>
# =============================================================================
def check_file_saved(locStr_file_path):
    
    locCounter = 0
    
    print('\n')
    
    # wait for the file has the same name to be deleted in function "save_animation_to_disk"
    sleep(1.5)
    
    while True:
        
        locBool_saved = os.path.isfile(locStr_file_path)
        
        if locBool_saved == True:
            
            print(date_time_now() + 'Animation saved')
            
            break
            
        else:
                       
            if np.mod(locCounter, 10) == 0:
            
                print(date_time_now() + 'Saving animation, please wait...')
                
            else:
                
                pass
            
            sleep(2)
            
        locCounter += 1
# =============================================================================
# </Function: check whther the file exists periodically>    
# =============================================================================


# =============================================================================
# <Function: save the animation to harddrive>    
# =============================================================================
def save_animation_to_disk(locObj_animation, locStr_video_temp_path, locStr_video_path, locFFwriter):
    
    try:
        
        locTime_start = time.time()
    
        if os.path.isfile(locStr_video_temp_path) == True:
            
            os.remove(locStr_video_temp_path)
            
        else:
            
            pass
        
        if os.path.isfile(locStr_video_path) == True:
            
            os.remove(locStr_video_path)
            
        else:
            
            pass
    
        locObj_animation.save(locStr_video_temp_path, writer=locFFwriter)
        
        os.rename(locStr_video_temp_path, locStr_video_path)
        
        locTime_end = time.time()
        
        minute, second = divmod(locTime_end - locTime_start, 60)
        
        hour, minute = divmod(minute, 60)
        
        print(date_time_now() + 'Time taken : ' +  ('%d:%02d:%02d' % (hour, minute, second)))
        
        win32api.MessageBox(None, ('Video save finished.' 
                                   + '\n' + '\n' + locStr_video_path), 
                            'Video save finished', 
                            win32con.MB_ICONINFORMATION)
            
    except:
        
        try:
            
            os.remove(locStr_video_temp_path)
            
        except:
                
            pass
        
        print(date_time_now() + 'Fatal error while trying to save the animation')
        
        win32api.MessageBox(None, ('Video save failed.' 
                                   + '\n'
                                   + '\n' + 'Source: "save_animation_to_disk"'),
                            'Video save failed', 
                            win32con.MB_ICONERROR)
        
        return None
# =============================================================================
# </Function: save the animation to harddrive>    
# =============================================================================
        