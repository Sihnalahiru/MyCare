# SSW Caregiver Master Self-Study PWA

This build is the **Premium final app package** for the offline SSW Caregiver study PWA. The large source PDFs are intentionally delivered separately so the app ZIP stays Windows-download safe.

## What was fixed
- Reorganized study view into compact topic blocks.
- Illustration-only pseudo-pages are not shown as giant empty study cards; their source illustrations are attached to nearby study content.
- Repaired common Sinhala PDF text-extraction artifacts in the app data.
- Added topic chips and clearer English/Sinhala/Japanese presentation.
- Added responsive mobile-first layout and drawer navigation.
- Added robust voice queue/chunking so long text does not stop after the first sentence.
- Added separate English, Sinhala and Japanese voice buttons.
- Voice selection searches installed device voices for the requested language and never silently substitutes an English voice for Sinhala/Japanese.
- Added Japanese Care section with all 52 official answer-key entries and 52 official source-question page previews.
- Expanded dashboard with study statistics, curriculum, daily plan, supplied exam-note focus map and high-yield urine numbers.
- Offline cache now includes study JSON, Japanese question previews and all 314 source illustrations.
- Added stronger automated verification.

## Verification
Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\ONE-COMMAND-BUILD.ps1
```

The included verifier should report **37/37 checks passed** on this package.

## Local test

```powershell
python -m http.server 8080
```

Open:

`http://localhost:8080`

Keep the terminal open while testing.

## GitHub deployment

After local testing:

```powershell
powershell -ExecutionPolicy Bypass -File .\ONE-COMMAND-BUILD.ps1 -Deploy
```

The workflow in `.github/workflows/pages.yml` is included for GitHub Pages deployment.

## Voice note
The PWA voice feature uses the browser/device Speech Synthesis engine so it can work without sending study text to a cloud API. Actual offline Sinhala/Japanese voice availability depends on whether the device/browser has a corresponding installed voice.


## Final package note
The app package intentionally does not contain `assets/official-source.pdf` or `assets/source-book.pdf`. Those original PDFs are preserved separately; the PWA itself contains the extracted study data, all 314 source illustrations, and all 52 Japanese question-page previews required by the UI.
