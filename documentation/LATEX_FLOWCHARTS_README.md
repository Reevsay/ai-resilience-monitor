# LaTeX Flowcharts for AI Resilience Monitor

This directory contains comprehensive LaTeX flowcharts documenting the chaos engineering and circuit breaker implementation.

## Files

### 1. `multi-provider-ai-service.tex`
**Multi-provider AI service integration with intelligent fallback**

Shows the complete AI service provider cascade:
- Request parsing and service selection
- Preferred service vs default order
- API key validation
- Provider cascade (Gemini → Cohere → HuggingFace)
- Individual provider API call details
- Error handling and retry logic
- Simulation fallback when all providers fail
- Response formatting and metadata
- Metrics tracking

**Key Features:**
- Color-coded provider attempts
- Detailed API call specifications for each provider
- Error handling flow
- Fallback layer visualization
- Provider comparison table
- Configuration panel with environment variables

### 2. `chaos-engineering-flowchart.tex`
**Complete request processing flow with chaos engineering integration**

Shows the entire lifecycle of an AI service request including:
- Request validation and initialization
- Chaos experiment application (6 types)
- Circuit breaker state checking (CLOSED/OPEN/HALF-OPEN)
- Real API vs simulation fallback
- Response corruption
- Metrics and database logging

**Key Features:**
- Color-coded layers (Chaos, Circuit Breaker, AI Service)
- Success/failure path differentiation
- Comprehensive legend
- All 6 chaos types documented

### 3. `chaos-experiment-lifecycle.tex`
**Detailed chaos experiment lifecycle from start to finish**

Documents the complete chaos experiment process:
- Experiment configuration and validation
- Active monitoring loop
- Request interception and chaos application
- Circuit breaker impact tracking
- Manual stop capability
- Results generation

**Key Features:**
- Side panels with chaos types and API endpoints
- Active experiment loop visualization
- Manual stop flow
- Status API integration

### 4. `circuit-breaker-state-machine.tex`
**Circuit breaker state machine with transitions**

Comprehensive state machine diagram showing:
- Three states: CLOSED, OPEN, HALF-OPEN
- All state transitions with conditions
- Detailed behavior for each state
- Configuration parameters
- Metrics tracking
- API endpoints

**Key Features:**
- Large circular state nodes
- Self-loops for state-specific behavior
- Detailed state behavior boxes
- Configuration and metrics panels

## Compilation Instructions

### Prerequisites

Install a LaTeX distribution:
- **Windows**: MiKTeX or TeX Live
- **macOS**: MacTeX
- **Linux**: TeX Live

```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# macOS (with Homebrew)
brew install --cask mactex

# Windows (with Chocolatey)
choco install miktex
```

### Required LaTeX Packages

All flowcharts use the `standalone` document class and require:
- `tikz` - Main drawing package
- `tikz` libraries: `shapes.geometric`, `arrows.meta`, `positioning`, `fit`, `backgrounds`, `shadows`, `automata`

These are typically included in full LaTeX distributions.

### Compilation Commands

#### Compile to PDF

```bash
# Navigate to documentation directory
cd ai-resilience-monitor/documentation

# Compile each flowchart
pdflatex multi-provider-ai-service.tex
pdflatex chaos-engineering-flowchart.tex
pdflatex chaos-experiment-lifecycle.tex
pdflatex circuit-breaker-state-machine.tex
```

#### Compile to PNG (High Resolution)

```bash
# Method 1: Using ImageMagick (after PDF generation)
convert -density 300 chaos-engineering-flowchart.pdf -quality 100 chaos-engineering-flowchart.png
convert -density 300 chaos-experiment-lifecycle.pdf -quality 100 chaos-experiment-lifecycle.png
convert -density 300 circuit-breaker-state-machine.pdf -quality 100 circuit-breaker-state-machine.png

# Method 2: Using pdftoppm
pdftoppm -png -r 300 chaos-engineering-flowchart.pdf chaos-engineering-flowchart
pdftoppm -png -r 300 chaos-experiment-lifecycle.pdf chaos-experiment-lifecycle
pdftoppm -png -r 300 circuit-breaker-state-machine.pdf circuit-breaker-state-machine
```

#### Compile to SVG (Vector Graphics)

```bash
# Using pdf2svg
pdf2svg chaos-engineering-flowchart.pdf chaos-engineering-flowchart.svg
pdf2svg chaos-experiment-lifecycle.pdf chaos-experiment-lifecycle.svg
pdf2svg circuit-breaker-state-machine.pdf circuit-breaker-state-machine.svg
```

### Online Compilation

If you don't have LaTeX installed locally, use **Overleaf**:

