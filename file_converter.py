# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 12:30:13 2017

@author: Shih-Yang Lin

This GUI script is to convert STATA .dta file, Excel .xls and .xlsx file
to .csv or .txt file with ascii or utf-8 format.

version: 1.0
"""
# Load packages
import pandas as pd
import astropy as ast
import astropy.table as table
import tkinter as tk
import tkinter.filedialog as fd
# import string

# Create user interface

interface = tk.Tk()
interface.title("Format converter 1.0") # Set windows name
interface.geometry("720x200") # Set windows size

# Create a label to display message
des1 = tk.Label(interface, text = "Please select your file.")


# Get file path
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
folder = str()
interface.file_path = tk.StringVar() # The variable is to store file path

# The function when button 'Open File' is clicked 
def click_file_choose():
    global folder
    folder = fd.askopenfilename() 
    interface.file_path.set(folder)

# Create button to set file path    
file_choose = tk.Button(interface, command = click_file_choose, \
                        text = "Open file")
path_name = tk.Label(interface, textvariable = interface.file_path, \
                     relief = 'sunken', width = 60)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Set import configuration
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create a panel to contain the configs
Import_panel = tk.LabelFrame(interface, text = 'Please choose your import preference.')
# Create a menubotton to store import file type
import_list1 = ('xls', 'xlsx', 'dta', 'csv')
interface.file_type = tk.StringVar()
interface.file_type.set(import_list1[1])
om1 = tk.OptionMenu(Import_panel, interface.file_type, *import_list1)

# Create a menubotton to store header preference
mb1 = tk.Menubutton(Import_panel, text = 'Does the import file has header?', \
                   relief = 'raised')
mb1.menu = tk.Menu(mb1, tearoff = 0)
mb1['menu'] = mb1.menu

def on_header():
    # set header = row number
    global header
    header = 0
def off_header():
    # set header = None
    global header
    header = None

mb1.menu.add_checkbutton(label = 'header', command = on_header)
mb1.menu.add_checkbutton(label = 'no header', command = off_header)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#Set export configuration
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create a panel to contain the configs
Export_panel = tk.LabelFrame(interface, text = 'Please choose your export preference.')
# Create a menubotton to store export data type
export_list1 = ('txt', 'csv')
interface.export_type = tk.StringVar()
interface.export_type.set(export_list1[1])
om3 = tk.OptionMenu(Export_panel, interface.export_type, *export_list1)

# Create a menubotton to store export data encoding
export_list2 = ('ascii', 'utf-8')
interface.export_encoding = tk.StringVar()
interface.export_encoding.set(export_list2[1])
om4 = tk.OptionMenu(Export_panel, interface.export_encoding, *export_list2)

# Create a menubotton to store the separation notation
export_list3 = ('comma', 'space')
interface.export_separate = tk.StringVar()
interface.export_separate.set(export_list3[0])
om5 = tk.OptionMenu(Export_panel, interface.export_separate, *export_list3)
separate = {'comma': ',', 'space': ' '}

# Create a checkbutton to store export header preference
interface.export_header = tk.IntVar()
cb = tk.Checkbutton(Export_panel, text = 'header', variable = interface.export_header)

# Create a report frame to show export path and file name
interface.report = tk.StringVar()
interface.report.set("Please select the file you want to convert, then click the 'file convert' button!")
mess = tk.Message(interface, width = 10000, textvariable = interface.report, \
                  relief = 'sunken')
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# File transform procedure
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def execute():
    # This is the core file transform procedure
    # Input information
    #=========================================================================
    file_type = interface.file_type.get()
    exporter = 'pandas' # 'pandas' or 'astropy'
    export_type = interface.export_type.get()
    #=========================================================================
    # Export options for pandas
    encoding = interface.export_encoding.get()
    sep = separate[interface.export_separate.get()] # Seperation method: ' ' or ','
    na_rep = ' ' # Notation for missing data
    header_e = interface.export_header.get() # True or False (Column names)
    index = False # True or False (Row names)
    #=========================================================================

    # Load Data
    if file_type == 'dta':
        df = pd.read_stata(folder)
    elif file_type == 'xls' or file_type == 'xlsx':
        df = pd.read_excel(folder, header= header)
    elif file_type == 'csv':
        df = pd.read_csv(folder, header= header)

    # Add column names
    if header == None:
        n_cols = df.shape[1]
        column_names = {}
        for i in range(0, n_cols):
            column_names[i] = 'Var'+str(i)
        df = df.rename(index=str, columns= column_names)

    # In fact, use to_csv function can export ascii file
    k = len(file_type)
    if exporter == 'astropy':
        tbl = ast.table.Table.from_pandas(df)
        ast.io.ascii.write(tbl, folder[0:len(folder)-k] + export_type, \
                           format = 'no_header', overwrite = True)
    elif exporter == 'pandas':
        df.to_csv(folder[0:len(folder)-k] + export_type, \
                  sep = sep, na_rep = na_rep, header = header_e, \
                  index = index, encoding = encoding)
    interface.report.set('Your file ' + '"' + folder[0:len(folder)-k] + \
                                                    export_type + '"' + ' is ready!')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    

#_____________________________
def close():                 #|
    # To terminate this app  #|
    interface.destroy()      #|
#____________________________#|


#The control panel to run or terminate this app
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create a panel to contain the buttons
Control_panel = tk.LabelFrame(interface, text = 'Control')
# Create a run button
file_run = tk.Button(Control_panel, command = execute, text = "File convert")
# Create a terminate button
program_off = tk.Button(Control_panel, command = close, text = 'Close')
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Control the item locations
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
des1.grid(row = 1, column = 1) # An Explaination
file_choose.grid(row = 1, column = 2) # The buttom to choose directory
path_name.grid(row = 2, column = 1, columnspan = 2) # Display the directory

Import_panel.grid(row = 3, column = 1)
om1.grid(row = 1, column = 1)
mb1.grid(row = 1, column = 2)

Export_panel.grid(row = 4, column = 1)
om3.grid(row = 1, column = 1)
om4.grid(row = 1, column = 2)
om5.grid(row = 1, column = 3)
cb.grid(row = 1, column = 4)

mess.grid(row = 5, column = 1, columnspan = 2)

Control_panel.grid(row = 4, column = 3)
file_run.grid(row = 1, column = 1) # This is the start buttom
program_off.grid(row = 1, column = 2)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

interface.mainloop()

