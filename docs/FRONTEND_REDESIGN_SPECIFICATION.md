# AI Resilience Monitor - Frontend Redesign Specification

## Project Overview

**Current State**: Functional dashboard with custom CSS, complex layout, and mixed design patterns
**Target**: Modern, responsive dashboard using Tailwind CSS with clean component architecture
**Framework**: Vanilla JavaScript + Tailwind CSS v3.x + Chart.js

---

## Page Structure & Layout

### Main Layout Grid
```
┌─────────────────────────────────────────────────────────┐
│                    Header Bar                           │
├─────────────────────────────────────────────────────────┤
│  Metrics Cards Row (3-4 cards)                        │
├─────────────────────────────────────────────────────────┤
│ Left Panel (60%)          │ Right Panel (40%)          │
│                           │                            │
│ • AI Services Grid        │ • Analytics Section        │
│ • Chaos Engineering      │ • Circuit Breaker Status   │
│ • Request History         │ • Performance Charts       │
│                           │ • Service Leaderboard      │
└─────────────────────────────────────────────────────────┘
```

### Responsive Breakpoints
- **Desktop**: 1200px+ (2-column layout)
- **Tablet**: 768px-1199px (stacked layout)
- **Mobile**: <768px (single column, collapsible sections)

---

## Component Inventory

### 1. Header Component
**Elements:**
- Dashboard title with emoji icon
- Connection status indicator (dot + text)
- Last updated timestamp
- Optional: Settings/export buttons

**States:**
- Connected (green dot)
- Disconnected (red dot)
- Connecting (yellow dot, animated)

### 2. Metrics Cards Grid
**Cards (4 total):**
- Total Requests (number + change indicator)
- Success Rate (percentage + trend)
- Average Latency (milliseconds + trend)
- Active Experiments (count + status)

**Card Elements:**
- Large metric value
- Descriptive label
- Change indicator (up/down arrow + text)
- Optional: Mini sparkline chart

### 3. AI Services Grid
**Service Cards (3 services):**
- Google Gemini (💎 icon)
- Cohere (🧠 icon)
- Hugging Face (🤗 icon)

**Each Card Contains:**
- Service icon + name
- Status indicator (healthy/warning/error)
- Metrics row: Requests | Failures | Avg Latency
- Circuit breaker state badge
- Chaos experiment indicator (if active)

### 4. Chaos Engineering Panel
**Collapsible Section with:**
- Section header with toggle arrow
- Control form:
  - Service selector dropdown
  - Chaos type dropdown (6 types)
  - Intensity slider with dynamic units
  - Duration input field
  - Action buttons: Inject Chaos | Stop All
- Active experiments list:
  - Experiment cards with service, type, timer
  - Individual stop buttons

### 5. Analytics Section
**Sub-components:**
- Automation controls bar
- Real-time performance chart
- Service response time trends chart
- Service performance leaderboard
- Key insights grid (6 metrics)

### 6. Circuit Breaker Status Panel
**Elements:**
- Service status rows with state indicators
- Reset buttons per service
- Global reset all button
- State badges: CLOSED | OPEN | HALF_OPEN

### 7. Request History Table
**Features:**
- Scrollable table with fixed header
- Columns: Timestamp | Service | Status | Latency | Response Size
- Status indicators (success/failed)
- Pagination or infinite scroll

---

## Component States & Interactions

### Service Status States
- **Healthy**: Green indicator, normal metrics
- **Warning**: Yellow indicator, degraded performance
- **Error**: Red indicator, failures detected
- **Unknown**: Gray indicator, no data

### Chaos Experiment States
- **Inactive**: Normal service appearance
- **Active**: Red border, chaos badge, pulsing animation
- **Stopping**: Transition state with loading indicator

### Circuit Breaker States
- **CLOSED**: Green badge, normal operation
- **OPEN**: Red badge, blocking requests
- **HALF_OPEN**: Yellow badge, testing recovery

### Chart Interactions
- Hover tooltips with detailed metrics
- Zoom/pan capabilities for time series
- Legend toggle for multi-service charts
- Clear/reset chart data buttons

---

## Data Flow & API Integration

