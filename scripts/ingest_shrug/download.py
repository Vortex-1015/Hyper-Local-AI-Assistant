"""Download verified SHRUG v2.2 source artifacts.

This intentionally does not guess hidden DDL download URLs. Pass a verified
file URL obtained from the official SHRUG v2.2 download portal.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from urllib.request import Request, urlopen

USER_AGENT = "ARTHA-SETU-SHRUG-ingestor/0.1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=120) as response, destination.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    return sha256_file(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Acquire a verified SHRUG v2.2 artifact")
    parser.add_argument("--url", required=True, help="Verified direct download URL")
    parser.add_argument("--name", required=True, help="Local filename")
    parser.add_argument("--sha256", help="Expected SHA-256 checksum")
    parser.add_argument("--output", default="data/raw/shrug/v2.2", help="Raw data directory")
    args = parser.parse_args()

    destination = Path(args.output) / args.name
    checksum = download(args.url, destination)
    print(f"downloaded={destination}")
    print(f"sha256={checksum}")

    if args.sha256 and checksum.lower() != args.sha256.lower():
        destination.unlink(missing_ok=True)
        raise SystemExit("SHA-256 mismatch; downloaded file was removed")


if __name__ == "__main__":
    main()
