# TOOL SANDBOXING SPECIFICATION
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** TSS-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** FINAL & APPROVED  
**Classification:** Confidential — Security & Systems Architecture  
**Security Standard:** gVisor / Firecracker MicroVM / Hardened Linux Namespaces  

---

## TABLE OF CONTENTS
1. [Security Threat Model & Sandboxing Rationale](#1-security-threat-model--sandboxing-rationale)
2. [Sandboxing Technology Evaluation & Architecture Choice](#2-sandboxing-technology-evaluation--architecture-choice)
3. [Isolation Boundary Specifications](#3-isolation-boundary-specifications)
   - 3.1 [Process & Kernel Isolation (gVisor runsc)](#31-process--kernel-isolation-gvisor-runsc)
   - 3.2 [Filesystem Isolation & Ephemeral Overlays](#32-filesystem-isolation--ephemeral-overlays)
   - 3.3 [Network Restrictions & Egress Filtering](#33-network-restrictions--egress-filtering)
   - 3.4 [Compute Quotas (CPU, RAM, PIDs)](#34-compute-quotas-cpu-ram-pids)
4. [SSRF (Server-Side Request Forgery) Mitigation Engine](#4-ssrf-server-side-request-forgery-mitigation-engine)
5. [Credential Injection & Secret Isolation](#5-credential-injection--secret-isolation)
6. [Command Filtering & System Call Interception](#6-command-filtering--system-call-interception)
7. [Execution Lifecycle, Timeouts & Watchdog Kill Strategy](#7-execution-lifecycle-timeouts--watchdog-kill-strategy)
8. [Audit Logging & Forensics](#8-audit-logging--forensics)

---

## 1. SECURITY THREAT MODEL & SANDBOXING RATIONALE

AI agents operating autonomously in enterprise environments may invoke external tools, generate shell commands, query internal databases, or fetch remote URLs. 

### Core Threat Vectors
1. **Host Compromise & Container Escape**: Untrusted code escaping container namespaces to gain root access to the underlying Kubernetes host.
2. **Server-Side Request Forgery (SSRF)**: An AI agent tricked via prompt injection into querying the AWS instance metadata service (`http://169.254.169.254`) or internal VPC endpoints.
3. **Data Exfiltration**: Tools sending tenant documents or environment secrets to external command-and-control servers.
4. **Denial of Service (DoS)**: Fork bombs, runaway recursion, or memory exhaustion starving co-located tenant workers.
5. **Cross-Tenant Credential Bleed**: Leaking decrypted OAuth tokens or database passwords into shared execution environments.

---

## 2. SANDBOXING TECHNOLOGY EVALUATION & ARCHITECTURE CHOICE

### Evaluation Matrix

| Strategy | Security Isolation | Performance / Startup Latency | Operational Complexity | Recommendation |
|---|---|---|---|---|
| **Docker-in-Docker (DinD)** | ❌ Unsafe (`--privileged` root required) | Medium (~1.5s) | High | **REJECTED (High Risk)** |
| **Vanilla Docker Containers** | ⚠️ Moderate (Shared Host Kernel) | Medium (~1.0s) | Low | Insufficient for untrusted code |
| **gVisor (`runsc`)** | ✅ High (User-space Kernel Emulation) | Fast (~150ms) | Moderate | **PRIMARY CHOICE (Containers)** |
| **Firecracker MicroVMs** | ✅ Maximum (Hardware Virtualization) | Fast (~250ms) | High (Bare-metal KVM) | Phase 2 for arbitrary multi-tenant code |

### Final Architectural Choice
**gVisor (`runsc`)** is selected as the primary execution engine for all tool executions and Model Context Protocol (MCP) tool workers. gVisor implements a user-space virtual kernel that intercepts and emulates Linux system calls, completely isolating the host Linux kernel from malicious syscall attacks.

---

## 3. ISOLATION BOUNDARY SPECIFICATIONS

```
┌────────────────────────────────────────────────────────┐
│                   KUBERNETES WORKER HOST               │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │     Tool Runner Pod (RuntimeClass: gVisor)       │  │
│  │                                                  │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │      gVisor Sandbox Boundary (runsc)       │  │  │
│  │  │                                            │  │  │
│  │  │  • Read-only Root Filesystem               │  │  │
│  │  │  • Ephemeral /tmp tmpfs (Max 64MB)         │  │  │
│  │  │  • CPU Limit: 0.5 Cores                    │  │  │
│  │  │  • RAM Limit: 256MB                        │  │  │
│  │  │  • PID Limit: 32 Processes                 │  │  │
│  │  │  • Blocked Syscalls: ptrace, mount, bpf    │  │  │
│  │  │                                            │  │  │
│  │  │  ┌──────────────────────────────────────┐  │  │  │
│  │  │  │       Tool Payload Execution         │  │  │  │
│  │  │  │   (Python Script / MCP JSON-RPC)     │  │  │  │
│  │  │  └──────────────────┬───────────────────┘  │  │  │
│  │  └─────────────────────┼──────────────────────┘  │  │
│  │                        │ Outbound HTTP/gRPC      │  │
│  │                        ▼                         │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │      Egress Proxy & SSRF Filter Gate       │  │  │
│  │  │  • Blocks 169.254.169.254 (IMDS)           │  │  │
│  │  │  • Blocks 10.0.0.0/8, 172.16.0.0/12, 127.0.0.1 │  │
│  │  │  • Whitelists verified tenant domains      │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

### 3.1 Process & Kernel Isolation (gVisor runsc)
- Tool execution pods configure Kubernetes `runtimeClassName: gvisor`.
- Capabilities dropped: `CAP_SYS_ADMIN`, `CAP_NET_ADMIN`, `CAP_SYS_PTRACE`, `CAP_DAC_OVERRIDE`.
- No root access allowed; child processes execute as `UID 10001 (sandboxuser)`.

### 3.2 Filesystem Isolation & Ephemeral Overlays
- **Root Filesystem**: Mounted as strictly **read-only** (`readOnlyRootFilesystem: true`).
- **Scratch Directory**: Ephemeral `/tmp` mounted via memory-backed `tmpfs` with a strict `sizeLimit: 64Mi`.
- **Zero Host Mounts**: No host directories (`/var/run/docker.sock`, `/etc`, `/proc`) are mounted into the sandbox.
- **Teardown**: The entire sandbox environment is destroyed immediately upon completion of the tool execution.

### 3.3 Network Restrictions & Egress Filtering
- Network namespace is completely disabled (`network: none`) for tools that only process text or compute mathematical operations.
- For tools requiring outbound network access (REST API tools), traffic is routed through a local sidecar egress proxy that validates target domains.

### 3.4 Compute Quotas (CPU, RAM, PIDs)
- **CPU Limit**: Maximum 0.5 CPU core (`cpu: 500m`).
- **Memory Limit**: Maximum 256MB (`memory: 256Mi`). OOM-killer terminates processes exceeding memory cap.
- **Process ID (PID) Limit**: Maximum 32 PIDs (`pids.max: 32`) to eliminate fork-bomb exploits.

---

## 4. SSRF (SERVER-SIDE REQUEST FORGERY) MITIGATION ENGINE

All outbound HTTP calls made by API tools or MCP servers pass through a strict in-line IP filtering gate:

### Non-Routable IP Blocklist
The proxy automatically resolves destination DNS and rejects connections to:
- `169.254.169.254/32` (AWS / GCP / Azure Instance Metadata Services)
- `127.0.0.0/8` (Localhost loopback)
- `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` (RFC 1918 Private Subnets)
- `100.64.0.0/10` (Carrier-grade NAT)
- `::1/128`, `fc00::/7` (IPv6 Loopback and Unique Local Addresses)
- Internal DNS names matching `*.cluster.local` or `*.internal`.

### DNS Rebinding Defense
DNS resolution is performed by the proxy, and the connection is initiated directly to the verified public IP address. Redirects (`HTTP 301/302`) are re-inspected against the blocklist before following.

---

## 5. CREDENTIAL INJECTION & SECRET ISOLATION

1. **No Disk Persistence**: API keys, Bearer tokens, and basic auth credentials are never written to configuration files or mounted volumes.
2. **Ephemeral In-Memory Injection**: The tool runner injects credentials into the outbound request header directly within process memory.
3. **Environment Scrubbing**: Sensitive environment variables (`DATABASE_URL`, `MASTER_ENCRYPTION_KEY`, `JWT_SECRET_KEY`) are stripped from the sandbox process environment before launch.
4. **Header Masking in Logs**: Authorization headers (`Bearer ...`, `Basic ...`, `X-Api-Key: ...`) are irreversibly masked to `[REDACTED]` prior to trace persistence.

---

## 6. COMMAND FILTERING & SYSTEM CALL INTERCEPTION

For tools executing scripts or shell commands:
- Executables permitted: `python3`, `node`, `jq`, `curl`.
- Dangerous utilities banned: `nc`, `ncat`, `nmap`, `iptables`, `sudo`, `su`, `chmod`, `chown`, `mkfifo`.
- Syscalls blocked via Seccomp profile: `ptrace`, `bpf`, `sys_chroot`, `kexec_load`, `mount`, `umount2`.

---

## 7. EXECUTION LIFECYCLE, TIMEOUTS & WATCHDOG KILL STRATEGY

```
   [Task Received] ──► [Spin Up gVisor Pod]
                              │
                              ▼
                       [Start Watchdog Timer (30s)]
                              │
                    ┌─────────┴─────────┐
                    │                   │
         [Completes in <30s]     [Exceeds 30s]
                    │                   │
                    ▼                   ▼
           [Capture Stdout]      [Watchdog Sends SIGKILL]
                    │                   │
                    ▼                   ▼
           [Teardown Sandbox]    [Record TIMEOUT Status]
```

1. **Hard Timeout Watchdog**: A background thread initiates a 30-second countdown upon sandbox invocation.
2. **Graceful / Forced Kill**:
   - At $t = 30\text{s}$: Sends `SIGTERM` to the process group.
   - At $t = 32\text{s}$: Sends `SIGKILL` to forcefully terminate hanging processes.
3. **Output Cap**: Standard output (`stdout`) and error output (`stderr`) are capped at **1MB**. Output exceeding 1MB is truncated with a warning notice to prevent memory bloat.

---

## 8. AUDIT LOGGING & FORENSICS

Every tool execution emits an immutable audit record:

```json
{
  "event": "tool.executed",
  "organization_id": "018f3a9e-2200-7299-8832-7492cbb3e200",
  "tool_id": "018f3b50-4400-7700-9912-330291029313",
  "tool_name": "refund_customer",
  "sandbox_type": "gvisor_runsc",
  "duration_ms": 420,
  "exit_code": 0,
  "cpu_time_ms": 112,
  "memory_peak_bytes": 48234496,
  "egress_domain": "api.stripe.com",
  "risk_level": "HIGH",
  "approval_id": "018f3b90-8800-8100-9912-770291029317",
  "timestamp": "2026-10-07T18:40:00.000Z"
}
```

---

*End of Tool Sandboxing Specification*  
*Document Version: 1.0.0 | Status: FINAL & APPROVED*
