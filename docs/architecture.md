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
- **Concurrency**: Routers and switches are represented as independent threads.  
- **IPC Mechanism**: An in‑memory queue models FIFO/TCP communication between devices. 
- **Scalability**: Supports extension to more devices, advanced simulation scenarios, and real configuration grammars.  
- **Outputs**: All results (logs, reports, diagrams) are stored under `outputs/` for traceability and evaluation.  
