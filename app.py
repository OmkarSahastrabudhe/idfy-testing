from http.server import BaseHTTPRequestHandler, HTTPServer
import json

NAME = "Omkar"
ROLE = "DevOps Engineer"
COMPANY = "IDfy"

# ---------------------------------------------------------------------------
# Routes: path -> what the page shows.
# To add a new path, just add another entry here.
# ---------------------------------------------------------------------------
ROUTES = {
    "/": {
        "title": "Hello World",
        "subtitle": f"My name is <span class='name'>{NAME}</span>",
        "badge": f"I am a {ROLE} at {COMPANY}",
        "gradient": "#667eea, #764ba2, #f64f59",
    },
    "/omkar/v1": {
        "title": "Welcome to v1",
        "subtitle": f"This is <span class='name'>{NAME}</span>'s first version",
        "badge": "Deployed with Python, no frameworks needed",
        "gradient": "#11998e, #0f9b8e, #38ef7d",
    },
    "/omkar/v2": {
        "title": "Welcome to v2",
        "subtitle": f"<span class='name'>{NAME}</span> shipped an upgrade",
        "badge": "Automate everything: CI/CD, Docker, Kubernetes",
        "gradient": "#fc4a1a, #f7b733, #ee0979",
    },
}


def render_page(route_path, page):
    # Navigation links to every route, with the current one highlighted
    nav = "".join(
        f"<a href='{p}' class='{'active' if p == route_path else ''}'>{p}</a>"
        for p in ROUTES
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page['title']} | {NAME}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 24px;
      font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: linear-gradient(135deg, {page['gradient']});
      background-size: 200% 200%;
      animation: shift 10s ease infinite;
      padding: 16px;
    }}

    @keyframes shift {{
      0%   {{ background-position: 0% 50%; }}
      50%  {{ background-position: 100% 50%; }}
      100% {{ background-position: 0% 50%; }}
    }}

    .card {{
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-radius: 20px;
      padding: 48px 40px;
      max-width: 560px;
      width: 100%;
      text-align: center;
      color: #fff;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
    }}

    h1 {{ font-size: 3rem; margin-bottom: 12px; }}
    h2 {{ font-size: 1.6rem; font-weight: 400; margin-bottom: 20px; }}

    .name {{
      font-weight: 700;
      color: #fff;
      padding: 0 6px;
      border-radius: 6px;
      background: rgba(0, 0, 0, 0.25);
    }}

    .badge {{
      display: inline-block;
      padding: 10px 22px;
      border-radius: 999px;
      background: rgba(0, 0, 0, 0.25);
      font-weight: 600;
      font-size: 1.05rem;
    }}

    nav {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }}

    nav a {{
      color: #fff;
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.5);
      font-family: monospace;
      font-size: 0.95rem;
    }}

    nav a:hover, nav a.active {{
      background: #fff;
      color: #333;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>{page['title']}</h1>
    <h2>{page['subtitle']}</h2>
    <div class="badge">{page['badge']}</div>
  </div>
  <nav>{nav}</nav>
</body>
</html>
"""


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Ignore query strings and trailing slashes: /omkar/v1/ == /omkar/v1
        path = self.path.split("?")[0].rstrip("/") or "/"

        if path in ROUTES:
            body = render_page(path, ROUTES[path]).encode()
            content_type = "text/html; charset=utf-8"
            status = 200
        elif path == "/api/hello":
            body = json.dumps({
                "message": f"Hello, my name is {NAME}. I am a {ROLE} at {COMPANY}.",
                "routes": list(ROUTES),
            }).encode()
            content_type = "application/json"
            status = 200
        else:
            body = render_page(path, {
                "title": "404",
                "subtitle": "Page not found",
                "badge": f"No route for {path}",
                "gradient": "#232526, #414345, #232526",
            }).encode()
            content_type = "text/html; charset=utf-8"
            status = 404

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), HelloHandler)
    print("Server running at http://localhost:8000")
    for p in ROUTES:
        print(f"  http://localhost:8000{p}")
    print("  http://localhost:8000/api/hello")
    server.serve_forever()
