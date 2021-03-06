import subprocess
# import sys
import os
# import time
# import pexpect
import shlex
import click
import socket
from pathlib import PosixPath

container_bin = 'podman'
lvmt_root = os.environ["PWD"]
lvmt_image_source_local = "localhost"
lvmt_image_source_remote = "ghcr.io/sdss"
lvmt_image_name = 'lvmscraper'
lvmt_rmq = socket.gethostname()

@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--use-cache/--no-cache", default=True)
def build(lvmt_root:str, use_cache: bool):
    cam_dockerfile = f"{lvmt_root}/container"
    lvmt_image_fullbuild = "" if use_cache else " --no-cache"
    build = f"{container_bin} build --tag {lvmt_image_name} {lvmt_image_fullbuild} --rm {cam_dockerfile} --format docker"
    print(build)
    command = subprocess.run(shlex.split(build))


@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--name", "-n", default="lvmscraper", type=str)
@click.option("--debug/--no-debug", "-d", default=False)
@click.option("--kill/--no-kill", default=False)
@click.option("--rmq", default=lvmt_rmq, type=str)
def start(lvmt_root:str, name: str, debug:bool, kill:bool, rmq:str):
    if not subprocess.run(shlex.split(f"podman image exists {lvmt_image_source_local}/{lvmt_image_name}")).returncode:
       lvmt_image = f"{lvmt_image_source_local}/{lvmt_image_name}"
    else:
       if subprocess.run(shlex.split(f"podman image exists {lvmt_image_source_remote}/{lvmt_image_name}")).returncode:
           subprocess.run(shlex.split(f"podman pull {lvmt_image_source_remote}/{lvmt_image_name}:latest"))
       lvmt_image = f"{lvmt_image_source_remote}/{lvmt_image_name}"


    if kill:
        subprocess.run(shlex.split(f"podman kill {name}"))
        subprocess.run(shlex.split(f"podman rm {name} -f"))

    run_base = f"--rm -t --name={name}"
    
    run_base += f" -e LVMT_RMQ={rmq}"

    if debug:
        run_base +=  f" -e LVMT_DEBUG=true"

    run_scraper = f"-v {lvmt_root}:/root/lvmscraper:rw -p 8085:8085"
    run = f"{container_bin} run {run_base} {run_scraper} {lvmt_image}"
    print(run)
    #child = pexpect.spawn(run)
    #child.expect('BSC loaded')
    #assert isRunning(name) == True
    command = subprocess.run(shlex.split(f"{run}"))
    logs = subprocess.run(shlex.split(f"podman logs -f {name}"))
    
    print("done")

@click.command()   
@click.option("--name", "-n", default="lvmscraper", type=str)
def stop(name: str):
    command = subprocess.run(shlex.split(f"{container_bin} kill {name}"))

