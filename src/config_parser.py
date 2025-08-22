from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import re, pathlib

@dataclass
class Interface:
    name: str
    ip: str
    vlan: Optional[int]
    mtu: int
    bw_mbps: int
    neighbor: Optional[str]

@dataclass
class Endpoint:
    name: str
    app_type: str
    peak_mbps: int
    avg_mbps: int

@dataclass
class Device:
    hostname: str
    role: str  # router or switch
    interfaces: List[Interface] = field(default_factory=list)
    endpoints: List[Endpoint] = field(default_factory=list)
    gateway: Optional[str] = None
    ospf_enabled: bool = False

def parse_config_file(path: pathlib.Path) -> Device:
    text = path.read_text()
    hostname = re.search(r"hostname\s+(\S+)", text).group(1)
    role = re.search(r"role\s+(\S+)", text).group(1)
    dev = Device(hostname=hostname, role=role)

    for m in re.finditer(r"interface\s+(\S+)\s+ip\s+(\S+)\s+vlan\s+(\d+)\s+mtu\s+(\d+)\s+bw_mbps\s+(\d+)(?:\s+neighbor\s+(\S+))?", text):
        name, ip, vlan, mtu, bw, neigh = m.groups()
        dev.interfaces.append(Interface(name=name, ip=ip, vlan=int(vlan), mtu=int(mtu), bw_mbps=int(bw), neighbor=neigh))

    for m in re.finditer(r"endpoint\s+(\S+)\s+type\s+(\S+)\s+peak_mbps\s+(\d+)\s+avg_mbps\s+(\d+)", text):
        ep = Endpoint(name=m.group(1), app_type=m.group(2), peak_mbps=int(m.group(3)), avg_mbps=int(m.group(4)))
        dev.endpoints.append(ep)

    gw = re.search(r"gateway\s+(\S+)", text)
    if gw: dev.gateway = gw.group(1)
    if re.search(r"ospf\s+enabled", text): dev.ospf_enabled = True
    return dev

def load_directory(conf_dir: str) -> Dict[str, Device]:
    p = pathlib.Path(conf_dir)
    devices: Dict[str, Device] = {}
    for file in p.glob("*.dump"):
        d = parse_config_file(file)
        devices[d.hostname] = d
    return devices
