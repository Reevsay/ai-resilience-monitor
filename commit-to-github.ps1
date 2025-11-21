# Comprehensive GitHub Commit Script
# Commits each file individually with detailed messages to maximize commit count

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GitHub Commit Script" -ForegroundColor Cyan
Write-Host "  Individual commits for maximum count" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git initialized" -ForegroundColor Green
}

# Function to commit a file
function Commit-File {
    param(
        [string]$FilePath,
        [string]$Message
    )
    
    git add $FilePath
    git commit -m $Message
    Write-Host "✓ Committed: $FilePath" -ForegroundColor Green
}

Write-Host "Starting individual commits..." -ForegroundColor Yellow
Write-Host ""

# Core Configuration Files
Commit-File ".gitignore" "chore: update .gitignore to exclude documentation source files and test results

- Exclude LaTeX source files (keep compiled PDFs only)
- Exclude all test result files except samples
- Exclude database files (runtime data)
- Keep directory structure with README files
- Optimize for clean repository"

Commit-File "package.json" "build: add Node.js dependencies and project metadata

- Express.js for backend server
- Axios for HTTP requests
- Prometheus client for metrics
- SQLite3 for database
- CORS and dotenv for configuration
- Nodemailer and Slack webhook for notifications"

Commit-File "requirements.txt" "build: add Python dependencies for Flask frontend

- Flask 2.3.0 for web server
- requests 2.31.0 for HTTP client
- psutil 5.9.5 for system monitoring
- Minimal dependencies for lightweight deployment"

Commit-File "LICENSE" "docs: add MIT License for open source distribution

- Permissive open source license
- Allows commercial and private use
- Requires attribution
- No warranty or liability"

Commit-File "README.md" "docs: add comprehensive project documentation

- Project overview and features
- Installation instructions
- Usage guide with examples
- Architecture diagram
- API endpoints documentation
- Troubleshooting guide
- Performance characteristics
- Contributing guidelines"

# Main Application Files
Commit-File "app.py" "feat: implement Flask frontend server with auto-start capabilities

- Serves main dashboard on port 8080
- Proxies requests to Node.js backend
- Manages SQLite database operations
- Auto-starts backend and Prometheus
- Implements health checking
- Provides historical data APIs
- Handles graceful shutdown
- 493 lines of production-ready code"

Commit-File "src/index.js" "feat: implement main Node.js backend with circuit breakers and chaos engineering

- Express.js server on port 3000
- Multi-provider AI service integration (Gemini, Cohere, HuggingFace)
- Three-state circuit breaker implementation (CLOSED/OPEN/HALF-OPEN)
- Six chaos experiment types (latency, failure, timeout, intermittent, unavailable, corruption)
- Prometheus metrics export
- SQLite persistence with WAL mode
- Global error handlers for crash prevention
- Comprehensive API endpoints
- 1790 lines of core functionality"

Commit-File "backend/database.py" "feat: implement SQLite database module with WAL mode

- Database connection management
- WAL mode for concurrent access
- Automatic table creation
- Busy timeout configuration
- Thread-safe operations
- Used by Flask frontend for data persistence"

# Templates
Commit-File "templates/dashboard.html" "feat: implement comprehensive real-time monitoring dashboard

- Real-time Chart.js visualizations
- Circuit breaker state displays
- Chaos experiment controls
- Request automation system
- Historical data tables
- Service health cards
- Responsive Bootstrap design
- 4663 lines of interactive UI
- Auto-refresh every 2 seconds
- Dark theme with modern styling"

# Test Files
Commit-File "test/ci-test.js" "test: add CI integration tests for automated testing

- Service availability checks
- Health endpoint validation
- Metrics endpoint testing
- Suitable for CI/CD pipelines
- Quick smoke tests"

Commit-File "test/real-ai-load-tester.js" "test: add comprehensive load testing tool for real AI services

- Tests multiple AI providers
- Configurable request count and concurrency
- Realistic AI prompts
- Performance metrics collection
- Service comparison analysis
- Sample response capture
- 200+ lines of load testing logic"

Commit-File "test/payloads.json" "test: add test payload data for load testing

- Sample AI prompts
- Request templates
- Test scenarios
- Used by load testing tools"

# Configuration Files
Commit-File "config/README.md" "docs: add configuration directory documentation

- Explains configuration file structure
- Environment variable setup
- Prometheus configuration
- Grafana dashboard setup"

Commit-File "config/prometheus.yml" "config: add Prometheus scrape configuration

- Scrapes backend metrics every 5 seconds
- Configured for localhost:3000
- Optimized for real-time monitoring"

Commit-File "config/grafana-dashboard.json" "config: add Grafana dashboard configuration

- Pre-configured panels for AI service metrics
- Request rate visualization
- Latency percentiles (p50, p95, p99)
- Error rate tracking
- Circuit breaker state monitoring"

# Data Directory
Commit-File "data/README.md" "docs: add database directory documentation

- Explains SQLite database structure
- Schema documentation
- Backup and restore procedures
- Query examples
- Performance optimization tips"

# Documentation Files
Commit-File "docs/README.md" "docs: add documentation directory overview

- Links to all documentation
- Quick start guide
- Architecture overview
- API reference"

Commit-File "docs/CONTRIBUTING.md" "docs: add contribution guidelines

- Code style requirements
- Pull request process
- Testing requirements
- Documentation standards
- Issue reporting guidelines"

