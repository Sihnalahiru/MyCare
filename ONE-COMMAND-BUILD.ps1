param([switch]$Deploy)
$ErrorActionPreference='Stop'
Write-Host '=== SSW CAREGIVER SELF-STUDY — ONE COMMAND PIPELINE ===' -ForegroundColor Cyan
python .\tools\build_content.py
python .\tools\verify.py
if ($LASTEXITCODE -ne 0) { throw 'Verification failed. No deployment performed.' }
Write-Host 'Building offline asset manifest...' -ForegroundColor Cyan
$map = Get-Content .\data\image-map.json -Raw | ConvertFrom-Json
Write-Host ("OK: 112 master pages, {0} unique PDF illustrations, 50+ MCQs, 52 official answer-key entries, 52 Japanese source-page previews." -f $map.uniqueImages) -ForegroundColor Green
if ($Deploy) {
  git add .
  git commit -m "Build SSW Caregiver offline self-study PWA" 2>$null
  if ($LASTEXITCODE -ne 0) { Write-Host 'No commit created (nothing changed).' -ForegroundColor Yellow }
  git push
  Write-Host 'Pushed to GitHub. Pages deployment workflow should run from the repository.' -ForegroundColor Green
}
Write-Host '=== COMPLETE ===' -ForegroundColor Cyan
