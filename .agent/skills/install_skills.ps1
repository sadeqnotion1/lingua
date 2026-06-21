# install_skills.ps1 - Powershell script to clone and install custom skills for Antigravity

$ErrorActionPreference = "Stop"

# Define target skills and their source repositories
$skills = @(
    # Backend Skills
    @{ Name = "supabase-postgres-best-practices"; Repo = "https://github.com/supabase/agent-skills.git" },
    @{ Name = "tdd"; Repo = "https://github.com/mattpocock/skills.git" },
    @{ Name = "systematic-debugging"; Repo = "https://github.com/obra/superpowers.git" },

    # Frontend Skills
    @{ Name = "frontend-design"; Repo = "https://github.com/anthropics/skills.git" },
    @{ Name = "vercel-react-best-practices"; Repo = "https://github.com/vercel-labs/agent-skills.git" },
    @{ Name = "shadcn"; Repo = "https://github.com/shadcn/ui.git" },
    @{ Name = "next-best-practices"; Repo = "https://github.com/vercel-labs/next-skills.git" },

    # UI/UX & Design
    @{ Name = "ui-ux-pro-max"; Repo = "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git" },
    @{ Name = "minimalist-ui"; Repo = "https://github.com/leonxlnx/taste-skill.git" },
    @{ Name = "design-taste-frontend"; Repo = "https://github.com/leonxlnx/taste-skill.git" },

    # Developer Workflow
    @{ Name = "improve-codebase-architecture"; Repo = "https://github.com/mattpocock/skills.git" },
    @{ Name = "webapp-testing"; Repo = "https://github.com/anthropics/skills.git" },
    @{ Name = "to-issues"; Repo = "https://github.com/mattpocock/skills.git" }
)

# Workspace Customization Root for Antigravity is ".agents"
$destDir = Join-Path (Get-Location) ".agents/skills"
$tempDir = Join-Path (Get-Location) ".agent/skills/temp"

Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host " Antigravity Skills Installer" -ForegroundColor Cyan
Write-Host " Target Directory: $destDir" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan

# Create directories
New-Item -ItemType Directory -Force $destDir | Out-Null
New-Item -ItemType Directory -Force $tempDir | Out-Null

$clonedRepos = @{}

foreach ($skill in $skills) {
    Write-Host ""
    Write-Host "--> Process: $($skill.Name)" -ForegroundColor Yellow
    
    $repoUrl = $skill.Repo
    $ownerName = ($repoUrl -split '/')[-2]
    $repoShortName = (($repoUrl -split '/')[-1] -replace '\.git$', '')
    $repoName = $ownerName + "_" + $repoShortName
    $repoLocalPath = Join-Path $tempDir $repoName
    
    # Clone repo if not already done in this run
    if (-not $clonedRepos.ContainsKey($repoUrl)) {
        if (Test-Path $repoLocalPath) {
            Remove-Item -Recurse -Force $repoLocalPath | Out-Null
        }
        Write-Host "  Cloning $repoUrl..." -ForegroundColor DarkGray
        git clone --depth 1 --quiet $repoUrl $repoLocalPath
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  Failed to clone repository: $repoUrl" -ForegroundColor Red
            continue
        }
        $clonedRepos[$repoUrl] = $repoLocalPath
    }
    
    # Locate the skill folder containing a SKILL.md
    $foundPath = $null
    
    # Case 1: The repo itself is the skill (has SKILL.md at the root)
    if (Test-Path (Join-Path $repoLocalPath "SKILL.md")) {
        $foundPath = $repoLocalPath
    } else {
        # Case 2: The repo is a collection of skills. Look for a directory matching the skill name containing SKILL.md
        $candidatePaths = Get-ChildItem -Path $repoLocalPath -Filter "SKILL.md" -Recurse -Force | ForEach-Object { $_.DirectoryName }
        foreach ($path in $candidatePaths) {
            $folderName = Split-Path $path -Leaf
            if ($folderName -eq $skill.Name) {
                $foundPath = $path
                break
            }
        }
        
        # Case 3: Broad search. If directory name doesn't match exactly, find any SKILL.md whose file content name matches the skill
        if (-not $foundPath) {
            foreach ($path in $candidatePaths) {
                $skillFile = Join-Path $path "SKILL.md"
                if (Test-Path $skillFile) {
                    $content = Get-Content $skillFile -Raw
                    if ($content -match "name:\s*$($skill.Name)") {
                        $foundPath = $path
                        break
                    }
                }
            }
        }
    }
    
    if ($foundPath) {
        $targetDest = Join-Path $destDir $skill.Name
        if (Test-Path $targetDest) {
            Remove-Item -Recurse -Force $targetDest | Out-Null
        }
        
        # Copy files excluding .git folder
        Copy-Item -Path $foundPath -Destination $targetDest -Recurse -Force
        if (Test-Path (Join-Path $targetDest ".git")) {
            Remove-Item -Recurse -Force (Join-Path $targetDest ".git") | Out-Null
        }
        
        Write-Host "  [SUCCESS] Installed $($skill.Name) to $targetDest" -ForegroundColor Green
    } else {
        Write-Host "  [WARNING] Skill '$($skill.Name)' could not be located in $repoName" -ForegroundColor Yellow
    }
}

# Clean up temp
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir | Out-Null
}

Write-Host ""
Write-Host "====================================================================" -ForegroundColor Green
Write-Host " Installation complete!" -ForegroundColor Green
Write-Host " All active skills are installed in .agents/skills and will be loaded" -ForegroundColor Green
Write-Host " automatically by Antigravity." -ForegroundColor Green
Write-Host "====================================================================" -ForegroundColor Green
