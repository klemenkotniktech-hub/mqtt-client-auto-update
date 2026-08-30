from pathlib import Path
import zipfile
import hashlib

VERSION = "1.1.0"

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = PROJECT_DIR / f"mqtt_client_v{VERSION}.zip"

FILES = [
    "database.py",
    "publisher.py",
    "subscriber.py",
    "update.py",
    "version.py",
    "pyproject.toml",
    "uv.lock",
    "README.md",
]

DIRECTORIES = [
    "certs",
]


def calculate_sha256(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def create_release():
    with zipfile.ZipFile(
        OUTPUT_FILE,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        for file in FILES:
            path = PROJECT_DIR / file

            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")

            zip_file.write(
                path,
                arcname=file
            )

        for directory in DIRECTORIES:
            directory_path = PROJECT_DIR / directory

            if not directory_path.exists():
                raise FileNotFoundError(
                    f"Directory not found: {directory_path}"
                )

            for path in directory_path.rglob("*"):
                if path.is_file():
                    arcname = path.relative_to(PROJECT_DIR)

                    zip_file.write(
                        path,
                        arcname=arcname
                    )

    sha256 = calculate_sha256(OUTPUT_FILE)

    checksum_file = OUTPUT_FILE.with_suffix(
        OUTPUT_FILE.suffix + ".sha256"
    )

    with open(checksum_file, "w") as file:
        file.write(f"{sha256}  {OUTPUT_FILE.name}\n")

    print(f"Release created: {OUTPUT_FILE}")
    print(f"SHA-256: {sha256}")
    print(f"Checksum created: {checksum_file}")


if __name__ == "__main__":
    create_release()