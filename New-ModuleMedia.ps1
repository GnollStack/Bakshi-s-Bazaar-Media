param(
  [Parameter(Mandatory = $true)]
  [ValidatePattern('^[a-z0-9]+(?:-[a-z0-9]+)*$')]
  [string]$ModuleId,
  [string]$Title = ''
)

$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($PSScriptRoot)
$template = Join-Path $root '_module-template'
$destination = [IO.Path]::GetFullPath((Join-Path $root $ModuleId))

if (-not $destination.StartsWith($root + '\', [StringComparison]::OrdinalIgnoreCase)) {
  throw 'The new module folder must stay inside this media repository.'
}
if (Test-Path -LiteralPath $destination) {
  throw "This path already exists; nothing was changed: $destination"
}
if (-not (Test-Path -LiteralPath (Join-Path $template 'README.md') -PathType Leaf)) {
  throw 'The _module-template folder or its README is missing.'
}
if ([string]::IsNullOrWhiteSpace($Title)) { $Title = $ModuleId }

# Start with the same two media folders every time. Existing modules are left alone.
Copy-Item -LiteralPath $template -Destination $destination -Recurse
$readme = Join-Path $destination 'README.md'
$content = [IO.File]::ReadAllText($readme)
$content = $content.Replace('__MODULE_ID__', $ModuleId).Replace('__MODULE_TITLE__', $Title)
[IO.File]::WriteAllText($readme, $content, (New-Object Text.UTF8Encoding $false))

Write-Host "Created $destination"
Write-Host 'Add your GIFs and images, update the media links, then commit and push when ready.'
