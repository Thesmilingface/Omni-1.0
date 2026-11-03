# Security and privacy

The service binds to loopback by default and has no remote authentication because it is not intended to listen on a network interface. Never change its bind address without adding authentication and threat-modeling. Provider requests send conversation text to the selected external provider. SQLite history is local and currently has no retention limit UI or encryption. Credentials are environment-backed and excluded from git; `.env` is not a production secret vault. Rotate credentials disclosed in conversation. No credentials were committed.

No VPN, Tor routing, secure deletion, or system-wide traffic control is provided.
