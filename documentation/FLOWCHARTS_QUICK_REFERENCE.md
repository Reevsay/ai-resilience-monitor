# Flowcharts Quick Reference

## Overview

Three comprehensive LaTeX flowcharts documenting the AI Resilience Monitor's chaos engineering and circuit breaker implementation.

## Quick Start

### Windows
```powershell
cd ai-resilience-monitor\documentation
.\compile-flowcharts.ps1
```

### Linux/macOS
```bash
cd ai-resilience-monitor/documentation
chmod +x compile-flowcharts.sh
./compile-flowcharts.sh
```

### Manual Compilation
```bash
pdflatex chaos-engineering-flowchart.tex
pdflatex chaos-experiment-lifecycle.tex
pdflatex circuit-breaker-state-machine.tex
```

## Flowchart Descriptions

### 1. Multi-Provider AI Service
**File:** `multi-provider-ai-service.tex`

**Purpose:** Shows AI service provider cascade with intelligent fallback

**Key Components:**
- Request parsing and service selection
- Preferred service vs default order
- API key validation per provider
- Provider cascade (Gemini → Cohere → HuggingFace)
- Individual API call specifications
- Error handling and retry logic
- Simulation fallback when all fail
- Response formatting and metadata

**Visual Features:**
- Purple provider boxes
- Red fallback layer
- Green success path
- Detailed API specifications for each provider
- Provider comparison table
- Configuration panel

**Best For:** Understanding multi-provider integration and fallback strategy

---

### 2. Chaos Engineering Flowchart
**File:** `chaos-engineering-flowchart.tex`

**Purpose:** Shows complete AI service request processing with chaos engineering integration

**Key Components:**
- Request validation and initialization
- Chaos experiment application (6 types)
- Circuit breaker state checking
- Real API vs simulation fallback
- Response corruption handling
- Metrics and database logging

**Visual Features:**
- Color-coded layers (Chaos, Circuit Breaker, AI Service)
- Green arrows = success paths
- Red arrows = failure/chaos paths
- Comprehensive legend

**Best For:** Understanding the complete request flow

---

### 3. Chaos Experiment Lifecycle
**File:** `chaos-experiment-lifecycle.tex`

**Purpose:** Documents chaos experiment lifecycle from injection to completion

**Key Components:**
- Experiment configuration and validation
- Active monitoring loop
- Request interception
- Circuit breaker impact tracking
- Manual stop capability
- Results generation

**Visual Features:**
- Side panels with chaos types and API endpoints
- Active experiment loop visualization
- Blue arrows = loop/continue paths
- Red arrows = error/stop paths

**Best For:** Understanding how chaos experiments work

---

### 4. Circuit Breaker State Machine
**File:** `circuit-breaker-state-machine.tex`

**Purpose:** State machine diagram showing circuit breaker behavior

**Key Components:**
- Three states: CLOSED, OPEN, HALF-OPEN
- State transitions with conditions
- Detailed behavior for each state
- Configuration parameters
- Metrics tracking

**Visual Features:**
- Large circular state nodes
- Self-loops for state-specific behavior
- Detailed state behavior boxes
- Configuration and metrics panels

**Best For:** Understanding circuit breaker logic

---

## Color Coding

### Chaos Engineering Flowchart
- **Green** (Start/End): Entry and exit points
- **Blue** (Process): Normal operations
- **Yellow** (Decision): Decision points
- **Red** (Chaos): Chaos operations
- **Purple** (Circuit Breaker): Circuit breaker operations

### Chaos Experiment Lifecycle
- **Green** (Start/End): Entry and exit points
- **Blue** (Process): Normal operations
- **Yellow** (Decision): Decision points
- **Red** (Chaos): Chaos operations
- **Orange** (Monitor): Monitoring operations

### Circuit Breaker State Machine
- **Green** (CLOSED): Normal operation state
- **Red** (OPEN): Failing fast state
- **Yellow** (HALF-OPEN): Testing recovery state
- **Blue** (Info boxes): Configuration and metrics

---

## Chaos Types Reference

| Type | Description | Intensity | Effect |
|------|-------------|-----------|--------|
| **Latency** | Adds artificial delay | 0-10000ms | Tests timeout handling |
| **Failure** | Forces random failures | 0-100% | Tests error handling |
| **Timeout** | Hangs requests | 0-3000ms | Tests timeout mechanisms |
| **Intermittent** | Random failure patterns | 0-100% | Tests retry logic |
| **Unavailable** | Complete service outage | N/A | Tests fallback mechanisms |
| **Corruption** | Corrupts response data | N/A | Tests data validation |

---

## Circuit Breaker States

| State | Behavior | Transition Condition |
|-------|----------|---------------------|
| **CLOSED** | Allow all requests | failureCount ≥ 5 → OPEN |
| **OPEN** | Reject all requests | timeout (30s) → HALF-OPEN |
| **HALF-OPEN** | Allow limited requests | 2 successes → CLOSED<br>Any failure → OPEN |

---

## Configuration Parameters

