
import docker
import json
import logging

import psutil

from .Composer import Composer
from . import vpns

class Qar:
    def __init__(self, config_path: str):
        self.docker_client = docker.from_env()
        self.config_path = config_path
        self.composer = Composer("/qar/docker-compose.yml")
        self.config = self._load_config()
        self.vpn_service = self._create_vpn_service()
        self.torrent_service = self._create_torrent_service()
        self.torrent_proxy_service = self._create_torrent_proxy_service()
        self.jellyfin_service = self._create_jellyfin_service()
    
    def _load_config(self):
        with open(self.config_path, "r") as file:
            config = json.load(file)
        
        return config

    def start(self):
        self._update_torrent_config()

        self.composer.start("qarvpn")
        self.composer.start("qbittorrent")
        self.composer.start("qbittorrent-proxy")
        self.composer.start("jellyfin")

    def stop(self):
        self.composer.stop("jellyfin")
        self.composer.stop("qbittorrent-proxy")
        self.composer.stop("qbittorrent")
        self.composer.stop("qarvpn")

    def _create_vpn_service(self):
        config = self.config["vpn"]

        if config is None:
            raise ValueError("No VPN configuration found")
        
        if "provider" not in config:
            raise ValueError("No VPN provider specified")
        elif "username" not in config:
            raise ValueError("No VPN username specified")
        elif "password" not in config:
            raise ValueError("No VPN password specified")

        config_id = config["provider"]
        config_username = config["username"]
        config_password = config["password"]
        provider = vpns.find(config_id)
        
        if provider is None:
            raise ValueError(f"Invalid VPN provider '{config_id}'")
        
        data_dir = f"/qar/data/{config_id}"

        return {
            "image": provider["image"],
            # We give each network connection an alias so we can reference it in other services
            # and resolve it as a hostname in the container
            "networks": {
                "qar_lan": {
                    "aliases": ["vpn-macvlan"]
                },
                "bridge": {
                    "aliases": ["vpn-bridge"]
                }
            },
            "volumes": [
                f"{data_dir}:/pia",
                f"{data_dir}/shared:/pia-shared"
            ],
            "cap_add": ["NET_ADMIN", "SYS_MODULE"],
            "sysctls": {
                "net.ipv4.conf.all.src_valid_mark": "1",
                "net.ipv6.conf.default.disable_ipv6": "1",
                "net.ipv6.conf.all.disable_ipv6": "1",
                "net.ipv6.conf.lo.disable_ipv6": "1",
            },
            "healthcheck": {
                "test": "ping -c 1 www.google.com || exit 1",
                "interval": "30s",
                "timeout": "10s",
                "retries": "3",
            }
        }
    
    def _create_torrent_service(self):
        config_path = "/qar/data/qbittorrent"
        downloads_path = "/qar/storage/downloads"

        return {
            "image": "lscr.io/linuxserver/qbittorrent:latest",
            "network_mode": "service:qarvpn",
            "environment": {
                "PUID": "0",
                "PGID": "0",
                "UMASK": "022",
                "TZ": "Etc/UTC",
                "WEBUI_PORT": "8080"
            },
            "volumes": [
                f"{config_path}:/config",
                f"{downloads_path}:/downloads"
            ],
        }

    def _create_torrent_proxy_service(self):
        config_path = ""

        pod = Pod(self.docker_client)
        pod.image = "nginx:alpine"
        pod.volumes[f"{config_path}/nginx.conf"] = { 'bind': '/etc/nginx/nginx.conf', 'mode': 'rw' }
        
        return pod
    
    def _create_jellyfin_service(self):
        media_path = "/qarb/media"
        config_path = "/qar/data/jellyfin/config"
        cache_path = "/qar/data/jellyfin/cache"

        return {
            "image": "jellyfin/jellyfin:latest",
            "network_mode": "qar_lan",
            "volumes": [
                f"{media_path}:/media",
                f"{config_path}:/config",
                f"{cache_path}:/cache"
            ]
        }

    def _create_lan_network(self):
        device_name = self._get_default_network_device()
        gateway_ip = self._get_gateway_ip(device_name)

        options = {
            "parent": device_name
        }

        ipam_config = docker.types.IPAMConfig(
            pool_configs=[
                docker.types.IPAMPool(
                    subnet="192.168.1.0/24",
                    gateway=gateway_ip,
                    iprange="192.168.1.224/27"
                )
            ]
        )
        # Create the macvlan network
        network = self.docker_client.networks.create(
            name="qarlan",
            driver="macvlan",
            options=options,
            ipam=ipam_config
        )

    def _get_default_network_device(self):
        gateways = psutil.net_if_addrs()
        default_gateway = psutil.net_if_stats()

        for interface, stats in default_gateway.items():
            if stats.isup:
                return interface
                
    def _get_gateway_ip(self, device_name):
        gateways = psutil.net_if_addrs()

        for interface, addresses in gateways.items():
            if interface == device_name:
                for address in addresses:
                    if address.family == 2:
                        return address.address


