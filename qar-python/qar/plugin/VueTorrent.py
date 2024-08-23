
import requests
import subprocess
import os
import os.path

class VueTorrent:
    def __init__(self, qar):
        self.qar = qar

    def activate(self):
        self.update_vuetorrent()

        # Update the qBittorrent configuration to use the alternative web UI
        self.qar.set_qbittorrent_config(
            alternative_webui_path='/config/vuetorrent',
            alternative_webui_enabled=True,
        )
    
    def update_vuetorrent(self):
        latest_url, latest_version = self.get_latest_release("VueTorrent", "VueTorrent", "vuetorrent.zip")

        # Find the path to the qBittorrent configuration directory
        config_path = self.qar.get_qbittorrent_config_path()

        # Store the skin within the config directory
        skin_path = f"{config_path}/vuetorrent"
        current_version = None

        if os.path.exists(f"{skin_path}/version.txt"):
            with open(f"{skin_path}/version.txt", "r") as version_file:
                current_version = version_file.read().strip()
        
        if current_version == latest_version:
            print(f"VueTorrent is already up-to-date at version {latest_version}")
            return
        
        # Remove the old backup if it exists
        if os.path.exists(f"{skin_path}-backup"):
            os.remove(f"{skin_path}-backup")

        if os.path.exists(skin_path):
            # Rename existing VueTorrent skin directory
            os.rename(skin_path, f"{skin_path}-backup")

        # Store the release zip file in the /tmp directory
        tmp_path = '/tmp/vuetorrent.zip'

        # Use curl to download the zip file to tmp_path
        subprocess.run(['curl', '-L', latest_url, '-o', tmp_path], check=True)

        # Extract the VueTorrent skin to the qBittorrent configuration directory
        subprocess.run(['unzip', '-o', tmp_path, '-d', skin_path], check=True)

    def deactivate(self):
        pass

    def get_latest_release(self, repo_owner, repo_name, file_name):
        # GitHub API URL for the latest release
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        
        # Send a request to the GitHub API
        response = requests.get(api_url)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the latest release: {response.status_code}")
        
        release_data = response.json()
        
        # Get the version of the release
        release_version = release_data.get('tag_name', 'Unknown version')
        
        # Iterate over the assets in the latest release
        for asset in release_data.get('assets', []):
            if asset['name'] == file_name:
                # Return the download URL of the file and the release version
                return asset['browser_download_url'], release_version
        
        # If the file is not found in the latest release
        raise Exception(f"File '{file_name}' not found in the latest release of {repo_owner}/{repo_name}.")
