# Script para criar o repositório no GitHub
# Execute este script após criar um Personal Access Token (PAT) em:
# https://github.com/settings/tokens (com scopes: repo)

param(
    [Parameter(Mandatory = $true)]
    [string]$AccessToken,
    
    [string]$RepoName = "holocron-career-ai",
    [string]$Owner = "guinatural",
    [string]$Description = "Multi-tenant SaaS career management platform with AI agents",
    [switch]$Private = $false
)

$Headers = @{
    "Authorization" = "token $AccessToken"
    "Accept" = "application/vnd.github.v3+json"
}

$Body = @{
    name        = $RepoName
    description = $Description
    private     = $Private.IsPresent
}

Write-Host "Creating repository $Owner/$RepoName..."

try {
    $Response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $Headers -Body ($Body | ConvertTo-Json)
    
    Write-Host "Repository created successfully!"
    Write-Host "Repository URL: $($Response.html_url)"
    Write-Host "Clone URL: $($Response.clone_url)"
    
    # Add remote
    Write-Host "`nSetting up git remote..."
    git remote set-url origin $Response.clone_url
    Write-Host "Remote configured!"
    
} catch {
    Write-Error "Failed to create repository: $_"
    Write-Error "Response: $($_.Exception.Response | ConvertFrom-Json)"
}

Write-Host "`nNext steps:"
Write-Host "  git push -u origin main"