+++
title = "Fixing tmux Local Network Access on macOS"
subtitle = "Embedding Info.plist to Bypass Local Network Privacy Restrictions"
date = 2025-10-30T00:00:00Z
author = "colosieve"
tags = ["macos", "tmux", "networking", "privacy", "troubleshooting"]
+++

## The Problem

On macOS Tahoe (and potentially earlier versions), an insidious networking issue affects **unsigned third-party tools** running from within unsigned tools like tmux (installed from Homebrew): connections to local network addresses (like `192.168.x.x`) are silently blocked with a cryptic "no route to host" error.

### My Environment

- **macOS Version:** Tahoe 26.0.1
- **tmux:** 3.5a (installed via Homebrew)
- **Go:** 1.24.6 (installed via Homebrew)
- **curl:** `/usr/bin/curl` (system binary)

### What's Actually Happening

The problem is **deceptively selective** that I am still wrapping my head around from my frustration:

```bash
# Run directly in Terminal.app (NOT in tmux or screen)
$ which go
/opt/homebrew/bin/go                   # Third-party Homebrew - unsigned

$ go run my_app.go                     # Connects to 192.168.50.2
SUCCESS: Connected                     # ✅ Works! Even though go is unsigned Homebrew!

# Run from inside screen (system binary at /usr/bin/screen)
$ which screen
/usr/bin/screen                        # System binary - signed by Apple

$ screen
$ go run my_app.go                     # Same app, same unsigned go
SUCCESS: Connected                     # ✅ Still works!

# Now from inside tmux session (unsigned Homebrew)
$ which curl
/usr/bin/curl                          # System binary - signed by Apple

$ curl https://192.168.50.2
HTTP/1.1 200 OK                        # ✅ Still works!

$ go run my_app.go                     # Same app, same 192.168.50.2
ERROR: no route to host                # ❌ NOW BLOCKED!

$ node my_script.js                    # Same script, same 192.168.50.2
ERROR: ECONNREFUSED                    # ❌ NOW BLOCKED!
```

**The maddening part:** curl shows the server is reachable, but your Go apps, Node apps, and AI coding CLIs mysteriously fail to connect to the **same IP address**.

This creates a deeply confusing situation:
- The network is clearly working (curl succeeds)
- The server is reachable (curl confirms it)
- But your application fails with "no route to host"

**What seems to be happening:** When you run scripts or programs from within tmux (unsigned Homebrew tool), those scripts are executed by interpreters/runtimes (node, python - also unsigned Homebrew tools), or compiled into unsigned executable by unsigned compiler toolchain (go), creating a chain of unsigned tools. The observed behavior suggests macOS blocks local network access when this toolchain consists of more than 1 hop of unsigned binaries, though I'm not certain of the exact logic involved.

**The million dollar question this raises:** How do you even know these apps are connecting directly to the IP you specified? Could they be secretly routing through a cloud proxy and failing because private IPs aren't routable through their infrastructure? The error message provides no indication that this is a macOS permission issue rather than a networking or application architecture problem.

This particularly scares people when they are setting up **AI coding assistants** and development tools, that for privacy reason you want it to only connect to local AI model running on your private network.

### Root Cause: Unsigned Binary from Unsigned Parent

macOS enforces **Local Network Privacy** restrictions. Based on observed behavior, it appears to check **both the application making the connection AND its parent process**, though the exact logic remains unclear to me.

```bash
$ which curl
/usr/bin/curl          # System binary (Apple-signed) → ✅ Exempt

$ which go
/opt/homebrew/bin/go   # Third-party Homebrew binary → ⚠️ Checked by macOS

$ which node
/opt/homebrew/bin/node # Third-party Homebrew binary → ⚠️ Checked by macOS
```

**The critical observation:** Unsigned tools (go, node) work fine when run directly from Terminal.app:

```
Terminal.app (system app - signed)
  └─ go run my_app.go
      └─ go (Homebrew - UNSIGNED)
          → ✅ WORKS!
```

They also work through system binaries like screen:

```
Terminal.app (system app - signed)
  └─ screen (system binary - /usr/bin/screen - signed)
      └─ go run my_app.go
          └─ go (Homebrew - UNSIGNED)
              → ✅ WORKS!
```

But the SAME unsigned tools fail when spawned from unsigned tmux:

```
Terminal.app (system app - signed)
  └─ tmux (Homebrew - UNSIGNED)
      └─ go run my_app.go
          └─ go (Homebrew - UNSIGNED)
              └─ compiled binary tries TCP connection to 192.168.x.x → ❌ BLOCKED!
```

Same with Node.js:

```
# Works directly from Terminal.app:
Terminal.app (signed)
  └─ node my_script.js (UNSIGNED) → ✅ WORKS!

# Fails from within tmux:
Terminal.app (signed)
  └─ tmux (UNSIGNED)
      └─ node my_script.js (UNSIGNED) → ❌ BLOCKED!
```

