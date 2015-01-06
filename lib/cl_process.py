#!/usr/bin/env Python

# IMPORTANT
# ---------
# This tool is for ethical testing purposes only.
#
# Cleveridge and its developers can't be held responsible 
# for any misuse by users. 
# Users have to act as permitted by local law rules.

import dns.resolver
import os
import re
import time
import Tkinter
from Tkinter import *

from threading import Thread

from cnf.cl_config import Cl_config

#support for python 2.7 and 3
try:
    import queue
except:
    import Queue as queue

#-- exit handler for signals.  So ctrl+c will work,  even with py threads. --#
def killme(signum = 0, frame = 0):
    os.kill(os.getpid(), 9)



#-- Return a list of unique sub domains,  alfab. sorted . --#
def extract_subdomains(file_name):
    subs = {}
    sub_file = open(file_name).read()
    #Only match domains that have 3 or more sections subdomain.domain.tld
    domain_match = re.compile("([a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)+")
    f_all = re.findall(domain_match, sub_file)
    del sub_file
    for i in f_all:
        if i.find(".") >= 0:
            p = i.split(".")[0:-1]
            #gobble everything that might be a TLD
            while p and len(p[-1]) <= 3:
                p = p[0:-1]
            #remove the domain name
            p = p[0:-1]
            #do we have a subdomain.domain left?
            if len(p) >= 1:
                #print(str(p) + " : " + i)
                for q in p:
                    if q :
                        #domain names can only be lower case.
                        q = q.lower()
                        if q in subs:
                            subs[q] += 1
                        else:
                            subs[q] = 1
    #Free some memory before the sort...
    del f_all
    #Sort by freq in desc order
    subs_sorted = sorted(subs.keys(), key = lambda x: subs[x], reverse = True)
    return subs_sorted
    
    
    
class lookup(Thread):

    def __init__(self, in_q, out_q, domain, wildcard = False, resolver_list = []):
        Thread.__init__(self)
        self.in_q = in_q
        self.out_q = out_q
        self.domain = domain
        self.wildcard = wildcard
        self.resolver_list = resolver_list
        self.resolver = dns.resolver.Resolver()
        if len(self.resolver.nameservers):
            self.backup_resolver = self.resolver.nameservers
        else:
            #we must have a resolver,  and this is the default resolver on my system...
            self.backup_resolver = ['127.0.0.1']
        if len(self.resolver_list):
            self.resolver.nameservers = self.resolver_list

    def check(self, host):
        slept = 0
        while True:
            try:
                answer = self.resolver.query(host)
                if answer:
                    return str(answer[0])
                else:
                    return False
            except Exception as e:
                if type(e) == dns.resolver.NXDOMAIN:
                    #not found
                    return False
                elif type(e) == dns.resolver.NoAnswer  or type(e) == dns.resolver.Timeout:
                    if slept == 4:
                        #This dns server stopped responding.
                        #We could be hitting a rate limit.
                        if self.resolver.nameservers == self.backup_resolver:
                            #if we are already using the backup_resolver use the resolver_list
                            self.resolver.nameservers = self.resolver_list
                        else:
                            #fall back on the system's dns name server
                            self.resolver.nameservers = self.backup_resolver
                    elif slept > 5:
                        #hmm the backup resolver didn't work, 
                        #so lets go back to the resolver_list provided.
                        #If the self.backup_resolver list did work, lets stick with it.
                        self.resolver.nameservers = self.resolver_list
                        #I don't think we are ever guaranteed a response for a given name.
                        return False
                    #Hmm,  we might have hit a rate limit on a resolver.
                    time.sleep(1)
                    slept += 1
                    #retry...
                elif type(e) == IndexError:
                    #Some old versions of dnspython throw this error,
                    #doesn't seem to affect the results,  and it was fixed in later versions.
                    pass
                else:
                    #dnspython threw some strange exception...
                    raise e

    def run(self):
        while True:
            sub = self.in_q.get()
            if sub != False :
               print 'Try: %s' % (sub)
            	
            if not sub:
                #Perpetuate the terminator for all threads to see
                self.in_q.put(False)
                #Notify the parent of our death of natural causes.
                self.out_q.put(False)
                break
            else:
                try :
                  test = "%s.%s" % (sub, self.domain)
                  addr = self.check(test)
                  if addr and addr != self.wildcard:
                      test = (test, str(addr))
                      self.out_q.put(test)
                except Exception as ex :
                    # do nothing
                    nothing = True