### Real-time Updates
- WebSocket or polling every 2-5 seconds
- Metrics endpoint: `/api/metrics`
- Health endpoint: `/api/health`
- Chaos status: `/chaos/status`

### User Actions
- Chaos injection: `POST /chaos/inject`
- Stop chaos: `POST /chaos/stop`
- Circuit breaker reset: `POST /circuit-breaker/reset`
- Automation toggle: Client-side state management

### Historical Data
- Request history: `/api/history/requests`
- Performance trends: `/api/history/trends`
- Error patterns: `/api/history/errors`

---

## Visual Design Elements

### Color System
- **Primary**: Blue (#3b82f6) for actions and highlights
- **Success**: Green (#10b981) for healthy states
- **Warning**: Yellow (#f59e0b) for caution states
- **Error**: Red (#ef4444) for failures
- **Background**: Dark slate (#0f172a, #1e293b)

### Typography
- **Font**: Inter or system fonts
- **Sizes**: 12px-36px scale
- **Weights**: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)

### Spacing
- **Base unit**: 4px (Tailwind's spacing scale)
- **Card padding**: 16-24px
- **Section gaps**: 16-32px
- **Component margins**: 8-16px

### Animations
- **Hover effects**: Subtle scale/shadow changes
- **Loading states**: Pulse or spinner animations
- **State transitions**: 200-300ms ease transitions
- **Chaos indicators**: Pulsing red glow

---

## Accessibility Requirements

### Keyboard Navigation
- Tab order through interactive elements
- Enter/Space for button activation
- Arrow keys for slider controls
- Escape to close modals/dropdowns

### Screen Reader Support
- Semantic HTML structure
- ARIA labels for complex components
- Status announcements for dynamic updates
- Alternative text for visual indicators

### Visual Accessibility
- High contrast ratios (4.5:1 minimum)
- Focus indicators on all interactive elements
- No color-only information conveyance
- Scalable text up to 200%

---

## Performance Considerations

### Optimization Strategies
- Lazy loading for charts and heavy components
- Debounced API calls for real-time updates
- Virtual scrolling for large data tables
- Efficient DOM updates (avoid full re-renders)

### Bundle Size
- Tree-shake unused Tailwind classes
- Minimize JavaScript dependencies
- Optimize Chart.js bundle
- Compress assets in production

---

## Technical Implementation Notes

### Component Architecture
- Modular JavaScript classes for each major component
- Event-driven communication between components
- Centralized state management for shared data
- Separation of concerns (data, view, interactions)

### CSS Organization
- Tailwind utility classes for styling
- Custom CSS properties for theming
- Component-specific styles in separate files
- Responsive design with mobile-first approach

### JavaScript Patterns
- ES6+ modern syntax
- Async/await for API calls
- Error boundaries for graceful failures
- Debouncing for performance optimization

---

## Migration Strategy

### Phase 1: Core Layout
- Header and metrics cards
- Basic service status grid
- Responsive grid system

### Phase 2: Interactive Components
- Chaos engineering panel
- Circuit breaker controls
- Real-time data updates

### Phase 3: Analytics & Charts
- Performance charts integration
- Historical data visualization
- Advanced analytics features

### Phase 4: Polish & Optimization
- Animations and micro-interactions
- Accessibility improvements
- Performance optimization
- Cross-browser testing

---

## File Structure

```
templates/
├── dashboard-new.html          # Main dashboard template
├── components/
│   ├── header.html            # Header component
│   ├── metrics-cards.html     # Metrics grid
│   ├── service-grid.html      # AI services
│   ├── chaos-panel.html       # Chaos engineering
│   └── analytics.html         # Analytics section
├── assets/
│   ├── css/
│   │   ├── tailwind.css       # Tailwind build
│   │   └── custom.css         # Custom styles
│   └── js/
│       ├── dashboard.js       # Main dashboard logic
│       ├── components/        # Component modules
│       └── utils/             # Utility functions
```

This specification provides the complete structural foundation for implementing a modern, maintainable dashboard using Tailwind CSS while preserving all existing functionality.tify-between">
          <div>
            <div class="font-medium text-slate-100">Gemini - Latency Injection</div>
            <div class="text-sm text-slate-400">500ms delay, 45s remaining</div>
          </div>
          <button class="bg-red-600 hover:bg-red-700 text-white text-xs font-semibold px-3 py-1 rounded">
            Stop
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
```

### 5. Analytics Chart Card
```html
<div class="bg-slate-800 rounded-lg border border-slate-700 p-6">
  <!-- Chart Header -->
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-lg font-semibold text-slate-100">⚡ Real-time Performance</h3>
    <div class="flex space-x-2">
      <button class="bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs px-3 py-1 rounded transition-colors">
        Clear
      </button>
      <button class="bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs px-3 py-1 rounded transition-colors">
        Export
      </button>
    </div>
  </div>
  
  <!-- Chart Container -->
  <div class="bg-slate-900 rounded-md p-4 h-64">
    <canvas id="performanceChart" class="w-full h-full"></canvas>
  </div>
</div>
```

### 6. Service Leaderboard
```html
<div class="bg-slate-800 rounded-lg border border-slate-700 p-6">
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-lg font-semibold text-slate-100">🏆 Service Performance Leaderboard</h3>
    <div class="flex items-center space-x-4 text-xs">
      <div class="flex items-center space-x-1">
        <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
        <span class="text-slate-400">1st Place</span>
      </div>
      <div class="flex items-center space-x-1">
        <div class="w-2 h-2 bg-slate-400 rounded-full"></div>
        <span class="text-slate-400">2nd Place</span>
      </div>
      <div class="flex items-center space-x-1">
        <div class="w-2 h-2 bg-amber-600 rounded-full"></div>
        <span class="text-slate-400">3rd Place</span>
      </div>
    </div>
  </div>
  
  <div class="space-y-3">
    <!-- 1st Place -->
    <div class="bg-gradient-to-r from-yellow-500/10 to-transparent border border-yellow-500/30 rounded-lg p-4 hover:from-yellow-500/20 transition-all">
      <div class="flex items-center space-x-4">
        <div class="text-2xl">🥇</div>
        <div class="flex-1">
          <div class="flex items-center space-x-2 mb-2">
            <span class="text-xl">💎</span>
            <span class="font-semibold text-slate-100">Google Gemini</span>
          </div>
          <div class="grid grid-cols-4 gap-4 text-sm">
            <div>
              <div class="text-slate-400 text-xs uppercase">Requests</div>
              <div class="font-semibold text-slate-100">156</div>
            </div>
            <div>
              <div class="text-slate-400 text-xs uppercase">Success Rate</div>
              <div class="font-semibold text-emerald-400">98.7%</div>
            </div>
            <div>
              <div class="text-slate-400 text-xs uppercase">Avg Speed</div>
              <div class="font-semibold text-blue-400">245ms</div>
            </div>
            <div>
              <div class="text-slate-400 text-xs uppercase">Failures</div>
              <div class="font-semibold text-red-400">2</div>
            </div>
          </div>
        </div>
        <div class="bg-emerald-500 text-white px-3 py-1 rounded-full text-xs font-bold">
          EXCELLENT
        </div>
      </div>
    </div>
    
    <!-- 2nd Place -->
    <div class="bg-gradient-to-r from-slate-400/10 to-transparent border border-slate-400/30 rounded-lg p-4 hover:from-slate-400/20 transition-all">
      <!-- Similar structure with 🥈 and different colors -->
    </div>
    
    <!-- 3rd Place -->
    <div class="bg-gradient-to-r from-amber-600/10 to-transparent border border-amber-600/30 rounded-lg p-4 hover:from-amber-600/20 transition-all">
      <!-- Similar structure with 🥉 and different colors -->
    </div>
  </div>
</div>
```

### 7. Circuit Breaker Status
```html
<div class="bg-slate-800 rounded-lg border border-slate-700 p-6">
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-lg font-semibold text-slate-100">⚡ Circuit Breaker Status</h3>
    <button class="bg-blue-600 hover:bg-blue-700 text-white text-sm px-3 py-1 rounded transition-colors">
      🔄 Reset All
    </button>
  </div>
  
  <div class="space-y-3">
    <!-- Closed State -->
    <div class="bg-slate-700 rounded-lg p-4 border-l-4 border-emerald-500">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <span class="text-xl">💎</span>
          <div>
            <div class="font-semibold text-slate-100">Google Gemini</div>
            <div class="flex items-center space-x-2">
              <span class="bg-emerald-500 text-white px-2 py-1 rounded-full text-xs font-bold uppercase">Closed</span>
            </div>
          </div>
        </div>
        <div class="text-right text-sm">
          <div class="text-slate-400">Failures: <span class="text-slate-100 font-medium">0/5</span></div>
          <div class="text-slate-400">Success Rate: <span class="text-emerald-400 font-medium">100%</span></div>
        </div>
      </div>
    </div>
    
    <!-- Open State -->
    <div class="bg-slate-700 rounded-lg p-4 border-l-4 border-red-500 animate-pulse">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <span class="text-xl">🧠</span>
          <div>
            <div class="font-semibold text-slate-100">Cohere</div>
            <div class="flex items-center space-x-2">
              <span class="bg-red-500 text-white px-2 py-1 rounded-full text-xs font-bold uppercase">Open</span>
            </div>
          </div>
        </div>
        <div class="text-right text-sm">
          <div class="text-slate-400">Failures: <span class="text-red-400 font-medium">5/5</span></div>
          <div class="text-slate-400">Next Retry: <span class="text-amber-400 font-medium">45s</span></div>
        </div>
      </div>
    </div>
    
    <!-- Half-Open State -->
    <div class="bg-slate-700 rounded-lg p-4 border-l-4 border-amber-500">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <span class="text-xl">🤗</span>
          <div>
            <div class="font-semibold text-slate-100">Hugging Face</div>
            <div class="flex items-center space-x-2">
              <span class="bg-amber-500 text-white px-2 py-1 rounded-full text-xs font-bold uppercase">Half-Open</span>
            </div>
          </div>
        </div>
        <div class="text-right text-sm">
          <div class="text-slate-400">Testing: <span class="text-amber-400 font-medium">1/3</span></div>
          <div class="text-slate-400">Success Rate: <span class="text-slate-100 font-medium">33%</span></div>
        </div>
      </div>
    </div>
  </div>
</div>
```

### 8. Automation Controls
```html
<div class="bg-slate-800 rounded-lg border border-slate-700 p-6">
  <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 sm:space-x-4">
    <!-- Automation Toggle -->
    <div class="flex items-center space-x-3">
      <button id="automationToggle" class="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-4 py-2 rounded-md transition-colors flex items-center space-x-2">
        <span>🔄</span>
        <span>Start Auto Requests</span>
      </button>
      <div class="text-sm">
        <div class="font-medium text-slate-100">Status: <span class="text-emerald-400">Stopped</span></div>
        <div class="text-slate-400">0 requests sent</div>
      </div>
    </div>
    
    <!-- Service Selection -->
    <div class="flex items-center space-x-3">
      <label class="text-sm font-medium text-slate-300">Target Service:</label>
      <select class="bg-slate-700 border border-slate-600 rounded-md px-3 py-2 text-slate-100 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="all">🌐 All Services (Round Robin)</option>
        <option value="gemini">💎 Google Gemini Only</option>
        <option value="cohere">🧠 Cohere Only</option>
        <option value="huggingface">🤗 Hugging Face Only</option>
      </select>
    </div>
    
    <!-- Interval Selection -->
    <div class="flex items-center space-x-3">
      <label class="text-sm font-medium text-slate-300">Interval:</label>
      <select class="bg-slate-700 border border-slate-600 rounded-md px-3 py-2 text-slate-100 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="5000">5 seconds</option>
        <option value="10000" selected>10 seconds</option>
        <option value="30000">30 seconds</option>
        <option value="60000">1 minute</option>
      </select>
    </div>
  </div>
</div>
```

---

## Interactive Elements & States

### Button States
```html
<!-- Primary Button -->
<button class="bg-blue-600 hover:bg-blue-700 active:bg-blue-800 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-semibold px-4 py-2 rounded-md transition-all duration-200 transform hover:scale-105 active:scale-95">
  Primary Action
</button>

<!-- Danger Button -->
<button class="bg-red-600 hover:bg-red-700 active:bg-red-800 text-white font-semibold px-4 py-2 rounded-md transition-all duration-200 transform hover:scale-105 active:scale-95">
  Danger Action
</button>

<!-- Secondary Button -->
<button class="bg-slate-600 hover:bg-slate-700 active:bg-slate-800 text-white font-semibold px-4 py-2 rounded-md transition-all duration-200">
  Secondary Action
</button>

<!-- Ghost Button -->
<button class="border border-slate-600 hover:border-slate-500 hover:bg-slate-700 text-slate-300 hover:text-slate-100 font-semibold px-4 py-2 rounded-md transition-all duration-200">
  Ghost Action
</button>
```

### Form Elements
```html
<!-- Select Dropdown -->
<select class="w-full bg-slate-700 border border-slate-600 rounded-md px-3 py-2 text-slate-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
  <option>Select option</option>
</select>

<!-- Text Input -->
<input type="text" class="w-full bg-slate-700 border border-slate-600 rounded-md px-3 py-2 text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" placeholder="Enter value">

<!-- Range Slider -->
<input type="range" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer slider focus:outline-none focus:ring-2 focus:ring-blue-500">

<!-- Custom Slider Styles -->
<style>
.slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #1e293b;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #1e293b;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
</style>
```

### Loading States
```html
<!-- Loading Spinner -->
<div class="flex items-center justify-center space-x-2">
  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
  <span class="text-slate-400">Loading...</span>
</div>

<!-- Skeleton Loading -->
<div class="animate-pulse">
  <div class="h-4 bg-slate-700 rounded w-3/4 mb-2"></div>
  <div class="h-4 bg-slate-700 rounded w-1/2"></div>
</div>

<!-- Pulse Animation for Live Data -->
<div class="animate-pulse bg-emerald-500 w-2 h-2 rounded-full"></div>
```

### Status Indicators
```html
<!-- Success Status -->
<div class="flex items-center space-x-2">
  <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
  <span class="text-emerald-500 font-medium">Healthy</span>
</div>

<!-- Warning Status -->
<div class="flex items-center space-x-2">
  <div class="w-2 h-2 bg-amber-500 rounded-full animate-pulse"></div>
  <span class="text-amber-500 font-medium">Warning</span>
</div>

<!-- Error Status -->
<div class="flex items-center space-x-2">
  <div class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
  <span class="text-red-500 font-medium">Error</span>
</div>

<!-- Unknown Status -->
<div class="flex items-center space-x-2">
  <div class="w-2 h-2 bg-slate-500 rounded-full"></div>
  <span class="text-slate-500 font-medium">Unknown</span>
</div>
```

---

## Responsive Design Patterns

### Mobile Layout (< 768px)
```html
<!-- Single column, stacked layout -->
<div class="space-y-4">
  <!-- Header: Simplified, vertical stack -->
  <header class="bg-slate-800 p-4">
    <h1 class="text-lg font-bold mb-2">AI Resilience Monitor</h1>
    <div class="flex items-center space-x-2">
      <div class="w-2 h-2 bg-emerald-500 rounded-full"></div>
      <span class="text-sm text-slate-300">Connected</span>
    </div>
  </header>
  
  <!-- Metrics: 2x2 grid -->
  <div class="grid grid-cols-2 gap-3 px-4">
    <div class="bg-slate-800 p-4 rounded-lg">
      <div class="text-2xl font-bold text-blue-400">1.2K</div>
      <div class="text-xs text-slate-400">Requests</div>
    </div>
    <!-- More metric cards -->
  </div>
  
  <!-- Services: Single column -->
  <div class="space-y-3 px-4">
    <!-- Service cards stacked -->
  </div>
</div>
```

### Tablet Layout (768px - 1024px)
```html
<!-- Two column layout -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
  <div class="space-y-6">
    <!-- Left column content -->
  </div>
  <div class="space-y-6">
    <!-- Right column content -->
  </div>
</div>
```

### Desktop Layout (> 1024px)
```html
<!-- Full 12-column grid -->
<div class="grid grid-cols-12 gap-6">
  <div class="col-span-8 space-y-6">
    <!-- Main content area -->
  </div>
  <div class="col-span-4 space-y-6">
    <!-- Sidebar content -->
  </div>
</div>
```

---

## Animation & Transitions

### CSS Animations (Tailwind Classes)
```css
/* Fade In/Out */
.fade-in { @apply opacity-0 animate-fade-in; }
.fade-out { @apply opacity-100 animate-fade-out; }

/* Slide Animations */
.slide-in-right { @apply transform translate-x-full animate-slide-in-right; }
.slide-out-right { @apply transform translate-x-0 animate-slide-out-right; }

/* Scale Animations */
.scale-in { @apply transform scale-95 animate-scale-in; }
.scale-out { @apply transform scale-100 animate-scale-out; }

/* Pulse for Live Data */
.pulse-slow { @apply animate-pulse; }
.pulse-fast { animation: pulse 1s ease-in-out infinite; }

/* Bounce for Notifications */
.bounce-in { @apply animate-bounce; }

/* Spin for Loading */
.spin { @apply animate-spin; }
```

### Custom Keyframes
```css
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-in-right {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

@keyframes scale-in {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.5); }
  50% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.8); }
}
```

### Transition Classes
```html
<!-- Hover Transitions -->
<div class="transition-all duration-200 hover:scale-105 hover:shadow-lg">
  Hover to scale and shadow
</div>

<!-- Color Transitions -->
<button class="bg-blue-600 hover:bg-blue-700 transition-colors duration-200">
  Color transition
</button>

<!-- Transform Transitions -->
<div class="transform transition-transform duration-300 hover:rotate-3 hover:scale-110">
  Transform on hover
</div>

<!-- Opacity Transitions -->
<div class="opacity-50 hover:opacity-100 transition-opacity duration-200">
  Fade in on hover
</div>
```

---

## Accessibility Features

### ARIA Labels & Roles
```html
<!-- Screen Reader Support -->
<button aria-label="Start automated testing" role="button">
  🔄 Start Auto Requests
</button>

<!-- Status Announcements -->
<div aria-live="polite" aria-atomic="true" id="statusAnnouncements">
  <!-- Dynamic status updates -->
</div>

<!-- Progress Indicators -->
<div role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" aria-label="Chaos experiment progress">
  <div class="bg-blue-600 h-2 rounded" style="width: 75%"></div>
</div>

<!-- Form Labels -->
<label for="chaosService" class="block text-sm font-medium text-slate-300">
  Target Service
</label>
<select id="chaosService" aria-describedby="chaosServiceHelp">
  <!-- Options -->
</select>
<div id="chaosServiceHelp" class="text-xs text-slate-400">
  Select which AI service to target for chaos experiments
</div>
```

### Keyboard Navigation
```html
<!-- Focus Styles -->
<button class="focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-slate-800 focus:outline-none">
  Keyboard accessible button
</button>

<!-- Tab Index Management -->
<div tabindex="0" class="focus:ring-2 focus:ring-blue-500 focus:outline-none">
  Focusable container
</div>

<!-- Skip Links -->
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-600 text-white px-4 py-2 rounded">
  Skip to main content
</a>
```

### Color Contrast & Readability
```html
<!-- High Contrast Text -->
<div class="text-slate-100 bg-slate-900">High contrast text</div>
<div class="text-slate-900 bg-slate-100">Inverted high contrast</div>

<!-- Status Colors with Sufficient Contrast -->
<span class="text-emerald-400 bg-slate-800">Success (4.5:1 contrast)</span>
<span class="text-red-400 bg-slate-800">Error (4.5:1 contrast)</span>
<span class="text-amber-400 bg-slate-800">Warning (4.5:1 contrast)</span>

<!-- Alternative Text for Icons -->
<span aria-hidden="true">🚀</span>
<span class="sr-only">Rocket icon indicating launch</span>
```

---

## Performance Optimizations

### CSS Optimizations
```css
/* Use transform instead of changing layout properties */
.hover-scale {
  transform: scale(1);
  transition: transform 0.2s ease;
}
.hover-scale:hover {
  transform: scale(1.05);
}

/* Optimize animations with will-change */
.animate-element {
  will-change: transform, opacity;
}

/* Use contain for isolated components */
.chart-container {
  contain: layout style paint;
}

/* Optimize repaints with transform3d */
.gpu-accelerated {
  transform: translate3d(0, 0, 0);
}
```

### JavaScript Optimizations
```javascript
// Debounce resize events
const debouncedResize = debounce(() => {
  updateChartSizes();
}, 250);

window.addEventListener('resize', debouncedResize);

// Use requestAnimationFrame for smooth animations
function updateMetrics() {
  requestAnimationFrame(() => {
    // Update DOM elements
    updateMetricValues();
  });
}

// Lazy load charts
const chartObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      initializeChart(entry.target);
      chartObserver.unobserve(entry.target);
    }
  });
});

