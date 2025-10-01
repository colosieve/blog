+++
title = "MacOS Dev Setup"
date = 2025-09-29T00:00:00Z
author = "colosieve"
layout = "slides"
+++

## MacOS 26 Tahoe

Upgraded to **MacOS 26 Tahoe**—the latest release brings:
- Enhanced performance
- Security patches
- Improved developer tooling integration

---

## Homebrew

Installed **Homebrew**, the de facto package manager for macOS:
- Think of it as `apt` or `yum` for Mac
- Streamlines installing, updating, and managing open-source software
- No more wrestling DMG files

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

## Node via Homebrew

Set up **Node.js** using Homebrew with **nvm** (Node Version Manager):
- Allows switching between Node versions per project
- No version conflicts across different codebases

```bash
brew install nvm
nvm install --lts
nvm use --lts
```

---

## What is LTS?

**LTS** = Long-Term Support

Node.js releases designated as LTS receive:
- Critical bug fixes for 30 months
- Security patches for 36 months
- Stable APIs—no breaking changes

Production apps should always use LTS versions. Current LTS releases use even-numbered major versions (18.x, 20.x, 22.x).

**Other software with LTS:**
- **Ubuntu Linux** (e.g., 22.04 LTS, 24.04 LTS) — 5 years support
- **Java** (e.g., Java 11, 17, 21) — years of updates
- **Python** (e.g., 3.9, 3.10, 3.11) — bug fixes and security patches

---

## GitHub Account

Created a **GitHub account**—essential infrastructure for modern development:
- Host repositories
- Collaborate via pull requests
- Integrate with CI/CD pipelines

---

## Git SSH Credentials

Set up SSH key authentication for GitHub:

```bash
$ ssh-keygen -t ed25519 -C "your_email@example.com"

$ cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAAC3Nza...9GKJl your_email@example.com
# ^ Copy this entire line to GitHub
```

Add the public key to GitHub: Settings → SSH and GPG keys → New SSH key

After setup, you can clone repositories directly:

```bash
$ git clone git@github.com:username/repo.git
```

---

## VS Code

Installed **Visual Studio Code**—Microsoft's lightweight, extensible editor:
- Built-in Git support
- IntelliSense code completion
- Integrated debugging
- Massive extension marketplace

```bash
brew install --cask visual-studio-code
```

---

## Copilot in VS Code

Configured **GitHub Copilot** in VS Code—Microsoft's catch-all AI brand:
- Tab completion for code
- AI-assisted coding suggestions
- In the VS Code context: inline code generation

---

## Claude Code

