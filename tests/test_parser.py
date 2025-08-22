from src.config_parser import load_directory
def test_loads():
    devs = load_directory('tests/sample_configs')
    assert 'R1' in devs and 'R2' in devs
    assert any(i.vlan==10 for i in devs['R1'].interfaces)
