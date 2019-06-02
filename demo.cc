#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("Datacenter");

int main (int argc, char *argv[])
{
  int pattern = 0;

  CommandLine cmd;
  cmd.AddValue ("pattern", "Tell echo applications to log if true", pattern); //参数，选择模式几，默认模式1

  cmd.Parse (argc,argv);

  LogComponentEnable ("PacketSink", LOG_LEVEL_INFO); //输出sink收发数据包情况
  LogComponentEnable ("OnOffApplication", LOG_LEVEL_INFO);

  NodeContainer server,tor_switch,agg_switch,core_switch; //创建4类网络节点
  server.Create(8);
  tor_switch.Create(4);
  agg_switch.Create(2);
  core_switch.Create(2);

  NodeContainer csma11=NodeContainer(server.Get(0),server.Get(1),tor_switch.Get(0));
  NodeContainer csma12=NodeContainer(server.Get(2),server.Get(3),tor_switch.Get(1));
  NodeContainer csma13=NodeContainer(server.Get(4),server.Get(5),tor_switch.Get(2));
  NodeContainer csma14=NodeContainer(server.Get(6),server.Get(7),tor_switch.Get(3)); //第一层节点

  NodeContainer csma21=NodeContainer(tor_switch.Get(0),tor_switch.Get(1),agg_switch.Get(0));
  NodeContainer csma22=NodeContainer(tor_switch.Get(2),tor_switch.Get(3),agg_switch.Get(1)); //第二层节点

  NodeContainer csma31=NodeContainer(agg_switch.Get(0),core_switch.Get(0));
  NodeContainer csma32=NodeContainer(agg_switch.Get(1),core_switch.Get(0)); //第三层节点

  NodeContainer csma311=NodeContainer(agg_switch.Get(0),core_switch.Get(1));
  NodeContainer csma322=NodeContainer(agg_switch.Get(1),core_switch.Get(1));


  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("1.5Mbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("0.5ms"));

  NetDeviceContainer p2pDevices[4];
  p2pDevices[0] = pointToPoint.Install (csma31);
  p2pDevices[1] = pointToPoint.Install (csma32); //第三层链路设置

  p2pDevices[2] = pointToPoint.Install (csma311);
  p2pDevices[3] = pointToPoint.Install (csma322);

  CsmaHelper csma;
  csma.SetChannelAttribute ("DataRate", StringValue ("1Mbps"));
  csma.SetChannelAttribute ("Delay", TimeValue (NanoSeconds (500)));

  NetDeviceContainer csmaDevices[6];
  csmaDevices[0] = csma.Install (csma11);
  csmaDevices[1] = csma.Install (csma12);
  csmaDevices[2] = csma.Install (csma13);
  csmaDevices[3] = csma.Install (csma14);
  csmaDevices[4] = csma.Install (csma21);
  csmaDevices[5] = csma.Install (csma22); //前两层链路设置

  InternetStackHelper stack;
  stack.Install (core_switch);
  stack.Install (server);
  stack.Install (agg_switch);
  stack.Install (tor_switch);

  Ipv4AddressHelper address;
  address.SetBase ("192.168.1.0", "255.255.255.0");
  Ipv4InterfaceContainer ip31;
  ip31 = address.Assign (p2pDevices[0]);
  address.SetBase ("192.168.2.0", "255.255.255.0");
  Ipv4InterfaceContainer ip32;
  ip32 = address.Assign (p2pDevices[1]); //设置第三层IP

  address.SetBase ("192.168.3.0", "255.255.255.0");
  Ipv4InterfaceContainer ip311;
  ip311 = address.Assign (p2pDevices[2]); //设置第三层IP
  address.SetBase ("192.168.4.0", "255.255.255.0");
  Ipv4InterfaceContainer ip322;
  ip322 = address.Assign (p2pDevices[3]); //设置第三层IP

  address.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer ip21;
  ip21 = address.Assign (csmaDevices[4]);
  address.SetBase ("10.2.1.0", "255.255.255.0");
  Ipv4InterfaceContainer ip22;
  ip22 = address.Assign (csmaDevices[5]); //设置第二层IP

  address.SetBase ("10.0.1.0", "255.255.255.0");
  Ipv4InterfaceContainer ip1[4];
  ip1[0] = address.Assign (csmaDevices[0]);
  address.SetBase ("10.0.2.0", "255.255.255.0");
  ip1[1] = address.Assign (csmaDevices[1]);
  address.SetBase ("10.0.3.0", "255.255.255.0");
  ip1[2] = address.Assign (csmaDevices[2]);
  address.SetBase ("10.0.4.0", "255.255.255.0");
  ip1[3] = address.Assign (csmaDevices[3]); //设置第一层IP

  Config::SetDefault("ns3::Ipv4GlobalRouting::RandomEcmpRouting",BooleanValue(true));
  Ipv4GlobalRoutingHelper::PopulateRoutingTables (); //初始化路由表

  ApplicationContainer clientApp[8];
  ApplicationContainer sinkApp[8];

  int port=12345; //端口为123456

  for(unsigned int i = 0;i <8; i++) //在每个服务器上设置sink
  {
    PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress(ip1[i/2].GetAddress(i%2),port));
    sinkApp[i] = packetSinkHelper.Install (server.Get(i));
    sinkApp[i].Start(Seconds (1.0));
    sinkApp[i].Stop(Seconds (60.0));
  }

  for(unsigned int i = 0; i < 8; i++)
  {
    if(pattern==1&&i!=0) //在pattern1中设置2-1,3-1,4-1,5-1,6-1,7-1,8-1
    {
     OnOffHelper client("ns3::TcpSocketFactory", InetSocketAddress(ip1[0].GetAddress(0), port));
     client.SetAttribute ("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=50]"));
     client.SetAttribute ("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=0]"));
     client.SetAttribute ("DataRate", DataRateValue (DataRate ("1Mbps")));
     client.SetAttribute ("PacketSize", UintegerValue (2000));

     clientApp[i] = client.Install (server.Get(i));
     clientApp[i].Start(Seconds (1.0));
     clientApp[i].Stop (Seconds (51.0));
   }
   if(pattern==0) //在pattern0中设置1-5,5-1,2-6,6-2,3-7,7-3,4-8,8-4
   {
     OnOffHelper client("ns3::TcpSocketFactory", InetSocketAddress(ip1[((i+4)%8)/2].GetAddress(i%2), port));
     client.SetAttribute ("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=50]"));
     client.SetAttribute ("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=0]"));
     client.SetAttribute ("DataRate", DataRateValue (DataRate ("1Mbps")));
     client.SetAttribute ("PacketSize", UintegerValue (2000));

     clientApp[i] = client.Install (server.Get(i));
     clientApp[i].Start(Seconds (1.0));
     clientApp[i].Stop (Seconds (51.0));
   }
  }

  pointToPoint.EnablePcapAll ("p2p");
  csma.EnablePcapAll ("csma");

  Simulator::Stop (Seconds(50));
  Simulator::Run ();
  Simulator::Destroy ();

  return 0;
}
