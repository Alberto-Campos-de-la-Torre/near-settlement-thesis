# Public repository safeguards

Run `python tools/check_publication.py` before committing or publishing. CI runs the same check. The guard rejects media/subtitles/recording materials, local secrets/configuration, common credential formats, personal email addresses and private execution identifiers. It reports paths and rule names, never matched secret values.

Signing keys, API credentials, cloud authentication and video production assets belong outside Git. Use environment variables or local credential stores when optional acquisition/signing features are needed. The published reconstruction uses committed data without credentials. Never interpret synthetic test keys or public transaction signatures as actual wallet signing credentials.

The content scan is a bounded check, not a proof that unknown secret formats cannot exist. Public source/measurement metadata and public blockchain addresses are intentionally retained for reproducibility. See `PROVENANCE.md` for the snapshot's origin and redactions.
