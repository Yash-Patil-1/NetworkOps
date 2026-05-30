# Application Flow
## NetworkOps — Network Operations Learning Platform

---

## Navigation

```
┌─────────────────────────────────────────────────────────────┐
│  Sidebar (fixed)                │  Main Content              │
│                                 │                            │
│  🌐 NetworkOps                  │                            │
│                                 │                            │
│  📊 Dashboard                   │  (varies by route)         │
│  📖 Learning Paths              │                            │
│  📚 Topics                      │                            │
│  🧪 Quiz                        │                            │
│  🔌 Protocols                   │                            │
│  📈 Progress                    │                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Pages

### Topic Detail (Theory)
```
┌─────────────────────────────────────────────────────┐
│  OSPF Fundamentals                                   │
│  Domain: Network Engineering | Phase: 2 | Medium    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  📋 WHAT                                             │
│  Open Shortest Path First is a link-state...        │
│                                                      │
│  ❓ WHY                                              │
│  OSPF is the most widely used IGP because...        │
│                                                      │
│  ⚙️  HOW                                             │
│  OSPF builds a Link-State Database by...            │
│  [Diagram: OSPF neighbor states]                    │
│                                                      │
│  📅 WHEN                                             │
│  Use OSPF when you need fast convergence...         │
│                                                      │
│  💻 CONFIGURATION                                    │
│  ┌─────────────────────────────────────────────┐    │
│  │ router ospf 1                                │    │
│  │  network 10.0.0.0 0.0.0.255 area 0         │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  🔧 TROUBLESHOOTING                                  │
│  • show ip ospf neighbor                            │
│  • show ip ospf database                            │
│                                                      │
│  [🧪 Take Quiz] [✅ Mark Learned]                    │
└─────────────────────────────────────────────────────┘
```

### Quiz Page
```
┌─────────────────────────────────────────────────────┐
│  Quiz: OSPF                          Question 3/10  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  SCENARIO:                                           │
│  You notice that two OSPF routers on the same       │
│  segment are not forming a neighbor relationship.    │
│  Both have matching area IDs and hello timers.       │
│  What else could prevent adjacency?                  │
│                                                      │
│  ┌─────────────────────────────────────────────┐    │
│  │ Type your answer here...                     │    │
│  │                                              │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  [💡 Hint] [Submit Answer]                           │
│                                                      │
│  ─── After Submit ───                                │
│                                                      │
│  ✅ Correct! Mismatched subnet masks or              │
│  authentication mismatch can prevent adjacency.      │
│                                                      │
│  [Next Question →]                                   │
└─────────────────────────────────────────────────────┘
```
