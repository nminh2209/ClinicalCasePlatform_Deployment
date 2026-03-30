# ========================================
# Stress Test - 100 Concurrent Users
# Clinical Case Platform Backend
# ========================================

param(
    [int]$UserCount = 100,
    [int]$DurationSeconds = 60,
    [string]$BaseUrl = "http://localhost:8000"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Stress Test - $UserCount Concurrent Users" -ForegroundColor Cyan
Write-Host "Duration: $DurationSeconds seconds" -ForegroundColor Cyan
Write-Host "Base URL: $BaseUrl" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Test credentials
$email = "instructor@test.com"
$password = "testpass123"

# User session script block
$userSessionScript = {
    param($UserId, $BaseUrl, $Email, $Password)
    
    $ErrorActionPreference = "SilentlyContinue"
    $results = @()
    
    try {
        # Random think time
        $thinkTime = Get-Random -Minimum 500 -Maximum 2000
        
        # 1. Login
        $loginStart = Get-Date
        $loginBody = @{
            email = $Email
            password = $Password
        } | ConvertTo-Json
        
        $loginResponse = Invoke-RestMethod `
            -Uri "$BaseUrl/api/auth/login/" `
            -Method POST `
            -Body $loginBody `
            -ContentType "application/json" `
            -TimeoutSec 30 `
            -ErrorAction Stop
        
        $loginTime = ((Get-Date) - $loginStart).TotalMilliseconds
        $results += @{Endpoint="Login"; Time=$loginTime; Success=$true}
        
        $token = $loginResponse.tokens.access
        $headers = @{
            "Authorization" = "Bearer $token"
            "Content-Type" = "application/json"
        }
        
        Start-Sleep -Milliseconds $thinkTime
        
        # 2. Get Profile
        $profileStart = Get-Date
        $profileResponse = Invoke-RestMethod `
            -Uri "$BaseUrl/api/auth/profile/" `
            -Method GET `
            -Headers $headers `
            -TimeoutSec 30 `
            -ErrorAction Stop
        $profileTime = ((Get-Date) - $profileStart).TotalMilliseconds
        $results += @{Endpoint="Profile"; Time=$profileTime; Success=$true}
        
        Start-Sleep -Milliseconds $thinkTime
        
        # 3. List Cases
        $page = Get-Random -Minimum 1 -Maximum 5
        $casesStart = Get-Date
        $casesResponse = Invoke-RestMethod `
            -Uri "$BaseUrl/api/cases/?page=$page" `
            -Method GET `
            -Headers $headers `
            -TimeoutSec 30 `
            -ErrorAction Stop
        $casesTime = ((Get-Date) - $casesStart).TotalMilliseconds
        $results += @{Endpoint="List Cases"; Time=$casesTime; Success=$true}
        
        Start-Sleep -Milliseconds $thinkTime
        
        # 4. Get Case Detail
        if ($casesResponse.results.Count -gt 0) {
            $randomCase = $casesResponse.results | Get-Random
            $caseDetailStart = Get-Date
            $caseDetail = Invoke-RestMethod `
                -Uri "$BaseUrl/api/cases/$($randomCase.id)/" `
                -Method GET `
                -Headers $headers `
                -TimeoutSec 30 `
                -ErrorAction Stop
            $caseDetailTime = ((Get-Date) - $caseDetailStart).TotalMilliseconds
            $results += @{Endpoint="Case Detail"; Time=$caseDetailTime; Success=$true}
            
            Start-Sleep -Milliseconds $thinkTime
            
            # 5. Get Comments
            $commentsStart = Get-Date
            $comments = Invoke-RestMethod `
                -Uri "$BaseUrl/api/comments/?case=$($randomCase.id)" `
                -Method GET `
                -Headers $headers `
                -TimeoutSec 30 `
                -ErrorAction Stop
            $commentsTime = ((Get-Date) - $commentsStart).TotalMilliseconds
            $results += @{Endpoint="Comments"; Time=$commentsTime; Success=$true}
        }
        
        Start-Sleep -Milliseconds $thinkTime
        
        # 6. Search Cases
        $searchTerms = @("test", "patient", "cardiac", "diabetes", "acute", "chronic")
        $searchTerm = $searchTerms | Get-Random
        $searchStart = Get-Date
        $searchResponse = Invoke-RestMethod `
            -Uri "$BaseUrl/api/cases/?search=$searchTerm" `
            -Method GET `
            -Headers $headers `
            -TimeoutSec 30 `
            -ErrorAction Stop
        $searchTime = ((Get-Date) - $searchStart).TotalMilliseconds
        $results += @{Endpoint="Search"; Time=$searchTime; Success=$true}
        
        Start-Sleep -Milliseconds $thinkTime
        
        # 7. Get Notifications
        $notificationsStart = Get-Date
        $notifications = Invoke-RestMethod `
            -Uri "$BaseUrl/api/notifications/" `
            -Method GET `
            -Headers $headers `
            -TimeoutSec 30 `
            -ErrorAction Stop
        $notificationsTime = ((Get-Date) - $notificationsStart).TotalMilliseconds
        $results += @{Endpoint="Notifications"; Time=$notificationsTime; Success=$true}
        
        # 8. Occasionally create a case (10% chance)
        if ((Get-Random -Minimum 1 -Maximum 100) -le 10) {
            Start-Sleep -Milliseconds $thinkTime
            $caseBody = @{
                title = "Stress Test Case - User $UserId - $(Get-Date -Format 'HHmmss')"
                repository = 1
                patient_name = "Test Patient $UserId"
                patient_age = Get-Random -Minimum 20 -Maximum 80
                patient_gender = @("male", "female") | Get-Random
                chief_complaint_brief = "Test symptoms from stress test"
                specialty = "General Medicine"
            } | ConvertTo-Json
            
            $createStart = Get-Date
            $newCase = Invoke-RestMethod `
                -Uri "$BaseUrl/api/cases/" `
                -Method POST `
                -Headers $headers `
                -Body $caseBody `
                -TimeoutSec 30 `
                -ErrorAction Stop
            $createTime = ((Get-Date) - $createStart).TotalMilliseconds
            $results += @{Endpoint="Create Case"; Time=$createTime; Success=$true}
        }
        
    } catch {
        $endpoint = "Request"
        if ($_.Exception.Message -match "login") { $endpoint = "Login" }
        elseif ($_.Exception.Message -match "profile") { $endpoint = "Profile" }
        elseif ($_.Exception.Message -match "cases") { $endpoint = "Cases" }
        
        $results += @{Endpoint=$endpoint; Time=0; Success=$false; Error=$_.Exception.Message}
    }
    
    return $results
}

Write-Host "Starting stress test..." -ForegroundColor Yellow
Write-Host "Launching $UserCount concurrent user sessions...`n" -ForegroundColor Gray

$startTime = Get-Date
$jobs = @()

# Launch user sessions with staggered start
for ($i = 1; $i -le $UserCount; $i++) {
    $job = Start-Job -ScriptBlock $userSessionScript -ArgumentList $i, $BaseUrl, $email, $password
    $jobs += $job
    
    # Stagger starts to simulate realistic ramp-up
    $delay = ($DurationSeconds * 1000) / $UserCount
    if ($delay -gt 100) {
        Start-Sleep -Milliseconds $delay
    }
    
    if ($i % 10 -eq 0) {
        Write-Host "  Launched $i/$UserCount users..." -ForegroundColor Gray
    }
}

Write-Host "`nWaiting for user sessions to complete (max $DurationSeconds seconds)...`n" -ForegroundColor Yellow

# Monitor progress
$timeout = $startTime.AddSeconds($DurationSeconds + 30)
$lastUpdate = Get-Date
while ((Get-Job -State Running).Count -gt 0 -and (Get-Date) -lt $timeout) {
    $completed = ($jobs | Where-Object { $_.State -eq 'Completed' }).Count
    $running = ($jobs | Where-Object { $_.State -eq 'Running' }).Count
    $failed = ($jobs | Where-Object { $_.State -eq 'Failed' }).Count
    
    if (((Get-Date) - $lastUpdate).TotalSeconds -ge 2) {
        Write-Host "`r  Progress: Completed: $completed | Running: $running | Failed: $failed" -NoNewline
        $lastUpdate = Get-Date
    }
    
    Start-Sleep -Milliseconds 500
}

Write-Host "`n`nCollecting results..." -ForegroundColor Yellow

# Force stop any remaining jobs
Get-Job -State Running | Stop-Job -PassThru | Out-Null

# Collect all results
$allResults = @()
foreach ($job in $jobs) {
    $jobResults = Receive-Job -Job $job -ErrorAction SilentlyContinue
    if ($jobResults) {
        $allResults += $jobResults
    }
}

# Cleanup jobs
$jobs | Remove-Job -Force

$duration = (Get-Date) - $startTime

# Process results
$totalRequests = $allResults.Count
$successfulRequests = ($allResults | Where-Object { $_.Success }).Count
$failedRequests = $totalRequests - $successfulRequests
$responseTimes = ($allResults | Where-Object { $_.Success }).Time

$endpointStats = @{}
foreach ($result in $allResults) {
    if (-not $endpointStats.ContainsKey($result.Endpoint)) {
        $endpointStats[$result.Endpoint] = @{
            Total = 0
            Success = 0
            Failed = 0
            Times = @()
        }
    }
    $endpointStats[$result.Endpoint].Total++
    if ($result.Success) {
        $endpointStats[$result.Endpoint].Success++
        $endpointStats[$result.Endpoint].Times += $result.Time
    } else {
        $endpointStats[$result.Endpoint].Failed++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Stress Test Results" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Test Configuration:" -ForegroundColor Yellow
Write-Host "  Target Users: $UserCount"
Write-Host "  Duration: $DurationSeconds seconds"
Write-Host "  Actual Runtime: $([math]::Round($duration.TotalSeconds, 2)) seconds"
Write-Host ""

Write-Host "Request Statistics:" -ForegroundColor Yellow
Write-Host "  Total Requests: $totalRequests"
Write-Host "  Successful: $successfulRequests" -ForegroundColor Green
Write-Host "  Failed: $failedRequests" -ForegroundColor $(if($failedRequests -gt 0){"Red"}else{"Gray"})
$successRate = if ($totalRequests -gt 0) { [math]::Round(($successfulRequests / $totalRequests) * 100, 2) } else { 0 }
Write-Host "  Success Rate: $successRate%"
$reqPerSec = if ($duration.TotalSeconds -gt 0) { [math]::Round($totalRequests / $duration.TotalSeconds, 2) } else { 0 }
Write-Host "  Throughput: $reqPerSec requests/sec"
Write-Host ""

if ($responseTimes.Count -gt 0) {
    $sortedTimes = $responseTimes | Sort-Object
    $avgTime = [math]::Round(($responseTimes | Measure-Object -Average).Average, 0)
    $minTime = [math]::Round(($responseTimes | Measure-Object -Minimum).Minimum, 0)
    $maxTime = [math]::Round(($responseTimes | Measure-Object -Maximum).Maximum, 0)
    
    $p50Index = [math]::Floor($sortedTimes.Count * 0.50)
    $p90Index = [math]::Floor($sortedTimes.Count * 0.90)
    $p95Index = [math]::Floor($sortedTimes.Count * 0.95)
    $p99Index = [math]::Floor($sortedTimes.Count * 0.99)
    
    $p50 = [math]::Round($sortedTimes[$p50Index], 0)
    $p90 = [math]::Round($sortedTimes[$p90Index], 0)
    $p95 = [math]::Round($sortedTimes[$p95Index], 0)
    $p99 = [math]::Round($sortedTimes[$p99Index], 0)
    
    Write-Host "Response Time Statistics (ms):" -ForegroundColor Yellow
    Write-Host "  Average: $avgTime ms"
    Write-Host "  Minimum: $minTime ms"
    Write-Host "  Maximum: $maxTime ms"
    Write-Host "  Median (P50): $p50 ms"
    Write-Host "  P90: $p90 ms"
    Write-Host "  P95: $p95 ms"
    Write-Host "  P99: $p99 ms"
    Write-Host ""
}

Write-Host "Breakdown by Endpoint:" -ForegroundColor Yellow
$endpointStats.GetEnumerator() | Sort-Object Key | ForEach-Object {
    $endpoint = $_.Key
    $stats = $_.Value
    $avgTime = if ($stats.Times.Count -gt 0) { [math]::Round(($stats.Times | Measure-Object -Average).Average, 0) } else { 0 }
    $successPct = if ($stats.Total -gt 0) { [math]::Round(($stats.Success / $stats.Total) * 100, 1) } else { 0 }
    
    Write-Host "  $endpoint"
    Write-Host "    Requests: $($stats.Total) | Success: $($stats.Success) | Failed: $($stats.Failed) | Success Rate: $successPct% | Avg RT: $avgTime ms"
}
Write-Host ""

Write-Host "Performance Evaluation:" -ForegroundColor Yellow
if ($successRate -ge 95 -and $avgTime -lt 5000 -and $reqPerSec -gt 10) {
    Write-Host "  Status: EXCELLENT" -ForegroundColor Green
    Write-Host "  The system handles concurrent load very well with high success rate and good response times."
} elseif ($successRate -ge 90 -and $avgTime -lt 10000 -and $reqPerSec -gt 5) {
    Write-Host "  Status: GOOD" -ForegroundColor Green
    Write-Host "  The system performs adequately under concurrent load with acceptable response times."
} elseif ($successRate -ge 80 -and $avgTime -lt 15000) {
    Write-Host "  Status: FAIR" -ForegroundColor Yellow
    Write-Host "  The system shows signs of stress under concurrent load. Consider optimization or scaling."
} else {
    Write-Host "  Status: POOR" -ForegroundColor Red
    Write-Host "  The system struggles under concurrent load. Performance optimization or infrastructure scaling needed."
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Stress test completed at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
