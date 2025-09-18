import json, time, urllib.request, webbrowser, sys

def ping(url, timeout=2.0):
    t0 = time.time()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            resp.read(8)
        return (time.time() - t0) * 1000.0
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        print("Uso: python pick_node_and_open.py NOME_DO_ARQUIVO (ex.: demo.mp4)")
        return
    filename = sys.argv[1]
    cfg = json.load(open("nodes.json", "r", encoding="utf-8"))

    # FORÇAR IPv4 no Windows (127.0.0.1)
    nodes = []
    for n in cfg["nodes"]:
        nodes.append({**n, "host": "127.0.0.1"})

    scores = []
    for n in nodes:
        url = f"http://{n['host']}:{n['port']}/health"
        ms = ping(url)
        print(f"Ping {n['name']} ({url}): {'OFF' if ms is None else f'{ms:.0f} ms'}")
        scores.append((ms, n))

    up = [s for s in scores if s[0] is not None]
    if not up:
        print("Nenhum nó está respondendo. Inicie pelo menos um start_node.py.")
        return

    best_ms, best = sorted(up, key=lambda x: x[0])[0]
    file_url = f"http://{best['host']}:{best['port']}/{filename}"
    print(f"=> Nó mais rápido: {best['name']} ({best_ms:.0f} ms). Abrindo {file_url} ...")
    webbrowser.open(file_url)

if __name__ == "__main__":
    main()
