# Secret Scanning

**Currently building this tool out into a complete local SAST scanner.  No longer maintaining this version.**

Simple script to clone repos, scan for secrets with gitleaks, and store results to outfile files. Requires local installation of the Python version of Gitleaks, although it can be easily retrofitted for other versions, as well as other scanners - like TruffleHog.

Ideal for integrating into automated processes to kick off secret scans on events.
