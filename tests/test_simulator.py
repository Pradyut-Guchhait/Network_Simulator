from src.config_parser import load_directory
from src.topology_builder import build_topology
from src.simulator import run_simulation
def test_simulation_runs():
    devs = load_directory('tests/sample_configs')
    topo = build_topology(devs)
    logs, affected = run_simulation(devs, topo, link_fail='R1-R2')
    assert any('Link failure' in l for l in logs)
