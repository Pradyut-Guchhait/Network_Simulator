from src.config_parser import load_directory
from src.topology_builder import build_topology
from src.validator import find_mtu_mismatches
def test_mtu_mismatch_detected():
    devs = load_directory('tests/sample_configs')
    topo = build_topology(devs)
    issues = find_mtu_mismatches(topo)
    assert any('MTU mismatch' in m for m in issues)
