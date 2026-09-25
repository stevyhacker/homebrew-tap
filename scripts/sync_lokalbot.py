"""Synchronize the cask with the latest complete, stable public release."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

# GitHub reports release asset URLs with the canonical repository name.
REPOSITORY = "stevyhacker/LokalBot"
SPARKLE = "{http://www.andymatuschak.org/xml-namespaces/sparkle}"
CASK = Path(__file__).resolve().parents[1] / "Casks/lokalbot.rb"


def release_info(release):
    tag = release["tag_name"]
    if release.get("draft") or release.get("prerelease") or not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError("Only stable vMAJOR.MINOR.PATCH releases may update the cask")
    assets = {}
    for name in ("LokalBot.dmg", "appcast.xml"):
        matches = [asset for asset in release["assets"] if asset["name"] == name]
        if len(matches) != 1:
            raise ValueError(f"Release must contain exactly one {name}")
        asset = matches[0]
        expected_url = f"https://github.com/{REPOSITORY}/releases/download/{tag}/{name}"
        if asset["browser_download_url"] != expected_url:
            raise ValueError(f"Unexpected release asset URL for {name}")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", asset.get("digest") or ""):
            raise ValueError(f"Missing SHA-256 release digest for {name}")
        if not isinstance(asset["size"], int) or asset["size"] <= 0:
            raise ValueError(f"Invalid asset size for {name}")
        # Download counters change during our own verification. Only compare
        # immutable identity/content fields when rechecking the release.
        assets[name] = {key: asset.get(key) for key in (
            "id", "name", "browser_download_url", "digest", "size")}
    return tag[1:], assets


def cask_field(text, field):
    matches = re.findall(rf'^  {field} "([^"\n]+)"$', text, flags=re.MULTILINE)
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one cask {field}")
    return matches[0]


def needs_update(text, version, digest):
    current = cask_field(text, "version")
    if not re.fullmatch(r"\d+\.\d+\.\d+", current):
        raise ValueError("Unexpected current cask version")
    if tuple(map(int, current.split("."))) > tuple(map(int, version.split("."))):
        raise ValueError("Refusing to downgrade the cask")
    if current == version:
        if cask_field(text, "sha256") != digest:
            raise ValueError("Same-version asset changed; manual review is required")
        return False
    return True


def verify_assets(directory, version, assets):
    for name, metadata in assets.items():
        path = directory / name
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if f"sha256:{digest}" != metadata["digest"] or path.stat().st_size != metadata["size"]:
            raise ValueError(f"Downloaded {name} does not match release digest/size")
    items = ET.parse(directory / "appcast.xml").findall("./channel/item")
    if len(items) != 1:
        raise ValueError("Expected the single-release LokalBot appcast")
    item = items[0]
    enclosure = item.find("enclosure")
    if item.findtext(f"{SPARKLE}shortVersionString") != version or enclosure is None:
        raise ValueError("Appcast version does not match the release")
    if (enclosure.get("url") != assets["LokalBot.dmg"]["browser_download_url"]
            or enclosure.get("length") != str(assets["LokalBot.dmg"]["size"])
            or not enclosure.get(f"{SPARKLE}edSignature")):
        raise ValueError("Appcast enclosure does not match the DMG")


def updated_cask(text, version, digest):
    # Fixed-format validated values; never execute release text or interpolate
    # it into shell commands. Preserve all unrelated cask fields.
    cask_field(text, "version")
    cask_field(text, "sha256")
    text = re.sub(r'^  version "[^"\n]+"$', f'  version "{version}"', text, flags=re.MULTILINE)
    return re.sub(r'^  sha256 "[^"\n]+"$', f'  sha256 "{digest}"', text, flags=re.MULTILINE)


def main():
    release = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/{REPOSITORY}/releases/latest"], text=True))
    version, assets = release_info(release)
    digest = assets["LokalBot.dmg"]["digest"].removeprefix("sha256:")
    original = CASK.read_text()
    if not needs_update(original, version, digest):
        print(f"LokalBot {version} is already synchronized")
        return
    with tempfile.TemporaryDirectory(prefix="lokalbot-release-") as directory:
        subprocess.run([
            "gh", "release", "download", release["tag_name"], "--repo", REPOSITORY,
            "--pattern", "LokalBot.dmg", "--pattern", "appcast.xml", "--dir", directory,
        ], check=True)
        verify_assets(Path(directory), version, assets)
    # Recheck after download so a newer release cannot be overlooked or an
    # asset replacement silently accepted while verification was running.
    refreshed = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/{REPOSITORY}/releases/latest"], text=True))
    if release_info(refreshed) != (version, assets):
        raise ValueError("Release changed during verification; retry synchronization")
    CASK.write_text(updated_cask(original, version, digest))
    print(f"Updated LokalBot to {version}; downloaded asset digests and appcast match")


if __name__ == "__main__":
    main()
