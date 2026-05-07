import os
import shlex
import subprocess
import threading

import sublime
import sublime_plugin

SETTINGS_FILE = "LilyPondRenderer.sublime-settings"
PANEL_NAME = "lilypond_renderer"

# Common locations where `lilypond` may live but which Sublime's launch env
# might not include (especially on macOS when launched from the Dock).
EXTRA_PATH_DIRS = [
    "/opt/homebrew/bin",
    "/usr/local/bin",
    "/Applications/LilyPond.app/Contents/Resources/bin",
]


def load_settings():
    return sublime.load_settings(SETTINGS_FILE)


def is_lilypond_file(view):
    if view is None:
        return False
    name = view.file_name() or ""
    if name.lower().endswith((".ly", ".ily")):
        return True
    syntax = (view.settings().get("syntax") or "").lower()
    return "lilypond" in syntax


def build_env():
    env = os.environ.copy()
    path_parts = env.get("PATH", "").split(os.pathsep)
    for extra in EXTRA_PATH_DIRS:
        if extra not in path_parts and os.path.isdir(extra):
            path_parts.insert(0, extra)
    env["PATH"] = os.pathsep.join(path_parts)
    return env


def get_output_panel(window):
    panel = window.find_output_panel(PANEL_NAME)
    if panel is None:
        panel = window.create_output_panel(PANEL_NAME)
        panel.settings().set("line_numbers", False)
        panel.settings().set("gutter", False)
        panel.settings().set("scroll_past_end", False)
        panel.settings().set("word_wrap", True)
    return panel


def show_panel(window):
    window.run_command("show_panel", {"panel": "output." + PANEL_NAME})


def append_panel(window, text):
    panel = get_output_panel(window)
    panel.run_command("append", {"characters": text, "scroll_to_end": True})


def open_pdf(pdf_path, settings):
    open_cmd = settings.get("open_command", ["open", "$pdf"])
    if isinstance(open_cmd, str):
        parts = shlex.split(open_cmd)
    else:
        parts = list(open_cmd)
    substituted = False
    cmd = []
    for part in parts:
        if "$pdf" in part:
            cmd.append(part.replace("$pdf", pdf_path))
            substituted = True
        else:
            cmd.append(part)
    if not substituted:
        cmd.append(pdf_path)
    try:
        subprocess.Popen(cmd, env=build_env())
    except Exception as e:
        sublime.error_message("LilyPondRenderer: failed to open PDF\n%s" % e)


class LilypondRenderCommand(sublime_plugin.WindowCommand):
    """Render the active LilyPond file to PDF."""

    def is_enabled(self):
        return is_lilypond_file(self.window.active_view())

    def run(self, open_after=None):
        view = self.window.active_view()
        if view is None or not view.file_name():
            sublime.status_message("LilyPondRenderer: save the file first")
            return
        if view.is_dirty():
            view.run_command("save")

        settings = load_settings()
        source_path = view.file_name()
        source_dir = os.path.dirname(source_path)
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        pdf_path = os.path.join(source_dir, base_name + ".pdf")

        lilypond_path = settings.get("lilypond_path", "lilypond")
        extra_args = settings.get("extra_args", []) or []
        if isinstance(extra_args, str):
            extra_args = shlex.split(extra_args)

        cmd = [lilypond_path, "-o", base_name] + list(extra_args) + [source_path]

        if open_after is None:
            open_after = bool(settings.get("auto_open", True))

        panel = get_output_panel(self.window)
        panel.run_command("select_all")
        panel.run_command("right_delete")
        show_panel(self.window)
        append_panel(
            self.window,
            "$ %s\n(cwd: %s)\n\n" % (" ".join(shlex.quote(c) for c in cmd), source_dir),
        )

        thread = threading.Thread(
            target=self._run_render,
            args=(cmd, source_dir, pdf_path, open_after, settings),
        )
        thread.daemon = True
        thread.start()

    def _run_render(self, cmd, cwd, pdf_path, open_after, settings):
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=cwd,
                env=build_env(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
        except FileNotFoundError:
            sublime.set_timeout(
                lambda: append_panel(
                    self.window,
                    "ERROR: `%s` not found. Set `lilypond_path` in "
                    "LilyPondRenderer settings.\n" % cmd[0],
                ),
                0,
            )
            return
        except Exception as e:
            sublime.set_timeout(
                lambda: append_panel(self.window, "ERROR: %s\n" % e), 0
            )
            return

        for line in iter(proc.stdout.readline, ""):
            sublime.set_timeout(lambda l=line: append_panel(self.window, l), 0)
        proc.stdout.close()
        rc = proc.wait()

        def finish():
            if rc == 0:
                append_panel(self.window, "\nRender succeeded.\n")
                sublime.status_message("LilyPond: render OK")
                if open_after and os.path.exists(pdf_path):
                    open_pdf(pdf_path, settings)
            else:
                append_panel(self.window, "\nRender failed (exit %d).\n" % rc)
                sublime.status_message("LilyPond: render failed")

        sublime.set_timeout(finish, 0)


class LilypondOpenPdfCommand(sublime_plugin.WindowCommand):
    """Open the PDF that sits next to the active LilyPond file."""

    def is_enabled(self):
        return is_lilypond_file(self.window.active_view())

    def run(self):
        view = self.window.active_view()
        if not view or not view.file_name():
            return
        pdf_path = os.path.splitext(view.file_name())[0] + ".pdf"
        if not os.path.exists(pdf_path):
            sublime.status_message("LilyPondRenderer: no PDF found — render first")
            return
        open_pdf(pdf_path, load_settings())


class LilypondRenderOnSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        if not is_lilypond_file(view):
            return
        settings = load_settings()
        if not settings.get("render_on_save", False):
            return
        window = view.window()
        if window is None:
            return
        # auto_open is honored inside the render command itself.
        window.run_command("lilypond_render")
