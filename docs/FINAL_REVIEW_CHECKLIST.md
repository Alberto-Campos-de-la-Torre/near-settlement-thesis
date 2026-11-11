# Final human review of the English demo

Use the locally running build at http://127.0.0.1:8765/. This is a local preview, not a new public deployment. Keep its server terminal running. Open the same URL in a private window to avoid persisted theme settings.

1. **Language and first impression.** Read the opening question, verdict, all three evidence checks and six KPIs. They must be English, coherent and readable. The original sampled-volume check remains failing; complete-day validation is a separate result, not a hidden replacement.
2. **Narrative and navigation.** Follow all five argument steps and the sticky section index. Scrolling should update the active step and pinned chart; nothing should overlap or jump unexpectedly.
3. **Dates and themes.** Try All, Since 2023, Since 2024, Since Intents and Last 12 months. Toggle Auto, Light and Dark, then reload to check persistence. Distinguish analysis cutoff, acquisition dates and page-generation time.
4. **Charts and evidence.** Hover a chart for its tooltip, open Table and Source and query, and inspect units, dates, negative values and missing-data explanations. Follow a method link: the English document should open locally. Use Back to dashboard to return. Open THESIS.md and Executed notebook from the side panel.
5. **Scientific qualifications.** Read Evidence against and How much the headlines move. QAA is behavioral and its sampled share is not a population count. Buyback traces distinguish observed events, approximate reconciliation and inferred fund allocation. Results do not imply proven returns or holder distributions.
6. **Mobile, keyboard and readability.** Resize to approximately 375px and 768px. Check no horizontal overflow, overlapping labels or clipped controls. Tab through navigation/buttons; activate with Enter/Space. Confirm visible focus and readable light/dark contrast. SVG charts still deserve a human readability check despite automated coverage.
7. **Reproduction.** If you want the final technical sign-off, run the four commands below, then reload the demo. Compare key numbers with the dashboard tables rather than a rounded headline alone.

```bash
uv sync --locked --all-extras
make build
make test
make check-generated
```

Until this translation and its intentionally updated link specification are committed, comparison with the old HEAD can report those expected changes. The localization evidence separately records reproducibility against the corrected snapshot; after committing, the Git-based check should pass against the new HEAD.

Record your final verdict, browser/device and any exact text or screenshot that failed. This human check approves the local product; it does not submit the hackathon application or publish the demo/X post. Those remain separate actions.
