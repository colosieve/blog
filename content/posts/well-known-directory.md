+++
title = 'The /.well-known/ Directory'
date = 2025-11-28T00:00:00Z
draft = false
tags = ['web', 'standards', 'http']
author = 'colosieve'
+++

## What Is It?

The `/.well-known/` directory is a standardized location on HTTP servers
for hosting site metadata. Defined by [RFC 8615](https://tools.ietf.org/html/rfc8615),
it's the "public reception desk" where bots and services ask standard
questions about your site.

## Common Uses

**SSL/TLS Certificates** (`/.well-known/acme-challenge/`)
- Let's Encrypt uses this to verify domain ownership
- Server places a random file here to prove control

**App Links**
- `/.well-known/apple-app-site-association` - iOS deep linking
- `/.well-known/assetlinks.json` - Android app verification

**Security** (`/.well-known/security.txt`)
- Contact info for reporting vulnerabilities
- Used by bug bounty programs

**Authentication** (`/.well-known/openid-configuration`)
- OAuth/OIDC discovery endpoint
- Auto-configures login URLs and public keys

**Password Management** (`/.well-known/change-password`)
- Browser integration for password resets
- Redirects to your actual password change page

## Example: opencode CLI

The opencode CLI uses `/.well-known/opencode` for custom authentication:

```bash
opencode auth login https://ai.example.com
```

The CLI fetches `https://ai.example.com/.well-known/opencode`:

```json
{
  "auth": {
    "command": ["gcloud", "auth", "print-identity-token"],
    "env": "OPENCODE_TOKEN"
  },
  "config": {
    "api": "https://ai.example.com/v1"
  }
}
```

This tells the CLI to run `gcloud auth print-identity-token`, store the
output in `OPENCODE_TOKEN`, and use the custom API endpoint.

## Why It Exists

Prevents cluttering the root directory with config files while ensuring
automated tools can always find them at predictable paths.
