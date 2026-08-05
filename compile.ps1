# Simple build script for the Signal-88 compiler

# Compiler to use
$Compiler = "gcc"

# Source files
$SourceFiles = @(
    "singal-88.c",
    "frontend/lexer.c",
    "frontend/parser.c",
    "frontend/utils.c"
)

# Output executable
$OutputFile = "signal-88.exe"

# Include directories
$IncludeDirs = @(
    "-Ifrontend/include"
)

# Build command
$Command = "$Compiler $SourceFiles $IncludeDirs -o $OutputFile"

# Print the command
Write-Host "Executing: $Command"

# Execute the build command
Invoke-Expression $Command

# Check if the build was successful
if ($?) {
    Write-Host "Build successful! Executable created: $OutputFile"
} else {
    Write-Host "Build failed."
}
