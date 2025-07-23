import subprocess
import time
import os
import socket
import pytest
import threading

def stream_output(stream, label):
    for line in iter(stream.readline, ''):
        print(f"[{label}] {line}", end='')

def wait_for_port(host, port, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.2)
    return False

@pytest.fixture(scope="session", autouse=True)
def flask_server():
    """Start the Flask server before tests and tear it down after."""
    proc = subprocess.Popen(
        ["python", "-m", "server.main"],
        env={**os.environ, "FLASK_ENV": "development"},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    threading.Thread(target=stream_output, args=(proc.stdout, "stdout"), daemon=True).start()
    threading.Thread(target=stream_output, args=(proc.stderr, "stderr"), daemon=True).start()

    if not wait_for_port("127.0.0.1", 5000, timeout=10):
        stderr = proc.stderr.read()
        proc.terminate()
        raise RuntimeError(f"Flask server failed to start:\n{stderr}")

    print("[pytest] Flask server started on http://127.0.0.1:5000")

    yield  # tests run here

    proc.terminate()
    proc.wait()