import http.server
import os
import bz2

PORT = 8080
SERVE_DIR = r"D:\csServer\server_plugins\Helpers\fastdl\Rainbow_CSDM"

os.chdir(SERVE_DIR)

# Стискаємо кастомний контент в .bz2 при першому запуску
COMPRESS_DIRS = ("models", "sound", "sprites", "maps", "overviews", "ui")

def compress_all():
    count = 0
    for folder in COMPRESS_DIRS:
        folder_path = os.path.join(SERVE_DIR, folder)
        if not os.path.isdir(folder_path):
            continue
        for root, _, files in os.walk(folder_path):
            for fname in files:
                if fname.endswith(".bz2"):
                    continue
                path = os.path.join(root, fname)
                bz2_path = path + ".bz2"
                if not os.path.exists(bz2_path) or os.path.getmtime(path) > os.path.getmtime(bz2_path):
                    with open(path, "rb") as f_in, bz2.open(bz2_path, "wb") as f_out:
                        f_out.write(f_in.read())
                    count += 1
    if count:
        print(f"Compressed {count} files to .bz2")

compress_all()

BLOCKED_PREFIXES = ("/addons/", "/addons")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        for prefix in BLOCKED_PREFIXES:
            if self.path.startswith(prefix):
                self.send_error(403)
                return
        super().do_GET()

    def do_HEAD(self):
        for prefix in BLOCKED_PREFIXES:
            if self.path.startswith(prefix):
                self.send_error(403)
                return
        super().do_HEAD()

    def log_message(self, *_):
        pass  # вимкнути — суттєво прискорює при 100+ файлах

    def end_headers(self):
        self.send_header("Connection", "keep-alive")
        self.send_header("Cache-Control", "public, max-age=86400")
        super().end_headers()

print(f"FastDL server on port {PORT}")
print(f"Serving: {SERVE_DIR}")
print("Press Ctrl+C to stop\n")

with http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()