// Virtual scrolling for large lists
function renderVisibleItems(startIndex, endIndex) {
  const visibleItems = data.slice(startIndex, endIndex);
  return visibleItems.map(item => renderItem(item));
}
```

---

## Chart.js Integration

### Chart Styling for Dark Theme
```javascript
const chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#f1f5f9', // text-slate-100
        font: {
          family: 'Inter, system-ui, sans-serif',
          size: 12
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(15, 23, 42, 0.95)', // bg-slate-900
      titleColor: '#f1f5f9', // text-slate-100
      bodyColor: '#f1f5f9', // text-slate-100
      borderColor: '#3b82f6', // border-blue-500
      borderWidth: 1,
      cornerRadius: 8,
      displayColors: true,
      titleFont: {
        family: 'Inter, system-ui, sans-serif',
        size: 13,
        weight: 'bold'
      },
      bodyFont: {
        family: 'Inter, system-ui, sans-serif',
        size: 12
      }
    }
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(148, 163, 184, 0.1)', // slate-400 with opacity
        borderColor: '#334155' // border-slate-700
      },
      ticks: {
        color: '#94a3b8', // text-slate-400
        font: {
          family: 'Inter, system-ui, sans-serif',
          size: 11
        }
      },
      title: {
        color: '#94a3b8', // text-slate-400
        font: {
          family: 'Inter, system-ui, sans-serif',
          size: 12,
          weight: 'bold'
        }
      }
    },
    y: {
      grid: {
        color: 'rgba(148, 163, 184, 0.1)', // slate-400 with opacity
        borderColor: '#334155' // border-slate-700
      },
      ticks: {
        color: '#94a3b8', // text-slate-400
        font: {
          family: 'Inter, system-ui, sans-serif',
          size: 11
        }
      },
      title: {
        color: '#94a3b8', // text-slate-400
        font: {
          family: 'Inter, system-ui, sans-serif',
          size: 12,
          weight: 'bold'
        }
      }
    }
  }
};

