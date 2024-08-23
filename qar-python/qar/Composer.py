
import subprocess

class Composer:
    def __init__(self, metadata_path: str):
        self.services = {}
        self.metadata_path = metadata_path

    def _cmd(self, args):
        result = subprocess.run(
            ["docker", "compose", "ps", "--format", '{{.ID}} {{.Names}}'],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )

        return result.stdout.strip()
    
    def _compose_cmd(self, args):
        return self._cmd(["docker", "compose", "-f", self.metadata_path] + args)

    def get_running_containers(self):
        result = self._compose_cmd(["ps", "--format", '{{.ID}} {{.Names}}'])
        containers = []

        for line in result.split("\n"):
            container_id, name = line.split(' ')
            
            containers.append({
                "id": container_id,
                "name": name
            })

        return containers
    
    def start(self, name):
        self._compose_cmd(["start", name])
    
    def stop(self, name):
        self._compose_cmd(["stop", name])

    def rm(self, name):
        self.stop(name)
        self._compose_cmd(["rm", name])
    
    def is_service_running(self, name):
        containers = self.get_running_containers()
        return name in containers

    def has_service(self, name):
        return name in self.services
    
    def add_service(self, service):
        self.services[service["name"]] = service
    
    def remove_service(self, name):
        if name in self.services:
            del self.services[name]
    
    def generate_config(self):
        return {
            "services": self.services,
            "volumes": self.volumes,
            "networks": self.networks
        }