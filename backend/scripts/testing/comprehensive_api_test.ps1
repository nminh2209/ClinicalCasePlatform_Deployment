# Comprehensive API Test - Clinical Case Platform
# Tests all major endpoints with functional validation

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Comprehensive API Test Suite" -ForegroundColor Cyan
Write-Host "Clinical Case Platform Backend" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000"
$global:testResults = @()
$global:accessToken = $null
$global:testCaseId = $null
$global:commentId = $null

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Method,
        [string]$Url,
        [hashtable]$Headers = @{},
        [string]$Body = $null,
        [int]$ExpectedStatus = 200,
        [scriptblock]$Validation = $null
    )
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
            Headers = $Headers
            UseBasicParsing = $true
        }
        
        if ($Body) {
            $params['Body'] = $Body
            $params.Headers['Content-Type'] = 'application/json'
        }
        
        $stopwatch = [Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-RestMethod @params
        $stopwatch.Stop()
        
        $status = "PASS"
        $message = "OK"
        
        # Run custom validation if provided
        if ($Validation) {
            try {
                & $Validation $response
            } catch {
                $status = "FAIL"
                $message = $_.Exception.Message
            }
        }
        
        Write-Host "  [PASS] $Name" -ForegroundColor Green -NoNewline
        Write-Host " ($($stopwatch.ElapsedMilliseconds) ms)" -ForegroundColor Gray
        
        $global:testResults += @{
            Name = $Name
            Status = $status
            Time = $stopwatch.ElapsedMilliseconds
            Message = $message
        }
        
        return $response
    }
    catch {
        Write-Host "  [FAIL] $Name" -ForegroundColor Red -NoNewline
        Write-Host " - $($_.Exception.Message)" -ForegroundColor Gray
        
        $global:testResults += @{
            Name = $Name
            Status = "FAIL"
            Time = 0
            Message = $_.Exception.Message
        }
        
        return $null
    }
}

# Test Suite 1: Authentication
Write-Host "Test Suite 1: Authentication" -ForegroundColor Yellow
Write-Host "------------------------------" -ForegroundColor Gray

$loginBody = @{
    email = "instructor@test.com"
    password = "testpass123"
} | ConvertTo-Json

$loginResponse = Test-Endpoint `
    -Name "POST /api/auth/login/" `
    -Method POST `
    -Url "$baseUrl/api/auth/login/" `
    -Body $loginBody `
    -Validation {
        param($r)
        if (-not $r.tokens.access) { throw "No access token in response" }
        if (-not $r.user) { throw "No user data in response" }
        $global:accessToken = $r.tokens.access
    }

$authHeaders = @{ "Authorization" = "Bearer $global:accessToken" }

Test-Endpoint `
    -Name "GET /api/auth/profile/" `
    -Method GET `
    -Url "$baseUrl/api/auth/profile/" `
    -Headers $authHeaders `
    -Validation {
        param($r)
        if (-not $r.email) { throw "No email in profile" }
        if (-not $r.role) { throw "No role in profile" }
    }

$refreshBody = @{ refresh = $loginResponse.tokens.refresh } | ConvertTo-Json
Test-Endpoint `
    -Name "POST /api/auth/token/refresh/" `
    -Method POST `
    -Url "$baseUrl/api/auth/token/refresh/" `
    -Body $refreshBody `
    -Validation {
        param($r)
        if (-not $r.access) { throw "No new access token" }
    }

Write-Host ""

# Test Suite 2: Cases - Read Operations
Write-Host "Test Suite 2: Cases - Read Operations" -ForegroundColor Yellow
Write-Host "--------------------------------------" -ForegroundColor Gray

$casesResponse = Test-Endpoint `
    -Name "GET /api/cases/" `
    -Method GET `
    -Url "$baseUrl/api/cases/" `
    -Headers $authHeaders `
    -Validation {
        param($r)
        if (-not $r.results) { throw "No results in response" }
        if ($r.results.Count -gt 0) {
            $global:testCaseId = $r.results[0].id
        }
    }

