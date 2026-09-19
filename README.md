# Homebrew tap for LokalBot

```sh
brew install --cask stevyhacker/tap/lokalbot
```

## Release synchronization

The `Sync LokalBot release` workflow checks the latest stable public release of
[`stevyhacker/lokalbot`](https://github.com/stevyhacker/lokalbot/releases) hourly
and can be run manually from Actions. GitHub may delay scheduled runs; this is
eventual synchronization, not an instantaneous release hook.

For a new version it downloads the DMG and appcast, verifies their published
SHA-256 digests and sizes, checks that the appcast names the same version and
DMG, then updates only the cask's version and checksum. It refuses downgrades,
prereleases, incomplete releases, and same-version checksum replacements.
No app is installed or launched. Digest/feed checks are not a fresh Apple or
Sparkle signature verification; the upstream release pipeline owns signing.

The workflow uses this repository's `GITHUB_TOKEN` with `contents: write`;
no cross-repository credential is needed. Failed runs remain visible in Actions
and leave the previous cask intact. Do not force-push around a failed update.
Public-repository schedules can be disabled after 60 days without repository
activity; re-enable the workflow and run it manually if that happens.

CI uses its system Python 3.11+ and Ruby with no additional dependencies.
For local checks:

```sh
uv run --no-project python -m unittest discover -s scripts -p 'test_*.py' -v
uv run --no-project python scripts/sync_lokalbot.py
ruby -c Casks/lokalbot.rb
```
