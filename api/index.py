from http.server import BaseHTTPRequestHandler
import json
import smtplib
from email.mime.text import MIMEText

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        to_email = data.get('to')
        code = data.get('code')

        # Настройки твоей почты Mail.ru
        smtp_server = "smtp.mail.ru"
        smtp_port = 465
        sender_email = "sam_official@inbox.ru"
        # Твой 24-значный пароль для внешних приложений из Mail.ru
        sender_password = "tk7l6KKRnqjmW1f9Oxkp" 

        msg = MIMEText(f"Ваш одноразовый код для входа в SAM Messenger: {code}\nКод действует 5 минут.")
        msg['Subject'] = "Код подтверждения SAM Messenger"
        msg['From'] = f"SAM Messenger <{sender_email}>"
        msg['To'] = to_email

        try:
            # Vercel без проблем пропустит это SMTP-подключение!
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())