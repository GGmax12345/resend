from http.server import BaseHTTPRequestHandler
import json
import resend

resend.api_key = "re_3w3iU343_3gH2hvQxETgK6niFWUBPxRaf"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        to_email = data.get('to')
        code = data.get('code')

        try:
            r = resend.Emails.send({
                "from": "SAM Messenger <onboarding@resend.dev>",
                "to": to_email,
                "subject": "Код подтверждения SAM Messenger",
                "html": f"<p>Ваш одноразовый код: <strong>{code}</strong></p>"
            })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())