And system tools always work:

```
Terminal.app (signed)
  └─ tmux (UNSIGNED)
      └─ curl (system binary - SIGNED)
          → ✅ WORKS
```

**My best guess:** Based on testing, it appears that macOS checks the entire parent chain and permits unsigned tools to access local networks only if ALL parents in the chain are signed. Examples:
- Terminal.app (signed) → go (unsigned) = ✅ Works
- Terminal.app (signed) → screen (signed) → go (unsigned) = ✅ Works
- Terminal.app (signed) → tmux (unsigned) → go (unsigned) = ❌ Blocked

System binaries (curl, ssh) work regardless because they're signed by Apple themselves. However, I don't know the exact logic macOS uses internally - this is simply what the observed behavior suggests.

### Why This is Particularly Bad

This behavior creates a serious **transparency and trust problem**:

1. **No Clear Error Message:** "no route to host" suggests a networking/routing problem, not a permissions issue. There's no indication that macOS is actively blocking the connection.

2. **Inconsistent Behavior:** System tools (curl, ssh) work fine, but third-party tools fail. This makes debugging nearly impossible without deep system knowledge.

3. **Trust Erosion:** When an application you downloaded from the internet to read and process your personal data fails to connect to a local IP, you're forced to question: "Is this app secretly proxying my data through their cloud service? Why wouldn't it be able to reach a private IP on my network?"

4. **Developer Friction:** I only came to the conclusion that the application could be trusted because: a) they are open source, b) I examined their source code and found no suspicious business in making TCP connections - just straightforward network calls, and c) I had compiled one of the apps myself personally for entirely different reasons. This allowed me to rule out the "secret cloud proxy" theory and eventually identify the actual macOS permissions issue. Imagine hours spent debugging this from potential users.

Apple's implementation of Local Network Privacy, while well-intentioned, well, just sucks.

---

## The Solution: Embed Info.plist

The fix involves embedding an `Info.plist` file directly into the tmux binary during compilation. This provides macOS with:

1. A proper bundle identifier
2. A local network usage description
3. Information needed to track permissions

---

## Implementation

### Step 1: Create Info.plist

Create an `Info.plist` file in your tmux source directory:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>com.github.tmux</string>
    <key>CFBundleName</key>
    <string>tmux</string>
    <key>CFBundleVersion</key>
    <string>3.5a</string>
    <key>NSLocalNetworkUsageDescription</key>
    <string>tmux needs access to the local network to manage terminal sessions.</string>
</dict>
</plist>
```

**Key fields:**
- `CFBundleIdentifier`: Unique identifier for macOS to track permissions
- `NSLocalNetworkUsageDescription`: **Critical** - Describes why local network access is needed

### Step 2: Build with Embedded Plist

The magic happens in the linker flags. Use the `-Wl,-sectcreate` flag to embed the Info.plist into the `__TEXT` segment of the binary:

```bash
./configure --disable-utf8proc \
    LDFLAGS="-Wl,-sectcreate,__TEXT,__info_plist,Info.plist"

make clean
make
```

**What this does:**
- `-Wl,` - Pass the following arguments to the linker
- `-sectcreate` - Create a new section in the binary
- `__TEXT` - Place it in the TEXT segment
- `__info_plist` - Name the section `__info_plist` (what macOS looks for)
- `Info.plist` - Use this file as the section content

### Step 3: Code Sign

```bash
codesign -s - -f ./tmux
```

### Step 4: Install

```bash
sudo cp ./tmux /opt/homebrew/Cellar/tmux/3.5a/bin/tmux
```

Adjust the path based on your tmux version.

### Step 5: Restart tmux Server

**Critical step:** tmux keeps the old binary in memory. You must restart the server:

```bash
tmux kill-server
tmux new -s test
```

Detaching from sessions is **not enough** - you must kill the server to reload the binary from disk.

---

## Automated Build Script

Save this as `build-with-plist.sh`:

```bash
#!/bin/bash
set -e

echo "=== Building tmux with embedded Info.plist ==="

# Clean previous build
make clean 2>/dev/null || true

# Reconfigure with Info.plist linker flag
./configure --disable-utf8proc \
    LDFLAGS="-Wl,-sectcreate,__TEXT,__info_plist,Info.plist"

# Build
make

# Verify Info.plist is embedded
echo ""
echo "=== Verifying Info.plist embedding ==="
if otool -l ./tmux | grep -q "__info_plist"; then
    echo "✓ Info.plist found in binary!"
    echo ""
    segedit ./tmux -extract __TEXT __info_plist /tmp/tmux-plist.txt 2>/dev/null || true
    cat /tmp/tmux-plist.txt
else
    echo "✗ Info.plist NOT embedded"
    exit 1
fi