// Performance Chart Configuration
const performanceChartConfig = {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Response Time (ms)',
      data: [],
      borderColor: '#3b82f6', // blue-500
      backgroundColor: 'rgba(59, 130, 246, 0.1)', // blue-500 with opacity
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#3b82f6',
      pointBorderColor: '#1e293b', // slate-800
      pointBorderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6
    }]
  },
  options: {
    ...chartDefaults,
    scales: {
      ...chartDefaults.scales,
      y: {
        ...chartDefaults.scales.y,
        beginAtZero: true,
        title: {
          ...chartDefaults.scales.y.title,
          display: true,
          text: 'Response Time (ms)'
        }
      }
    }
  }
};

// Multi-Service Latency Chart
const latencyChartConfig = {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        label: 'Gemini',
        data: [],
        borderColor: '#10b981', // emerald-500
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderWidth: 2,
        tension: 0.4
      },
      {
        label: 'Cohere',
        data: [],
        borderColor: '#f59e0b', // amber-500
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        borderWidth: 2,
        tension: 0.4
      },
      {
        label: 'Hugging Face',
        data: [],
        borderColor: '#8b5cf6', // violet-500
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        borderWidth: 2,
        tension: 0.4
      }
    ]
  },
  options: {
    ...chartDefaults,
    interaction: {
      intersect: false,
      mode: 'index'
    }
  }
};
```

---

## Implementation Guidelines

### File Structure
```
templates/
├── dashboard.html              # Main dashboard template
├── components/                 # Reusable component templates
│   ├── header.html
│   ├── metric-card.html
│   ├── service-card.html
│   ├── chaos-panel.html
│   ├── chart-card.html
│   └── leaderboard.html
├── layouts/                    # Base layouts
│   └── base.html
└── partials/                   # Partial templates
    ├── navigation.html
    └── footer.html

