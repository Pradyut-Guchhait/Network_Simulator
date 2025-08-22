# Project Report — Network Topology Generation, Validation, and Simulation

**Objective.** Build a tool that automatically creates a hierarchical topology from router configs, validates configuration health, recommends optimizations, and simulates Day‑1/Day‑2 network events. 【5†source】

## 1. Architecture

- **config_parser** parses simplified device configs into a device graph.
- **topology_builder** connects neighbors and annotates links with VLAN, MTU, and bandwidth.
- **validator** performs checks: duplicate IPs in VLANs, MTU mismatches, loops, and missing configs.
- **optimizer** computes peak demands and recommends load balancing, protocol choices (BGP vs OSPF), and node aggregation.
- **simulator** spins threads per device, exchanges metadata over an IPC bus, and records Day‑1 discovery plus fault injection.
- **main** orchestrates the pipeline and writes outputs (logs, PNG, and report).

A lightweight in‑memory IPC queue stands in for FIFO/TCP sockets; swap with sockets for multi‑process runs. 【5†source】

## 2. Configuration Grammar

Example:

```
hostname R1
role router
interface Gi0/0 ip 10.0.0.1/24 vlan 10 mtu 1500 bw_mbps 100 neighbor R2
gateway 10.0.0.254
```

This is intentionally small yet expressive enough to demonstrate the full workflow.

## 3. Algorithms

- **Topology build:** neighbor join + VLAN tagging on links.
- **Validation:** O(V+E) scans; cycle detection via BFS; MTU pairwise check on edges.
- **Capacity & LB:** sum endpoint peak Mbps per node; flag links where sum(load) > bw; recommend secondary path or shaping.
- **Simulation:** short‑running threaded exchange of HELLO messages; optional OSPF flag triggers discovery logs.

## 4. Testing

`pytest`-style tests check parser basics, MTU mismatch detection, and simulation behavior.

## 5. Outputs (sample run)

See `outputs/` after running `python -m src.main`:
- `topology.png` – simple diagram with routers on top, switches below.
- `logs.txt` – inter‑thread messages and OSPF/ARP actions.
- `simulation_report.txt` – validations and recommendations list.

## 6. Limitations & Future Work

- Real CLI configs vary widely; extend parser to vendor‑specific syntaxes.
- True IPC (TCP/FIFO) and message capacity provisioning. 【5†source】
- Detailed protocol state machines (ARP tables, OSPF LSAs), MTU black‑hole simulation.
- Path‑based load sharing (ECMP), policy routing, and failure domains.

## 7. Conclusion

The submission demonstrates automatic topology generation, policy checks, optimization advice, and Day‑1/Day‑2 simulation with fault injection, aligning with the VIP 2025 problem statement. 【5†source】
