"""`daydreamd schedule install|remove`: run `daydreamd dream` nightly.

macOS: a launchd plist under `~/Library/LaunchAgents/`. Linux: a crontab line tagged
`# daydreamd`. The file or line is always printed before it is installed.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

LABEL = "io.daydreamd.dream"
CRON_TAG = "# daydreamd"


def launch_agents_dir() -> Path:
    override = os.environ.get("DAYDREAMD_LAUNCH_AGENTS")
    return Path(override) if override else Path.home() / "Library" / "LaunchAgents"


def command_for(path: Path, kind: str, out: Path, n: int) -> list[str]:
    exe = shutil.which("daydreamd")
    base = [exe] if exe else [sys.executable, "-m", "daydreamd.cli"]
    return base + ["dream", str(path), "--kind", kind, "--out", str(out), "--n", str(n)]


def plist_text(argv: list[str], hour: int, minute: int, log: Path) -> str:
    args = "\n".join(f"        <string>{a}</string>" for a in argv)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>{LABEL}</string>
    <key>ProgramArguments</key>
    <array>
{args}
    </array>
    <key>StartCalendarInterval</key>
    <dict><key>Hour</key><integer>{hour}</integer><key>Minute</key><integer>{minute}</integer></dict>
    <key>StandardOutPath</key><string>{log}</string>
    <key>StandardErrorPath</key><string>{log}</string>
    <key>EnvironmentVariables</key>
    <dict><key>PATH</key><string>{os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")}</string></dict>
</dict>
</plist>
"""


def cron_line(argv: list[str], hour: int, minute: int, log: Path) -> str:
    cmd = " ".join(f"'{a}'" if " " in a else a for a in argv)
    return f"{minute} {hour} * * * {cmd} >> {log} 2>&1 {CRON_TAG}"


def install(
    path: Path, kind: str, out: Path, n: int, at: str, load: bool = True, home: Path | None = None
) -> tuple[Path | None, str]:
    """Return (file written or None for cron, the text that was installed)."""
    hour, minute = (int(x) for x in at.split(":"))
    log = (home or Path.home() / ".daydreamd") / "schedule.log"
    argv = command_for(path.expanduser().resolve(), kind, out.expanduser().resolve(), n)
    if platform.system() == "Darwin":
        text = plist_text(argv, hour, minute, log)
        target = launch_agents_dir() / f"{LABEL}.plist"
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"writing {target}:\n{text}")
        target.write_text(text, encoding="utf-8")
        if load:
            subprocess.run(["launchctl", "unload", str(target)], capture_output=True, check=False)
            subprocess.run(["launchctl", "load", "-w", str(target)], check=False)
        return target, text
    line = cron_line(argv, hour, minute, log)
    print(f"adding to crontab:\n{line}")
    if load:
        current = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=False)
        kept = [ln for ln in current.stdout.splitlines() if CRON_TAG not in ln]
        subprocess.run(
            ["crontab", "-"], input="\n".join([*kept, line]) + "\n", text=True, check=False
        )
    return None, line


def remove(load: bool = True) -> str:
    if platform.system() == "Darwin":
        target = launch_agents_dir() / f"{LABEL}.plist"
        if target.exists():
            if load:
                subprocess.run(
                    ["launchctl", "unload", str(target)], capture_output=True, check=False
                )
            target.unlink()
            return f"removed {target}"
        return "nothing installed"
    current = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=False)
    kept = [ln for ln in current.stdout.splitlines() if CRON_TAG not in ln]
    if load:
        subprocess.run(["crontab", "-"], input="\n".join(kept) + "\n", text=True, check=False)
    return "removed the daydreamd crontab line"
