"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""
from mininet.topo import Topo

class MyTopo(Topo):
    "Simple topology example."

    def __init__(self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        core_s=list()
        agg_s=list()
        edge_s=list()
        host=list()

        # Add hosts and switches
        for i in range(20):
            if i>15:
                core_s.append(self.addSwitch('s'+str(i)))
            elif i>7 and i<16:
                agg_s.append(self.addSwitch('s'+str(i)))
            else:
                edge_s.append(self.addSwitch('s'+str(i)))
        for i in range(16):
            host.append(self.addHost('h'+str(i)))

        # Add links
        for i in range(16):
            self.addLink(edge_s[int(i/2)],host[i])
        for i in range(4):
            self.addLink(agg_s[2*i],edge_s[2*i])
            self.addLink(agg_s[2*i],edge_s[2*i+1])
            self.addLink(agg_s[2*i+1],edge_s[2*i])
            self.addLink(agg_s[2*i+1],edge_s[2*i+1])
        for i in range(4):
            for k in range(4):
                if i<2:
                    self.addLink(core_s[i], agg_s[2*k])
                else:
                    self.addLink(core_s[i], agg_s[2*k+1])

topos = { 'mytopo': ( lambda: MyTopo() ) }
