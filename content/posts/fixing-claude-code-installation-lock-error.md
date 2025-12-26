+++
date = '2025-12-26'
title = 'Fixing Claude Code Installation Lock Error'
author = "colosieve"
tags = ["cli", "troubleshooting"]
+++

Fixed Claude Code update stuck on "another process is currently installing" error.

```
❯ claude update
Setting up Claude Code...

✘ Installation failed

Could not install - another process is currently installing Claude. Please try again in a moment.

Try running with --force to override checks
```

Very frustrating:
- "Try running with --force to override checks" can't be applied with how Claude
  Code is installed or updated
- Even fully uninstalling Claude didn't work
- Rebooting also didn't help

Turns out stale lock directories in `~/.local/state/claude/locks/` were blocking
new installs. Remove those and the update works instantly:

```bash
rm -rf ~/.local/state/claude/locks/*
claude update
```

```
Setting up Claude Code...
✔ Claude Code successfully installed!

  Version: 2.0.76

  Location: ~/.local/bin/claude

  Next: Run claude --help to get started

✅ Installation complete!
```