Commit-File "docs/LITERATURE_REVIEW.md" "docs: add comprehensive literature review

- Academic research on chaos engineering
- Circuit breaker patterns
- AI service resilience
- Industry best practices
- Citations and references"

# Literature Files
Commit-File "literature/PAPER_SUMMARIES.md" "docs: add academic paper summaries

- Summaries of 8 research papers
- Key findings and insights
- Relevance to project
- Citations and references"

Commit-File "literature/Base Paper .txt" "docs: add base research paper reference

- Foundation paper for project
- Core concepts and methodology
- Research questions addressed"

Commit-File "literature/reference paper .txt" "docs: add reference paper for implementation

- Implementation guidance
- Technical specifications
- Best practices"

# Scripts Directory
Commit-File "scripts/README.md" "docs: add scripts directory documentation

- Explains utility scripts
- Usage instructions
- Script categories
- Automation workflows"

Commit-File "scripts/setup-prometheus-grafana.ps1" "feat: add automated Prometheus and Grafana setup script

- Downloads and installs Prometheus
- Downloads and installs Grafana
- Configures both services
- Sets up dashboards
- Windows PowerShell automation"

Commit-File "scripts/stop-all-services.ps1" "feat: add script to stop all running services

- Stops backend server
- Stops frontend server
- Stops Prometheus
- Stops Grafana
- Clean shutdown"

# Monitoring Scripts
Commit-File "scripts/monitoring/monitor-all-services.py" "feat: add comprehensive service monitoring script

- Monitors backend health
- Monitors frontend health
- Monitors Prometheus
- Monitors Grafana
- Sends alerts on failures
- Continuous monitoring loop"

# Testing Scripts
Commit-File "scripts/testing/chaos-test.py" "feat: add automated chaos testing script

- Runs comprehensive chaos experiments
- Tests all six chaos types
- Validates circuit breaker behavior
- Generates detailed reports
- Exports results to CSV
- Validation and full test modes"

# Setup Scripts
Commit-File "scripts/setup/start-monitor-enhanced.ps1" "feat: add enhanced startup script for all services

- Starts backend with monitoring
- Starts frontend with monitoring
- Starts Prometheus
- Starts Grafana
- Health checks for all services
- Colored output and logging"

# Utility Scripts
Commit-File "scripts/utilities/cleanup-project.py" "feat: add project cleanup utility

- Removes temporary files
- Cleans Python cache
- Removes old logs
- Cleans test results
- Maintains directory structure"

# Documentation - Keep only README files
Commit-File "documentation/FLOWCHARTS_QUICK_REFERENCE.md" "docs: add flowcharts quick reference guide

- Overview of all flowcharts
- Chaos types reference
- Circuit breaker states
- Provider details
- Configuration examples
- Troubleshooting guide"

Commit-File "documentation/LATEX_FLOWCHARTS_README.md" "docs: add LaTeX flowcharts compilation guide

- Compilation instructions
- Prerequisites and setup
- Customization options
- Troubleshooting
- Integration with papers
- File size information"

Commit-File "documentation/MULTI_PROVIDER_AI_OVERVIEW.md" "docs: add comprehensive multi-provider AI service documentation

- Architecture overview
- Provider specifications
- Service selection logic
- Error handling strategy
- Performance characteristics
- Configuration examples
- Best practices
- 400+ lines of technical documentation"

# Logs and Results
Commit-File "logs/README.md" "docs: add logs directory documentation

- Log file descriptions
- Log rotation procedures
- Viewing and searching logs
- Log levels explanation"

Commit-File "chaos-test-results/README.md" "docs: add chaos test results documentation

- File types explanation
- Running tests guide
- Cleanup procedures
- Sample files reference"

Commit-File "chaos-test-results/sample_chaos_test_report.txt" "docs: add sample chaos test report

- Example output format
- Shows test structure
- Demonstrates resilience scoring
- Reference for users"

# Cleanup Reports
Commit-File "CLEANUP_REPORT_2024.md" "docs: add detailed cleanup analysis report

- Lists all removed files
- Explains removal reasons
- Impact analysis
- Cleanup actions performed
- Verification steps
- Post-cleanup structure"

Commit-File "CLEANUP_SUMMARY.md" "docs: add cleanup summary

- Quick reference for cleanup
- Files removed list
- Current active files
- Benefits achieved
- Verification checklist"

Commit-File "CLEANUP_COMPLETE.md" "docs: add cleanup completion report

- Final cleanup status
- Verification results
- System status
- Next steps
- Recommendations
- Project health metrics"

Commit-File "verify-cleanup.ps1" "test: add cleanup verification script

- Verifies core files exist
- Checks deleted files removed
- Validates directory structure
- Tests syntax
- Comprehensive verification
- Colored output"

# GitHub Workflows
if (Test-Path ".github/workflows/ci.yml") {
    Commit-File ".github/workflows/ci.yml" "ci: add GitHub Actions CI workflow

- Automated testing on push
- Node.js and Python setup
- Dependency installation
- Test execution
- Multi-platform support"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Commit Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$commitCount = (git rev-list --count HEAD)
Write-Host "Total commits created: $commitCount" -ForegroundColor Green
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Add remote: git remote add origin <your-repo-url>" -ForegroundColor White
Write-Host "2. Push to GitHub: git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "Or if you already have a remote:" -ForegroundColor Yellow
Write-Host "git push -u origin main" -ForegroundColor White
Write-Host ""
