import os
import subprocess
from sync import sync_json


def open_file_in_vim(file_path: str) -> None:
    """
    Open the file in the default editor at the last unchecked task or the bottom.
    Syncs JSON after closing the editor.
    """
    line_number = None

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines, start=1):
                if line.strip().startswith("- [ ]"):
                    line_number = i

    # Open Vim at the specified line and move the cursor to the fourth character
    editor_cmd = (
        f"{os.getenv('EDITOR', 'vim')} +{line_number} +'normal 03l' {file_path}"
        if line_number
        else f"{os.getenv('EDITOR', 'vim')} + {file_path}"
    )
    os.system(editor_cmd)
    sync_json(file_path)


def open_file_in_browser(file_path: str) -> None:
    """
    Render Markdown file to HTML and open it in the browser.
    """
    html_output = file_path.replace(".md", ".html")
    custom_css_url = "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown-dark.min.css"

    subprocess.run(
        [
            "pandoc",
            file_path,
            "-f",
            "markdown",
            "-t",
            "html",
            "-s",
            "-o",
            html_output,
            "--css",
            custom_css_url,
            "--highlight-style",
            "tango",
        ]
    )
    os.system(f"open {html_output}")
