# Network Topology Simulator

## Overview

The **Network Topology Simulator** is a reference implementation developed as part of the Cisco-AICTE VIP Program. 
It automates topology generation from router and switch configuration files, validates network consistency, provides 
optimization recommendations, and simulates Day‑1 and Day‑2 events such as link failures and routing discovery.

The tool addresses a common challenge in networking: the absence of a solution that can automatically construct and verify 
a topology from raw device configurations while also supporting simulation and fault injection.

## Key Features

- **Topology Generation**: Automatic construction of hierarchical topologies from device configuration files. 
- **Validation**: Detection of duplicate IP addresses, VLAN inconsistencies, incorrect gateways, MTU mismatches, and network loops. 
- **Performance & Load Management**: Bandwidth‑aware checks with load balancing recommendations under peak demand.  
- **Optimization**: Node aggregation opportunities, protocol recommendations (BGP vs. OSPF), and fault‑tolerant designs.  
- **Simulation**:  
  - Day‑1 scenarios: ARP, neighbor discovery, and OSPF discovery.  
  - Link failure injection: analysis of affected endpoints and impact on traffic.   
- **Implementation Architecture**: Multithreaded device simulation with inter‑process communication (IPC) and per‑node statistics/logging.   

## Project Layout

```
src/                # Application source code
tests/              # Unit tests and sample device configurations
outputs/            # Generated artifacts (topology diagram, logs, reports)
docs/               # Documentation (report, architecture notes, README)
requirements.txt    # Python dependencies
```

## Quick Start

```bash
# (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with provided sample configurations
python -m src.main --conf tests/sample_configs --out outputs

# Inject a link failure between two nodes (example: R1-R2)
python -m src.main --link-fail R1-R2
```

### Outputs

- **topology.png** – Auto‑generated topology diagram.  
- **logs.txt** – Per‑device logs of discovery and simulation events.  
- **simulation_report.txt** – Consolidated validations, optimizations, and fault analysis.  

## Extensibility

The implementation is modular and can be extended with:  
- Real device configuration grammars (Cisco IOS, JunOS, etc.).  
- More advanced IPC mechanisms (FIFO or TCP sockets).  
- Detailed packet‑level protocol simulations.  
- Enhanced visualization and performance dashboards.  

## License

This implementation is released under the MIT license for academic and research purposes.
