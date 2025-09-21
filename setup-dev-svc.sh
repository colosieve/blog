#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_TEMPLATE="$SCRIPT_DIR/syslog-hugo.service.template"
SERVICE_NAME="syslog-hugo.service"
WORKDIR="${SYSLOG_WORKDIR:-$SCRIPT_DIR}"

HUGO_BIN="$(command -v hugo || true)"

if [[ ! -f "$SERVICE_TEMPLATE" ]]; then
  echo "Template not found: $SERVICE_TEMPLATE" >&2
  exit 1
fi

if [[ -z "$HUGO_BIN" ]]; then
  echo "hugo binary not found on PATH. Please install Hugo first." >&2
  exit 1
fi

if [[ ! -d "$WORKDIR" ]]; then
  echo "Working directory '$WORKDIR' does not exist." >&2
  exit 1
fi

SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
mkdir -p "$SYSTEMD_DIR"

TARGET_UNIT="$SYSTEMD_DIR/$SERVICE_NAME"

sed -e "s|__WORKDIR__|$WORKDIR|g" \
    -e "s|__HUGO_BIN__|$HUGO_BIN|g" \
    "$SERVICE_TEMPLATE" > "$TARGET_UNIT"

echo "Wrote unit to $TARGET_UNIT (WorkingDirectory=$WORKDIR)"

env XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}" systemctl --user daemon-reload
systemctl --user enable --now "$SERVICE_NAME"

echo "Service $SERVICE_NAME enabled and started via systemd --user."