Installed **[Claude Code](https://github.com/anthropics/claude-code)**—Anthropic's CLI tool powered by Claude AI:
- Interactive coding assistance
- Codebase understanding
- Automated refactoring
- Works directly from the terminal

---

## OpenCode.ai

Set up **OpenCode.ai**—an open-source alternative to commercial AI coding tools:
- Code generation and refactoring
- Intelligent suggestions
- Code explanations
- Still needs some love and development

---

## Ghostty

Installed **Ghostty**, a fast, native terminal emulator built in Zig:
- GPU-accelerated rendering
- Minimal latency
- Native macOS integration
- Designed for performance-conscious developers

```bash
brew install --cask ghostty
```

---

## Nerd Fonts

Installed **JetBrains Mono Nerd Font**—currently the most popular choice among developers:
- Excellent readability
- Ligature support
- Thousands of glyphs for icons
- Works in terminal prompts and editors

```bash
brew install --cask font-jetbrains-mono-nerd-font
```

---

## What is a "Terminal"?

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

A **terminal** (or terminal emulator) is a text-based interface to the operating system shell.

**Historical context:**
- Physical hardware (teletypes, VT100s) connecting to mainframes

**For developers, terminals provide:**
- Direct access to system commands
- Shell scripting and automation
- Remote server management via SSH
- Version control operations (Git)
- Build tools and package managers

</div>
<div style="flex: 0 0 auto;">

<svg width="350" height="262" viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
  <!-- VT100 Terminal Body -->
  <rect x="20" y="20" width="160" height="110" rx="5" fill="#2d2d2d" stroke="#1a1a1a" stroke-width="2"/>
  <!-- Screen -->
  <rect x="30" y="30" width="140" height="80" fill="#0a0a0a"/>
  <!-- Green phosphor glow -->
  <text x="40" y="50" font-family="monospace" font-size="10" fill="#33ff33">$ login:</text>
  <text x="40" y="65" font-family="monospace" font-size="10" fill="#33ff33">username_</text>
  <!-- Keyboard suggestion -->
  <rect x="35" y="115" width="130" height="10" rx="2" fill="#3d3d3d"/>
  <circle cx="45" cy="120" r="1.5" fill="#555"/>
  <circle cx="55" cy="120" r="1.5" fill="#555"/>
  <circle cx="65" cy="120" r="1.5" fill="#555"/>
</svg>

</div>
</div>

---

## Starship Prompt

Installed **[Starship](https://starship.rs/)**—makes your terminal prompt nice and clean.

```bash
brew install starship
echo 'eval "$(starship init zsh)"' >> ~/.zshrc
```

<svg width="900" height="500" viewBox="0 0 450 250" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: 0 auto;">
  <!-- Modern Terminal Window -->
  <rect x="10" y="10" width="430" height="230" rx="8" fill="#1e1e2e" stroke="#313244" stroke-width="2"/>
  <!-- Title Bar -->
  <rect x="10" y="10" width="430" height="30" rx="8" fill="#313244"/>
  <circle cx="25" cy="25" r="5" fill="#f38ba8"/>
  <circle cx="42" cy="25" r="5" fill="#fab387"/>
  <circle cx="59" cy="25" r="5" fill="#a6e3a1"/>
  <!-- Terminal Content with Starship Prompt -->
  <text x="25" y="65" font-family="monospace" font-size="13" fill="#89b4fa">~/projects/myapp</text>
  <text x="25" y="85" font-family="monospace" font-size="13" fill="#cdd6f4">❯</text>
  <text x="40" y="85" font-family="monospace" font-size="13" fill="#a6e3a1">git</text>
  <text x="70" y="85" font-family="monospace" font-size="13" fill="#cdd6f4">status</text>
  <text x="25" y="110" font-family="monospace" font-size="12" fill="#94e2d5">On branch main</text>
  <text x="25" y="130" font-family="monospace" font-size="12" fill="#94e2d5">Your branch is up to date</text>
  <text x="25" y="160" font-family="monospace" font-size="13" fill="#89b4fa">~/projects/myapp</text>
  <text x="170" y="160" font-family="monospace" font-size="11" fill="#f9e2af">on</text>
  <text x="190" y="160" font-family="monospace" font-size="11" fill="#f38ba8"> main</text>
  <text x="25" y="180" font-family="monospace" font-size="13" fill="#cdd6f4">❯</text>
  <rect x="40" y="168" width="8" height="14" fill="#cdd6f4"/>
</svg>

---

## Unix/BSD/Linux and MacOS

**Unix** (1969): Original operating system from Bell Labs—introduced hierarchical filesystem, pipes, and shell scripting.

**BSD** (Berkeley Software Distribution): Unix variant developed at UC Berkeley—introduced TCP/IP networking, virtual memory, and the C shell.

**Linux** (1991): Unix-like kernel by Linus Torvalds—open source, powers servers, Android, embedded systems.

**macOS**: Built on **Darwin**, which derives from BSD and the Mach microkernel. macOS is **POSIX-compliant** and **UNIX 03 certified**—shares common utilities (`ls`, `grep`, `ssh`) with Linux/BSD but uses Apple frameworks (Cocoa, Metal) for the GUI layer.

In practice: macOS gives you a Unix foundation with commercial polish—familiar CLI tools, package managers like Homebrew, but filesystem layout and some utilities differ from Linux (e.g., `sed` and `grep` behavior).

---

## Next Topics

Coming up in future sessions:
- Crash course on shell
- Crash course on git