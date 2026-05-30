#!/usr/bin/env python3
import json
from pathlib import Path
TOPICS_DIR = Path(__file__).parent.parent / "data" / "topics"

def t(id,dom,ph,name,diff,what,why,concepts,tags):
    return {"id":id,"domain":dom,"phase":ph,"name":name,"difficulty":diff,
            "theory":{"what":what,"why":why,"how":"See documentation.",
            "when":"Apply in relevant scenarios.",
            "key_concepts":concepts,
            "configuration":"# See official docs",
            "troubleshooting":["Check logs","Verify config","Test connectivity"]},
            "related_topics":[],"tags":tags}

noc=[
t("nagios-mon","noc_operations",3,"Nagios","intermediate","Open-source monitoring for hosts and services.","Legacy but widely deployed in enterprises.",["Host checks","Service checks","Plugins","Notifications"],["nagios","monitoring"]),
t("snmp-traps2","noc_operations",3,"SNMP Traps","intermediate","Async notifications from devices to NMS.","Immediate notification vs polling delay.",["Trap vs Inform","Trap receiver","OID mapping"],["snmp","traps","async"]),
t("config-backup","noc_operations",3,"Automated Config Backup","beginner","Auto-backup device configs on schedule.","Manual backups get forgotten.",["Oxidized","RANCID","Git","Scheduling"],["backup","config","automated"]),
t("forecasting","noc_operations",3,"Capacity Forecasting","advanced","Predicting future needs from trends.","Prevents resource exhaustion.",["Linear regression","Growth rate","Lead time"],["forecasting","capacity"]),
t("runbooks2","noc_operations",3,"NOC Runbooks","beginner","Step-by-step incident procedures.","Ensures consistent handling.",["Procedures","Decision trees","Escalation"],["runbooks","procedures"]),
t("correlation","noc_operations",3,"Event Correlation","advanced","Relating events to find root cause.","Single events are noise; correlated reveal problems.",["Temporal","Topological","Rule-based"],["correlation","events"]),
t("weathermap","noc_operations",3,"Network Weather Maps","intermediate","Visual utilization on topology.","Instant visual network status.",["Topology overlay","Color coding","Real-time"],["weathermap","visualization"]),
t("oncall","noc_operations",3,"On-Call Management","beginner","24/7 coverage with rotations.","Networks run 24/7.",["Rotation","Escalation","Response SLA"],["on-call","rotation"]),
t("maint-window","noc_operations",3,"Maintenance Windows","beginner","Scheduled change periods.","Minimize business impact.",["Scheduling","Communication","Freeze periods"],["maintenance","window"]),
t("vendor-mgmt","noc_operations",3,"Vendor/ISP Management","intermediate","Managing ISP relationships.","Need contacts when links fail.",["Circuit IDs","Escalation","SLA tracking"],["vendor","isp"]),
t("dr-network","noc_operations",3,"Network DR","advanced","Recovery after major failures.","Without DR, recovery is chaotic.",["DR site","Failover","RTO/RPO","Testing"],["disaster-recovery","failover"]),
t("inventory-mgmt","noc_operations",3,"Inventory Management","beginner","Tracking all network assets.","Can't manage what you don't know.",["Asset tracking","EOL","Warranty","Location"],["inventory","assets"]),
t("log-techniques","noc_operations",3,"Log Analysis Techniques","intermediate","Efficiently analyzing large log volumes.","Extract actionable insights from noise.",["Pattern matching","Regex","Aggregation","Timeline"],["logs","analysis"]),
]
eng=[
t("redistribution","network_engineering",2,"Route Redistribution","advanced","Sharing routes between protocols.","Multi-protocol needs route sharing.",["Seed metric","Route maps","Loop prevention"],["redistribution","routing"]),
t("route-filter","network_engineering",2,"Route Filtering","intermediate","Controlling advertised/accepted routes.","Prevents route leaks.",["Prefix lists","Route maps","AS-path filters"],["filtering","routes"]),
t("campus-design","network_engineering",2,"Campus Network Design","intermediate","Three-tier or collapsed core for LANs.","Proper design ensures scalability.",["Access","Distribution","Core","Collapsed"],["campus","design"]),
t("dc-design","network_engineering",2,"Data Center Design","advanced","Leaf-spine for modern data centers.","Three-tier doesn't scale for east-west.",["Leaf-spine","ECMP","Oversubscription"],["datacenter","leaf-spine"]),
t("wan-tech","network_engineering",2,"WAN Technologies","intermediate","MPLS, Metro Ethernet, broadband, SD-WAN.","Understanding options for site connectivity.",["MPLS","Metro Ethernet","LTE/5G","SD-WAN"],["wan","connectivity"]),
t("multicast","network_engineering",2,"IP Multicast","advanced","One-to-many efficient delivery.","Efficient for video/streaming.",["IGMP","PIM","RP","Multicast addresses"],["multicast","igmp"]),
t("ipv6-route","network_engineering",2,"IPv6 Routing","intermediate","OSPFv3, MP-BGP for IPv6.","IPv6 adoption requires routing knowledge.",["OSPFv3","MP-BGP","Link-local next-hops"],["ipv6","routing"]),
t("gre","network_engineering",2,"GRE Tunnels","intermediate","Point-to-point tunnels over IP.","Connect non-contiguous networks.",["Encapsulation","MTU","Recursive routing"],["gre","tunnel"]),
t("pbr","network_engineering",2,"Policy-Based Routing","advanced","Route by source, protocol, not just destination.","Traffic engineering beyond destination routing.",["Route maps","Match criteria","Set next-hop"],["pbr","policy"]),
t("redundancy-design","network_engineering",2,"Redundancy Design","intermediate","No single point of failure.","Ensures continuity.",["Dual-homed","Active/Standby","ECMP"],["redundancy","ha"]),
t("qos-voice","network_engineering",2,"QoS for VoIP","intermediate","Prioritizing voice traffic.","Voice needs <150ms delay, <1% loss.",["EF marking","Priority queue","LLQ"],["qos","voip"]),
t("rstp-mstp","network_engineering",2,"RSTP/MSTP","intermediate","Fast STP convergence (1-2s).","Classic STP takes 30-50s.",["RSTP roles","Edge ports","BPDU Guard"],["rstp","mstp","fast"]),
t("dhcp-relay2","network_engineering",2,"DHCP Relay","beginner","Forward DHCP across subnets.","Broadcasts don't cross routers.",["ip helper-address","Option 82"],["dhcp","relay"]),
t("acls","network_engineering",2,"Access Control Lists","beginner","Packet filtering on routers.","Basic network security building block.",["Standard","Extended","Named","Wildcard masks"],["acl","filtering"]),
]
cloud=[
t("direct-connect","cloud_networking",5,"AWS Direct Connect","advanced","Dedicated connection to AWS.","Consistent performance vs internet VPN.",["Dedicated","Hosted","LAG","Virtual interfaces"],["direct-connect","aws"]),
t("expressroute","cloud_networking",5,"Azure ExpressRoute","advanced","Private connectivity to Azure.","Predictable performance.",["Private peering","Microsoft peering","Global Reach"],["expressroute","azure"]),
t("cloud-dns2","cloud_networking",5,"Cloud DNS Services","intermediate","Managed DNS — Route 53, Cloud DNS.","Global, highly available DNS.",["Hosted zones","Health checks","Routing policies"],["dns","cloud"]),
t("cdn","cloud_networking",5,"Cloud CDN","intermediate","Cache content at edge locations.","Reduces latency for users.",["Edge locations","Cache","TTL","Invalidation"],["cdn","caching"]),
t("cloud-waf2","cloud_networking",5,"Cloud WAF","intermediate","Managed WAF services.","Protect web apps without hardware.",["Managed rules","Rate limiting","Bot protection"],["waf","cloud"]),
t("service-mesh2","cloud_networking",5,"Service Mesh","advanced","Service-to-service communication layer.","Microservices need discovery, LB, encryption.",["Sidecar proxy","mTLS","Traffic management"],["service-mesh","istio"]),
t("container-net","cloud_networking",5,"Container Networking","intermediate","How containers communicate.","Containers need networking.",["Bridge","Overlay","CNI","Pod networking"],["container","kubernetes"]),
t("cloud-fw","cloud_networking",5,"Cloud Firewall","intermediate","Cloud-native firewalls.","Stateful inspection for cloud.",["Stateful","IDS/IPS","URL filtering"],["firewall","cloud"]),
t("private-ep","cloud_networking",5,"Private Endpoints","intermediate","Access cloud services privately.","No internet exposure for service access.",["Interface endpoints","PrivateLink","DNS"],["private-endpoint","secure"]),
t("cloud-mon","cloud_networking",5,"Cloud Network Monitoring","intermediate","VPC Flow Logs, Network Watcher.","Visibility into cloud traffic.",["Flow Logs","Traffic Analytics","Packet Mirroring"],["monitoring","cloud"]),
]

