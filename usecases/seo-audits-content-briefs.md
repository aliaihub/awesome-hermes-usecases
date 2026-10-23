# SEO Audits, Structured Data, and Content Briefs

<!-- catalog-summary:start -->
[← Browse use cases](../README.md#content--marketing) · **Content & Marketing**

| At a glance | Details |
| --- | --- |
| **Outcome** | Technical audits, structured-data checks, local-search analysis, and content briefs. |
| **Requires** | hermes-seo and its managed runtime; browser dependencies; optional provider credentials. |
| **Available** | Plugin |
| **Validation** | Sources linked below; workflow not run during this catalog redesign. |
<!-- catalog-summary:end -->

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** Public plugin + runbook; not executed for this catalog update

## Pain Point

A website owner needs evidence-backed priorities for crawlability, on-page content, and structured data rather than a generic SEO checklist.

## What It Does

`yuzushi-dev/hermes-seo` ports Claude SEO workflows into a native Hermes plugin. Its router selects specialist skills for site audits, technical checks, page reviews, content briefs, local search, and Schema.org JSON-LD. Bundled scripts handle specific checks; optional provider integrations require separate configuration.

## Setup

The plugin declares Hermes 0.22.2+, Python 3.10+ with `venv`, and Linux or macOS. The upstream README provides this release-pinned installation:

```bash
hermes plugins install https://github.com/yuzushi-dev/hermes-seo.git --ref 5f04951e8fddc8b869378236a7ff5b584a0d023d --yes-deps --enable
hermes plugins doctor hermes-seo --ci
```

That SHA is the README's v0.1.0 release pin, not a claim that v0.1.0 is the newest source version. Check upstream release notes before choosing a different revision.

Run `hermes seo setup` to provision the managed runtime when needed. It downloads dependencies and can download Chromium. Start a new Hermes session and use `skills_list` to inspect the installed namespaced skills.

## Prompts

Published upstream example, using its placeholder target:

```text
Run hermes-seo:seo-audit on https://example.com and give me the highest-priority findings with evidence.
```

Replace the target with the website you intend to inspect. Other published workflows include `hermes-seo:seo-schema`, `hermes-seo:seo-content-brief`, and `hermes-seo:seo-technical`.

## Skills Needed

- `hermes-seo` plugin and managed Python runtime
- Its SEO router and focused audit/content skills
- Browser dependencies for checks that require rendering
- Optional service credentials for provider-backed checks

## Notes

- Google Search Console, GA4, Google Ads, and Indexing API OAuth flows are disabled in the documented port. Do not present it as a connected Google reporting pipeline.
- Some demos and growth figures in the README belong to the original Claude SEO project; they do not establish Hermes deployment results.
- Paid integrations stay inactive until configured. The runtime tool itself does not enforce every approval instruction carried by the skills.
- This adds website-analysis workflows beyond the catalog's email marketing and social-research entries.

## Sources

- Plugin, installation pin, examples, and limitations: <https://github.com/yuzushi-dev/hermes-seo>
- Official Hermes community listing: <https://hermes-agent.nousresearch.com/docs/plugins/hermes-seo>
