
providers = [
    {
        "id": "pia",
        "name": "Private Internet Access",
        "image": "thrnz/docker-wireguard-pia"
    }
]

def find(id):
    for provider in providers:
        if provider["id"] == id:
            return provider
        
    return None

def pia(service, config):
    return {
        "environment": {
            "LOC": "monaco",
            "USER": config_username,
            "PASS": config_password,
            "ROUTE": "192.168.1.0/24",
            "LOCAL_NETWORK": "192.168.1.0/24",
            "KEEPALIVE": "25",
            "PORT_FORWARDING": "1",
            "PORT_PERSIST": "1",
            "PORT_FILE_CLEANUP": "0",
        },
    }