sec=[
t("ikev2","network_security",4,"IKEv2 VPN","intermediate","Modern VPN with fast reconnection.","Preferred for modern VPNs.",["MOBIKE","EAP","Dead peer detection"],["ikev2","vpn"]),
t("ssl-vpn2","network_security",4,"SSL/TLS VPN","intermediate","VPN using TLS — works through firewalls.","Works anywhere HTTPS works.",["Clientless","Full tunnel","Split tunnel"],["ssl-vpn","remote"]),
t("seg-patterns","network_security",4,"Segmentation Patterns","intermediate","DMZ, three-zone, micro-perimeter.","Proper design limits blast radius.",["DMZ","Three-zone","PCI CDE isolation"],["segmentation","patterns"]),
t("ips-tuning","network_security",4,"IPS Tuning","advanced","Balance detection vs false positives.","Out-of-box IPS is too noisy.",["Signature tuning","Thresholds","Exclusions"],["ips","tuning"]),
t("net-encryption","network_security",4,"Network Encryption","intermediate","MACsec, IPsec, WireGuard.","Protect data in transit.",["MACsec","IPsec","WireGuard","Key management"],["encryption","transit"]),
t("ndr","network_security",4,"Network Detection & Response","advanced","Behavioral threat detection.","Catches unknown threats signatures miss.",["NDR","Behavioral analytics","ML-based"],["ndr","detection"]),
t("honeypots","network_security",4,"Honeypots/Deception","advanced","Fake services to detect attackers.","Zero false positives.",["Honeypots","Canary tokens","Early warning"],["deception","honeypot"]),
t("radius-tacacs2","network_security",4,"RADIUS & TACACS+","intermediate","Centralized AAA protocols.","Consistent access control.",["RADIUS","TACACS+","AAA model"],["radius","tacacs","aaa"]),
t("port-sec","network_security",4,"Port Security","beginner","Limit MACs per switch port.","Prevent rogue devices.",["MAC limiting","Sticky MAC","Violation modes"],["port-security","mac"]),
t("dhcp-snoop","network_security",4,"DHCP Snooping","intermediate","Block rogue DHCP servers.","Prevent MITM via rogue DHCP.",["Trusted/untrusted","Binding table","DAI"],["dhcp-snooping","layer2"]),
]

