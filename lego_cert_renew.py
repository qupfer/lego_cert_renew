#!/usr/bin/env python3

import argparse
import subprocess


def curent_lego_certs() -> list[str]:
    """return all lego certificates as a list of str"""
    result = subprocess.run(
        ["lego", "list", "--names"],
        text=True,
        capture_output=True,
        cwd="/home/henning/",
    )
    cur_cert_list = result.stdout.splitlines()
    print(f"cert list: {cur_cert_list}")
    return cur_cert_list


def gen_domain_command(domain: str) -> list[str]:
    """generate the arguments for lego based on a space sperated list of domains"""
    domain_args = []
    split_domains = domain.split(" ")
    for d in split_domains:
        domain_args += ["--domains", d]
    return domain_args


def new_cert(domain: str, create: bool = False) -> bool:
    """create or renew a certificate"""
    print(f"create cert for {domain}")
    email = "lego@qupfer.de"
    domaincommand = gen_domain_command(domain)
    subcommand = "run" if create else "renew"
    command = [
        "lego",
        "--accept-tos",
        *domaincommand,
        "--email",
        email,
        "--pem",
        "--http",
        "--http.port",
        "127.0.0.1:9999",
        subcommand,
        "--profile",
        "shortlived",
    ] + ([] if create else ["--dynamic", "--no-random-sleep"])

    try:
        print(f"running...{' '.join(command)}")
        result = subprocess.run(
            command,
            capture_output=True,
            cwd="/home/henning/",
            timeout=900,
            check=True,
            text=True,
        )
        print(result.stdout)
        print(result.stderr)
    except subprocess.TimeoutExpired as timeout_result:
        print(f"stdout: {timeout_result.stdout}")
        print(f"stderr: {timeout_result.stderr}")
        return False
    except subprocess.CalledProcessError as returncorde_result:
        print("Command failed...")
        print(f"stdout: {returncorde_result.stdout}")
        print(f"stderr: {returncorde_result.stderr}")
    return True


def main() -> int:
    """the main loop"""
    parser = argparse.ArgumentParser(description="Lego Zertifikate erstellen/erneuern")
    parser.add_argument(
        "domain", nargs="?", help="Domain für neues Zertifikat (create=True)"
    )
    args = parser.parse_args()

    if args.domain:
        new_cert(domain=args.domain, create=True)
    else:
        for cert in curent_lego_certs():
            new_cert(domain=cert)
    return 0


if __name__ == "__main__":
    exit(main())
