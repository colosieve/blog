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

Configured **GitHub Copilot** in VS Code using GitHub login—AI pair programmer:
- Context-aware code completions
- Function implementations
- Documentation generation
- Backed by OpenAI Codex

---

## OpenCode.ai

Set up **OpenCode.ai**—a platform for AI-assisted development:
- Code generation and refactoring
- Intelligent suggestions
- Code explanations
- Automated test generation

---

## Claude Code (Maybe Next)

Considering **Claude Code**—Anthropic's CLI tool powered by Claude AI:
- Interactive coding assistance
- Codebase understanding
- Automated refactoring
- Works directly from the terminal

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

A **terminal** (or terminal emulator) is a text-based interface to the operating system shell.

**Historical context:**
- Physical hardware (teletypes, VT100s) connecting to mainframes

**For developers, terminals provide:**
- Direct access to system commands
- Shell scripting and automation
- Remote server management via SSH
- Version control operations (Git)
- Build tools and package managers

---

## Starship Prompt

Installed **Starship**—a minimal, fast, and customizable prompt for any shell:
- Shows git branch and status
- Displays language versions (Node, Python, Rust, etc.)
- Indicates command execution time
- Nerd Font icon support

```bash
brew install starship
echo 'eval "$(starship init zsh)"' >> ~/.zshrc
```

---

## Unix/BSD/Linux and MacOS

**Unix** (1969): Original operating system from Bell Labs—introduced hierarchical filesystem, pipes, and shell scripting.

**BSD** (Berkeley Software Distribution): Unix variant developed at UC Berkeley—introduced TCP/IP networking, virtual memory, and the C shell.

**Linux** (1991): Unix-like kernel by Linus Torvalds—open source, powers servers, Android, embedded systems.

**macOS**: Built on **Darwin**, which derives from BSD and the Mach microkernel. macOS is **POSIX-compliant** and **UNIX 03 certified**—shares common utilities (`ls`, `grep`, `ssh`) with Linux/BSD but uses Apple frameworks (Cocoa, Metal) for the GUI layer.

In practice: macOS gives you a Unix foundation with commercial polish—familiar CLI tools, package managers like Homebrew, but filesystem layout and some utilities differ from Linux (e.g., `sed` and `grep` behavior).