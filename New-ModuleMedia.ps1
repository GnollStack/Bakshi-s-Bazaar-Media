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
foreach ($name in @('README.md', 'CHANGELOG.md')) {
  $document = Join-Path $destination $name
  $content = [IO.File]::ReadAllText($document)
  $content = $content.Replace('__MODULE_ID__', $ModuleId).Replace('__MODULE_TITLE__', $Title)
  [IO.File]::WriteAllText($document, $content, (New-Object Text.UTF8Encoding $false))
}

Write-Host "Created $destination"
Write-Host 'Add your GIFs and images, update the media links and changelog, then commit and push when ready.'
