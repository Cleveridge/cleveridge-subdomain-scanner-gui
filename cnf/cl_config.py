#!/usr/bin/env Python

# IMPORTANT
# ---------
# This tool is for ethical testing purposes only.
#
# Cleveridge and its developers can't be held responsible 
# for any misuse by users. 
# Users have to act as permitted by local law rules.

# GENERAL SETTINGS

global company, company_url
company       = "Cleveridge"
company_url   = "http://www.cleveridge.org"
developer     = "redN00ws"
developer_url = "http://www.hackcommunity.com/User-redN00ws"


class Cl_config:
	prog_title = "Cleveridge Subdomain Scanner"
	prog_version = "0.02"
	prog_build   = "001 gamma"
	prog_size    = '1024x500'
	prog_pos     = '+25+300' 	# include + or -
	prog_icon    = 'lib/img/icon_cleveridge.ico'
	prog_footer  = 'C l e v e r i d g e - Ethical Hacking Lab - https://cleveridge.org'
	prog_logdir  = 'log'
	prog_file_resolvers = 'lib/cl_resolvers.txt'
	prog_file_subs_XS   = 'lib/cl_subs_xsmall.txt'
	prog_file_subs_S    = 'lib/cl_subs_small.txt'
	prog_file_subs_M    = 'lib/cl_subs_medium.txt'
	prog_file_subs_L    = 'lib/cl_subs_large.txt'
	prog_file_subs_XL    = 'lib/cl_subs_xlarge.txt'