1. Go to [overleaf.com](https://www.overleaf.com)
2. Create a new blank project
3. Upload the `.tex` file
4. Click "Recompile"
5. Download PDF

### Batch Compilation Script

#### Windows (PowerShell)

```powershell
# compile-flowcharts.ps1
$files = @(
    "multi-provider-ai-service",
    "chaos-engineering-flowchart",
    "chaos-experiment-lifecycle",
    "circuit-breaker-state-machine"
)

foreach ($file in $files) {
    Write-Host "Compiling $file.tex..."
    pdflatex "$file.tex"
    
    # Clean up auxiliary files
    Remove-Item "$file.aux", "$file.log" -ErrorAction SilentlyContinue
    
    Write-Host "✓ Generated $file.pdf"
}

Write-Host "`nAll flowcharts compiled successfully!"
```

#### Linux/macOS (Bash)

```bash
#!/bin/bash
# compile-flowcharts.sh

files=(
    "multi-provider-ai-service"
    "chaos-engineering-flowchart"
    "chaos-experiment-lifecycle"
    "circuit-breaker-state-machine"
)

for file in "${files[@]}"; do
    echo "Compiling $file.tex..."
    pdflatex "$file.tex"
    
    # Clean up auxiliary files
    rm -f "$file.aux" "$file.log"
    
    echo "✓ Generated $file.pdf"
done

echo -e "\nAll flowcharts compiled successfully!"
```

## Customization

### Changing Colors

Edit the color definitions at the top of each file:

```latex
\definecolor{startcolor}{RGB}{46, 204, 113}    % Green
\definecolor{processcolor}{RGB}{52, 152, 219}  % Blue
\definecolor{chaoscolor}{RGB}{231, 76, 60}     % Red
```

### Adjusting Node Sizes

Modify the `tikzstyle` definitions:

```latex
\tikzstyle{process} = [rectangle, minimum width=3cm, minimum height=1cm, ...]
```

### Changing Fonts

Add font packages and modify font commands:

```latex
\usepackage{helvet}  % Use Helvetica
\renewcommand{\familydefault}{\sfdefault}
```

## Troubleshooting

### Common Issues

**Issue**: `! LaTeX Error: File 'tikz.sty' not found`
**Solution**: Install the `pgf` package (includes TikZ)
```bash
# MiKTeX
mpm --install=pgf

# TeX Live
tlmgr install pgf
```

**Issue**: PDF is too large/small
**Solution**: Adjust the `border` parameter in `\documentclass[border=10pt]{standalone}`

**Issue**: Text overlapping
**Solution**: Increase `node distance` or adjust `xshift`/`yshift` values

**Issue**: Compilation takes too long
**Solution**: Use `pdflatex -interaction=nonstopmode` to skip errors

### Getting Help

- TikZ Documentation: `texdoc tikz`
- Online: [TikZ & PGF Manual](https://tikz.dev/)
- Stack Exchange: [tex.stackexchange.com](https://tex.stackexchange.com/)

## Integration with Research Paper

These flowcharts are designed for inclusion in academic papers:

### LaTeX Paper Integration

```latex
\documentclass{article}
\usepackage{graphicx}

\begin{document}

\section{Chaos Engineering Architecture}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{chaos-engineering-flowchart.pdf}
    \caption{Complete chaos engineering request processing flow}
    \label{fig:chaos-flow}
\end{figure}

As shown in Figure~\ref{fig:chaos-flow}, the chaos engineering...

\end{document}
```

### Word/Google Docs Integration

1. Compile to high-resolution PNG (300 DPI)
2. Insert as image
3. Ensure "Lock aspect ratio" is enabled
4. Add caption and cross-reference

## File Sizes

Approximate compiled sizes:
- `multi-provider-ai-service.pdf`: ~60-90 KB
- `chaos-engineering-flowchart.pdf`: ~50-80 KB
- `chaos-experiment-lifecycle.pdf`: ~60-90 KB
- `circuit-breaker-state-machine.pdf`: ~40-70 KB

PNG exports (300 DPI): ~500-800 KB each

## Version History

- **v1.1** (2024-11-19): Added multi-provider AI service flowchart
  - Multi-provider AI service integration
  - Provider cascade with fallback
  - Detailed API specifications
- **v1.0** (2024-11-19): Initial creation
  - Complete chaos engineering flow
  - Experiment lifecycle diagram
  - Circuit breaker state machine

## License

These flowcharts are part of the AI Resilience Monitor project and follow the same MIT License.

## Credits

Created for the AI Resilience Monitor research project by Yashveer Ahlawat.
Based on the implementation in `src/index.js` and chaos engineering principles.
