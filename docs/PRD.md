# Product Requirements Document (PRD)
## NetworkOps — Network Operations Learning Platform

---

## 1. Product Overview

**Product Name:** NetworkOps  
**Version:** 1.0  
**Author:** Yash Patil  
**Date:** 2026-05-30  

### 1.1 Vision Statement
NetworkOps is a local-first networking learning platform that teaches network engineering, NOC operations, network security, cloud networking, and automation through structured theory, practical examples, and an intelligent quiz system. Inspired by TryHackMe + Cisco Packet Tracer + Wireshark + Grafana.

### 1.2 Problem Statement
- Networking knowledge is scattered across vendor docs, RFCs, and certifications
- No single platform teaches NOC + Engineering + Security + Cloud + Automation together
- Existing tools (Packet Tracer, GNS3) focus on simulation, not conceptual understanding
- Learners need theory (why/how/when) + practical commands + quizzes to retain knowledge

### 1.3 Target Users
| User Type | Description |
|-----------|-------------|
| CCNA/CCNP Students | Preparing for Cisco certifications |
| NOC Engineers | Learning monitoring and troubleshooting |
| Network Security Engineers | Understanding firewalls, IDS, segmentation |
| Cloud Engineers | Learning AWS/Azure/GCP networking |
| DevOps/NetOps | Learning automation (Ansible, Terraform) |

---

## 2. Goals & Success Metrics

| Metric | Target |
|--------|--------|
| Topics documented | 300+ |
| Theory chapters | 50+ |
| Quiz questions | 500+ (100 per domain minimum) |
| Domains covered | 6 |
| Protocols explained | 40+ |

---

## 3. Features & Requirements

### 3.1 Core Features

#### F1: Theory Engine (Why, How, When)
- Each topic has a structured theory section explaining:
  - **What** it is (definition, purpose)
  - **Why** it matters (real-world importance)
  - **How** it works (mechanism, packet flow, architecture)
  - **When** to use it (scenarios, use cases)
  - **Configuration examples** (commands, configs)
  - **Troubleshooting** (common issues, debugging)
  - **Related topics** (prerequisites, next steps)

#### F2: Quiz System (Intelligent, Low-Repetition)
- Questions per chapter/topic
- **Question types:**
  - Theory recall (what is X?)
  - Command-type (user types actual command as answer)
  - Scenario-based (unseen scenario, test real understanding)
  - Troubleshooting (given symptoms, identify cause)
  - Configuration (write the config for scenario X)
- **Repetition control:** Question repeats only after 80+ others from same chapter
- **Answer validation:**
  - Check local answer database first
  - If not found, validate against known patterns
  - Support multiple correct answers (e.g., different valid commands)
- **Scoring:** Track correct/incorrect per topic, show weak areas

#### F3: Knowledge Base (Structured JSON)
- 300+ topics across 6 domains
- Each topic: theory + examples + commands + quiz questions
- Searchable, filterable by domain/protocol/difficulty

#### F4: Learning Paths (6 Phases)
1. Networking Fundamentals
2. Network Engineering
3. NOC Operations
4. Network Security
5. Cloud Networking
6. Network Automation

#### F5: Protocol Explorer
- Visual protocol explanations
- Packet structure diagrams (text-based)
- Header field explanations
- Real-world examples

#### F6: Configuration Explorer
- Device configurations (router, switch, firewall)
- Annotated line-by-line explanations
- Best practices vs common mistakes

#### F7: Progress & Analytics
- Track topics learned, quizzes taken
- Identify weak areas
- Recommended next topics
- Streak tracking

### 3.2 Nice-to-Have (v2)
- Topology visualization
- Packet flow animation
- AI-powered question generation
- Flashcard mode
- Export study notes

---

## 4. Constraints

| Constraint | Details |
|-----------|---------|
| No Docker / VMs / Cloud | Runs locally |
| No paid APIs | All content is local JSON |
| No simulation | Educational theory + quiz, not lab |
| Offline capable | Works without internet |
| Performance | 4GB+ RAM |

