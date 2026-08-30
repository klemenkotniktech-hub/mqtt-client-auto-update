import requests
from version import VERSION
from packaging.version import Version

REPO = "klemenkotniktech-hub/mqtt-client-auto-update"






def check_for_update():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"

    response = requests.get(url)
    response.raise_for_status()

    latest_version = response.json()["tag_name"].lstrip("v")

    print(f"Current version: {VERSION}")
    print(f"Latest version: {latest_version}")

    if Version(latest_version) > Version(VERSION):
        print("Update available: True")
        return latest_version
    else:
        print("Update available: False")
        return None

if __name__ == "__main__":
    check_for_update()