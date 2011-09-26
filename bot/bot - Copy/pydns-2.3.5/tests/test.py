#!/usr/bin/python

import sys ; sys.path.insert(0, '..')

import DNS
# automatically load nameserver(s) from /etc/resolv.conf
# (works on unix - on others, YMMV)
# DNS.ParseResolvConf()
DNS.DiscoverNameServers() 

# lets do an all-in-one request
# set up the request object
r = DNS.DnsRequest(name='munnari.oz.au',qtype='A')
# do the request
a=r.req()
# and do a pretty-printed output
a.show()

# now lets setup a reusable request object
r = DNS.DnsRequest(qtype='ANY')
res = r.req("a.root-servers.nex",qtype='ANY')
res.show()
res = r.req("proxy.connect.com.au")
res.show()

# do a TCP reply
r = DNS.DnsRequest("imsavscan.netvigator.com", qtype="A", server=['8.8.8.8'], protocol='tcp', timeout=300)
res = r.req()
res.show()
