# Simple Performance Test for Clinical Case Platform
param(
    [int]$RequestCount = 50
)

Write-Host "==================================`n" -ForegroundColor Cyan
Write-Host "Performance Test - Clinical Case Platform`n" -ForegroundColor Cyan
Write-Host "==================================`n" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000"

# Test 1: Login Performance
Write-Host "Test 1: Login Performance ($RequestCount requests)`n" -ForegroundColor Yellow

$loginBody = @{
    email = "instructor@test.com"
    password = "testpass123"
} | ConvertTo-Json

$loginTimes = @()
$successCount = 0

for ($i = 1; $i -le $RequestCount; $i++) {
    try {
        $stopwatch = [Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-RestMethod -Uri "$baseUrl/api/auth/login/" `
            -Method POST `
            -Headers @{"Content-Type"="application/json"} `
            -Body $loginBody
        $stopwatch.Stop()
        
        if ($response.tokens.access) {
            $successCount++
            $loginTimes += $stopwatch.ElapsedMilliseconds
            $accessToken = $response.tokens.access
        }
        
        if ($i % 10 -eq 0) {
            Write-Host "  Progress: $i/$RequestCount..." -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "  Request $i failed" -ForegroundColor Red
    }
}

$avgLogin = [Math]::Round(($loginTimes | Measure-Object -Average).Average, 0)
$minLogin = ($loginTimes | Measure-Object -Minimum).Minimum
$maxLogin = ($loginTimes | Measure-Object -Maximum).Maximum

Write-Host "`nLogin Results:" -ForegroundColor Cyan
Write-Host "  Success Rate: $successCount/$RequestCount" -ForegroundColor Green
Write-Host "  Avg: $avgLogin ms | Min: $minLogin ms | Max: $maxLogin ms`n" -ForegroundColor White

# Test 2: List Cases Performance
Write-Host "Test 2: List Cases Performance ($RequestCount requests)`n" -ForegroundColor Yellow

$caseTimes = @()
$caseSuccess = 0

for ($i = 1; $i -le $RequestCount; $i++) {
    try {
        $stopwatch = [Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-RestMethod -Uri "$baseUrl/api/cases/" `
            -Method GET `
            -Headers @{"Authorization"="Bearer $accessToken"}
        $stopwatch.Stop()
        
        if ($response.count -ge 0) {
            $caseSuccess++
            $caseTimes += $stopwatch.ElapsedMilliseconds
        }
        
        if ($i % 10 -eq 0) {
            Write-Host "  Progress: $i/$RequestCount..." -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "  Request $i failed" -ForegroundColor Red
    }
}

$avgCase = [Math]::Round(($caseTimes | Measure-Object -Average).Average, 0)
$minCase = ($caseTimes | Measure-Object -Minimum).Minimum
$maxCase = ($caseTimes | Measure-Object -Maximum).Maximum

Write-Host "`nList Cases Results:" -ForegroundColor Cyan
Write-Host "  Success Rate: $caseSuccess/$RequestCount" -ForegroundColor Green
Write-Host "  Avg: $avgCase ms | Min: $minCase ms | Max: $maxCase ms`n" -ForegroundColor White

# Test 3: Search Performance  
Write-Host "Test 3: Search Performance (25 requests)`n" -ForegroundColor Yellow

$searchTimes = @()
$searchSuccess = 0
$searchCount = 25

for ($i = 1; $i -le $searchCount; $i++) {
    try {
        $stopwatch = [Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-RestMethod -Uri "$baseUrl/api/cases/?search=tim" `
            -Method GET `
            -Headers @{"Authorization"="Bearer $accessToken"}
        $stopwatch.Stop()
        
        if ($response.count -ge 0) {
            $searchSuccess++
            $searchTimes += $stopwatch.ElapsedMilliseconds
        }
        
        if ($i % 10 -eq 0) {
            Write-Host "  Progress: $i/$searchCount..." -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "  Request $i failed" -ForegroundColor Red
    }
}

$avgSearch = [Math]::Round(($searchTimes | Measure-Object -Average).Average, 0)
$minSearch = ($searchTimes | Measure-Object -Minimum).Minimum
$maxSearch = ($searchTimes | Measure-Object -Maximum).Maximum

Write-Host "`nSearch Results:" -ForegroundColor Cyan
Write-Host "  Success Rate: $searchSuccess/$searchCount" -ForegroundColor Green
Write-Host "  Avg: $avgSearch ms | Min: $minSearch ms | Max: $maxSearch ms`n" -ForegroundColor White

# Summary
Write-Host "==================================`n" -ForegroundColor Cyan
Write-Host "Performance Summary`n" -ForegroundColor Cyan
Write-Host "==================================`n" -ForegroundColor Cyan

$allTimes = $loginTimes + $caseTimes + $searchTimes
$totalRequests = $RequestCount + $RequestCount + $searchCount
$totalSuccess = $successCount + $caseSuccess + $searchSuccess
$overallAvg = [Math]::Round(($allTimes | Measure-Object -Average).Average, 0)

Write-Host "Total Requests: $totalRequests" -ForegroundColor White
Write-Host "Total Successful: $totalSuccess" -ForegroundColor Green
Write-Host "Overall Avg Response Time: $overallAvg ms`n" -ForegroundColor White

if ($overallAvg -lt 500) {
    Write-Host "Performance: EXCELLENT" -ForegroundColor Green
} elseif ($overallAvg -lt 1000) {
    Write-Host "Performance: GOOD" -ForegroundColor Yellow
} elseif ($overallAvg -lt 2000) {
    Write-Host "Performance: ACCEPTABLE" -ForegroundColor Yellow
} else {
    Write-Host "Performance: NEEDS IMPROVEMENT" -ForegroundColor Red
}

Write-Host "`nCompleted at $(Get-Date -Format 'HH:mm:ss')`n" -ForegroundColor Gray
