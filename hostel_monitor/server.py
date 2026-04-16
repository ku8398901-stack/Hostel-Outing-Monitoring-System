import http.server
import socketserver
import subprocess
import urllib.parse
import json

PORT = 8086

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DSA Web Panel</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #121212; --panel: rgba(20,20,30,0.8);
            --primary: #FF3366; --secondary: #00F0FF;
        }
        body {
            background-color: var(--bg); color: #fff; font-family: 'Outfit', sans-serif;
            padding: 2rem; display: flex; flex-direction: column; align-items: center;
        }
        h1 { background: linear-gradient(90deg, var(--primary), var(--secondary));
             -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .glass { background: var(--panel); border-radius: 12px; padding: 20px; border: 1px solid #333; margin-bottom: 20px; width: 100%; max-width: 600px;}
        input { width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 6px; background: #000; border: 1px solid #555; color: white; box-sizing: border-box; }
        .btnRow { display: flex; gap: 10px; flex-wrap: wrap;}
        button { flex: 1; padding: 10px; cursor: pointer; font-weight: bold; font-family: 'Outfit'; color: white; border-radius: 6px; border: none; }
        
        .c-out { background: var(--primary); }
        .c-in { background: var(--secondary); color: black;}
        .c-norm { background: #333; border: 1px solid #777;}
        
        #console { background: #000; color: #0f0; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; height: 180px; overflow-y: auto;}
    </style>
</head>
<body>
    <h1>Hostel Admin Dashboard</h1>
    
    <div class="glass">
        <label>Student Register Number</label>
        <input type="text" id="regNo" value="25XYZ9861">
        <label>Time (DD/MM/YYYY HH:MM AM/PM)</label>
        <input type="text" id="timeVal" value="10/04/2026 10:30 AM" placeholder="DD/MM/YYYY HH:MM AM">
        
        <div class="btnRow">
            <button class="c-out" onclick="fire('checkout')">Check Out</button>
            <button class="c-in" onclick="fire('checkin')">Check In</button>
        </div>
    </div>
    
    <div class="glass btnRow">
        <button class="c-norm" onclick="fire('top')">Show Top Violators</button>
        <button class="c-norm" onclick="fire('search')">Search Report</button>
        <button class="c-norm" onclick="fire('nextday')">Fast-Forward Timeline</button>
    </div>
    
    <div class="glass" style="max-width: 800px; width: 100%">
        <div id="console">Loading Database Modules...</div>
    </div>

    <script>
        function fire(cmd) {
            const reg = document.getElementById('regNo').value;
            const t = document.getElementById('timeVal').value;
            
            fetch('/api', {
                method: 'POST', body: JSON.stringify({action: cmd, reg: reg, time: t})
            })
            .then(r => r.text())
            .then(data => {
                const con = document.getElementById('console');
                con.innerHTML = "> Executing " + cmd + "...\\n" + data;
            });
        }
    </script>
</body>
</html>
"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        
    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length).decode('utf-8')
        try:
            req = json.loads(body)
            action = req.get('action')
            reg = req.get('reg', 'NULL')
            t = req.get('time', '0')
            
            # Construct standard bash argument array natively linked to compiled cpp codebase
            args = ["./main", action]
            if action in ["checkout", "checkin"]: args.extend([reg, t])
            elif action == "search": args.append(reg)
            
            # Subprocess execution cleanly links the Python to the C++ logic output directly!
            output = subprocess.check_output(args, stderr=subprocess.STDOUT, text=True)
            out_str = output
            
        except Exception as e:
            out_str = f"Execution Error: {str(e)}"

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(out_str.encode('utf-8'))

print(f"Native Python Web Server successfully booted!")
print(f"Listening on http://localhost:{PORT}")
print(f"- Bound accurately to the C++ Backend Processing File.")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