# Sign it
echo ""
echo "=== Signing binary ==="
codesign -s - -f ./tmux

# Install over Homebrew version
echo ""
echo "=== Installing to /opt/homebrew/bin/tmux ==="
sudo cp ./tmux /opt/homebrew/bin/tmux

echo ""
echo "✓ SUCCESS! tmux rebuilt with Info.plist and installed"
echo ""
echo "Test it in Terminal.app:"
echo "  tmux kill-server"
echo "  tmux new -s test"
```

Make it executable and run:

```bash
chmod +x build-with-plist.sh
./build-with-plist.sh
```

---

## Verification

### Check if Info.plist is Embedded

```bash
otool -l /opt/homebrew/bin/tmux | grep "__info_plist"
```

**Expected output:**
```
  sectname __info_plist
   segname __TEXT
```

### Extract and View Embedded Plist

```bash
segedit /opt/homebrew/bin/tmux -extract __TEXT __info_plist /tmp/extracted.plist
cat /tmp/extracted.plist
```

Should display your Info.plist content.

### Verify Code Signature

```bash
codesign -dvvv /opt/homebrew/bin/tmux 2>&1 | grep -E "Identifier=|Info.plist"
```

**Expected output:**
```
Identifier=com.github.tmux
Info.plist entries=4
```

---

## Testing

### Test Script

Create `test_network.go` to verify local network access:

```go
package main

import (
	"fmt"
	"net"
	"net/http"
	"time"
)

func main() {
	// Test 1: Raw TCP connection to local network
	fmt.Println("Test 1: TCP connection to 192.168.50.2:443")
	conn, err := net.DialTimeout("tcp", "192.168.50.2:443", 5*time.Second)
	if err != nil {
		fmt.Printf("  ERROR: %v\n", err)
	} else {
		fmt.Printf("  SUCCESS: Connected\n")
		conn.Close()
	}

	// Test 2: HTTP GET to local network
	fmt.Println("\nTest 2: HTTP GET to local server")
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get("https://192.168.50.2")
	if err != nil {
		fmt.Printf("  ERROR: %v\n", err)
	} else {
		fmt.Printf("  SUCCESS: HTTP %d\n", resp.StatusCode)
		resp.Body.Close()
	}
}
```

### Before Fix (Blocked)

```bash
# Inside tmux (before embedding Info.plist)
$ go run test_network.go

Test 1: TCP connection to 192.168.50.2:443
  ERROR: dial tcp 192.168.50.2:443: connect: no route to host

Test 2: HTTP GET to local server
  ERROR: Get "https://192.168.50.2": dial tcp 192.168.50.2:443: connect: no route to host
```

### After Fix (Working)

```bash
# Inside tmux (after embedding Info.plist and restarting server)
$ tmux kill-server
$ tmux new -s test
$ go run test_network.go

Test 1: TCP connection to 192.168.50.2:443
  SUCCESS: Connected

Test 2: HTTP GET to local server
  SUCCESS: HTTP 200
```

---

## Key Takeaways

### What I've Observed

1. **Unsigned tools work from Terminal.app**: Running `go run my_app.go` or `node my_script.js` directly from Terminal.app works perfectly, even though go and node are unsigned Homebrew binaries
2. **Unsigned tools also work through system screen**: The same unsigned tools work fine when run inside `screen` (system binary at `/usr/bin/screen`)
3. **Same unsigned tools fail from unsigned tmux**: The exact same commands fail with "no route to host" when run inside tmux (unsigned Homebrew binary)
4. **System binaries always work**: `/usr/bin/curl`, `/usr/bin/ssh` work fine everywhere - directly from Terminal.app, from within screen, AND from within unsigned tmux
5. **Signed intermediaries appear to "pass through" permissions**: It appears that as long as the chain includes only signed binaries (Terminal.app → screen → go), unsigned tools can access local networks. But if ANY link in the chain is unsigned (Terminal.app → tmux → go), the access is blocked
6. **Confusing diagnostics**: curl works (system binary), screen+go works, but the same go/node apps that work everywhere else mysteriously fail in tmux with misleading "no route to host" errors

### The Fix in Three Steps

1. Create `Info.plist` with `NSLocalNetworkUsageDescription`
2. Rebuild with `-Wl,-sectcreate,__TEXT,__info_plist,Info.plist`
3. **Restart tmux server** (not just detach!)

---

## Conclusion

macOS Local Network Privacy restrictions affect third-party command-line tools in unexpected ways. By embedding an `Info.plist` directly into the binary, we transform tmux from an "unknown binary" into a properly identified application, allowing it to request and receive local network access permissions like any other macOS app.

---

## References

- [Apple Documentation: NSLocalNetworkUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nslocalnetworkusagedescription)
- [Apple Code Signing Guide](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/)
- Linker documentation: `man ld` (search for "sectcreate")