class Cl_process():
	
    def __init__(self, version, build, statusbox, logbox):
        print("Processes initiated")
        self.version = version
        self.build   = build
        self.statusbox = statusbox
        self.logbox  = logbox
    
    
    #___ DEF INTRO ___
    #    ---------
        
    def intro(self, screen) :      
        txt = {}
        txt[0] = '************************************'
        txt[1] = '||  CLEVERIDGE SUBDOMAIN SCANNER  ||'
        txt[2] = '************************************'
        txt[3] = "|| IMPORTANT:                     ||"
        txt[4] = "|| This tool is for ethical       ||"
        txt[5] = "|| testing purpose only.          ||"
        txt[6] = "|| Cleveridge and its owners can't||"
        txt[7] = "|| be held responsible for misuse ||"
        txt[8] = "|| by users.                      ||"
        txt[9] = "|| Users have to act as permitted ||"
        txt[10]= "|| by local law rules.            ||"
        txt[11]= "************************************"
        txt[12]= "||      C l e v e r i d g e       ||"
        txt[13]= "||      Ethical Hacking Lab       ||"
        txt[14]= "||        cleveridge.org          ||"
        txt[15]= "************************************"
        txt[16]= "Version %s build %s" % (self.version, self.build)
        for k,v in txt.items():
            self.logthis(v, screen)  
	
	
	
    #___ DEF IS EXISTING DOMAIN ___
    #    ----------------------     Checks the existance of a domain
	
    def isExistingDomain(self, dmn): # Check if domain is on certain IP       
        from socket import getaddrinfo
		
        try:
            result = getaddrinfo(dmn, None)
            print result[0][0][0] + " | " + result[0][1][0] + " | " + result[0][2][0] + " | " + result[0][3][0]
            return result[0][4][0]
        except:	
            print "False 1"
            return False
        else:
            print "False 2"
            return False
        

    #___ DEF IS VALID DOMAIN ___
    #    -------------------     CHECKS THE STRUCTURE OF GIVEN DOMAIN
    def isValidDomain(self, hostname):
		
        if len(hostname) > 255:
            return False
        else :
            parts = hostname.split('.')
            if len(parts) < 2 or len(parts) > 3:
                return False
            elif len(parts[0]) < 2 or len(parts[1]) < 2:
                return False
            else:
                return True
    
    #___ DEF LOGTHIS ___
    #    -----------     LOGGING TO STATUS- OR LOGBOX (+ write to logfile)
    
    def logthis(self, insert, screen, f=False):
        screen.insert(INSERT, insert + "\n")
        screen.yview(END)
        if f != False:
            with open(f, 'a') as mylog:
                mylog.write(insert)
        screen.update_idletasks()
            
    
    
    #___ DEF ON FIRST RUN ___
    #    ----------------     ON FIRST RUN : SETTING UP BASIC FILES AND FOLDERS
    
    def onFirstRun(self,screen):
        logdir = Cl_config.prog_logdir
        if not os.path.exists(logdir):
            os.makedirs(logdir)
            txt = "\nDirectory 'log/' created"
            self.logthis(txt, screen)
    
    
    
    #___ DEF SCAN ___
    #    --------
    
    def scan(self, domain, method):
        import signal
        import time
                
        from datetime import datetime
        from threading import Thread
        from urllib import urlopen
        
        
        #___ SUB DEF : CHECK RESOLVERS ___#
        #    -------------------------
        def check_resolvers():
            txt = 'Checking Resolvers'
            self.logthis(txt, self.statusbox)
            ret = []
            resolver = dns.resolver.Resolver()
            res_file = open(Cl_config.prog_file_resolvers).read()
            for server in res_file.split("\n"):
                server = server.strip()
                if server:
                    resolver.nameservers = [server]
                    try:
                        resolver.query("www.google.com")
                        #should throw an exception before this line.
                        ret.append(server)
                    except:
                        pass
            return ret
            
        
        def run_target(target, hosts, resolve_list, thread_count):
            #The target might have a wildcard dns record...
            self.logthis('Running...', self.statusbox)
            wildcard = False
            print_numeric = True
            try:
        
                resp = dns.resolver.Resolver().query("would-never-be-a-fucking-domain-name-" + str(random.randint(1, 9999)) + "." + target)
                wildcard = str(resp[0])
            except:
                pass
            in_q = queue.Queue()
            out_q = queue.Queue()
            for h in hosts:
                in_q.put(h)
            #Terminate the queue
            in_q.put(False)
            step_size = int(len(resolve_list) / thread_count)
            #Split up the resolver list between the threads. 
            if step_size <= 0:
                step_size = 1
            step = 0
            for i in range(thread_count):
                threads.append(lookup(in_q, out_q, target, wildcard , resolve_list[step:step + step_size]))
                threads[-1].start()
            step += step_size
            if step >= len(resolve_list):
                step = 0
        
            threads_remaining = thread_count
            subdlist = {}
            subiplist = {}
            i = 0
            while True:
                try:
                    d = out_q.get(True, 10)
                    #we will get an empty exception before this runs. 
                    if not d:
                        threads_remaining -= 1
                    else:
                        if not print_numeric:
                            txt = "%s" % (d[0])
                            self.logthis(txt, self.logbox) 
                            print txt
                        else:
                            txt = "%s -> %s" % (d[0], d[1])
                            self.logthis(txt, self.logbox, logloc)             
                            print(txt)
                            subdlist[i] = txt
                            if d[1] in subiplist.keys() :
                                subiplist[d[1]].append(d[0])
                            else :
                                subiplist[d[1]] = [d[0]]
                            i += 1
                except queue.Empty:
                    pass
                #make sure everyone is complete	        
                if threads_remaining <= 0:
                    print " "
                    print "Done. "
                    txt = 'Subdomains found : %s' % (len(subdlist))
                    
                    # Alfab. ordered result list
                    self.logthis('\n' + txt + '\nOrdered list:\n-------------\n', self.logbox, logloc) 
                    print txt
                    print ' '
                    print 'Ordered List:'
                    for result in sorted(subdlist.values()) :
                       txt = result
                       self.logthis(str(txt) + '\n', self.logbox, logloc) 
                       print txt
                    print ' '
                    
                    # IP-ordered result list
                    txt = "IP-ordered List:"
                    self.logthis('\n' + txt + '\n----------------\n', self.logbox, logloc)
                    print txt
                    for ips in subiplist :
                        txt = ips
                        self.logthis(str(txt) + '\n', self.logbox, logloc)
                        print txt
                        for ipssub in subiplist[ips] :
                        	txt = "      |=> %s" % (ipssub)
                        	self.logthis(str(txt) + '\n', self.logbox, logloc)
                        	print txt
                       
                    end = datetime.now()
                    time_stamp_end = int(time.time())
                    duration = int(time_stamp_end) - int(time_stamp_start)
                    time_end = str(end.year) + "-" + str(end.month) + "-" + str(end.day) + "    " + str(end.hour) + ":" + str(end.minute) + ":" + str(end.second)
                    txt = "Scan Ended : %s" % (time_end)
                    txtB = "Duration : %ss" % (duration)
                    self.logthis('\n' + txt + '\n', self.logbox, logloc)
                    self.logthis(txt, self.statusbox)
                    self.logthis(txtB + '\n', self.logbox, logloc)
                    print " "
                    print txt
                    print txtB
                       
                    
                    break
        
        
        self.logthis(' \nStarting Scan Procedure', self.statusbox)
        
        #-- Checking stucture of given domain --#
        self.logthis('Checking structure of domain', self.statusbox)
        check = self.isValidDomain(domain)
        if check != True:
            self.logthis('   |=> False : Scan Stopped !!', self.statusbox)
        else :
            self.logthis('   |=> OK', self.statusbox)
            
            #-- Create Log File (every run) --#
            now = datetime.now()
            time_stamp_start = int(time.time())
            time_start = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "    " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
            self.logthis(' \nCreating Log File', self.statusbox)
            self.logbox.delete(1.0, END)
            logfile = domain.replace('.', '_') + '_' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + ".log"
            logloc = Cl_config.prog_logdir + "/" + logfile
            with open(logloc, "w") as mylog:
                os.chmod(logloc, 0660)
                self.logthis('   |=> OK, %s' % (logloc), self.statusbox)
                self.logthis("Log created by Cleveridge Subdomain Scanner - " + self.version + " build " + self.build + "\n\n", self.logbox, logloc)
            """  """
            txt = "Scan Started : %s" % (time_start)
            self.logthis(txt, self.statusbox)
            self.logthis(txt + "\n\n", self.logbox, logloc)
            
            #-- Visible IP --#
            try :
                visible_ip = urlopen('https://cleveridge.org/_exchange/open_files/return_ip.php?s=subd_scan_%s_%s' % (self.version, self.build)).read()
            except Exception :
                visible_ip = urlopen('https://enabledns.com/ip').read()
            txt = "Visible IP : " + visible_ip 
            self.logthis(txt, self.statusbox)
            self.logthis(txt + "\n\n", self.logbox, logloc)
            
            #-- Check if domain is active
            self.logthis('Checking response of domain', self.statusbox)
            check = os.system('ping -c1 %s' % (domain))
            check = str(check)
            if check != '0' : 
                txt = 'Domain is not active : Scan Stopped !!'
                self.logthis(txt, self.statusbox)
                self.logthis(txt, self.logbox, logloc)
            else :
                self.logthis("   |=> OK", self.statusbox)
                
                #-- Method --#
                txt = "Method : %s" % (method)
                self.logthis(txt, self.statusbox)
                self.logthis(txt + "\n", self.logbox, logloc)
                meth = {'XS':Cl_config.prog_file_subs_XS, 'S ':Cl_config.prog_file_subs_S, 'M ':Cl_config.prog_file_subs_M, 'L ':Cl_config.prog_file_subs_L, 'XL':Cl_config.prog_file_subs_XL}
                print meth[method[:2]]
                
                #-- Run target --#
                resolve_list = check_resolvers()
                threads = []
                signal.signal(signal.SIGINT, killme)
                hosts = open(meth[method[:2]]).read().split("\n")
                run_target(domain, hosts, resolve_list, 10)
                
        
