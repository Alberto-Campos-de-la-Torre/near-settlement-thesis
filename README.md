# From clicks to settlement: a reproducible investment thesis on NEAR

This is a reproducible investment thesis on NEAR, built for NEAR Hackathon 2026, track **Investment Thesis** (`thesis`). It tests whether falling account counts hide a shift toward cross-chain settlement. Run `make build` to rebuild the evidence and explore the dashboard: [Try it in two minutes](#reproduce-do-x-see-y).

**Question:** do falling account counts obscure a shift toward cross-chain settlement, and does the evidence support a token investment case? The project compares activity, behavioral proxies, Intents flows, net captured fees and forward associations. It reports failed cross-checks and inconclusive statistical tests. Settlement growth alone does not establish undervaluation.


The local build bundles English HTML editions of the thesis and methods. Dashboard method links open these local pages, including from `file://`. Use the [final human review checklist](docs/FINAL_REVIEW_CHECKLIST.md) before approving the demo.

## What is implemented

| Layer | Behavior | Code |
|---|---|---|
| L0 | Hashed public snapshots, including gross Intents fees, net captured receipts and buyback-labelled revenue | `near_thesis/fetch.py`, `data/raw/` |
| L1 | Retrospective HDBSCAN; separate frozen past-only GMM for predictive QAA, with next-month availability | `near_thesis/qaa.py` |
| L2 | Successful-receipt token-diff parser, exact asset identifiers, zero-event days and heuristic roles; historical events revalidated against 1,189 FastNear blocks; failed receipts excluded | `near_thesis/intents.py`, `data/blocks/` |
| L2 reconciliation | Written economic unit, per-day table against the DefiLlama/Dune reference, gap decomposition (coverage, valuation, routes, residual), pre-declared tolerance and holdout, receipt-level trace examples, intraday bias from hourly windows on pre-declared days | `near_thesis/reconcile.py`, `docs/RECONCILIATION.md` |
| L3 | Breaks, correlations, stationarity-gated VAR, stability/residual checks, explicit Johansen ranks | `near_thesis/econ.py` |
| L4 | Forward associations with block-bootstrap and familywise intervals; retrospective, temporally separated out-of-sample test with frozen sign, purge, familywise criterion, walk-forward hit rate, naive benchmark predictors and a persisted prospective plan (`make oos-freeze` writes `data/prospective/oos_freeze.json` once; builds load it and never recompute it); descriptive peer panel; capture-based scenarios | `near_thesis/signal.py` |
| Value bridge | Volume → gross fees → net captured revenue → buyback-labelled revenue → NEAR withdrawn from Intents into the buyback multisig (observed; purchase attribution inferred, pre-declared receipt trace) → ledger at the cutoff; issuance from total supply; adverse/base/favorable scenarios with the dominant assumption | `near_thesis/bridge.py`, `data/raw/nearblocks_buybacks_*.json` |
| Output | Generated thesis; static dashboard with a computed verdict, a five-step argument beside a pinned chart, evidence tags (observed, estimate, assumption, inconclusive) on every main claim, method links, a sensitivity block, separate data-cutoff, acquisition and generation dates, a sticky section index and an explicit evidence-against block (no dependencies, opens from `file://`); executed notebook, complete input hashes, regression tests | `THESIS.md`, `near_thesis/narrative.py`, `near_thesis/web/`, `tests/` |

QAA groups are named after observed behavior (`light_general`, `miniapp_pattern`, ...), not verified human identities; a name-only split tracks the share closely in the sparse sampled windows, and the thesis says so. The Intents sample is not a validated total or guaranteed lower bound. Buyback-labelled receipts are not proof of burning or holder dividends. The generated argument names the current consistency-test result or why it is unavailable, plus remaining limitations. The historical L2 extract was revalidated against FastNear on 2026-11-05: 53 failed-receipt logs were removed and 7,227 events retain explicit successful statuses. See [provenance](docs/PROVENANCE.md) for scope and evidence. Legacy extracts without execution status remain disabled by the pipeline.

## Reproduce: do X, see Y

Requirements: [uv](https://docs.astral.sh/uv/); Python 3.12 is configured by CI. No Google account or wallet keys are needed.

1. `uv sync --locked --all-extras` → installs the locked dependencies.
2. `make build` → rebuilds tables, models, chart data, `THESIS.md`, `site/index.html`, `site/walkthrough.html` and the local index from committed inputs. It uses no external HTTP requests. Jupyter opens localhost ports for its kernel, so environments must permit that. The build reuses matching fitted descriptive assignments and the serialized past-only model. `QAA_REFIT=1 make models` explicitly retrains them.
3. `make test` → runs metric, causal-availability, pricing, solver-mode, freshness, index-verification and regression tests.
4. `make check-generated` → exits successfully with no analytical changes against the committed artifacts. Run this after a build; a changed raw snapshot requires regenerating and committing its outputs.
5. `make serve` → open http://localhost:8080. Each chart provides its source/query, a table view and a short explanation. Theme and date-range controls are available.
6. Open http://localhost:8080/walkthrough.html → see the executed model walkthrough, diagnostics and revenue definitions.

Generated text and source hashes are compared exactly. Numerical arrays allow only `rtol=1e-9`, `atol=1e-11` for machine precision; stale market caps and changed methods still fail the check.

Optional browser checks: `uv run --with playwright python -m playwright install chromium`, then `uv run --with playwright python tests/browser_dashboard.py`. These exercise HTTP and local-file rendering, all six KPIs, verdict conditions, evidence tags against the computed spec, method links, the sensitivity block, the date line, keyboard navigation and focus, filters, themes, sources, tables, mobile layout and hostile/degenerate inputs. The script prints the temporary directory containing screenshots and JSON results.

Build time varies by machine; price tables are loaded once and bootstrap correlations are batched. Retraining clustering costs more than a normal cached build. Snapshot acquisition is separate from build time.

## Refreshing data and optional integrations

`make fetch` refreshes public APIs (`uv run near-thesis fetch --only buybacks` refreshes only the buyback multisig receipts from NearBlocks, slowly, within the key-less rate limit). `make blocks BLOCKS=100` tops up the cached FastNear block plan; acquiring thousands of public blocks can take hours under rate limits. `make blocks-intraday` fetches 24 hourly windows for the three motivating reconciliation days and `make blocks-intraday-validation` the three validation days chosen by position (several hours each); `make blocks-buyback-trace` reads the execution blocks of a pre-declared sample of buyback-wallet receipts (minutes). `make qaa-refits` refits the QAA clustering under other hyper-parameters into a committed sensitivity artifact (seconds, offline, platform-dependent). `make bq` runs the BigQuery extracts in `sql/` (complete sample days valued in SQL, full-month signer aggregates, buyback withdrawal attribution; each dry-run first, results committed in `data/bigquery/`); see `docs/SETUP_BIGQUERY.md`. Rebuild afterward. Snapshot acquisition timestamps and complete SHA-256 hashes are generated into `docs/REPRODUCIBILITY.md`; acquisition is always separate from the offline rebuild.

`make verify-events` revalidates all event-bearing blocks against FastNear, resumes from status-aware block caches and replaces the extract only after full verification. The historical revalidation checked all 1,189 blocks from the original event extract; respect the public rate limit and allow substantial time. `uv run near-thesis verify-events --offline` only uses already verified caches. Rebuild after verification. New samples preserve explicit successful receipt status.

The suggested track deliverable, a swap-volume pull from the **Intents Explorer API, is not implemented**: the team has no partner JWT for Explorer. DefiLlama/Dune serves as the substitute reference for the FastNear on-chain sample cross-check; it is not an Explorer API result. Setting `INTENTS_EXPLORER_JWT` alone does not enable this integration. An explicit `uv run near-thesis fetch --only intents` fails clearly; the default public-source fetch skips it. This gap is also recorded in [THESIS.md](THESIS.md#gaps-provenance-and-reproduction).

`make bq` is optional. It checks dataset freshness **before** L1/L2, estimates query size, sets a server-side byte ceiling and limits each run. See `docs/SETUP_BIGQUERY.md`; actual Google query/schema execution is not claimed for the block-sample build. Q0–Q3 auxiliary extracts are available for manual cross-checks; QAA and Intents consume L1/L2 extracts when present.

`make onchain` prints a dry-run NEAR Social payload. `make onchain SEND=1` signs only with an explicitly configured account/key. Empty `SEND` and `SEND=0` are dry runs; other values are rejected. `uv run near-thesis onchain --account team.testnet --network testnet` explicitly overrides the environment for a dry run; add `--send` only when you intend to sign on that selected network. `make onchain-verify` compares all local index fields against the published record, including hashes. The index is **not claimed published** without a transaction reference. Keys belong only in `.env`, which is ignored.

## NEAR's concrete role

NEAR is both the subject and the evidence layer: FastNear supplies NEAR blocks and receipts, and `intents.near` logs expose settlement activity. NearBlocks supplies daily activity; DefiLlama/Dune supplies reported settlement and revenue-wallet series. NEAR Social publication is an optional stretch. BigQuery, Explorer JWT and a deployed contract are not mandatory integrations for this track.

## Submission

This repository provides the reproducible Investment Thesis deliverable. Submission forms, the English presentation video and any required social post are handled separately by the team.


## Disclosure and license

Libraries and locked versions are listed in `pyproject.toml` and `uv.lock`. Development and review used automated coding assistance. This project continues the upstream research described in [provenance](docs/PROVENANCE.md), retaining its original MIT attribution. Statistical and sampling limits are part of the deliverable. See `LICENSE`.

## Security fixes and validation

CI checks the public release policy, rebuilds committed scientific inputs and runs regression tests with read-only repository permissions. No hosted deployment is claimed. See [security](docs/SECURITY.md).

## Dedicated public repository

This is the same thesis project continued in a dedicated repository with a single `main` branch. See [provenance](docs/PROVENANCE.md) for the upstream baseline, original development dates and retained MIT attribution. This public snapshot does not conceal pre-existing work or represent a second submission.

```bash
git clone https://github.com/Alberto-Campos-de-la-Torre/near-settlement-thesis.git
cd near-settlement-thesis
uv sync --locked --all-extras --python 3.12
make build
make test
make check-generated
uv run python -m http.server 8000 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:8000/. The site is rebuilt locally; no hosted deployment is claimed. No wallet, Google account or API keys are needed for this reconstruction. First dependency installation needs internet; Jupyter needs localhost ports.

Public release policy: video, audio, subtitles, storyboards/narration, recording/export scripts and private credentials are not included. Run `python tools/check_publication.py` before release. Only scientific source/data, product code and tests belong here.