---

## 5. Quiz System Detail

### Question Schema
```json
{
  "id": "q-ospf-areas-01",
  "topic_id": "ospf-areas",
  "domain": "network_engineering",
  "type": "scenario",
  "difficulty": "medium",
  "question": "You have a network with 500 routers. OSPF is running in a single area and the SPF calculation is taking too long. What architectural change would you make?",
  "correct_answers": ["divide into multiple areas", "create area 0 backbone with stub areas", "implement multi-area OSPF"],
  "explanation": "With 500 routers in one area, the LSDB becomes too large. Multi-area OSPF reduces SPF computation by limiting the LSDB size per area.",
  "hints": ["Think about OSPF scalability", "What limits SPF calculation time?"],
  "tags": ["ospf", "scalability", "design"]
}
```

### Command-Type Question
```json
{
  "id": "q-ospf-cmd-01",
  "topic_id": "ospf-config",
  "domain": "network_engineering",
  "type": "command",
  "difficulty": "easy",
  "question": "Write the command to enable OSPF process 1 on a Cisco router and advertise network 192.168.1.0/24 in area 0.",
  "correct_answers": [
    "router ospf 1\nnetwork 192.168.1.0 0.0.0.255 area 0",
    "router ospf 1\\nnetwork 192.168.1.0 0.0.0.255 area 0"
  ],
  "validation_type": "contains_all",
  "required_keywords": ["router ospf", "network 192.168.1.0", "area 0"],
  "explanation": "OSPF is enabled with 'router ospf <process-id>' and networks are advertised using wildcard masks."
}
```

### Repetition Algorithm
```
For each chapter with N questions:
- Maintain a "seen" queue per user per chapter
- When selecting next question:
  1. Filter out questions in the last min(80, N-1) seen
  2. Pick randomly from remaining
  3. Add to seen queue
- This ensures 81% minimum gap before repeat
```

---

## 6. Content Scope (v1)

### Domain 1: Networking Fundamentals (60 topics)
OSI Model, TCP/IP, Ethernet, ARP, DNS, DHCP, NAT, PAT, Subnetting, VLANs, Trunking, STP, IPv4, IPv6, ICMP, UDP, TCP, HTTP, HTTPS, FTP, SSH, Telnet, SNMP, NTP, Syslog...

### Domain 2: Network Engineering (50 topics)
OSPF, BGP, EIGRP, RIP, Static Routing, MPLS, VXLAN, EtherChannel, HSRP, VRRP, GLBP, QoS, Network Design, Campus Design, WAN Design, SD-WAN...

### Domain 3: NOC Operations (40 topics)
Monitoring (SNMP, NetFlow, sFlow), Alerting, Dashboards, Incident Response, Capacity Planning, Troubleshooting Methodology, Root Cause Analysis, SLA Management, Change Management...

### Domain 4: Network Security (50 topics)
Firewalls (stateful, stateless, NGFW), IDS/IPS, NAC, 802.1X, Segmentation, Microsegmentation, Zero Trust, VPN (IPSec, SSL), WAF, DDoS Mitigation, SIEM, Packet Analysis...

### Domain 5: Cloud Networking (40 topics)
AWS VPC, Subnets, Route Tables, Security Groups, NACLs, NAT Gateway, Transit Gateway, VPC Peering, Azure VNet, NSGs, GCP VPC, Hybrid Connectivity, Direct Connect, ExpressRoute...

### Domain 6: Network Automation (60 topics)
Python for Networking, Netmiko, Paramiko, NAPALM, Nornir, Ansible (network modules), Terraform (network resources), REST APIs, NETCONF, YANG, gNMI, Infrastructure as Code...

**Total: ~300 topics, 500+ quiz questions**

---

## 7. Out of Scope (v1)
- Live network simulation/emulation
- Actual device configuration
- Packet capture/analysis (use Wireshark separately)
- Cloud account integration
- User authentication