if ($global:testCaseId) {
    Test-Endpoint `
        -Name "GET /api/cases/$global:testCaseId/" `
        -Method GET `
        -Url "$baseUrl/api/cases/$global:testCaseId/" `
        -Headers $authHeaders `
        -Validation {
            param($r)
            if (-not $r.id) { throw "No case ID" }
            if (-not $r.title) { throw "No case title" }
            if (-not $r.clinical_history) { throw "No clinical history" }
        }
}

Test-Endpoint `
    -Name "GET /api/cases/?search=test" `
    -Method GET `
    -Url "$baseUrl/api/cases/?search=test" `
    -Headers $authHeaders `
    -Validation {
        param($r)
        if (-not $r.results) { throw "No results" }
    }

Write-Host ""

# Test Suite 3: Cases - Write Operations
Write-Host "Test Suite 3: Cases - Write Operations" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray

$newCaseBody = @{
    title = "API Test Case - $(Get-Date -Format 'HHmmss')"
    patient_name = "Test Patient"
    patient_age = 45
    patient_gender = "male"
    chief_complaint_brief = "Test symptoms"
    specialty = "General Medicine"
    repository = 1
} | ConvertTo-Json

$newCase = Test-Endpoint `
    -Name "POST /api/cases/" `
    -Method POST `
    -Url "$baseUrl/api/cases/" `
    -Headers $authHeaders `
    -Body $newCaseBody `
    -ExpectedStatus 201 `
    -Validation {
        param($r)
        if (-not $r.title) { throw "Case not created" }
    }

if ($newCase -and $newCase.title) {
    $createdCaseId = $newCase.title -replace '[^0-9]', ''
    if (-not $createdCaseId) { 
        # Fallback: get the case ID from the list
        $latestCase = Invoke-RestMethod -Uri "$baseUrl/api/cases/" -Headers $authHeaders
        if ($latestCase.results -and $latestCase.results.Count -gt 0) {
            $global:testCaseId = $latestCase.results[0].id
        }
    }
    
    Start-Sleep -Milliseconds 500
    
    $updateBody = @{
        case_summary = "Updated via comprehensive API test"
    } | ConvertTo-Json
    
    if ($global:testCaseId) {
        Test-Endpoint `
            -Name "PATCH /api/cases/$global:testCaseId/" `
            -Method PATCH `
            -Url "$baseUrl/api/cases/$global:testCaseId/" `
            -Headers $authHeaders `
            -Body $updateBody `
            -Validation {
                param($r)
                if ($r.case_summary -notlike "*comprehensive*") { throw "Update failed" }
            }
        
        Test-Endpoint `
            -Name "POST /api/cases/$global:testCaseId/submit/" `
            -Method POST `
            -Url "$baseUrl/api/cases/$global:testCaseId/submit/" `
            -Headers $authHeaders
    }
}

Write-Host ""

# Test Suite 4: Comments
Write-Host "Test Suite 4: Comments" -ForegroundColor Yellow
Write-Host "----------------------" -ForegroundColor Gray

# Ensure we have a valid case ID
if (-not $global:testCaseId -and $casesResponse.results.Count -gt 0) {
    $global:testCaseId = $casesResponse.results[0].id
}

if ($global:testCaseId) {
    Test-Endpoint `
        -Name "GET /api/comments/?case=$global:testCaseId" `
        -Method GET `
        -Url "$baseUrl/api/comments/?case=$global:testCaseId" `
        -Headers $authHeaders `
        -Validation {
            param($r)
            if (-not $r.results) { throw "No results" }
        }
    
    $commentBody = @{
        case = $global:testCaseId
        content = "Test comment from API test - $(Get-Date -Format 'HHmmss')"
        comment_type = "general"
    } | ConvertTo-Json
    
    $newComment = Test-Endpoint `
        -Name "POST /api/comments/" `
        -Method POST `
        -Url "$baseUrl/api/comments/" `
        -Headers $authHeaders `
        -Body $commentBody `
        -ExpectedStatus 201 `
        -Validation {
            param($r)
            if (-not $r.id) { throw "Comment not created" }
            $global:commentId = $r.id
        }
    
    if ($global:commentId) {
        Test-Endpoint `
            -Name "GET /api/comments/$global:commentId/" `
            -Method GET `
            -Url "$baseUrl/api/comments/$global:commentId/" `
            -Headers $authHeaders `
            -Validation {
                param($r)
                if (-not $r.content) { throw "Comment not found" }
            }
    }
} else {
    Write-Host "  [SKIP] Comments tests - No case ID available" -ForegroundColor Yellow
}

Write-Host ""

# Test Suite 5: Notifications
Write-Host "Test Suite 5: Notifications" -ForegroundColor Yellow
Write-Host "---------------------------" -ForegroundColor Gray

