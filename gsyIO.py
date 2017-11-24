# -*- coding: utf-8 -*-
"""
Custom module for genreal IO.

Author : 高斯羽 博士 (Dr. GAO, Siyu)

Version : 0.1.1

Last Modified : 2017-11-24

List of functions
----------------------

* save_txt_
* save_txt_on_event_
* search_file_and_start_

Function definitions
----------------------

"""

import tkinter as tk
import tkinter.messagebox as msgbox
import os
import glob

from tkinter import filedialog

# =============================================================================
# <Function: save the text as a txt file>
# =============================================================================

def save_txt(str_file_path, str_txt):
    
    """
    .. _save_txt :     
        
    This funciton saves the given string into the given file.
    
    Parameters
    ----------
    str_file_path : str
        The text file full path.
        
    str_txt : str
        The string to be write into the text file.

    Returns
    -------
    
    bool
        Returns True if read successful (no exception). 
        Returns False on exception.
    
    Examples
    --------
    .. code:: python
    
        bool_success = save_txt(str_file_path, str_txt)
    """

    try:

        file = open(str_file_path, 'w')
        
        file.write(str_txt)
        
        file.close()
        
        return True
    
    except:
        
        return False

# =============================================================================
# </Function: save the text as a txt file>
# =============================================================================


# =============================================================================
# <Function: save the text as a txt file on event>
# =============================================================================

def save_txt_on_event(event, str_txt):
    
    """
    .. _save_txt_on_event :     
        
    This funciton calls the "save_txt" function to save the string into a text
    file.
    
    This function prompts file save dialogue to allow the user to interactively
    save the file.
    
    This function prompts messages to tell the user whether the save is successful
    or not.
    
    Reference for using "lambda" : https://goo.gl/zDmGPR

    Parameters
    ----------
    event : event
        The event that triggers this function.
        
    str_txt : str
        The string to be saved.

    Returns
    -------
    
    bool
        Returns True if read successful (no exception). 
        Returns False on exception.
    
    Examples
    --------
    .. code:: python
    
        button_save_help.on_clicked(lambda x: save_txt_on_event(x, CONST_STR_HELP))
        
    """
    
    bool_success = False
    
    try:
    
        locRoot = tk.Tk()
        
        locRoot.withdraw()
        
        str_file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                      title="Save as txt",
                                                      filetypes = (("Text files","*.txt"),
                                                                   ("all files","*.*")))
            
        locRoot.destroy()
        
        # if user cancelled, exit
        if len(str_file_path) == 0:
            
            return False
        
        else:
            
            pass
        
        if (str_file_path.endswith('.txt') == True) or (str_file_path.endswith('.TXT') == True):
            
            pass
        
        else:
            
            str_file_path = str_file_path + '.txt'
            
        bool_success = save_txt(str_file_path, str_txt)
    
        if bool_success == True:
            
            # prompt finish message
            locRoot = tk.Tk()
            
            locRoot.withdraw()
            
            msgbox.showinfo('Text file save finished', 
                            'Text file save finished.' + '\n' + '\n' + str_file_path)
            
            locRoot.destroy()
            
            return True
        
        else:
            
            # prompt fail message
            locRoot = tk.Tk()
            
            locRoot.withdraw()
            
            msgbox.showinfo('Text file save failed', 
                            'Text file save failed.')
            
            locRoot.destroy()
            
            return False
        
    except:
        
        # prompt fail message
        locRoot = tk.Tk()
        
        locRoot.withdraw()
        
        msgbox.showinfo('Text file save failed', 
                        'Text file save failed.')
        
        locRoot.destroy()
        
        return False        

# =============================================================================
# </Function: save the text as a txt file on event>
# =============================================================================


# =============================================================================
# <Function: search the file according to the given filename and start it with os default app>    
# =============================================================================
    
def search_file_and_start(str_pattern, str_filename):
    
    """
    .. _search_file_and_start :     
        
    This funciton searchs for the given file according to the given pattern. 
    If the given file is found, this function would try to start the file with
    os default application.
    
    The search is recursive. 
    
    This function uses "glob" for search.
        
    .. code :: python
    
        for item in glob.iglob(str_pattern, recursive=True):
            
            if item.endswith(os.path.join(os.sep , str_filename)):
                
                os.startfile(item)
                
                bool_found = True
                
                break
    
    Parameters
    ----------
    str_pattern : str
        The pattern for searching. E.g.  './\**/\*.html'
        
    str_filename : str
        The filename of the file to be started with os default application.

    Returns
    -------    
    bool
        Returns True if file found. 
        Returns False file not found or on exception.
    
    Examples
    --------
    .. code:: python
    
        bool_found = search_file_and_start(str_pattern, str_doct_filename)
    """
    
    bool_found = False
    
    try:
                
        for item in glob.iglob(str_pattern, recursive=True):
            
            if item.endswith(os.path.join(os.sep , str_filename)):
                
                os.startfile(item)
                
                bool_found = True
                
                break
            
    except:
        
        bool_found = False
        
        pass
    
    return bool_found
    
# =============================================================================
# </Function: search the file according to the given filename and start it with os default app>    
# =============================================================================