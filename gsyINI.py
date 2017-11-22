# -*- coding: utf-8 -*-
"""
Custom module for INI file read/write.

Author : Dr. Gao, Siyu

Version : 0.1.0

Last Modified : 2017-11-22

Created : 2017-11-22

Function 1 :
------------
    .. code:: python
    
        read_ini_to_tb(locStr_ini_file_path, locList_textbox)
        
    This function reads an INI file and assign the values of the elements into
    the given matplotlib textboxes.

Function 2 :
------------
    .. code:: python
    
        write_ini(locStr_ini_file_path, locStr_ini)
        
    This function writes the given string into the given INI file path.
"""

from gsyDqLib import date_time_now

# =============================================================================
# <Function: read ini file and put the configs to text boxes>
# =============================================================================
def read_ini_to_tb(locStr_ini_file_path, locList_textbox):    
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
        
    locConfig : list
        Each element in the list is a line of content read from the given INI file.    
    
    Examples
    --------
    >>> read_ini_to_tb(r'C:\some.ini', list_textbox)
    2017-11-21, 13:46:29:Read INI file start
    2017-11-21, 13:46:29:Setting config : InputHarmonicOrder=1.3
    2017-11-21, 13:46:29:Setting config : InputPLLOrder=1
    2017-11-21, 13:46:29:Setting config : Samples=200
    2017-11-21, 13:46:29:Setting config : FPS=30
    2017-11-21, 13:46:29:Setting config : BaseFreq=50
    2017-11-21, 13:46:29:Setting config : FFmpegpath=
    2017-11-21, 13:46:29:Read INI file complete
    """
    
    print(date_time_now() + 'Reading INI file...')
    
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
                locStr_temp_label = (j.label.get_text()
                                        .replace(' ', '')
                                        .replace('\n', '')
                                        .replace('\r', '')
                                        .replace(':', ''))
                                
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
            
        return True, locConfig
            
    except:
        
        print(date_time_now() + 'INI file read failed')
        
        return False
# =============================================================================
# </Function: read ini file and put the configs to text boxes>
# =============================================================================
        

# =============================================================================
# <Function: write ini file>
# =============================================================================
def write_ini(locStr_ini_file_path, locStr_ini):
    
    """Write the given string into the given INI file path.

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
    >>> write_ini('C:\\Temp\\testini', '[User configurations]\\nsome string')
    2017-11-21, 16:24:40:INI file save start
    2017-11-21, 16:24:40:INI file save complete
    Out[51]: True
    
    Content of the INI file would be:
        |  '[User configurations]
        |  some string'
    """
    
    print(date_time_now() + 'INI file save start')
    
    try:
        
        # check whether the INI file path ends with '.ini' (case insensitive)
        if locStr_ini_file_path[-4:].lower() == '.ini':
            
            # if yes, pass
            pass
        
        else:
            
            # if no, append
            locStr_ini_file_path = locStr_ini_file_path + '.ini'      
            
        # open the INI for write
        locIni_file = open(locStr_ini_file_path, 'w')
        
        # write the string into the INI
        locIni_file.write(locStr_ini)
        
        # close the INI file
        locIni_file.close()
        
        print(date_time_now() + 'INI file save complete')
        
        return True
        
    except:
        
        print(date_time_now() + 'INI file save failed')
        
        return False        
# =============================================================================
# </Function: write ini file>
# =============================================================================