sudo ovs-ofctl add-flow s19 arp,arp_tpa=10.0.0.0/16,actions=output:1
sudo ovs-ofctl add-flow s19 arp,arp_tpa=10.1.0.0/16,actions=output:2
sudo ovs-ofctl add-flow s19 arp,arp_tpa=10.2.0.0/16,actions=output:3
sudo ovs-ofctl add-flow s19 arp,arp_tpa=10.3.0.0/16,actions=output:4
sudo ovs-ofctl add-flow s19 ip,nw_dst=10.0.0.0/16,actions=output:1
sudo ovs-ofctl add-flow s19 ip,nw_dst=10.1.0.0/16,actions=output:2
sudo ovs-ofctl add-flow s19 ip,nw_dst=10.2.0.0/16,actions=output:3
sudo ovs-ofctl add-flow s19 ip,nw_dst=10.3.0.0/16,actions=output:4