static/
├── css/
│   ├── tailwind.css           # Compiled Tailwind CSS
│   ├── custom.css             # Custom styles and overrides
│   └── components.css         # Component-specific styles
├── js/
│   ├── dashboard.js           # Main dashboard JavaScript
│   ├── charts.js              # Chart.js configurations
│   ├── chaos.js               # Chaos engineering controls
│   └── utils.js               # Utility functions
└── images/
    └── icons/                 # Custom icons if needed
```

### Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        slate: {
          750: '#293548', // Custom slate variant
          850: '#1a202c'  // Custom slate variant
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' }
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' }
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 5px rgba(59, 130, 246, 0.5)' },
          '50%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.8)' }
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
}
```

### Build Process
```json
{
  "scripts": {
    "build-css": "tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.css --watch",
    "build-css-prod": "tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.css --minify",
    "dev": "concurrently \"npm run build-css\" \"python app.py --debug\"",
    "build": "npm run build-css-prod"
  },
  "devDependencies": {
    "tailwindcss": "^3.3.0",
    "@tailwindcss/forms": "^0.5.0",
    "@tailwindcss/typography": "^0.5.0",
    "concurrently": "^8.0.0"
  }
}
```

### Integration Steps
1. **Install Tailwind CSS**: Set up Tailwind with PostCSS and configure the build process
2. **Create Base Template**: Build the main dashboard.html with Tailwind classes
3. **Component Migration**: Convert existing components to Tailwind-based implementations
4. **JavaScript Integration**: Update JavaScript to work with new class names and structure
5. **Chart.js Styling**: Apply dark theme styling to all charts
6. **Responsive Testing**: Test across all breakpoints and devices
7. **Accessibility Audit**: Ensure all components meet WCAG 2.1 AA standards
8. **Performance Testing**: Optimize CSS bundle size and runtime performance

