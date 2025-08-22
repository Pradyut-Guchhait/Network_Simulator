# Architecture Overview

```
+----------------------+      +------------------+      +---------------------+
|  Configuration Parser| ---> | Topology Builder | ---> | Validation Engine   |
+----------------------+      +------------------+      +---------------------+
             \                                          /             \
              \                                        /               \
               v                                      v                 v
          +------------------+                +----------------+   +------------+
          | Optimization     |                | Simulation     |   | Orchestrator|
          | Engine           |                | Engine         |   | (main.py)   |
          +------------------+                +----------------+   +------------+
```

### Design Principles

- **Modularity**: Each responsibility (parsing, building, validating, simulating) is encapsulated in a separate module.  
- **Concurrency**: Routers and switches are represented as independent threads. 【28†source】  
- **IPC Mechanism**: An in‑memory queue models FIFO/TCP communication between devices. 【28†source】  
- **Scalability**: Supports extension to more devices, advanced simulation scenarios, and real configuration grammars.  
- **Outputs**: All results (logs, reports, diagrams) are stored under `outputs/` for traceability and evaluation.  
