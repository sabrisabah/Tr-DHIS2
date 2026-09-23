# DHIS2 Training Agenda and Kobo Assessment

This static GitHub Pages project contains:

- `index.html`: public DHIS2 training agenda.
- `assessment.html`: embedded Kobo assessment and aggregated results.
- `analytics.json`: generated summary used by the assessment page.
- `.github/scripts/update_kobo_analytics.py`: reads Kobo submissions and calculates results.
- `.github/workflows/update-kobo-analytics.yml`: updates results every five minutes and deploys GitHub Pages.

## Required GitHub configuration

1. Create a repository Actions secret named `KOBO_TOKEN` containing the Kobo API token.
2. In **Settings → Actions → General**, select **Read and write permissions**.
3. In **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.
4. Open **Actions → Update Kobo Analytics and Deploy Pages** and run the workflow once.

The dashboard publishes aggregated scores only. Participant names and personal information are not written to `analytics.json`.