auto=[
t("jinja2","network_automation",6,"Jinja2 Templates","beginner","Config generation from variables.","Eliminate repetitive config writing.",["Variables","Loops","Conditionals","Filters"],["jinja2","templates"]),
t("textfsm","network_automation",6,"TextFSM Parsing","intermediate","Parse CLI output to structured data.","Automation needs structured data.",["Templates","State machine","NTC-templates"],["textfsm","parsing"]),
t("paramiko2","network_automation",6,"Paramiko SSH","intermediate","Low-level Python SSH library.","Foundation for Netmiko.",["SSH connection","Command execution","SFTP"],["paramiko","ssh"]),
t("openapi","network_automation",6,"OpenAPI/Swagger","beginner","API documentation standard.","Good docs enable faster integration.",["OpenAPI spec","Swagger UI","Schemas"],["api","swagger"]),
t("event-driven","network_automation",6,"Event-Driven Automation","advanced","Trigger automation on events.","Instant response without humans.",["Event sources","Triggers","StackStorm"],["event-driven","reactive"]),
t("batfish2","network_automation",6,"Batfish Analysis","advanced","Offline config analysis.","Test changes before production.",["Config analysis","Policy verification","What-if"],["batfish","offline"]),
t("ansible-roles2","network_automation",6,"Ansible Roles","intermediate","Reusable automation units.","Code reuse across projects.",["Role structure","Galaxy","Dependencies"],["ansible","roles"]),
t("sot","network_automation",6,"Source of Truth","intermediate","NetBox as authoritative data source.","Automation needs accurate data.",["NetBox","Intended state","API-driven"],["source-of-truth","netbox"]),
t("config-compliance2","network_automation",6,"Config Compliance","intermediate","Auto-check configs against standards.","Manual checking doesn't scale.",["Compliance rules","Deviation reporting","Audit"],["compliance","standards"]),
t("net-as-code","network_automation",6,"Network as Code","advanced","Entire network as version-controlled code.","Reproducible, testable infrastructure.",["GitOps","Declarative","Idempotent","CI/CD"],["network-as-code","gitops"]),
]

# Save
for name,data in [("gen4_noc.json",noc),("gen4_eng.json",eng),("gen4_cloud.json",cloud),("gen4_sec.json",sec),("gen4_auto.json",auto)]:
    with open(TOPICS_DIR/name,'w') as f: json.dump(data,f,indent=2)
    print(f"  {name}: {len(data)}")

total=0
for f in TOPICS_DIR.glob("*.json"):
    with open(f) as fp: total+=len(json.load(fp))
print(f"\nTOTAL: {total}")
