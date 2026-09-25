import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from sync_lokalbot import release_info, needs_update, updated_cask, verify_assets, REPOSITORY, SPARKLE


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.version = "0.8.3"
        self.url = f"https://github.com/{REPOSITORY}/releases/download/v0.8.3/"
        self.dmg = b"synthetic test archive"
        self.feed = (f'<rss xmlns:sparkle="{SPARKLE[1:-1]}"><channel><item>'
                     '<sparkle:shortVersionString>0.8.3</sparkle:shortVersionString>'
                     f'<enclosure url="{self.url}LokalBot.dmg" length="{len(self.dmg)}" '
                     'sparkle:edSignature="fixture"/></item></channel></rss>').encode()
        self.release = {"tag_name": "v0.8.3", "draft": False, "prerelease": False, "assets": []}
        for name, data in [("LokalBot.dmg", self.dmg), ("appcast.xml", self.feed)]:
            (self.directory / name).write_bytes(data)
            self.release["assets"].append({
                "name": name, "size": len(data), "browser_download_url": self.url + name,
                "digest": "sha256:" + hashlib.sha256(data).hexdigest(),
            })
        self.digest = hashlib.sha256(self.dmg).hexdigest()
        self.cask = 'cask "lokalbot" do\n  version "0.8.1"\n  sha256 "' + "a" * 64 + '"\n  auto_updates true\nend\n'

    def test_update_and_idempotent_recheck(self):
        version, assets = release_info(self.release)
        verify_assets(self.directory, version, assets)
        self.assertTrue(needs_update(self.cask, version, self.digest))
        updated = updated_cask(self.cask, version, self.digest)
        self.assertIn("  auto_updates true", updated)
        self.assertFalse(needs_update(updated, version, self.digest))

    def test_rejects_prereleases_drafts_and_unsafe_tags(self):
        for field, value in [("draft", True), ("prerelease", True), ("tag_name", "v0.9.0-beta"),
                             ("tag_name", "v0.9.0\nmalicious")]:
            with self.subTest(field=field, value=value):
                release = copy.deepcopy(self.release)
                release[field] = value
                with self.assertRaises(ValueError):
                    release_info(release)

    def test_rejects_incomplete_or_duplicate_assets(self):
        for assets in [self.release["assets"][:1], self.release["assets"] * 2]:
            with self.assertRaises(ValueError):
                release_info({**self.release, "assets": assets})

    def test_download_counter_changes_do_not_invalidate_release(self):
        refreshed = copy.deepcopy(self.release)
        refreshed["assets"][0]["download_count"] = 42
        self.assertEqual(release_info(self.release), release_info(refreshed))

    def test_rejects_untrusted_url_missing_digest_and_invalid_size(self):
        for field, value in [("browser_download_url", "https://example.com/evil.dmg"),
                             ("digest", None), ("size", 0)]:
            with self.subTest(field=field):
                release = copy.deepcopy(self.release)
                release["assets"][0][field] = value
                with self.assertRaises(ValueError):
                    release_info(release)

    def test_rejects_corrupted_download(self):
        (self.directory / "LokalBot.dmg").write_bytes(b"corrupt")
        with self.assertRaises(ValueError):
            verify_assets(self.directory, self.version, release_info(self.release)[1])

    def test_rejects_mismatched_appcast(self):
        # Even a correctly hashed feed must describe the correct release.
        with self.assertRaises(ValueError):
            verify_assets(self.directory, "0.8.4", release_info(self.release)[1])

    def test_refuses_downgrade(self):
        with self.assertRaises(ValueError):
            needs_update(self.cask, "0.7.9", self.digest)

    def test_refuses_same_version_checksum_replacement(self):
        updated = updated_cask(self.cask, self.version, self.digest)
        with self.assertRaises(ValueError):
            needs_update(updated, self.version, "b" * 64)

    def test_refuses_ambiguous_cask_fields(self):
        with self.assertRaises(ValueError):
            updated_cask(self.cask + '  version "0.9.0"\n', self.version, self.digest)


if __name__ == "__main__":
    unittest.main()
