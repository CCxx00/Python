from mininet.topo import Topo

class MyTopo(Topo):
    "Simple topology example."

    def __init__(self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        core_s=list() # core switch 列表
        agg_s=list() # aggregation switch 列表
        edge_s=list() # edge switch 列表
        host=list() # host switch 列表

        # Add hosts and switches
        for i in range(20):
            if i>15:
                core_s.append(self.addSwitch('s'+str(i))) # 创建4个core switch，命名为s16-s19
            elif i>7 and i<16:
                agg_s.append(self.addSwitch('s'+str(i))) # 创建8个aggregation switch，命名为s8-s15
            else:
                edge_s.append(self.addSwitch('s'+str(i))) # 创建8个edge switch，命名为s0-s7
        host.append(self.addHost('h0', ip='10.0.0.2')) # 创建16个host，命名为h0-h15，并分配ip
        host.append(self.addHost('h1', ip='10.0.0.3'))
        host.append(self.addHost('h2', ip='10.0.1.2'))
        host.append(self.addHost('h3', ip='10.0.1.3'))
        host.append(self.addHost('h4', ip='10.1.0.2'))
        host.append(self.addHost('h5', ip='10.1.0.3'))
        host.append(self.addHost('h6', ip='10.1.1.2'))
        host.append(self.addHost('h7', ip='10.1.1.3'))
        host.append(self.addHost('h8', ip='10.2.0.2'))
        host.append(self.addHost('h9', ip='10.2.0.3'))
        host.append(self.addHost('h10', ip='10.2.1.2'))
        host.append(self.addHost('h11', ip='10.2.1.3'))
        host.append(self.addHost('h12', ip='10.3.0.2'))
        host.append(self.addHost('h13', ip='10.3.0.3'))
        host.append(self.addHost('h14', ip='10.3.1.2'))
        host.append(self.addHost('h15', ip='10.3.1.3'))

        # Add links
        for i in range(16): # 根据fat tree结构，连接链路
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
