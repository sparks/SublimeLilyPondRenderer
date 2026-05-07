# LilyPondRenderer

A Sublime Text 4 package that renders the current [LilyPond](https://lilypond.org/) (`.ly` / `.ily`) file to PDF and (optionally) opens it in Preview — or any app you choose. Render and/or auto-open can be triggered manually or automatically on save.

## Features

- **Render** the active file via Command Palette, the Tools menu, or `⌘B`.
- **Auto-open** the resulting PDF in Preview (or a configured app).
- **Render-on-save** — re-render every time you save, hands-free.
- Output (including LilyPond errors) streams into a Sublime output panel.
- macOS Homebrew / `LilyPond.app` paths are added to `PATH` automatically so it Just Works when Sublime is launched from the Dock.

## Install

### Via Package Control (planned)

Once published:

1. `⌘⇧P` → *Package Control: Install Package*
2. Pick **LilyPondRenderer**

### From source (development / personal use)

Clone and symlink into Sublime's `Packages` directory using the included Makefile:

```sh
git clone git@github.com:sparks/SublimeLilyPondRenderer.git
cd SublimeLilyPondRenderer
make install      # symlinks this folder into Sublime's Packages dir
```

Other targets:

```sh
make uninstall    # remove the symlink
make reinstall    # uninstall + install
make package      # build LilyPondRenderer.sublime-package (zip) for manual install
make status       # show install state
```

## Usage

Open any `.ly` / `.ily` file, then:

- **Command Palette** (`⌘⇧P`):
  - *LilyPond: Render*
  - *LilyPond: Render (don't open)*
  - *LilyPond: Render and Open*
  - *LilyPond: Open PDF*
- **Tools → LilyPond → …**
- **`⌘B`** — render the active file.

## Settings

`Preferences → Package Settings → LilyPondRenderer → Settings`

```jsonc
{
    // Path to the lilypond binary. /opt/homebrew/bin, /usr/local/bin, and the
    // LilyPond.app bundle are added to PATH automatically.
    "lilypond_path": "lilypond",

    // Extra args passed to lilypond, e.g. ["-dno-point-and-click"].
    "extra_args": [],

    // After a successful render, open the resulting PDF.
    "auto_open": true,

    // Command used to open the PDF. "$pdf" is replaced with the PDF path; if
    // omitted, the path is appended.
    //   Default app (Preview): ["open", "$pdf"]
    //   Force Preview.app:     ["open", "-a", "Preview", "$pdf"]
    //   Skim:                  ["open", "-a", "Skim", "$pdf"]
    "open_command": ["open", "$pdf"],

    // Run lilypond automatically every time a .ly / .ily file is saved.
    // auto_open still controls whether the PDF opens after each save.
    "render_on_save": false
}
```

## Releasing for Package Control

Package Control consumes Git tags as releases.

1. Bump `messages.json` if there's an upgrade note.
2. Tag the release: `git tag -a v1.0.0 -m "v1.0.0"` and `git push --tags`.
3. Submit a PR to [`wbond/package_control_channel`](https://github.com/wbond/package_control_channel) adding an entry to `repository/l.json` (alphabetised by package name). See [Submitting a Package](https://packagecontrol.io/docs/submitting_a_package).

## License

MIT — see [LICENSE](LICENSE).
