from typing import Dict, List, Tuple
from collections import defaultdict

def summarize_endpoint_loads(devices):
    by_vlan = defaultdict(int)
    by_node = defaultdict(int)
    for d in devices.values():
        for ep in d.endpoints:
            # use peak_mbps for capacity planning
            by_node[d.hostname] += ep.peak_mbps
        for i in d.interfaces:
            by_vlan[i.vlan] += 0  # ensure key present
    return dict(by_node), dict(by_vlan)

def recommend_load_balancing(devices, topo):
    recs = []
    node_loads, _ = summarize_endpoint_loads(devices)
    # any link that under-caps aggregated adjacent loads -> recommend secondary path
    for l in topo.links:
        load = node_loads.get(l.a,0) + node_loads.get(l.b,0)
        if load > l.bw_mbps:
            recs.append(f"Link {l.a}-{l.b} ({l.bw_mbps} Mbps) may saturate under peak {load} Mbps. Recommend activating/engineering secondary paths or traffic shaping for low-priority flows.")
    return recs

def suggest_protocols(devices):
    # if many routers w/ multiple neighbors -> suggest BGP; otherwise OSPF ok
    routers = [d for d in devices.values() if d.role=='router']
    if len(routers) >= 2 and any(len([i for i in d.interfaces if i.neighbor])>=2 for d in routers):
        return ["Consider using BGP for inter-domain paths; keep OSPF intra-domain."]
    return ["OSPF appears adequate for this scale; revisit if peering expands."]

def node_aggregation(topo):
    # trivial heuristic: aggregate single-link switches into adjacent router
    recs = []
    degree = {}
    for n in topo.nodes:
        degree[n] = sum(1 for l in topo.links if l.a==n or l.b==n)
    for n, deg in degree.items():
        if deg == 1 and n.lower().startswith('sw'):
            recs.append(f"Aggregate {n} into its upstream router to reduce node count, if policy permits.")
    return recs
