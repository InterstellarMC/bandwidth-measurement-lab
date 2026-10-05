import socket
import sys

HOST = "31.97.60.60"
PORT = 7006

def try_connect(payload: bytes, wait_banner=True):
    s = socket.socket()
    s.settimeout(8)
    print(f"[*] connecting to {HOST}:{PORT} payload={payload!r}", flush=True)
    s.connect((HOST, PORT))
    print("[+] connected", flush=True)
    s.settimeout(5)
    if wait_banner:
        try:
            d = s.recv(4096)
            print(f"[banner] {d!r}", flush=True)
        except Exception as e:
            print(f"[no banner] {e}", flush=True)
    if payload:
        s.sendall(payload)
        print(f"[sent] {payload!r}", flush=True)
        try:
            while True:
                d = s.recv(4096)
                print(f"[recv] {d!r}", flush=True)
                if not d:
                    print("[closed by remote]", flush=True)
                    break
        except socket.timeout:
            print("[recv timeout - no more data]", flush=True)
        except Exception as e:
            print(f"[recv err] {e}", flush=True)
    s.close()

if __name__ == "__main__":
    # Test 1: just banner
    try_connect(b"", wait_banner=True)
    print("="*40, flush=True)
    # Test 2: hello
    try_connect(b"hello\n")
    print("="*40, flush=True)
    # Test 3: help
    try_connect(b"HELP\n")
