import argparse, json, pathlib
from .config_parser import load_directory
from .topology_builder import build_topology
from .validator import find_duplicate_ips, find_mtu_mismatches, detect_loops, find_missing_components
from .optimizer import recommend_load_balancing, suggest_protocols, node_aggregation
from .simulator import run_simulation

def run(conf_dir: str, outputs_dir: str, link_fail: str = None):
    devices = load_directory(conf_dir)
    topo = build_topology(devices)
    # Validations
    issues = []
    issues += find_duplicate_ips(devices)
    issues += find_mtu_mismatches(topo)
    issues += detect_loops(topo)
    issues += find_missing_components(devices)
    # Optimization
    recs = []
    recs += recommend_load_balancing(devices, topo)
    recs += suggest_protocols(devices)
    recs += node_aggregation(topo)
    # Simulation
    logs, affected = run_simulation(devices, topo, link_fail=link_fail)
    # Write outputs
    out_dir = pathlib.Path(outputs_dir); out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir/"logs.txt").write_text("\n".join(logs))
    sim_report = ["Simulation Report", "="*18, "", f"Link Failure: {link_fail or 'None'}", f"Affected nodes: {affected}", "", "Validations:"] + issues + ["", "Recommendations:"] + recs
    (out_dir/"simulation_report.txt").write_text("\n".join(sim_report))
    # Simple topology image (matplotlib)
    try:
        import matplotlib.pyplot as plt
        pos = {}
        routers = [n for n,d in devices.items() if d.role=='router']
        switches = [n for n,d in devices.items() if d.role=='switch']
        for i,n in enumerate(routers):
            pos[n] = (i*2, 2)
        for i,n in enumerate(switches):
            pos[n] = (i*2+1, 0)
        fig = plt.figure()
        for l in topo.links:
            x1,y1 = pos[l.a]; x2,y2 = pos[l.b]
            plt.plot([x1,x2],[y1,y2])
            mx,my = (x1+x2)/2, (y1+y2)/2
            plt.text(mx,my+0.1,f"VLAN {l.vlan}\n{l.bw_mbps}Mbps", ha='center')
        for n,(x,y) in pos.items():
            plt.scatter([x],[y])
            plt.text(x,y-0.1,n, ha='center')
        plt.axis('off')
        fig.savefig(out_dir/"topology.png", bbox_inches='tight')
        plt.close(fig)
    except Exception as e:
        (out_dir/"topology.png").write_text(f"Unable to draw topology: {e}")
    # Summary
    summary = {
        "devices": list(devices.keys()),
        "issues": issues,
        "recommendations": recs,
        "affected": affected,
    }
    return summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--conf', default='tests/sample_configs', help='Directory with *.dump config files')
    ap.add_argument('--out', default='outputs', help='Outputs directory')
    ap.add_argument('--link-fail', default=None, help='Inject a link failure as A-B')
    args = ap.parse_args()
    summary = run(args.conf, args.out, link_fail=args.link_fail)
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
