# LilyPondRenderer — repo notes

Sublime Text 4 package. Renders the active `.ly` / `.ily` file with `lilypond`, optionally opens the PDF, supports render-on-save.

## Layout

Package Control convention: the package files (`*.py`, `*.sublime-*`, `messages/`) live at the **repo root**, not in a nested folder. Don't introduce a subdirectory — Sublime treats the symlinked folder name (`LilyPondRenderer`) as the package name.

## Dev loop

The repo is symlinked into Sublime's Packages directory:

```
~/Library/Application Support/Sublime Text/Packages/LilyPondRenderer
  -> ~/Projects/sublime-plugins/SublimeLilyPondRenderer
```

Edits land live; Sublime auto-reloads `.py` on save. No build step.

## Runtime quirks

- Code runs inside Sublime's embedded Python — no `pip` deps. Standard library only.
- Default Python is 3.3 for back-compat. Adding a `.python-version` file with `3.8` would scope the package to ST4. Currently unset (works on either).
- `subprocess` calls explicitly extend `PATH` with `/opt/homebrew/bin`, `/usr/local/bin`, and the `LilyPond.app` bundle because Sublime launched from the Dock has a stripped `PATH`. If adding Linux/Windows support, extend `EXTRA_PATH_DIRS` in `LilyPondRenderer.py`.
- Long-running renders go on a background thread; UI updates must be marshalled back via `sublime.set_timeout`.

## Release / Package Control

1. Update `messages/install.txt` if there's a user-visible change.
2. `git tag -a vX.Y.Z -m vX.Y.Z && git push --tags` — Package Control consumes tags as releases.
3. First-time submission: PR an entry into [`wbond/package_control_channel`](https://github.com/wbond/package_control_channel) (`repository/l.json`).

## Don't

- Don't add a Makefile / install script back. Convention here is plain `ln -s` (see README).
- Don't bundle a `lilypond` binary or any large assets — Package Control fetches the repo as-is.
