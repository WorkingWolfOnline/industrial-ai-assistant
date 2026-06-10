# Security Guidelines

## Overview

This document outlines security principles and guidelines for deploying the Industrial AI Assistant Framework in industrial environments.

⚠️ **CRITICAL WARNING**: This framework is designed for **monitoring and advisory purposes only**. Direct AI control of industrial processes can pose serious safety risks.

## Core Security Principles

### 1. Defense in Depth

```
┌─────────────────────────────────────────────────────────────┐
│                    DEFENSE LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: Physical Security                                 │
│  ├── Secure server locations                                │
│  ├── Access controls                                        │
│  └── Environmental protections                              │
│                                                             │
│  Layer 2: Network Segmentation                              │
│  ├── Industrial DMZ                                         │
│  ├── Firewall rules                                         │
│  └── VLAN isolation                                         │
│                                                             │
│  Layer 3: Data Diode                                        │
│  ├── Unidirectional data flow                               │
│  ├── Hardware-enforced isolation                            │
│  └── No return path                                         │
│                                                             │
│  Layer 4: Application Security                              │
│  ├── Read-only enforcement                                  │
│  ├── Input validation                                       │
│  └── Authentication & authorization                         │
│                                                             │
│  Layer 5: Monitoring & Audit                                │
│  ├── Comprehensive logging                                  │
│  ├── Anomaly detection                                      │
│  └── Regular security reviews                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Read-Only by Design

**The AI system must NEVER directly write to DCS/PLC systems.**

```python
# ✅ CORRECT: Read-only implementation
class SafeDCSClient:
    """Read-only DCS client with safety enforcement."""

    def __init__(self):
        self._read_only = True  # Enforced at initialization

    def read_value(self, tag: str) -> Any:
        """Safe read operation."""
        return self._connection.read(tag)

    def write_value(self, tag: str, value: Any) -> None:
        """Write operations are blocked."""
        if self._read_only:
            raise SecurityError(
                "Write operations are prohibited. "
                "This is a read-only monitoring system."
            )
```

### 3. Human-in-the-Loop

All control recommendations require human operator confirmation:

```
AI Recommendation → Operator Review → Confirmation → Manual Execution
       │                  │               │
       ▼                  ▼               ▼
   Generated         Displayed in     Operator
   by LLM            HMI with         clicks
                     warnings         "Confirm"
```

## Network Architecture

### Recommended Network Segmentation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ENTERPRISE NETWORK                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │   Corporate     │  │   Engineering   │  │   AI Training   │         │
│  │   Workstations  │  │   Workstations  │  │   Environment   │         │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘         │
└───────────┼────────────────────┼────────────────────┼──────────────────┘
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         INDUSTRIAL DMZ                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │   AI Server     │  │   Data Gateway  │  │   Historian     │         │
│  │   (MCP Server)  │  │   (Read-Only)   │  │   (Optional)    │         │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘         │
└───────────┼────────────────────┼────────────────────┼──────────────────┘
            │                    │                    │
            │         ┌──────────┴──────────┐         │
            │         │    DATA DIODE       │         │
            │         │  (Unidirectional)   │         │
            │         └──────────┬──────────┘         │
            │                    │                    │
┌───────────┼────────────────────┼────────────────────┼──────────────────┐
│           │         CONTROL NETWORK (Isolated)      │                    │
│  ┌────────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐         │
│  │   DCS Server    │  │   PLC Rack 1    │  │   PLC Rack 2    │         │
│  │   (Honeywell/   │  │                 │  │                 │         │
│  │   Yokogawa/etc) │  │                 │  │                 │         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘         │
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │   Safety System │  │   Field Devices │  │   Sensors       │         │
│  │   (SIS)         │  │                 │  │   & Actuators   │         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Firewall Rules

| Source | Destination | Port | Protocol | Action | Purpose |
|:---|:---|:---:|:---:|:---:|:---|
| AI Server | Data Gateway | 4840 | OPC UA | ALLOW | Read process data |
| Data Gateway | DCS | 4840 | OPC UA | ALLOW | Read process data |
| DCS | Data Gateway | ANY | ANY | DENY | No reverse connection |
| Enterprise | AI Server | 443 | HTTPS | ALLOW | Web interface access |
| AI Server | Internet | 443 | HTTPS | ALLOW | LLM API access (if cloud) |
| Control Network | Enterprise | ANY | ANY | DENY | Isolation enforcement |

## Data Security

### Data Classification

| Classification | Examples | Handling |
|:---|:---|:---|
| **Public** | Documentation, open examples | No restrictions |
| **Internal** | Generic configurations, test data | Internal use only |
| **Confidential** | Production tag lists, process parameters | Encrypted storage |
| **Restricted** | Safety system details, security configs | Access control + audit |

### Data Sanitization

Before sharing logs or examples:

```python
def sanitize_log_entry(entry: dict) -> dict:
    """Remove sensitive information from log entries."""
    sanitized = entry.copy()

    # Remove specific tag names
    if 'tag_name' in sanitized:
        sanitized['tag_name'] = hash_tag_name(sanitized['tag_name'])

    # Remove IP addresses
    if 'source_ip' in sanitized:
        sanitized['source_ip'] = 'REDACTED'

    # Remove specific setpoints
    if 'setpoint' in sanitized:
        sanitized['setpoint'] = 'REDACTED'

    return sanitized
