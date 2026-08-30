from pathlib import Path
import shutil
import sys
import time
import psutil
import subprocess

def restart_application():
    subprocess.Popen([
        "uv",
        "run",
        "publisher.py"
    ],
    cwd=target_dir
    )

    print("Application restarted")


def install_update(source_dir, target_dir):
    print("Updater is running")
    source_dir = Path(source_dir)
    target_dir = Path(target_dir)

    for item in source_dir.iterdir():
        destination = target_dir / item.name

        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(item, destination)

    # Mark successful update
    (target_dir / "update_completed").touch()
    
    print(f"Update installed successfully.")


def wait_for_process(process_pid):
    print(f"Waiting for process {process_pid} to finish...")

    while psutil.pid_exists(process_pid):
        time.sleep(0.5)

    print("Process finished")


if __name__ == "__main__":
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    process_pid = int(sys.argv[3])

    print(f"Waiting for process: {process_pid}")
    wait_for_process(process_pid)

    print(f"Installing update from: {source_dir}")
    print(f"Installing update to:   {target_dir}")

    install_update(source_dir, target_dir)

    restart_application()