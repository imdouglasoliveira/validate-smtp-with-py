import smtplib
import ssl
import logging
import os
import datetime
import time
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def carregar_env():
    variaveis = {}
    try:
        with open(".env", "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha or linha.startswith("#"):
                    continue
                chave, valor = linha.split("=", 1)
                variaveis[chave.strip()] = valor.strip().strip('"').strip("'")
        return variaveis
    except Exception as e:
        print(f"Erro ao carregar arquivo .env: {e}")
        return {}

def configurar_logger(nivel=logging.INFO, salvar_arquivo=True):

    formato = "%(asctime)s [%(levelname)s]: %(message)s"
    data_formato = "%Y-%m-%d %H:%M:%S"
    
    logger = logging.getLogger()
    logger.setLevel(nivel)
    
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(formato, data_formato))
    logger.addHandler(console_handler)
    
    if salvar_arquivo:

        os.makedirs("logs", exist_ok=True)
        nome_arquivo = f"logs/smtp_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(nome_arquivo, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(formato, data_formato))
        logger.addHandler(file_handler)
        logging.info(f"Logs sendo salvos no arquivo: {nome_arquivo}")
        time.sleep(5)  # Delay
    
    return logger

# Função de log
def log_com_delay(logger, nivel, mensagem):
    if nivel == "info":
        logger.info(mensagem)
    elif nivel == "warning":
        logger.warning(mensagem)
    elif nivel == "error":
        logger.error(mensagem)
    elif nivel == "debug":
        logger.debug(mensagem)
    time.sleep(5)  # Delay

def validar_smtp():
    
    env_vars = carregar_env()
    
    SMTP_HOST = env_vars.get("SMTP_HOST", "")
    SMTP_PORT = int(env_vars.get("SMTP_PORT", 0))
    SMTP_USERNAME = env_vars.get("SMTP_USERNAME", "")
    SMTP_PASSWORD = env_vars.get("SMTP_PASSWORD", "")
    
    DESTINATARIO = "gestaodoed@gmail.com"
    ASSUNTO = "Teste de Conexão SMTP"
    CORPO = "Esta é uma mensagem de teste para verificar a conexão SMTP via Python."
    
    logger = configurar_logger(nivel=logging.INFO, salvar_arquivo=True)
    
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD]):
        log_com_delay(logger, "error", "Configurações SMTP incompletas no arquivo .env")
        return False
    
    log_com_delay(logger, "info", "Iniciando validação de conexão SMTP")
    log_com_delay(logger, "info", f"Servidor: {SMTP_HOST}")
    log_com_delay(logger, "info", f"Porta: {SMTP_PORT}")
    log_com_delay(logger, "info", f"Usuário: {SMTP_USERNAME}")
    log_com_delay(logger, "info", f"Destinatário de teste: {DESTINATARIO}")
    
    try:
        log_com_delay(logger, "info", "Preparando mensagem de teste...")
        mensagem = MIMEText(CORPO, "plain", "utf-8")
        mensagem["Subject"] = Header(ASSUNTO, "utf-8")
        mensagem["From"] = formataddr((str(Header("Remetente", "utf-8")), SMTP_USERNAME))
        mensagem["To"] = DESTINATARIO
        log_com_delay(logger, "info", "Mensagem preparada com sucesso")
    except Exception as e:
        log_com_delay(logger, "error", f"Erro ao preparar mensagem: {e}")
        return False
    
    try:
        log_com_delay(logger, "info", f"Tentando conexão com {SMTP_HOST}:{SMTP_PORT} (SSL)...")
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=10) as server:
            log_com_delay(logger, "info", "✓ Conexão SSL estabelecida com sucesso")
            
            log_com_delay(logger, "info", "Tentando autenticação...")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            log_com_delay(logger, "info", "✓ Autenticação bem-sucedida")
            
            log_com_delay(logger, "info", "Enviando e-mail de teste...")
            server.sendmail(SMTP_USERNAME, [DESTINATARIO], mensagem.as_string())
            log_com_delay(logger, "info", "✓ E-mail de teste enviado com sucesso")
            
        log_com_delay(logger, "info", "Teste de validação SMTP concluído com SUCESSO")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        log_com_delay(logger, "error", f"✗ Erro de autenticação: {e}")
        log_com_delay(logger, "error", "Verifique seu nome de usuário e senha")
        return False
    except smtplib.SMTPConnectError as e:
        log_com_delay(logger, "error", f"✗ Erro de conexão: {e}")
        log_com_delay(logger, "error", "Verifique se o servidor está acessível e se a porta está correta")
        return False
    except smtplib.SMTPServerDisconnected as e:
        log_com_delay(logger, "error", f"✗ Servidor desconectado: {e}")
        log_com_delay(logger, "error", "A conexão com o servidor foi perdida")
        return False
    except ssl.SSLError as e:
        log_com_delay(logger, "error", f"✗ Erro SSL: {e}")
        log_com_delay(logger, "error", "Problema com a conexão segura")
        return False
    except Exception as e:
        log_com_delay(logger, "error", f"✗ Erro não esperado: {e}")
        return False
    finally:
        log_com_delay(logger, "info", "Finalizando teste de conexão SMTP")

if __name__ == "__main__":
    validar_smtp()