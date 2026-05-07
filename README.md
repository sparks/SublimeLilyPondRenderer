# LilyPondRenderer

A Sublime Text 4 package that renders the current [LilyPond](https://lilypond.org/) (`.ly` / `.ily`) file to PDF and (optionally) opens it in Preview — or any app you choose. Render and/or auto-open can be triggered manually or automatically on save.

## Features

- **Render** the active file via Command Palette, the Tools menu, or `⌘B` — render-only by default.
- **Render and Open** — separate command that renders and then opens the PDF in Preview (or a configured app).
- **Render-on-save** — re-render every time you save, with an independent toggle for whether the PDF auto-opens.
- Output (including LilyPond errors) streams into a Sublime output panel.
- macOS Homebrew / `LilyPond.app` paths are added to `PATH` automatically so it Just Works when Sublime is launched from the Dock.

## Install

### Via Package Control (planned)

Once published:

1. `⌘⇧P` → *Package Control: Install Package*
2. Pick **LilyPondRenderer**

### From source (development / personal use)

Either clone straight into Sublime's `Packages` directory:

```sh
cd "$HOME/Library/Application Support/Sublime Text/Packages"
git clone git@github.com:sparks/SublimeLilyPondRenderer.git LilyPondRenderer
```

…or clone wherever you keep your projects and symlink it in:

```sh
git clone git@github.com:sparks/SublimeLilyPondRenderer.git
ln -s "$PWD/SublimeLilyPondRenderer" \
      "$HOME/Library/Application Support/Sublime Text/Packages/LilyPondRenderer"
```

To uninstall, just `rm` the symlink (or the directory).

## Usage

Open any `.ly` / `.ily` file, then:

- **Command Palette** (`⌘⇧P`):
  - *LilyPond: Render* — render only
  - *LilyPond: Render and Open* — render, then open the PDF
  - *LilyPond: Open PDF* — open the existing PDF without re-rendering
- **Tools → LilyPond → …**
- **`⌘B`** — render the active file and open the PDF.

## Settings

`Preferences → Package Settings → LilyPondRenderer → Settings`

```jsonc
{
    // Path to the lilypond binary. /opt/homebrew/bin, /usr/local/bin, and the
    // LilyPond.app bundle are added to PATH automatically.
    "lilypond_path": "lilypond",

    // Extra args passed to lilypond, e.g. ["-dno-point-and-click"].
    "extra_args": [],

    // Command used to open the PDF (used by "Render and Open", "Open PDF",
    // and the on-save flow when open_on_save is true).
    // "$pdf" is replaced with the PDF path; if omitted, the path is appended.
    //   Default app (Preview): ["open", "$pdf"]
    //   Force Preview.app:     ["open", "-a", "Preview", "$pdf"]
    //   Skim:                  ["open", "-a", "Skim", "$pdf"]
    "open_command": ["open", "$pdf"],

    // ---- Render-on-save (these only affect the on-save flow) ----

    // Run lilypond automatically every time a .ly / .ily file is saved.
    "render_on_save": false,

    // After a save-triggered render, also open the PDF.
    // Has no effect unless render_on_save is true.
    "open_on_save": true
}
```

The render-on-save settings are scoped to the save flow only — the manual *Render*, *Render and Open*, and *Open PDF* commands ignore them.

## Releasing for Package Control

Package Control consumes Git tags as releases.

1. Bump `messages.json` if there's an upgrade note.
2. Tag the release: `git tag -a v1.0.0 -m "v1.0.0"` and `git push --tags`.
3. Submit a PR to [`wbond/package_control_channel`](https://github.com/wbond/package_control_channel) adding an entry to `repository/l.json` (alphabetised by package name). See [Submitting a Package](https://packagecontrol.io/docs/submitting_a_package).

## License

MIT — see [LICENSE](LICENSE).
