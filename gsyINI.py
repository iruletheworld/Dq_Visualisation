# -*- coding: utf-8 -*-
"""
Custom module for INI file read/write.

Author : 高斯羽 博士 (Dr. GAO, Siyu)

Version : 0.1.2

Last Modified : 2017-11-24

List of functions
----------------------

* read_ini_
* read_ini_to_tb_
* write_ini_

Function definitions
----------------------
"""

from gsyDqLib import date_time_now


# =============================================================================
# <Read INI file by line return the strings as a list>
# =============================================================================
def read_ini(locStr_ini_file_path):
    """
    .. _read_ini :     
        
    This funciton reads the given INI file by line and return the read line
    as a list object. This does NOT manipulate the read contents.


    Parameters
    ----------
    locStr_ini_file_path : str
        The INI file full path.

    Returns
    -------
    
    **bool**
        Returns True if read successful (no exception). Returns False on exception.

    locConfig : list or int
        Returns the INI read by line contents if read successful.
        
        Returns 0 when read fail.
    
    Examples
    --------
    
    >>> read_ini(r'C:\some.ini')
    2017-11-23, 11:13:38:Reading INI file...
    2017-11-23, 11:13:38:Read INI file complete
    (True,
     ['[User configurations]\\n',
      'InputHarmonicOrder=1.7\\n',
      'InputPLLOrder=1\\n',
      'Samples=200\\n',
      'FPS=30\\n',
      'BaseFreq=50\\n',
      'FFmpegpath=\\n'])
    """
    
    print(date_time_now() + 'Reading INI file...')
    
    try:
        
        # open ini file
        locIni_file = open(locStr_ini_file_path, 'r')
        
        # read by lines
        locConfig = locIni_file.readlines()
        
        print(date_time_now() + 'Read INI file complete')
        
        return (True, locConfig)
        
    except:
        
        print(date_time_now() + 'Fail to read INI file.')
        
        locConfig = 0
        
        return (False, locConfig)
# =============================================================================
# </Read INI file by line return the strings as a list>
# =============================================================================


# =============================================================================
# <Function: read ini file and put the configs to text boxes>
# =============================================================================
def read_ini_to_tb(locStr_ini_file_path, locList_textbox):    
    """
    .. _read_ini_to_tb : 
    
    Read a INI file and assign the corresponding elements to the matplotlib
    textboxes.

    This function would assign the INI element value (right of the "=" sign in 
    the INI file) to the textbox if the label string of the textbox is the same
    as the INI element name (left of the "=" sign in the INI file). 
    
    The input list for textbox would be copied by value into a new list object
    first to prevent modification of the original list.
    
    .. code:: python
    
        locTemp_textbox = list(locList_textbox)
    
    If the INI element is found, the corresponding textbox is removed from 
    locTemp_textbox to make the search faster.

    Parameters
    ------------
    
    locStr_ini_file_path : string
        The path for the INI file.
        
    locList_textbox : list (containing all the matplotlib textboxes)
        The list of textboxes to be filled.

    Returns
    -------
    
    **bool**
        Returns True if deemed successful (no exception). Returns False if deemed
        unsuccessful (on exception).
        
    locConfig : list or int
        Each element in the list is a line of content read from the given INI 
        file if read successful.
        
        Returns 0 when read fail.
    
    Examples
    --------
    >>> read_ini_to_tb(r'C:\some.ini', list_textbox)
    2017-11-23, 10:33:29:Reading INI file...
    2017-11-23, 10:33:29:Read INI file complete
    2017-11-23, 10:33:29:Setting config : InputHarmonicOrder=2
    2017-11-23, 10:33:29:Setting config : InputPLLOrder=1
    2017-11-23, 10:33:29:Setting config : Samples=300
    2017-11-23, 10:33:29:Setting config : FPS=30
    2017-11-23, 10:33:29:Setting config : BaseFreq=50
    2017-11-23, 10:33:29:Setting config : FFmpegpath=
    """
    
    try:
        
        # call function to read INI file
        bool_ini, locConfig  = read_ini(locStr_ini_file_path)
        
        # if read INI fale, exit this function
        if bool_ini == False:
            
            return (False, locConfig)
        
        # get of the line break for each line
        locConfig = [item.strip('\n') for item in locConfig]
        
        locConfig = [item.strip('\r') for item in locConfig]
        
        # copy the values of the list, otherwise the original list object would be modified
        locTemp_textbox = list(locList_textbox)

        # double for-loop start   
        for i in locConfig:
            
            locIndex = i.find('=')
            
            # keep the left of the '='
            locStr_temp_config = i[:locIndex]
            
            for j in locTemp_textbox:
            
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
                    locTemp_textbox.pop(locTemp_textbox.index(j))
                    
                    break
                    
                else:
                    
                    pass
        # double for-loop end
            
        return (True, locConfig)
            
    except:
        
        print(date_time_now() + 'INI file read failed')
        
        locConfig = 0
        
        return (False, locConfig)
# =============================================================================
# </Function: read ini file and put the configs to text boxes>
# =============================================================================
        

# =============================================================================
# <Function: write ini file>
# =============================================================================
def write_ini(locStr_ini_file_path, locStr_ini):
    
    """
    .. _write_ini :
    
    Write the given string into the given INI file path.

    Parameters
    ----------
    
    locStr_ini_file_path : str
        The file full path of the INI file. If the extension ".ini" is not included,
        it would be added to the path.
        
    locStr_ini : str
        The string to be written into the INI file.

    Returns
    -------
    
    **bool**
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