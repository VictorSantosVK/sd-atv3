
import argparse, http.server, socketserver, time, threading, os
from functools import partial

class LatencyHandler(http.server.SimpleHTTPRequestHandler):
    latency_ms = 0
    server_version = "MiniNode/1.0"

    def do_GET(self):
        # endpoint de health sem tocar no disco
        if self.path == "/health":
            time.sleep(self.latency_ms / 1000.0)
            body = b'{"status":"ok"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # atraso artificial para todos os GETs
        start = time.time()
        time.sleep(self.latency_ms / 1000.0)
        super().do_GET()
        elapsed = int((time.time() - start) * 1000)
        print(f"[{self.log_date_time_string()}] GET {self.path} (latência simulada: {self.latency_ms} ms, total ~{elapsed} ms)")

    def log_message(self, format, *args):
        # logs mais enxutos
        pass

def run_server(name: str, port: int, root: str, latency_ms: int):
    import os
    from functools import partial
    os.chdir(root)

    # 1) Informar o 'directory' via partial (ok)
    handler = partial(LatencyHandler, directory=root)

    # 2) ***FUNDAMENTAL***: setar a latência na CLASSE, não no partial
    LatencyHandler.latency_ms = latency_ms

    with socketserver.ThreadingTCPServer(("", port), handler) as httpd:
        print(f"==> {name} rodando em http://localhost:{port} | pasta={root} | latência={latency_ms} ms")
        print("    Endpoints: / (arquivos), /health")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\nEncerrando {name} ...")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="node")
    ap.add_argument("--port", type=int, default=8001)
    ap.add_argument("--root", default="storage")
    ap.add_argument("--latency-ms", type=int, default=100)
    args = ap.parse_args()
    if not os.path.isdir(args.root):
        os.makedirs(args.root, exist_ok=True)
    run_server(args.name, args.port, args.root, args.latency_ms)
