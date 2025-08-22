# Network Topology Simulator

A ready-to-run reference implementation that:
- **Parses** router/switch configs to **generate a hierarchical topology**
- **Validates** duplicate IPs, VLAN labels, MTU mismatches, loops, and missing components
- **Plans capacity** and **recommends load balancing** if links can't support peak traffic
- **Simulates Day-1** behaviors (ARP, neighbor/OSPF discovery) and **injects link failures**
- **Uses multithreading** per device and simple **IPC** for metadata exchange
- Provides **logs, a topology image, and a simulation report**

> Built to meet the requirements in the VIP 2025 – Networking stream problem statement. 【5†source】

## Quickstart

```bash
# (Optional) create a virtualenv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Run with sample configs
python -m src.main --conf tests/sample_configs --out outputs

# Inject a link failure
python -m src.main --link-fail R1-R2
```

Outputs are written to `outputs/`:
- `topology.png` – rendered simple topology
- `logs.txt` – thread/device log lines
- `simulation_report.txt` – validations and recommendations

## How it maps to requirements

- **Topology generation** from config files, hierarchy-aware drawing. 【5†source】
- **Bandwidth awareness** and **load balancing recommendations** for saturated links. 【5†source】
- **Validation**: duplicate IPs (per VLAN), wrong/missing components, gateway presence, MTU mismatch, loops. 【5†source】
- **Simulation**: ARP/OSPF discovery; link failure impact listing. 【5†source】
- **Implementation**: multithreading per device; IPC via in-memory queues (FIFO analogue). 【5†source】
- **Day-2 readiness**: re-run after edits; link-failure flag emulates pause/resume scenarios. 【5†source】

## Project Layout

```
src/                # application modules
tests/              # unit tests + sample configs
outputs/            # generated artifacts
docs/               # report & architecture notes
requirements.txt
```

## Extending

- Swap `InMemoryIPC` with TCP sockets for cross-process simulation.
- Add packet-level simulation for real IP packets.
- Integrate richer config grammars (Cisco/Juniper show outputs).

## License

MIT (for your academic submission).
