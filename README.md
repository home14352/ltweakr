# NeonCtl

NeonCtl is a cyberpunk-themed Linux desktop system management application built with **Python 3.12 + PySide6**.

## Features (v1)
- Cross-distro detection and capability matrix
- Native package manager abstraction (best-effort)
- Installed package inventory browser with CSV export
- Updates, diagnostics, privilege strategy checks
- Tray integration with live CPU/RAM/disk/uptime tooltip
- XDG autostart helpers and desktop integration helpers
- Theme support with 5 bundled QSS themes

## Supported Linux families (detection)
- Fedora/RHEL family
- Debian/Ubuntu family
- Arch family
- openSUSE family
- Alpine, Void, Gentoo, NixOS, Solus
- Unknown fallback via `/etc/os-release`

## Supported package manager backends (best effort)
`apt`, `dnf`, `pacman`, `zypper`, `apk`, `xbps` (+ architecture to extend more managers).

---

## Installation

### 1) Prerequisites
On your Linux system, ensure these are available:
- Python **3.12+**
- `pip`
- `venv` module
- Qt runtime libraries required by PySide6 (installed automatically in most distributions through wheel dependencies)

### 2) Clone
```bash
git clone <your-repo-url> neonctl
cd neonctl
```

### 3) Recommended: Virtual environment install
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
```

Run:
```bash
neonctl
# or
python -m neonctl.main
# or
make run
```

### 4) User-local install (without virtualenv)
```bash
pip install --user .
```

If your user-local bin directory is not on PATH, add one of:
- `~/.local/bin` (most distros)
- `~/Library/Python/...` (not Linux; listed for completeness)

Then run:
```bash
neonctl
```

### 5) System-wide install (administrator-managed)
> Use this only when you intentionally want a machine-wide install.

```bash
sudo pip install .
```

Safer alternative for distro-managed environments:
- Build and package NeonCtl for your distribution (recommended for production deployment).

---

## Desktop launcher integration
NeonCtl includes desktop entry templates:
- `neonctl/assets/desktop/neonctl.desktop`
- `neonctl/assets/autostart/neonctl.desktop`

Manual user-level installation:
```bash
mkdir -p ~/.local/share/applications
cp neonctl/assets/desktop/neonctl.desktop ~/.local/share/applications/neonctl.desktop

mkdir -p ~/.local/share/icons/hicolor/256x256/apps
cp neonctl/assets/icons/neonctl.png ~/.local/share/icons/hicolor/256x256/apps/neonctl.png

update-desktop-database ~/.local/share/applications || true
gtk-update-icon-cache ~/.local/share/icons/hicolor || true
```

After this, NeonCtl should appear in your desktop launcher menu.

---

## Autostart (XDG)
NeonCtl uses:
- `~/.config/autostart/neonctl.desktop`

You can enable/disable autostart from Settings in-app, or manually:
```bash
mkdir -p ~/.config/autostart
cp neonctl/assets/autostart/neonctl.desktop ~/.config/autostart/neonctl.desktop
```

Disable:
```bash
rm -f ~/.config/autostart/neonctl.desktop
```

---

## Development commands
```bash
make lint     # ruff check .
make format   # black .
make test     # pytest -q
```

## Tray behavior notes
- Some Wayland desktop shells limit legacy system tray behavior.
- If tray is unavailable, NeonCtl falls back to normal window behavior (close exits app).

## Installed vs Available package modes
- **Installed Packages**: local package inventory on current machine.
- **Available Search**: repository query mode (backend-dependent).

## Safety model
- No `shell=True` command execution
- Centralized privilege strategy (`pkexec` / `sudo` / `doas`)
- Confirmation-first for destructive operations
- Graceful unsupported-feature messaging

## Known limitations (v1)
- Many distro-specific advanced operations are represented as safe limited support.
- Package hold/pin semantics are intentionally conservative and backend-specific.
- Snap/Flatpak functionality depends on those tools being installed.

## Screenshots
- Dashboard (system summary)
- Package inventory (installed list + filter + export)
- Settings (theme/tray/autostart)
- Diagnostics summary page