```

## Authentication & Authorization

### Role-Based Access Control (RBAC)

```yaml
# roles.yaml
roles:
  operator:
    permissions:
      - view_dashboard
      - view_recommendations
      - acknowledge_alarms
    restrictions:
      - cannot_modify_configuration
      - cannot_access_raw_logs

  engineer:
    permissions:
      - view_dashboard
      - view_recommendations
      - modify_configuration
      - view_analytics
    restrictions:
      - cannot_delete_audit_logs

  administrator:
    permissions:
      - all_permissions
    restrictions:
      - cannot_bypass_audit_logging
```

### API Authentication

```python
from functools import wraps
from flask import request, abort

def require_auth(roles=None):
    """Decorator for API endpoint authentication."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                abort(401, "Authentication required")

            user = validate_token(token)

            if not user:
                abort(401, "Invalid token")

            if roles and user.role not in roles:
                abort(403, "Insufficient permissions")

            # Log access
            audit_log.info(f"API access: {user.id} -> {request.endpoint}")

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage
@app.route('/api/recommendations')
@require_auth(roles=['operator', 'engineer', 'administrator'])
def get_recommendations():
    """Get AI recommendations (requires authentication)."""
    pass
```

## Audit Logging

### Required Log Events

| Event | Data to Log | Retention |
|:---|:---|:---:|
| User Login | User ID, timestamp, source IP | 2 years |
| Data Access | User ID, tags accessed, timestamp | 1 year |
| Recommendation Viewed | User ID, recommendation ID | 1 year |
| Configuration Change | User ID, change details, before/after | 3 years |
| System Alert | Alert type, severity, response | 2 years |
| API Access | Endpoint, user ID, timestamp | 1 year |

### Log Format

```json
{
  "timestamp": "2026-06-10T14:30:00Z",
  "event_type": "RECOMMENDATION_VIEWED",
  "user_id": "user_12345",
  "session_id": "sess_abcdef",
  "source_ip": "10.0.1.100",
  "details": {
    "recommendation_id": "rec_001",
    "equipment_id": "REACTOR_001",
    "severity": "warning"
  },
  "integrity_hash": "sha256:abc123..."
}
```

## Incident Response

### Security Incident Levels

| Level | Description | Response Time | Actions |
|:---|:---|:---:|:---|
| **1 - Critical** | Unauthorized access to control systems | Immediate | Isolate, investigate, notify |
| **2 - High** | Data breach, API key compromise | 1 hour | Rotate credentials, audit logs |
| **3 - Medium** | Suspicious activity, failed auth attempts | 4 hours | Monitor, analyze, document |
| **4 - Low** | Minor policy violations | 24 hours | Review, educate, document |

### Response Playbook

```
SECURITY INCIDENT RESPONSE

1. DETECTION
   □ Identify incident through monitoring or report
   □ Classify incident level
   □ Notify security team

2. CONTAINMENT
   □ Isolate affected systems if necessary
   □ Preserve evidence (logs, memory dumps)
   □ Document initial findings

3. INVESTIGATION
   □ Analyze logs and system state
   □ Determine scope of impact
   □ Identify root cause

4. REMEDIATION
   □ Patch vulnerabilities
   □ Rotate compromised credentials
   □ Update security controls

5. RECOVERY
   □ Restore normal operations
   □ Verify system integrity
   □ Resume monitoring

6. POST-INCIDENT
   □ Document lessons learned
   □ Update procedures
   □ Conduct team debrief
```

## Compliance

### Industry Standards

| Standard | Requirements | Implementation |
|:---|:---|:---|
| **IEC 62443** | Industrial cybersecurity | Zone-based architecture |
| **NIST CSF** | Cybersecurity framework | Risk assessment + controls |
| **ISO 27001** | Information security | ISMS implementation |
| **NERC CIP** | Critical infrastructure | Access controls + auditing |

### Safety Standards

| Standard | Focus Area |
|:---|:---|
| **IEC 61511** | Process industry safety |
| **IEC 61508** | Functional safety |
| **ISA-84** | Safety instrumented systems |

## Security Checklist

### Pre-Deployment

- [ ] Network segmentation verified
- [ ] Data diode/firewall rules tested
- [ ] Authentication system configured
- [ ] RBAC roles defined and assigned
- [ ] Audit logging enabled
- [ ] Encryption configured (TLS 1.3)
- [ ] Backup and recovery tested
- [ ] Incident response plan documented
- [ ] Security training completed
- [ ] Penetration testing performed

### Operational

- [ ] Daily log review
- [ ] Weekly access review
- [ ] Monthly vulnerability scan
- [ ] Quarterly security audit
- [ ] Annual penetration test
- [ ] Regular backup verification
- [ ] Incident response drills

## Contact

For security concerns or to report vulnerabilities:

- **Email**: security@yourproject.org
- **PGP Key**: [Download public key]
- **Bug Bounty**: [Program details]

Please do not disclose security issues publicly until they have been addressed.

---

**Remember**: Security is everyone's responsibility. When in doubt, err on the side of caution.