---

## Browser Support

### Target Browsers
- **Chrome**: 90+ (95% of users)
- **Firefox**: 88+ (3% of users)
- **Safari**: 14+ (2% of users)
- **Edge**: 90+ (1% of users)

### Fallbacks & Progressive Enhancement
```css
/* CSS Grid with Flexbox fallback */
.grid-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

@supports (display: grid) {
  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
}

/* Custom properties with fallbacks */
.card {
  background-color: #1e293b; /* Fallback */
  background-color: var(--slate-800, #1e293b);
}

/* Modern features with fallbacks */
.backdrop-blur {
  background-color: rgba(15, 23, 42, 0.8); /* Fallback */
}

@supports (backdrop-filter: blur(10px)) {
  .backdrop-blur {
    backdrop-filter: blur(10px);
    background-color: rgba(15, 23, 42, 0.6);
  }
}
```

---

## Testing Strategy

### Visual Regression Testing
- Screenshot comparison across breakpoints
- Component isolation testing
- Dark theme consistency validation
- Animation and transition verification

### Accessibility Testing
- Screen reader compatibility (NVDA, JAWS, VoiceOver)
- Keyboard navigation flow
- Color contrast validation (4.5:1 minimum)
- Focus management and indicators

### Performance Testing
- Lighthouse audit (90+ score target)
- Core Web Vitals optimization
- Bundle size analysis
- Runtime performance profiling

### Cross-Browser Testing
- Automated testing with Playwright/Cypress
- Manual testing on target browsers
- Mobile device testing (iOS Safari, Chrome Mobile)
- Feature detection and fallback validation

---

This specification provides a comprehensive foundation for implementing a modern, accessible, and performant Tailwind CSS-based frontend for the AI Resilience Monitor. The design system ensures consistency, the component library provides reusable patterns, and the implementation guidelines offer a clear path forward for development.