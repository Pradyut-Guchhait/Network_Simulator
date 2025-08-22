from typing import Dict, Tuple, List
from dataclasses import dataclass, field

@dataclass
class Link:
    a: str
    b: str
    vlan: int
    bw_mbps: int
    mtu_a: int
    mtu_b: int

@dataclass
class Topology:
    nodes: List[str] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)

def build_topology(devices) -> Topology:
    topo = Topology(nodes=list(devices.keys()))
    # naive neighbor join based on 'neighbor' tokens
    for d in devices.values():
        for iface in d.interfaces:
            if iface.neighbor and iface.neighbor in devices:
                # avoid duplicates A-B and B-A
                pair = tuple(sorted([d.hostname, iface.neighbor]))
                if not any({l.a,l.b}==set(pair) and l.vlan==iface.vlan for l in topo.links):
                    neigh_dev = devices[iface.neighbor]
                    # attempt to find reciprocal interface
                    mtu_b = next((i.mtu for i in neigh_dev.interfaces if i.vlan==iface.vlan), iface.mtu)
                    bw_b = next((i.bw_mbps for i in neigh_dev.interfaces if i.vlan==iface.vlan), iface.bw_mbps)
                    topo.links.append(Link(a=pair[0], b=pair[1], vlan=iface.vlan, bw_mbps=min(iface.bw_mbps,bw_b), mtu_a=iface.mtu, mtu_b=mtu_b))
    return topo
