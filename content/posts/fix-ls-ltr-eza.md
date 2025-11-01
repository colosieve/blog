+++
title = 'Making ls -ltr Work with eza'
date = 2025-11-01T23:30:00Z
draft = false
tags = ['shell', 'zsh', 'eza']
author = 'colosieve'
+++

## Problem

Muscle memory uses `ls -ltr` but eza doesn't support `-t -r` flags directly.

```bash
❯ ls -ltr
eza: Option --time (-t) has no "r" setting
```

## Root Cause

1. eza uses `--sort oldest/newest` instead of `-t -r`
2. oh-my-zsh sets `alias ls='ls -G'` in `theme-and-appearance.zsh`
3. Alias overrides function definitions unless explicitly removed

## Solution

Shell function that translates flags and removes oh-my-zsh alias.

```bash
# Remove oh-my-zsh's ls alias first
unalias ls 2>/dev/null

function ls() {
  local args=()
  local has_t=false
  local has_r=false

  # Parse user's flags
  for arg in "$@"; do
    if [[ "$arg" == -* ]] && [[ "$arg" != --* ]]; then
      [[ "$arg" == *t* ]] && has_t=true
      [[ "$arg" == *r* ]] && has_r=true
      # Remove t and r, keep other flags like 'a'
      local cleaned=$(echo "$arg" | sed 's/[tr]//g')
      [[ "$cleaned" != "-" ]] && args+=("$cleaned")
    else
      args+=("$arg")
    fi
  done

  # Build base args
  if $has_t; then
    # For time sorting: use all defaults
    args=(-lh --group-directories-first --icons=auto "${args[@]}")
    if $has_r; then
      args+=(--sort oldest)
    else
      args+=(--sort newest)
    fi
  else
    # For normal listing: use all defaults
    args=(-lh --group-directories-first --icons=auto "${args[@]}")
  fi

  eza "${args[@]}"
}
```

## Key Points

- `unalias ls 2>/dev/null` must run before function definition
- Translates `-ltr` → `-lh --group-directories-first --icons=auto --sort oldest`
- Translates `-lt` → `-lh --group-directories-first --icons=auto --sort newest`
- Preserves other flags like `-a` (becomes `-ltra`)
