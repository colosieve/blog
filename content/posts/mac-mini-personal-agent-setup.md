+++
date = '2026-06-13'
title = 'Mac Mini Personal Agent Setup'
author = "colosieve"
tags = ["macos", "agents", "setup"]
+++

Short setup notes for turning a fresh Mac Mini into a personal agent machine.

## Reset macOS

On the Mac Mini:

1. Apple menu -> `System Settings`
2. `General` -> `Transfer or Reset`
3. `Erase All Content and Settings`
4. Follow the assistant and confirm the erase.

After reboot:

1. Choose language, country, and Wi-Fi.
2. Migration Assistant: `Not Now`.
3. Sign in with Apple ID if desired.
4. Create the main admin user.
5. Enable FileVault.
6. Disable analytics sharing.
7. Open `System Settings` -> `General` -> `Sharing`.
8. Turn on `Remote Login`.
9. Optional: turn on `Screen Sharing`.
10. Set the computer name, for example `agent-mini`.

## Development Setup

Follow the macOS dev setup flow, but skip the OS upgrade step.

Install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install baseline tools:

```bash
brew install nvm git gh
mkdir -p ~/.nvm
```

Add nvm to `~/.zshrc`:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && . "/opt/homebrew/opt/nvm/nvm.sh"
```

Install Node:

```bash
source ~/.zshrc
nvm install --lts
nvm use --lts
```

Install editor and terminal tools:

```bash
brew install --cask visual-studio-code ghostty font-jetbrains-mono-nerd-font
brew install starship
echo 'eval "$(starship init zsh)"' >> ~/.zshrc
```

Set up GitHub SSH:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
```

Add the public key in GitHub:

`Settings` -> `SSH and GPG keys` -> `New SSH key`

Authenticate GitHub CLI:

```bash
gh auth login
```

## Agent Tools

Install Claude Code, OpenCode, and Codex:

```bash
npm install -g @anthropic-ai/claude-code
npm install -g opencode-ai
brew install --cask codex
```

Authenticate each tool:

```bash
claude
opencode
codex
```

For Codex, choose `Sign in with ChatGPT` unless the machine is intended for
API-key-based automation.

## Private Knowledge Repository

Create a private GitHub repository for personal knowledge:

```bash
mkdir -p ~/src/personal-knowledge
cd ~/src/personal-knowledge
git init
gh repo create personal-knowledge --private --source=. --remote=origin
```

A simple OKF-style layout works well:

```text
personal-knowledge/
  index.md
  tasks/
    inbox.md
  people/
  projects/
  references/
```

Example `index.md`:

```markdown
---
type: Index
title: Personal Knowledge
description: Private knowledge base for local agents.
---

# Personal Knowledge

- [[tasks/inbox]]
- [[projects]]
- [[people]]
```

Example `tasks/inbox.md`:

```markdown
---
type: Task List
title: Task Inbox
---

# Task Inbox

- [ ] 2026-06-13: Set up Mac Mini personal agent
- [ ] Renew passport (recurring: yearly, next: 2027-01-01) - see [[passport-renewal]]
```

Use one checkbox per task, dates as `YYYY-MM-DD`, and `next:` for recurring
tasks.

## Telegram Bot

In Telegram:

1. Open `@BotFather`.
2. Run `/newbot`.
3. Pick a display name.
4. Pick a username ending in `bot`.
5. Save the bot token.
6. Optional settings:
   - `/setdescription`
   - `/setuserpic`
   - `/setprivacy`

Keep privacy enabled unless the bot must read all group messages.

## OpenClaw

Install and onboard OpenClaw:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw gateway status
```

During onboarding:

1. Choose OpenAI or Codex auth if offered.
2. Use the Codex or ChatGPT login already created above.
3. Configure Telegram with the BotFather token.
4. Keep the direct-message policy as pairing or allowlist, not public open
   access.

If configuring manually, use `~/.openclaw/openclaw.json`:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "PASTE_BOTFATHER_TOKEN",
      dmPolicy: "pairing"
    }
  }
}
```

Start and pair:

```bash
openclaw gateway restart
openclaw logs --follow
```

Message the Telegram bot, then approve the pairing code:

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

## Daily Task Reminder

Create a daily OpenClaw reminder:

```bash
openclaw cron create "0 8 * * *" \
  "Read ~/src/personal-knowledge/tasks/inbox.md. Send me a short reminder of overdue and due-today tasks." \
  --name "Daily personal task reminder" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --announce \
  --channel telegram \
  --to "<YOUR_TELEGRAM_USER_ID>"
```

Check it:

```bash
openclaw cron list
openclaw cron run <job-id> --wait
openclaw doctor
```
