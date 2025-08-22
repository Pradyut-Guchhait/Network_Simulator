import threading, time, json
from typing import Dict, List
from .ipc import InMemoryIPC

class DeviceThread(threading.Thread):
    def __init__(self, device, neighbors: Dict[str, str], ipc: InMemoryIPC, log_lines: List[str]):
        super().__init__(daemon=True)
        self.device = device
        self.neighbors = neighbors  # neighbor hostname -> queue name
        self.ipc = ipc
        self.running = True
        self.log_lines = log_lines

    def run(self):
        # Day-1 discovery: announce presence
        for nb, qname in self.neighbors.items():
            self.ipc.send(qname, {"type":"hello", "from": self.device.hostname})
        start = time.time()
        while self.running and time.time() - start < 2.5:  # short demo run
            msg = self.ipc.recv(self.device.hostname, timeout=0.2)
            if msg:
                self.log_lines.append(f"{self.device.hostname} received {msg}")
        # ARP/OSPF discovery (simplified as log entries)
        if self.device.ospf_enabled:
            self.log_lines.append(f"{self.device.hostname} ran OSPF neighbor discovery")
        self.log_lines.append(f"{self.device.hostname} ARP cache primed (simulated)")

def run_simulation(devices, topo, link_fail: str = None):
    ipc = InMemoryIPC()
    logs: List[str] = []
    # map each device to a 'queue name' = hostname
    threads = []
    for dev in devices.values():
        neighbors = {}
        for l in topo.links:
            if l.a == dev.hostname and (link_fail != f"{l.a}-{l.b}"):
                neighbors[l.b] = l.b
            if l.b == dev.hostname and (link_fail != f"{l.a}-{l.b}"):
                neighbors[l.a] = l.a
        t = DeviceThread(dev, neighbors, ipc, logs)
        threads.append(t)
    for t in threads: t.start()
    for t in threads: t.join()
    # Impact analysis for link failure
    affected = []
    if link_fail:
        a,b = link_fail.split('-')
        affected = [a,b]
        logs.append(f"Link failure injected on {link_fail}. Endpoints behind {a} and {b} may be impacted.")
    return logs, affected
