# ============================================
# Run Tabular Editor scripts sequentially 
# ============================================

$tabularEditorPath = "C:\Program Files (x86)\Tabular Editor\TabularEditor.exe"
if (-not (Test-Path $tabularEditorPath)) {
    Write-Host "Error: The path to TabularEditor.exe is incorrect or the file does not exist." -ForegroundColor Red
    Write-Host "Expected path: $tabularEditorPath"
    pause
    exit 1
}
$modelPath = ".\src\workspace-serve\gamma\SemanticModel\GamMa - Reporting.SemanticModel\definition\database.tmdl"
if (-not (Test-Path $modelPath)) {
    Write-Host "Error: The model path (.tmdl) does not exist or is invalid." -ForegroundColor Red
    Write-Host "Expected path: $modelPath"
    pause
    exit 1
}
$scriptsBase = ".\src\workspace-serve\gamma\Tabular"
$scripts = @(
    # MEASURES
    "$scriptsBase\Measures\KPI\KPI_MEASURES.csx"
)
foreach ($script in $scripts) {
    Write-Host "Running script: $script" -ForegroundColor Cyan
    if (-not (Test-Path $script)) {
        Write-Host "Error executing: $script (file not found)" -ForegroundColor Red
        continue
    }
    $arguments = "`"$modelPath`" -S `"$script`" -D"
    $output = (& $tabularEditorPath $modelPath -S $script -D 2>&1 | Out-String).Trim()
    Write-Host $output
    if ($output -match 'Model metadata saved') {
        Write-Host "Completed: $script" -ForegroundColor Green
    } else {
        Write-Host "Error executing: $script" -ForegroundColor Red
        pause
    }
}
Write-Host "All scripts executed!" -ForegroundColor Green