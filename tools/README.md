# Tools

Standalone utilities and servers for DevOps workflows.

## Contents

### iso-server.py

HTTPS file server for serving ISOs over the network. Useful for bare-metal provisioning workflows where nodes need to fetch ISOs from a secure endpoint.

**Features:**
- Auto-generates self-signed TLS certificate
- Configurable port (default: 6183)
- Directory listing for ISO browsing

**Usage:**
```bash
python3 iso-server.py /path/to/iso/directory
python3 iso-server.py /path/to/iso/directory --port 8443
python3 iso-server.py /path/to/iso/directory --cert my.crt --key my.key
```

**Requirements:**
- Python 3.6+
- `openssl` CLI (for auto-certificate generation)