Test-Endpoint `
    -Name "GET /api/notifications/" `
    -Method GET `
    -Url "$baseUrl/api/notifications/" `
    -Headers $authHeaders `
    -Validation {
        param($r)
        if (-not $r.results) { throw "No results" }
    }

Test-Endpoint `
    -Name "GET /api/notifications/unread-count/" `
    -Method GET `
    -Url "$baseUrl/api/notifications/unread-count/" `
    -Headers $authHeaders `
    -Validation {
        param($r)
        if ($null -eq $r.unread_count) { throw "No unread count" }
    }

Write-Host ""

# Test Suite 6: Feedback and Grades
Write-Host "Test Suite 6: Feedback and Grades" -ForegroundColor Yellow
Write-Host "-------------------------------" -ForegroundColor Gray

# Ensure we have a valid case ID
if (-not $global:testCaseId -and $casesResponse.results.Count -gt 0) {
    $global:testCaseId = $casesResponse.results[0].id
}

if ($global:testCaseId) {
    Test-Endpoint `
        -Name "GET /api/feedback/?case=$global:testCaseId" `
        -Method GET `
        -Url "$baseUrl/api/feedback/?case=$global:testCaseId" `
        -Headers $authHeaders `
        -Validation {
            param($r)
            if (-not $r.results) { throw "No results" }
        }
    
    Test-Endpoint `
        -Name "GET /api/grades/?case=$global:testCaseId" `
        -Method GET `
        -Url "$baseUrl/api/grades/?case=$global:testCaseId" `
        -Headers $authHeaders `
        -Validation {
            param($r)
            if (-not $r.results) { throw "No results" }
        }
} else {
    Write-Host "  [SKIP] Feedback & Grades tests - No case ID available" -ForegroundColor Yellow
}

Write-Host ""

# Test Suite 7: Inquiries
Write-Host "Test Suite 7: Inquiries" -ForegroundColor Yellow
Write-Host "-----------------------" -ForegroundColor Gray

Test-Endpoint `
    -Name "GET /api/inquiries/threads/" `
    -Method GET `
    -Url "$baseUrl/api/inquiries/threads/" `
    -Headers $authHeaders `
    -Validation {
        param($r)
        if ($null -eq $r.results) { throw "Missing results property" }
    }
# Ensure we have a valid case ID for inquiry creation
if (-not $global:testCaseId -and $casesResponse.results.Count -gt 0) {
    $global:testCaseId = $casesResponse.results[0].id
}

if ($global:testCaseId) {
    $inquiryBody = @{
        case = [int]$global:testCaseId
        question = "Test inquiry question - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    }
    
    Test-Endpoint `
        -Name "POST /api/inquiries/create/" `
        -Method POST `
        -Url "$baseUrl/api/inquiries/create/" `
        -Headers $authHeaders `
        -Body $inquiryBody `
        -Validation {
            param($r)
            if (-not $r.question) { throw "No question in response" }
        }
} else {
    Write-Host "  [SKIP] Inquiry creation test - No case ID available" -ForegroundColor Yellow
}
Write-Host ""

# Summary Report
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Results Summary" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$passCount = ($global:testResults | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($global:testResults | Where-Object { $_.Status -eq "FAIL" }).Count
$totalCount = $global:testResults.Count
$successRate = [Math]::Round(($passCount / $totalCount) * 100, 1)

Write-Host "Total Tests: $totalCount" -ForegroundColor White
Write-Host "Passed: $passCount" -ForegroundColor Green
Write-Host "Failed: $failCount" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Red" })
Write-Host "Success Rate: $successRate%`n" -ForegroundColor White

if ($failCount -gt 0) {
    Write-Host "Failed Tests:" -ForegroundColor Red
    $global:testResults | Where-Object { $_.Status -eq "FAIL" } | ForEach-Object {
        Write-Host "  - $($_.Name): $($_.Message)" -ForegroundColor Gray
    }
    Write-Host ""
}

$avgTime = [Math]::Round(($global:testResults.Time | Measure-Object -Average).Average, 0)
Write-Host "Average Response Time: $avgTime ms" -ForegroundColor White

if ($global:testCaseId) {
    Write-Host "`nTest Data Created:" -ForegroundColor Cyan
    Write-Host "  Case ID: $global:testCaseId" -ForegroundColor Gray
    if ($global:commentId) {
        Write-Host "  Comment ID: $global:commentId" -ForegroundColor Gray
    }
}

Write-Host "`nTest completed at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""
