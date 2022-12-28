# AWS Encryption Scanner

Requires integration with authentication source to store temporary AWS auth token locally. Auth script not included here for privacy.
What it does

This script will run checks against AWS resources - S3, Redshift, RDS, etc. to confirm that default encryption at rest is enabled.

Input: None

Output: Text files listing resources and their encryption status.
