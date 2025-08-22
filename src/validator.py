from typing import Dict, List, Tuple, Set
from collections import defaultdict, deque

def _collect_ips(devices):
    by_vlan = defaultdict(list)
    for d in devices.values():
        for i in d.interfaces:
            by_vlan[i.vlan].append((d.hostname, i.ip))
    return by_vlan

def find_duplicate_ips(devices) -> List[str]:
    msgs = []
    by_vlan = _collect_ips(devices)
    for vlan, entries in by_vlan.items():
        ips = [ip for _, ip in entries]
        duplicates = set([ip for ip in ips if ips.count(ip) > 1])
        for dup in duplicates:
            hosts = [h for h, ip in entries if ip == dup]
            msgs.append(f"Duplicate IP {dup} in VLAN {vlan} on {hosts}")
    return msgs

def find_mtu_mismatches(topo) -> List[str]:
    msgs = []
    for l in topo.links:
        if l.mtu_a != l.mtu_b:
            msgs.append(f"MTU mismatch on link {l.a}-{l.b} VLAN {l.vlan}: {l.mtu_a} vs {l.mtu_b}")
    return msgs

def detect_loops(topo) -> List[str]:
    # simple cycle detection using BFS
    adj = defaultdict(list)
    for l in topo.links:
        adj[l.a].append(l.b); adj[l.b].append(l.a)
    visited: Set[str] = set()
    parent = {}
    msgs = []
    for start in adj.keys():
        if start in visited: continue
        q = deque([(start, None)])
        while q:
            node, par = q.popleft()
            if node in visited: 
                continue
            visited.add(node)
            parent[node] = par
            for nb in adj[node]:
                if nb == par: 
                    continue
                if nb in visited and parent[node] != nb:
                    msgs.append(f"Loop detected via {node} -> {nb}")
                else:
                    q.append((nb, node))
    return msgs

def find_missing_components(devices) -> List[str]:
    # endpoint neighbors that reference non-existent devices
    msgs = []
    known = set(devices.keys())
    referenced = set()
    for d in devices.values():
        for i in d.interfaces:
            if i.neighbor:
                referenced.add(i.neighbor)
    missing = referenced - known
    for m in missing:
        msgs.append(f"Missing device configuration for neighbor '{m}'")
    return msgs
