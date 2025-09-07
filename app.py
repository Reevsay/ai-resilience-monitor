import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).parent

def ensure_env():
    env = ROOT / ".env"
    example = ROOT / ".env.example"
    if not env.exists() and example.exists():
        env.write_text(example.read_text(), encoding="utf-8")
        print("[setup] Created .env from .env.example")


def run_compose():
    # Prefer docker compose v2 syntax
    cmd = ["docker", "compose", "up", "-d", "--build"]
    print("[docker] ", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(ROOT))
    if proc.returncode != 0:
        print("[error] docker compose up failed. Ensure Docker Desktop is running.")
        sys.exit(proc.returncode)


def wait_for(url: str, timeout: int = 45):
    import urllib.request
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                if 200 <= resp.status < 500:
                    return True
        except Exception:
            time.sleep(1)
    return False


def main():
    ensure_env()
    run_compose()

    url = "http://localhost:3000/"
    if wait_for(url, timeout=45):
        print(f"[open] {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"[warn] Could not open browser automatically: {e}")
    else:
        print("[warn] ai-proxy didn't become ready in time. You can open the dashboard manually at:")
        print(url)

    print("[info] Services:")
    print("- Dashboard: http://localhost:3000/")
    print("- Grafana:   http://localhost:3001/")
    print("- Prometheus:http://localhost:9090/")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
