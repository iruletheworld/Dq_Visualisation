# -*- coding: utf-8 -*-
"""
Custom module for supporting gsyDqMain.py

Author: Dr. Gao, Siyu
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
    locStr_time_date : str
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
    
    Returns the following arrays:
        |  time, theta, 
        |  Clarke's *α* component, Clarke's *β* component,   
        |  Park's *d* component, Park's *q* component, 
        |  the rotating *d* axis' projection on the x, y axes,
        |  the rotating *q* axis' projection on the x, y axes,
        |  the d component's projection on the x, y axes,
        |  the q component's projection on the x, y axes.
    

    Parameters
    ----------
    locInt_Samples : int
        The number of samples to be taken during one base period.
    
    locDbl_base_freq : float
        The base frequency of the system, e.g., 50 or 60 (Hz).
    
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
            |  1    means the PLL is rotating anti-clockwise and at 1 times the base frequency.            
            |  2.7  means the PLL is rotating anti-clockwise and at 2.7 times the base frequency.            
            |  -2   means the PLL is rotating clock-wise and at 2 times the base frequency.                        
            |  -3.3 means the PLL is rotating clock-wise and at 3.3 times the base frequency.
    
    
    Returns
    -------
    locTime : array 
        1d array according to the base frequency and the samples taken within the base period.
    
    locTheta : array
        Angel calculated according to the time array and the base frequency. *θ = 2πft*.
    
    locAlpha_vector : array
        *α* component of the amplitude invariant Clarke Transform.
    
    locBeta_vector : array
        *β* component of the amplitude invariant Clarke Transform.
    
    locD_vector : array
        *d* component of the Park Transform.
    
    locQ_vector : array
        *q* component of the Park Transform.
    
    locD_ax_on_x : array
        The rotating *d* axis' projection on the x axis.
    
    locD_ax_on_y : array
        The rotating *d* axis' projection on the y axis.
    
    locQ_ax_on_x : array
        The rotating *q* axis' projection on the x axis.
    
    locQ_ax_on_y : array
        The rotating *q* axis' projection on the y axis.
    
    locD_vector_on_x : array
        *d* component's projection on the x axis.
    
    locD_vector_on_y : array
        *d* component's projection on the y axis.
    
    locQ_vector_on_x : array
        *q* component's projection on the x axis.
    
    locQ_vector_on_y : array
        *q* component's projection on the y axis.

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

    Return a formatted string.

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
    """Decide the input harmonic sequence (zero, positive, negative). Calculate
    the frequencies of the input harmonic, the Clarke components, the Park components.
    Calculate the periods of the Clarke components and the Park components.

    Conversion frequencies to periods could lead to zero divition. To deal with this,
    if the frequency is zero, then the period would be set to zero.
    
    The sequence of the input harmonic is calculated by:  
        locInt_remainder = np.mod(locDbl_harmonic_order, 3)
            
    |  If locInt_remainder == 0, then it is a zero sequence.
    |  If locInt_remainder == 1, then it is a positive sequence.
    |  If locInt_remainder == 2, then it is a negative sequence.
    
    If locInt_remainder is not an integer, i.e., it is a decimal number, then
    the input harmonic is an interharmonic and the definition of sequence does not 
    apply.
    
    For Clarke Transform components, their frequencies are always equal to the
    input harmonic. For positive sequneces, *α* leads *β* by 90°. 
    For negative sequneces, *α* lags *β* by 90°.
        
    For Park Transform components, their frequencies are related to how the input
    harmonic rotates and how the PLL rotates. The rule is, the frequencies of the 
    Park Transform components are equal to the relative angular frequency between
    the input harmonic and the PLL. The phases between *d* and *q* are the same
    as the corresponding *α* and *β*. I.e., if *α* leads *β*, then *d* leads *q*
    and vice versa.
    
    Note that the aforementioned rule is only true when locInt_remainder
    is an integer. For interharmonics, this rule does not apply.
    
    E.g.:        
        |  locDbl_harmonic_order = 1 (positive sequence)
        |  locDbl_pll_order      = 1
        |  The relative angular frequency is (1 - 1)·*ω* = 0, thus *d*, *q* are DC
        |  
        |  locDbl_harmonic_order = 2 (negative sequence)
        |  locDbl_pll_order      = 1
        |  The relative angular frequency is (-2 - 1)·*ω* = -3, thus *d*, *q* are
           of 3 times the base frequency and *d* lags *q* by 90°.
        |
        |  Note that this function would take abs() on locDbl_harmonic_order and then
           calcualte its sequence and then to automatically assign the right sign
           to it to calculate the Park components' frequencies. 
        |   
        |  Therefore there is no need to input a negative number for a negative 
           sequence. The abs() would get rid of it anyway.

    Parameters
    ----------
    locDbl_base_freq : float
        Base frequency of the system, e.g., 50 or 60 (Hz)
    
    locDbl_harmonic_order : str
        Order of harmonic to be analysis, e.g., 1 (fundamental), 2, 2.3...
    
    locDbl_pll_order : float
        The PLL rotational direction and frequency as multiples of the base
        frequency.
        
        E.g., 
        1 (locked on to the fundamental), 1.3 (anti-clockwise 
        at 1.3 times the base frequency), -2 (locked on the 2nd harmonic,
        negative sign due to 2nd harmonic is a negative sequence),
        -3.6 (clockwise at 3.6 times the base frequency)

    Returns
    -------
    locStr_freq_harmonic : str
        string containing information of the input harmonic's frequency
    ..
    locStr_freq_clarke : str
        string containing information of the Clarke components' frequencies
    ..        
    locStr_freq_park :str
        string containing information of the Park components' frequencies
    ..    
    locDbl_period_clarke :  float
        Period of the Clarke components
    ..        
    locDbl_period_park : float
        Period of the Park components
    

    Examples
    --------
    >>>  In [10]: find_sequences(50, 1, 1)
    2017-11-21, 08:59:44:Haromnic Order = 1, Positive Sequence
    Out[10]: 
    ('$ f_{Harmoic} = \\ 1\\times 50\\ Hz$\\n$Positive-Sequence,$\\n$Anti-Clockwise$\\n$Rotating, \\ i.e.,$\\n$Positively \\ Rotating$',
     '$ f_{\\alpha\\beta} = 1\\times 50\\  Hz$\\n$\\alpha  \\  is  \\   leading$\\n$\\beta \\  by \\  90^{\\circ}$',
     '$f_{dq} = 0.0\\times 50\\ Hz$',
     0.02,
     0)
    
    >>> In [11]: find_sequences(50, 2, -2)
    2017-11-21, 09:03:04:Haromnic Order = 2, Negative Sequence
    Out[11]: 
    ('$ f_{Harmoic} = \\ 2\\times 50\\ Hz$\\n$Negative-Sequence,$\\n$Clockwise \\ Rotating,$\\n$i.e.,$\\n$Negatively \\ Rotating$',
     '$f_{\\alpha\\beta} = 2\\times 50\\ Hz$\\n$\\alpha \\ is \\ lagging$\\n$\\beta \\ by \\ 90^{\\circ}$',
     '$f_{dq} = 0.0000\\times 50\\ Hz$',
     0.01,
     0)
    """    
    
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
    """Decrese the font size with increased harmonic order.

    A deadband is included (between 4 pt and 10 pt).
    
    Equation for calculation:
        locDbl_font_size = -0.5 * abs(locDbl_harmonic_order) + 11    
        
    If the input harmonic order is bigger than 15, the font size would be set
    to 1e-6.

    Parameters
    ----------
    locDbl_harmonic_order : float
        The input harmonic order
    
    Returns
    -------
    locDbl_font_size : float
        The calculated font size.

    Examples
    --------
    >>> set_font_size(2)
    10.0
    
    >>> set_font_size(15)
    4.0
    
    >>> set_font_size(16)
    1e-06
    """
    
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
    """Read a INI file and assign the corresponding elements to the textboxes.

    This function would assign the INI element value (right of the "=" sign in 
    the INI file) to the textbox if the label string of the textbox is the same
    as the INI element name (left of the "=" sign in the INI file). 
    
    If the INI element is found, the corresponding textbox is removed from 
    locList_textbox.

    Parameters
    ----------
    locStr_ini_file_path : string
        The path for the INI file.
        
    locList_textbox : list (containing all the matplotlib textboxes)
        The list of textboxes to be filled.

    Returns
    -------
    bool
        Returns True if deemed successful (no exception). Returns False if deemed
        unsuccessful (on exception).

    Examples
    --------
    >>> read_ini(r'C:\some.ini', list_textbox)
    2017-11-21, 13:46:29:Read INI file start
    2017-11-21, 13:46:29:Setting config : InputHarmonicOrder=1.3
    2017-11-21, 13:46:29:Setting config : InputPLLOrder=1
    2017-11-21, 13:46:29:Setting config : Samples=200
    2017-11-21, 13:46:29:Setting config : FPS=30
    2017-11-21, 13:46:29:Setting config : BaseFreq=50
    2017-11-21, 13:46:29:Setting config : FFmpegpath=
    2017-11-21, 13:46:29:Read INI file complete
    """
    
    print(date_time_now() + 'Read INI file start')
    
    try:
        
        # open ini file
        locIni_file = open(locStr_ini_file_path, 'r')
        
        # read by lines
        locConfig = locIni_file.readlines()
        
        # get of the line break for each line
        locConfig = [item.strip('\n') for item in locConfig]
        
        locConfig = [item.strip('\r') for item in locConfig]

        # double loop start   
        for i in locConfig:
            
            locIndex = i.find('=')
            
            # keep the left of the '='
            locStr_temp_config = i[:locIndex]
            
            for j in locList_textbox:
            
                # strip chars from the labels
                locStr_temp_label = j.label.get_text().replace(' ', '').replace('\n', '').replace('\r', '').replace(':', '')
                                
                if locStr_temp_config == locStr_temp_label:
                    
                    # get the right part of the '=' and assgin it to the text boxes
                    j.set_val(i[(locIndex+1):])
                    
                    print(date_time_now() + 'Setting config : ' + i)
                    
                    # if found, remove from list
                    locList_textbox.pop(locList_textbox.index(j))
                    
                    break
                    
                else:
                    
                    pass
        # double loop end
        
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
    
    """Collect the input textboxes' labels and texts, replace some chars in the 
    labels and form a big string delimited by a line break.

    Bascially, this function is used to form the mainbody of an INI file.
    
    White spaces, '\\\\n' and '\\\\r' in the textbox labels would be replced by empty
    strings. The colon (":") would be replaced by "=".
    
    If a textbox's label is "I am god:" and its text is "I rule the world." Then
    this function would turn it into 'Iamgod=I rule the world\\n'.

    Parameters
    ----------
    locList_textbox : list (containing all the matplotlib textboxes)
        A list of matplotlib textboxes used in the figure
    
    Returns
    -------
    locStr_textbox : str
        Formatted string for INI elements.
        
        E.g.:
            'InputHarmonicOrder=1.3\\\\nInputPLLOrder=1\\\\nSamples=200\\\\nFPS=30\\\\nBaseFreq=50\\\\nFFmpegpath='

    Examples
    --------
    >>> collect_tb(list_textbox)
    2017-11-21, 15:57:06:Collecting text from text boxes
    2017-11-21, 15:57:06:Collection complete
    InputHarmonicOrder=2.2
    InputPLLOrder=1
    Samples=200
    FPS=30
    BaseFreq=50
    FFmpegpath=
    """
    
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
    
    """Write the given string into the given INI file path.

    A string of '[User configurations]\\n' would be added to the start of the file.
    Followed by the input string.

    Parameters
    ----------
    locStr_ini_file_path : str
        The file full path of the INI file. If the extension ".ini" is not included,
        it would be added to the path.
        
    locStr_ini : str
        The string to be written into the INI file.

    Returns
    -------
    bool
        Returns True if deemed successful (no exception). Returns False if deemed
        unsuccessful (on exception).

    Examples
    --------
    >>> write_ini('C:\\Temp\\testini', 'some string')
    2017-11-21, 16:24:40:INI file save start
    2017-11-21, 16:24:40:INI file save complete
    Out[51]: True
    
    Content of the INI file would be:
        |  '[User configurations]
        |  some string'
    """
    
    print(date_time_now() + 'INI file save start')
    
    try:
        
        locStr_ini = '[User configurations]\n' + locStr_ini
        
        # check whether the INI file path ends with '.ini' (case insensitive)
        if locStr_ini_file_path[-4:].lower() == '.ini':
            
            pass
        
        else:
            
            locStr_ini_file_path = locStr_ini_file_path + '.ini'      
            
                
        locIni_file = open(locStr_ini_file_path, 'w')
        
        locIni_file.write(locStr_ini)
        
        locIni_file.close()
        
        print(date_time_now() + 'INI file save complete')
        
        return True
        
    except:
        
        print(date_time_now() + 'INI file save failed')
        
        return False        
# =============================================================================
# </Function: write ini file>
# =============================================================================
        
    
# =============================================================================
# <Function: load ffmpeg.exe>
# =============================================================================
def load_ffmpeg():
    
    """This function prompts a file open dialog to allow the user to select the 
    FFmpeg binary ("ffmpeg.exe") and ONLY this binary.

    This is to prevent selection error.

    Parameters
    ----------
    None

    Returns
    -------
    locStr_ffmpeg_path : str
        The path of the FFmpeg binary.

    Examples
    --------
    >>> load_ffmpeg()
    'C:\\ffmpeg'
    """
    
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
    
    """Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    bool
        Description of return value

    Examples
    --------
    >>> func(1, "a")
    True
    """
    
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
    
    """Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    bool
        Description of return value

    Examples
    --------
    >>> func(1, "a")
    True
    """
    
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
        