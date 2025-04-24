import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

SMTP_HOST = "smtp.zoho.com"      
SMTP_PORT = 465                  
SMTP_USERNAME = "gestao@doed.com.br"
SMTP_PASSWORD = "WS0gURbaJBEy"

DESTINATARIO = "gestaodoed@gmail.com"
ASSUNTO = "Teste de Conexão SMTP"
CORPO = "Esta é uma mensagem de teste para verificar a conexão SMTP via Python."

# Cria o objeto MIMEText com codificação UTF-8
mensagem = MIMEText(CORPO, "plain", "utf-8")
mensagem["Subject"] = Header(ASSUNTO, "utf-8")
mensagem["From"] = formataddr((str(Header("Remetente", "utf-8")), SMTP_USERNAME))
mensagem["To"] = DESTINATARIO

try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=10) as server:
        print(f"Conectado ao {SMTP_HOST} na porta {SMTP_PORT} com SSL implícito")
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("Autenticação bem-sucedida!")
        # Envia o email usando a mensagem MIME corretamente formatada
        server.sendmail(SMTP_USERNAME, [DESTINATARIO], mensagem.as_string())
        print("Email de teste enviado com sucesso!")
except Exception as e:
    print("Ocorreu um erro ao testar a conexão SMTP:", e)
