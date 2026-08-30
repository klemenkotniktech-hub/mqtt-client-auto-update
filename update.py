import requests
from version import VERSION
from packaging.version import Version
from pathlib import Path
import hashlib
import zipfile
import subprocess
import os
import shutil

REPO = "klemenkotniktech-hub/mqtt-client-auto-update"
PROJECT_DIR = Path(__file__).resolve().parent
UPDATE_DIR = PROJECT_DIR / "updates"
UPDATE_TEMP_DIR = PROJECT_DIR / "update_temp"

def get_current_pid():
    return os.getpid()

def clean_directory(directory):
    directory = Path(directory)

    if directory.exists():
        shutil.rmtree(directory)

    directory.mkdir(parents=True)

def download_file(url, destination):
    response = requests.get(url)
    response.raise_for_status()

    with open(destination, "wb") as file:
        file.write(response.content)


def calculate_sha256(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def read_expected_sha256(filepath):
    with open(filepath, "r") as file:
        content = file.read().strip()

    return content.split()[0] # potrebujemo samo izračun, ne pa mqtt_client_vX.Y.Z.zip


def verify_checksum(zip_path, checksum_path):
    calculated = calculate_sha256(zip_path)
    expected = read_expected_sha256(checksum_path)

    print(f"Expected SHA-256: {expected}")
    print(f"Calculated SHA-256: {calculated}")

    if calculated.lower() == expected.lower():
        print("Checksum verification succesful")
        return True

    print("Checksum verification FAILED")
    return False


def extract_update(zip_path, destination):
    clean_directory(destination)

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(destination)

    print(f"Update extracted to: {destination}")


def check_for_update():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"

    response = requests.get(url)
    response.raise_for_status()

    release = response.json()

    latest_version = release["tag_name"].lstrip("v")

    print(f"Current version: {VERSION}")
    print(f"Latest version: {latest_version}")

    if Version(latest_version) > Version(VERSION):
        print("Update available: True")

        zip_path = None
        checksum_path = None

        clean_directory(UPDATE_DIR)

        for asset in release["assets"]:
            #print(asset["name"])
            #print(asset["browser_download_url"])

            if asset["name"].endswith(".zip"):
                filename = asset["name"]
                zip_path = UPDATE_DIR / filename

                download_file(
                    asset["browser_download_url"],
                    UPDATE_DIR / filename
                )
                #print(f"Downloaded: {filename}")

            elif asset["name"].endswith(".sha256"):
                filename = asset["name"]
                checksum_path = UPDATE_DIR / filename

                download_file(
                    asset["browser_download_url"],
                    UPDATE_DIR / filename
                )
                #print(f"Downloaded: {filename}")


        if zip_path and checksum_path:
            if verify_checksum(zip_path, checksum_path):
                print("Update package is valid")
                extract_update(zip_path, UPDATE_TEMP_DIR)
                start_updater()
            else:
                print("Update package is invalid")

        return latest_version
    else:
        print("Update available: False")
        return None


def start_updater():
    subprocess.Popen(
        [
            "uv",
            "run",
            str(PROJECT_DIR / "updater.py"),
            str(UPDATE_TEMP_DIR),
            str(PROJECT_DIR),
            str(os.getpid())
        ])
    print("Updater started.")



if __name__ == "__main__":
    check_for_update()