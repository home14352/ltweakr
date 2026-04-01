# NeonCtl

NeonCtl is a production-oriented Linux desktop system management application with a cyberpunk interface built with **Python 3.12 + PySide6**.

## Highlights
- Cross-distro detection and capability matrix
- Package abstraction (native + Flatpak + Snap + AppImage scanning)
- Installed package inventory with export
- Diagnostics, services, logs, network, disks, and process views
- Privilege strategy abstraction (`pkexec`/`sudo`/`doas`)
- XDG autostart support and desktop integration helpers
- Tray support with live CPU/RAM/disk/uptime monitoring
- Worker abstraction to keep UI responsive
- Themeable QSS skins (5 included)

## Screenshots
- Dashboard: system summary cards + capability badges
- Packages: installed inventory table and available search mode
- Settings: theme + tray + autostart controls
- Diagnostics: health checks and export action

## Supported distributions (detection)
Fedora/RHEL family, Debian/Ubuntu family, Arch family, openSUSE, Alpine, Void, Gentoo, NixOS, Solus, and unknown fallback via `/etc/os-release`.

## Supported package managers (best effort)
`dnf`, `yum`, `microdnf`, `apt`, `nala`, `pacman`, `yay`, `paru`, `zypper`, `apk`, `xbps-*`, `emerge`, `eopkg`, `nix profile`/`nix-env`, `flatpak`, `snap`.

## Install
### Virtual environment
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### User-local install
```bash
pip install --user .
```

### Run
```bash
neonctl
# or
make run
```

## Desktop launcher integration
Use NeonCtl Settings or backend helper to install:
- `~/.local/share/applications/neonctl.desktop`
- `~/.local/share/icons/hicolor/256x256/apps/neonctl.png`

## Autostart behavior
NeonCtl uses XDG autostart at `~/.config/autostart/neonctl.desktop`.

## Tray notes
Some Wayland shells restrict legacy tray behavior. NeonCtl degrades gracefully: if tray is unavailable, close exits normally.

## Installed vs Available packages
- **Installed Packages**: full local package inventory from the active native backend.
- **Available Search**: repository search for installable packages.

## Performance notes
Large installed package lists are loaded in a worker thread and incrementally added to the table.

## Privilege model
NeonCtl uses targeted elevation only for privileged actions through a centralized privilege strategy. No global root app launch required.

## Safety philosophy
- No `shell=True`
- Validate user input
- Confirm destructive operations
- Clear unsupported-feature messaging

## Known limitations
- Repo pin/hold semantics differ heavily by distro and are exposed conditionally.
- Snap and Flatpak actions require those tools to be installed.
- Some advanced distro-specific workflows remain informational in v1.

## Development
```bash
make lint
make test
make format
```