### Circuit Breaker
```javascript
failureThreshold: 5      // Failures before opening
successThreshold: 2      // Successes to close from half-open
timeout: 30000          // Wait time before half-open (30s)
halfOpenTimeout: 10000  // Max time in half-open (10s)
```

### Chaos Experiments
```javascript
intensity: 0-10000      // Varies by type
duration: 1-300         // Seconds (1s to 5min)
service: string         // gemini, cohere, huggingface
type: string           // latency, failure, timeout, etc.
```

---

## API Endpoints Reference

### Chaos Engineering
```
POST /chaos/inject      - Start chaos experiment
POST /chaos/stop        - Stop chaos experiment
GET  /chaos/status      - Get active experiments
```

### Circuit Breaker
```
GET  /circuit-breaker/status  - Get all breaker states
POST /circuit-breaker/reset   - Reset breakers
```

### AI Service
```
POST /ai                - AI service proxy
GET  /ai/health         - Health check
GET  /metrics           - Current metrics
```

---

## Metrics Tracked

### Request Metrics
- Total requests
- Successful requests
- Failed requests
- Average latency
- Per-service statistics

### Circuit Breaker Metrics
- Total calls
- Successful calls
- Failed calls
- Rejected calls (when OPEN)
- State transitions
- Time in each state

### Chaos Experiment Metrics
- Requests affected
- Failure rate increase
- Latency impact
- Circuit breaker state changes

---

## AI Provider Details

### Supported Providers

| Provider | Model | Endpoint | Auth Method | Timeout |
|----------|-------|----------|-------------|---------|
| **Google Gemini** | gemini-pro | generativelanguage.googleapis.com | API key in URL | 15s |
| **Cohere** | command | api.cohere.ai/v1/generate | Bearer token | 15s |
| **HuggingFace** | GPT-2 | api-inference.huggingface.co | Bearer token | 15s |
| **Simulation** | N/A | Local | None | 0.5-2.5s |

### Provider Cascade Order

1. **Preferred Service** (if specified) → Try first
2. **Google Gemini** → Default first choice
3. **Cohere** → Second fallback
4. **HuggingFace** → Third fallback
5. **Simulation** → Final fallback (always succeeds)

### API Response Formats

**Gemini:**
```json
{
  "candidates": [{
    "content": {
      "parts": [{"text": "Response here"}]
    }
  }]
}
```

**Cohere:**
```json
{
  "generations": [{
    "text": "Response here"
  }]
}
```

**HuggingFace:**
```json
[{
  "generated_text": "Response here"
}]
```

---

## File Sizes

| File | PDF Size | PNG Size (300 DPI) |
|------|----------|-------------------|
| multi-provider-ai-service | ~60-90 KB | ~500-800 KB |
| chaos-engineering-flowchart | ~50-80 KB | ~500-800 KB |
| chaos-experiment-lifecycle | ~60-90 KB | ~500-800 KB |
| circuit-breaker-state-machine | ~40-70 KB | ~400-600 KB |

---

## Common Use Cases

### For Research Papers
1. Compile to PDF
2. Include in LaTeX paper: `\includegraphics{chaos-engineering-flowchart.pdf}`
3. Add caption and reference

### For Presentations
1. Compile to high-res PNG (300 DPI)
2. Insert into PowerPoint/Google Slides
3. Ensure proper sizing and quality

### For Documentation
1. Compile to SVG for web use
2. Embed in HTML documentation
3. Link to interactive versions

---

## Troubleshooting

### PDF not generated
- Check if pdflatex is installed: `pdflatex --version`
- Look at .log file for errors
- Ensure all TikZ packages are installed

### Text overlapping
- Increase `node distance` in the .tex file
- Adjust `xshift` and `yshift` values
- Reduce font sizes

### Compilation slow
- Use `-interaction=nonstopmode` flag
- Compile on faster machine
- Use online service (Overleaf)

---

## Resources

- **Full Documentation:** `LATEX_FLOWCHARTS_README.md`
- **TikZ Manual:** `texdoc tikz` or https://tikz.dev/
- **Overleaf:** https://www.overleaf.com (online LaTeX editor)
- **Stack Exchange:** https://tex.stackexchange.com/

---

## Environment Variables

### AI Provider Configuration
```bash
GOOGLE_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key

# Optional: Custom endpoints
GOOGLE_API_URL=https://generativelanguage.googleapis.com/...
COHERE_API_URL=https://api.cohere.ai/v1/generate
HUGGINGFACE_API_URL=https://api-inference.huggingface.co/...
```

### Fallback Behavior
- **No API keys configured** → Simulation mode only
- **API call fails** → Try next provider in cascade
- **All providers fail** → Simulation fallback
- **Simulation failure rate** → 10% (for testing)

---

## Version Info

- **Created:** November 19, 2024
- **Version:** 1.1
- **Author:** Yashveer Ahlawat
- **Project:** AI Resilience Monitor
- **Latest Update:** Added multi-provider AI service flowchart

---

## License

MIT License - Part of AI Resilience Monitor project
