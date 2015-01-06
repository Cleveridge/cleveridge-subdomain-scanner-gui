#!/usr/bin/env python

#############################################################
# Tool to scan for  subdomains of a specific domain,        #
# thr. TOR with GUI                                         #
#                                                           #
# Initial file written by TheRook                           #
# edited and improved by redN00ws @ Cleveridge              #
#############################################################
#                                                           #
#        C l e v e r i d g e - Ethical Hacking Lab          #
#                 (https://cleveridge.org)                  #
#                                                           #
#############################################################
# Contribution from                                         #
#  - none yet                                               #
#############################################################
#                                                           #
version = "V0.02"
build = "018 gamma"
#############################################################

import os
import Tkinter

from Tkinter   import *

from cnf.cl_config  import Cl_config
from lib.cl_menu    import Cl_menu
from lib.cl_process import Cl_process


#___ INIT ___
#    ----
global logbox
global statusbox


#___ DEF LOGGING ___
#    -----------

def logging(box, insert, f=False):
    box.insert(INSERT, insert + "\n")
    if f == True:
        print 'logfile'

    

#___ MAINFRAME ___
#    ---------

Mainframe = Tkinter.Tk()
try:
	icon = Tkinter.Image("photo", file="lib/img/icon_cleveridge.gif")
	Mainframe.tk.call('wm','iconphoto',Mainframe._w,icon)
except:
	print("No Icon")
Mainframe.title(Cl_config.prog_title)
Mainframe.geometry(Cl_config.prog_size + Cl_config.prog_pos)
Mainframe.columnconfigure(0, weight=1)
Mainframe.rowconfigure(0, weight=1)

#__ MENUFRAME __
#   ---------
menu = Cl_menu()
menuframe = Menu(Mainframe)
projectmenu = Menu(menuframe, tearoff=0, bg="#FFFFFF")
projectmenu.add_command(label="New Project", command=menu.project_new)
projectmenu.add_command(label="View Logs", command=menu.project_viewlogs)
projectmenu.add_command(label="Close", command=Mainframe.quit)
projectmenu.insert_separator(2)
menuframe.add_cascade(label="Project", menu=projectmenu)

helpmenu = Menu(menuframe, tearoff=0, bg="#FFFFFF")
helpmenu.add_command(label="About", command=menu.help_about)
menuframe.add_cascade(label="Help", menu=helpmenu)
Mainframe.config(menu=menuframe)


#__ TOOLFRAME __
#   ---------
global domaininput
domaininput = StringVar()
spininput   = StringVar()

        
    
def layout_build_toolframe():
    
    def scan():
        domain = domaininput.get()
        method = spininput.get()
        print domain
        print spininput.get()
        process.scan(domain, method)
    
    toolframe = LabelFrame(Mainframe, text='Home', height=450)
    toolframe.grid(column=0, row=0, sticky=Tkinter.N+Tkinter.E+Tkinter.S+Tkinter.W, pady=5, padx=5)
    
    tool_domainframe = Frame(toolframe, height=40)
    tool_domainframe.grid(column=0, row=0, columnspan=2, sticky='nw', pady=5, padx=5)
    
    tool_domainframe_text = Label(tool_domainframe, text='Domain: http://www.')
    tool_domainframe_text.grid(column=0, row=0, pady=3, padx=3)
    
    tool_domainframe_input = Entry(tool_domainframe, width=30, textvariable=domaininput)
    tool_domainframe_input.grid(column=1, row=0, pady=3, padx=0)
    
    options = ["XS Scan (fastest, less complete)", "S Scan (fast)", "M Scan (recommended)", "L Scan (slow)", "XL Scan (slowest, most complete)"]
    spininput.set("M Scan (recommended)")
    tool_domainframe_spin = OptionMenu(tool_domainframe, spininput, *options)
    tool_domainframe_spin.grid(column=2, row=0, pady=3, padx=0)
    
    tool_domainframe_bttn = Button(tool_domainframe, text='Scan', command=scan)
    tool_domainframe_bttn.grid(column=3, row=0, pady=3, padx=0)
    
    # Status Frame
    tool_statusframe = LabelFrame(toolframe, text='Status', height=390, width=300)
    tool_statusframe.grid(column=0, row=1, sticky=N+S+E+W, pady=5, padx=5)
    
    statusframe_scroll = Scrollbar(tool_statusframe)
    statusbox = Text(tool_statusframe, bg="GRAY", height=25, width=40, yscrollcommand=statusframe_scroll.set)
    statusbox.grid(column=0, row=0, sticky=N+S+E+W)
    
    # Log Frame
    tool_logframe = LabelFrame(toolframe, text='Log', width=700)
    tool_logframe.grid(column=1, row=1, sticky=N+S+E+W, pady=5, padx=5)
    
    logframe_scroll = Scrollbar(tool_logframe)
    logbox = Text(tool_logframe, bg="WHITE", height=25, width=98, yscrollcommand=logframe_scroll.set)
    logbox.grid(column=0, row=0, sticky=N+S+E+W)
    logframe_scroll.config(command=logbox.yview)
    
    process = Cl_process(version, build, statusbox, logbox)
    process.intro(statusbox)
    process.onFirstRun(statusbox)
    

layout_build_toolframe()


#__ FOOTERFRAME __
#   -----------
footerframe = Frame(Mainframe, height=40)
footerframe.grid(column=0, row=1, sticky='ew',pady=5, padx=5)
footer_text = Label( footerframe, text=Cl_config.prog_footer)
footer_text.pack()



Mainframe.mainloop()
