+++
title = "Renaming macOS Machine from Command Line"
date = 2025-11-29T00:00:00Z
author = "colosieve"
tags = ["macos", "shell", "cli"]
draft = false
+++

Here is the summary of the items to update and the generic commands to rename your macOS machine thoroughly from the command line.

## 1. `/etc/hosts` entry

**Purpose:** This file maps IP addresses to hostnames. Update this if you have a custom entry for your old hostname. This is for local DNS resolution/self-identification.

**Command:**
(Replace `old-hostname` and `new-machine-name`. You will need sudo privileges to edit this file.)

```bash
sudo vi /etc/hosts
```

**Instructions:** Inside vi, find the line containing your `old-hostname` (e.g., `192.168.1.100 old-hostname`) and change `old-hostname` to `new-machine-name`. Save and exit (`:wq!`).

**Verify:**
Check that your new hostname is present in the file:
```bash
cat /etc/hosts
```

## 2. `HostName`

**Purpose:** The primary name the system identifies itself with (kernel hostname, used by `hostname -s`).

**Command:**

```bash
sudo scutil --set HostName "new-machine-name"
```

**Verify:**
```bash
scutil --get HostName
# or simply
hostname
```

## 3. `LocalHostName`

**Purpose:** The name other devices on your local network see (e.g., in Finder sidebar). This is the Bonjour/mDNS name.

**Command:**

```bash
sudo scutil --set LocalHostName "new-machine-name"
```

**Verify:**
```bash
scutil --get LocalHostName
```

## 4. `ComputerName`

**Purpose:** The user-friendly name displayed in System Settings (or System Preferences) and in Finder.

**Command:**

```bash
sudo scutil --set ComputerName "new-machine-name"
```

**Verify:**
```bash
scutil --get ComputerName
```