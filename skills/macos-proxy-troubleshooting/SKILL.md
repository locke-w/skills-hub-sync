---
name: macos-proxy-troubleshooting
description: "Use when an app hits region errors despite a proxy running."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [proxy, network, macos, google, region-block, vpn, antigravity, gemini]
---

# macOS Proxy / Region-Block Troubleshooting

Diagnose why an app's traffic is NOT going through the proxy on macOS, even though the
user has a proxy client installed/running. Typical symptoms:

- "User location is not supported for the API use." (Google APIs, code 400 FAILED_PRECONDITION)
- "Agent terminated due to error" in Google-based AI tools (Antigravity IDE, Gemini CLI/code assist)
- SSL_ERROR_SYSCALL / timeouts to foreign APIs while the user insists the proxy is on
- Any app that works in a browser (which may use an extension) but fails as a standalone app

Core mental model: region blocks are IP-based. If the app's requests egress from an
unsupported region (e.g. mainland China → Google), the API rejects. The fix is always
"make this app's traffic actually traverse the proxy" — usually the system proxy is simply OFF.

## Steps

1. **Confirm the real error in the app's own logs**, not the UI.
   - macOS app logs live in `~/Library/Logs/<App>/` (e.g. `language_server.log`, `main.log`).
   - `grep -iE "error|400|location|forbidden" <log>` and read the API error message verbatim.
   - Example (Antigravity): `~/Library/Logs/Antigravity/language_server.log` repeats
     `FAILED_PRECONDITION (code 400): User location is not supported for the API use.`
     once per question. See `references/antigravity-region-block.md` for the full case.

2. **Check system proxy state** — this is the #1 root cause:
   `scutil --proxy | grep -iE "enable|proxy|port"`
   If `HTTPEnable` / `HTTPSEnable` / `SOCKSEnable` are 0, Electron/Chromium apps and most
   standalone tools will NOT route through the proxy. System proxy off + client running
   = everything looks fine in the client GUI but the app still fails.

3. **Find the ACTUALLY RUNNING proxy client — never assume which one.**
   Users often have several clients installed; config files lie:
   - `~/.config/clash/config.yaml` is frequently a stale EMPTY stub (no proxies) even when
     the user's real client is a completely different app (airport-branded clients like
     猫猫云/CatCloud, Clash Verge, Mihomo Party, Surge, Stash…).
   - `ps aux | grep -iE "clash|mihomo|sing-box|surge|stash|verge|catcore"` → the client with
     a live core process is the real one. Ask the user which client they use if ambiguous —
     they will correct you (costly detour if you debug the wrong client).

4. **Find the proxy core's listening port** (mixed HTTP+SOCKS ports are commonly 7890/7892):
   - `netstat -anv -p tcp | grep -E "\.(7890|7891|7892|7893|1080|1086|8888|9090|2080)" | grep LISTEN`
   - or `lsof -nP -iTCP -sTCP:LISTEN | grep <core_pid>` (netstat is more reliable on macOS;
     lsof -p sometimes returns other processes' sockets).

5. **Verify the proxy path with a fake-key probe** — discriminates "proxy works" from
   "still direct", without needing the user's real credentials:
   `curl -sS --max-time 20 -x http://127.0.0.1:<port> "https://generativelanguage.googleapis.com/v1beta/models?key=test"`
   Read the JSON error, NOT the HTTP code:
   - `"API key not valid"` / `API_KEY_INVALID` → request REACHED Google and **passed the
     region check** → proxy path is good, egress region is supported.
   - `"User location is not supported"` → egress still in a blocked region (proxy not applied,
     or node is in the wrong region).
   - `SSL_ERROR_SYSCALL` / connection timeout → node unreachable, wrong port, or dead node.
   The same trick works for other providers: probe their API with a dummy key and compare error types.

6. **Enable the system proxy** (requires admin). Either:
   - Tell the user to flip the "系统代理" (System Proxy) toggle in their client GUI, or
   - Set it directly (needs admin; run via osascript so macOS pops the password prompt —
     the password never passes through the agent):
     ```bash
     osascript -e 'do shell script "networksetup -setwebproxy \"Wi-Fi\" 127.0.0.1 <port> && networksetup -setsecurewebproxy \"Wi-Fi\" 127.0.0.1 <port>" with administrator privileges'
     ```
     Find the service name first: `networksetup -listallnetworkservices` (usually "Wi-Fi").
   - Verify: `scutil --proxy` now shows HTTPEnable/HTTPSEnable 1 with the right port.

7. **Restart the failing app** (Command+Q, relaunch) — its language server / connection pool
   may have cached the failed state; new requests can keep failing until restart. Then retry.

## Pitfalls

- **Don't debug a proxy client from config files** — find the running process first. A default
  ClashX `config.yaml` has `proxies:` empty; loading it yields an empty GLOBAL group and every
  proxied request fails with SSL_ERROR_SYSCALL, and ClashX can even exit silently.
- **`networksetup` needs admin**: bare calls fail with "Command requires admin privileges".
  Use the osascript `with administrator privileges` wrapper (pops a GUI password dialog).
- **curl does NOT read macOS system proxy settings** (`scutil --proxy`). Always test the proxy
  with explicit `-x http://127.0.0.1:<port>`. To verify system-proxy effectiveness, either check
  `scutil --proxy` or test with a GUI app.
- **Region errors are often not the whole story**: check the app log for the FIRST failing call
  (Antigravity fails at the "pre-invocation hook: context summarization" step, before any real work).
- If the client supports TUN/enhanced mode, it's the most robust fix for apps that ignore the
  system proxy — mention it as an alternative.
- Teardown commands for the user:
  `networksetup -setwebproxystate "Wi-Fi" off` and `networksetup -setsecurewebproxystate "Wi-Fi" off`.

## References

- `references/antigravity-region-block.md` — full Antigravity case study: symptom, log evidence,
  probe results table, exact fix commands.
