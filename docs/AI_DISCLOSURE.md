# AI-assisted development disclosure

The project was developed with AI coding assistance, including **Claude Code** in the upstream implementation and **Codex** in the subsequent review and delivery work. These are development tools; human contributors retain responsibility and Git authorship.

| Scope | Assistance and provenance |
|---|---|
| Upstream research pipeline | The upstream README credits Claude Code for parts of the original implementation: Python analysis modules, SQL, notebook and static dashboard. The available record does not support a line-by-line attribution to a particular tool. |
| Review and hardening | Codex assisted with security and correctness fixes, receipt-status validation, statistical availability checks and regression tests across `near_thesis/` and `tests/`. |
| English reviewer interface | Codex assisted with English UI/documentation, local method pages, thesis/notebook navigation, shared themes and chart layout in `near_thesis/web/`, `documentation.py`, `reader.py` and related tests. |
| Dedicated repository and delivery | Codex assisted with private-identifier redaction, publication checks, reproducibility checks, repository documentation and deployment configuration. |

AI-assisted code is part of the checked-in source, not a separate proprietary dependency. No claim is made that the code was written entirely by humans. Locked libraries and versions are listed in `pyproject.toml` and `uv.lock`; upstream origin and the retained MIT license are documented in [PROVENANCE.md](PROVENANCE.md).

Generated numerical claims come from the committed data and pipeline. Passing tests does not remove the thesis's sampling, attribution or statistical limitations. No private keys, credentials or video production materials are required to reproduce the offline build.
