# Flowchart Creation Prompts - AI Resilience Monitor Procedures
**Date:** October 6, 2025  
**Project:** AI Service Resilience Monitor  
**Total Procedures:** 4 Core Procedures

---

## How to Use These Prompts

### **Option 1: AI Tools (ChatGPT, Claude, etc.)**
Copy the prompt → Paste into ChatGPT/Claude → Request Mermaid diagram code → Paste code into https://mermaid.live/ → Export as PNG

### **Option 2: Draw.io / Lucidchart**
Use the detailed steps in each prompt to manually create flowchart

### **Option 3: PowerPoint / Google Slides**
Follow the component descriptions to build flowchart using shapes

---

## Procedure 1: Circuit Breaker Pattern

### 🎨 AI Prompt for Flowchart Generation

```
Create a detailed flowchart for a Circuit Breaker pattern used in an AI service resilience monitoring system. The flowchart should show:

START
↓
[Input: Service Name, API Request]
↓
{Decision: Check Circuit State}
├─ If CLOSED:
│   ↓
│   [Execute API Request to AI Service]
│   ↓
│   {Decision: Request Successful?}
│   ├─ Yes:
│   │   ↓
│   │   [Reset Failure Count = 0]
│   │   ↓
│   │   [Record Success Metrics (latency, timestamp)]
│   │   ↓
│   │   [Return Response to Client]
│   │   ↓
│   │   END
│   │
│   └─ No (Error/Timeout):
│       ↓
│       [Increment Failure Count]
│       ↓
│       [Record Failure Metrics (error type, timestamp)]
│       ↓
│       {Decision: Failure Count >= Threshold (5)?}
│       ├─ Yes:
│       │   ↓
│       │   [Change State to OPEN]
│       │   ↓
│       │   [Record Last Failure Time]
│       │   ↓
│       │   [Throw Circuit Breaker Error]
│       │   ↓
│       │   END
│       │
│       └─ No:
│           ↓
│           [Keep State CLOSED]
│           ↓
│           [Throw Original Error]
│           ↓
│           END
│
├─ If OPEN:
│   ↓
│   [Calculate: Time Since Last Failure]
│   ↓
│   {Decision: Time Elapsed > Timeout (60s)?}
│   ├─ Yes:
│   │   ↓
│   │   [Change State to HALF_OPEN]
│   │   ↓
│   │   [Allow ONE Test Request]
│   │   ↓
│   │   [Execute API Request]
│   │   ↓
│   │   {Decision: Test Request Successful?}
│   │   ├─ Yes:
│   │   │   ↓
│   │   │   [Change State to CLOSED]
│   │   │   ↓
│   │   │   [Reset Failure Count = 0]
│   │   │   ↓
│   │   │   [Return Response]
│   │   │   ↓
│   │   │   END
│   │   │
│   │   └─ No:
│   │       ↓
│   │       [Keep State OPEN]
│   │       ↓
│   │       [Record Last Failure Time (reset timeout)]
│   │       ↓
│   │       [Throw Error]
│   │       ↓
│   │       END
│   │
│   └─ No:
│       ↓
│       [Block Request Immediately]
│       ↓
│       [Throw "Circuit Breaker Open" Error]
│       ↓
│       END
│
└─ If HALF_OPEN:
    ↓
    [Allow Test Request]
    ↓
    [Execute API Request]
    ↓
    {Decision: Request Successful?}
    ├─ Yes:
    │   ↓
    │   [Change State to CLOSED]
    │   ↓
    │   [Reset Failure Count]
    │   ↓
    │   [Return Response]
    │   ↓
    │   END
    │
    └─ No:
        ↓
        [Change State back to OPEN]
        ↓
        [Record Last Failure Time]
        ↓
        [Throw Error]
        ↓
        END

Use these symbols:
- START/END: Rounded rectangles (oval)
- Process boxes: Rectangles
- Decisions: Diamonds
- Data: Parallelograms
- Arrows: Solid lines with arrowheads
- States: Bold boxes with colors (CLOSED=Green, OPEN=Red, HALF_OPEN=Yellow)

Color scheme:
- Success paths: Green
- Failure paths: Red
- Decision paths: Blue
- State transitions: Orange

Generate Mermaid flowchart code for this.
```

---

### 📊 Mermaid Code (Copy-Paste Ready)

```mermaid
flowchart TD
    Start([START: API Request]) --> Input[/"Input: Service Name, Request"/]
    Input --> CheckState{Check Circuit<br/>State}
    
    CheckState -->|CLOSED| ExecReq[Execute API Request]
    ExecReq --> Success{Request<br/>Successful?}
    
    Success -->|Yes| Reset[Reset Failure Count = 0]
    Reset --> RecordSuccess[Record Success Metrics]
    RecordSuccess --> Return1[Return Response]
    Return1 --> End1([END])
    
    Success -->|No| IncFail[Increment Failure Count]
    IncFail --> RecordFail[Record Failure Metrics]
    RecordFail --> CheckThreshold{Failure Count<br/>>= 5?}
    
    CheckThreshold -->|Yes| ToOpen[Change State to OPEN]
    ToOpen --> RecordTime[Record Last Failure Time]
    RecordTime --> ThrowCB[Throw Circuit Breaker Error]
    ThrowCB --> End2([END])
    
    CheckThreshold -->|No| KeepClosed[Keep State CLOSED]
    KeepClosed --> ThrowOrig[Throw Original Error]
    ThrowOrig --> End3([END])
    
    CheckState -->|OPEN| CalcTime[Calculate Time Since Last Failure]
    CalcTime --> CheckTimeout{Time Elapsed<br/>> 60s?}
    
    CheckTimeout -->|Yes| ToHalfOpen[Change State to HALF_OPEN]
    ToHalfOpen --> TestReq[Allow ONE Test Request]
    TestReq --> ExecTest[Execute API Request]
    ExecTest --> TestSuccess{Test Successful?}
    
    TestSuccess -->|Yes| ToClosed1[Change State to CLOSED]
    ToClosed1 --> ResetCount1[Reset Failure Count]
    ResetCount1 --> Return2[Return Response]
    Return2 --> End4([END])
    
    TestSuccess -->|No| StayOpen[Keep State OPEN]
    StayOpen --> ResetTimer[Reset Last Failure Time]
    ResetTimer --> ThrowErr1[Throw Error]
    ThrowErr1 --> End5([END])
    
    CheckTimeout -->|No| BlockReq[Block Request Immediately]
    BlockReq --> ThrowOpen[Throw Circuit Breaker Open Error]
    ThrowOpen --> End6([END])
    
    CheckState -->|HALF_OPEN| AllowTest[Allow Test Request]
    AllowTest --> ExecHalf[Execute API Request]
    ExecHalf --> HalfSuccess{Request<br/>Successful?}
    
    HalfSuccess -->|Yes| ToClosed2[Change State to CLOSED]
    ToClosed2 --> ResetCount2[Reset Failure Count]
    ResetCount2 --> Return3[Return Response]
    Return3 --> End7([END])
    
    HalfSuccess -->|No| BackToOpen[Change State back to OPEN]
    BackToOpen --> RecordTime2[Record Last Failure Time]
    RecordTime2 --> ThrowErr2[Throw Error]
    ThrowErr2 --> End8([END])
    
    style Start fill:#90EE90
    style End1 fill:#90EE90
    style End4 fill:#90EE90
    style End7 fill:#90EE90
    style End2 fill:#FFB6C1
    style End3 fill:#FFB6C1
    style End5 fill:#FFB6C1
    style End6 fill:#FFB6C1
    style End8 fill:#FFB6C1
    style ToOpen fill:#FF6B6B
    style ToClosed1 fill:#51CF66
    style ToClosed2 fill:#51CF66
    style ToHalfOpen fill:#FFD93D
```

---

## Procedure 2: Metrics Collection & Aggregation

### 🎨 AI Prompt for Flowchart Generation

```
Create a flowchart for the Metrics Collection and Aggregation procedure in an AI resilience monitoring system. Show:

START
↓
[Trigger: Timer (5-second interval) OR API Call]
↓
[Initialize Empty Metrics Object]
↓
[Get Current Timestamp]
↓
[Read metricsHistory from Backend]
↓
[Process: Calculate Total Requests]
├─ totalRequests = metricsHistory.totalRequests
↓
[Process: Calculate Successful Requests]
├─ successfulRequests = metricsHistory.successfulRequests
↓
[Process: Calculate Failed Requests]
├─ failedRequests = metricsHistory.failedRequests
↓
[Calculate: Success Rate %]
├─ successRate = (successfulRequests / totalRequests) × 100
↓
[Calculate: Average Latency]
├─ avgLatency = totalLatency / successfulRequests
↓
[Calculate: System Uptime]
├─ uptime = currentTime - serverStartTime
↓
[Loop: For Each AI Service (Gemini, Cohere, Hugging Face)]
│
├─ [Get Service-Specific Data]
│   ├─ service.requests
│   ├─ service.failures
│   ├─ service.successRate
│   ├─ service.avgLatency
│   ├─ service.status (up/down)
│   ↓
├─ [Calculate Service Health Score]
│   ├─ uptimeScore = (uptime / maxUptime) × 40
│   ├─ successScore = (successRate / 100) × 40
│   ├─ speedScore = (1 - avgLatency / maxLatency) × 20
│   ├─ healthScore = uptimeScore + successScore + speedScore
│   ↓
├─ [Store Service Metrics in Object]
│   └─ aiServices[serviceName] = {health, latency, success, status}
↓
[Aggregate All Metrics into Response Object]
├─ {
│     totalRequests,
│     successfulRequests,
│     failedRequests,
│     successRate,
│     avgLatency,
│     uptime,
│     aiServices: {...}
│   }
↓
[Send Metrics to Frontend Dashboard]
↓
[Update Charts and Health Scores]
↓
[Store in localStorage (last 500 requests)]
↓
END

Use standard flowchart symbols with color coding for different metric types.
Generate Mermaid code.
```

---

### 📊 Mermaid Code (Copy-Paste Ready)

```mermaid
flowchart TD
    Start([START: Metrics Collection]) --> Trigger[Trigger: 5s Timer OR API Call]
    Trigger --> Init[Initialize Empty Metrics Object]
    Init --> GetTime[Get Current Timestamp]
    GetTime --> ReadHist[Read metricsHistory from Backend]
    
    ReadHist --> CalcTotal[Calculate Total Requests<br/>totalRequests = metricsHistory.totalRequests]
    CalcTotal --> CalcSuccess[Calculate Successful Requests<br/>successfulRequests = metricsHistory.successfulRequests]
    CalcSuccess --> CalcFail[Calculate Failed Requests<br/>failedRequests = metricsHistory.failedRequests]
    
    CalcFail --> CalcRate[Calculate Success Rate<br/>successRate = successful / total × 100]
    CalcRate --> CalcLatency[Calculate Avg Latency<br/>avgLatency = totalLatency / successful]
    CalcLatency --> CalcUptime[Calculate System Uptime<br/>uptime = now - startTime]
    
    CalcUptime --> LoopStart{For Each AI Service}
    LoopStart -->|Gemini| GetService1[Get Service Data]
    LoopStart -->|Cohere| GetService2[Get Service Data]
    LoopStart -->|HuggingFace| GetService3[Get Service Data]
    
    GetService1 --> CalcHealth1[Calculate Health Score]
    GetService2 --> CalcHealth2[Calculate Health Score]
    GetService3 --> CalcHealth3[Calculate Health Score]
    
    CalcHealth1 --> Store1[Store in aiServices Object]
    CalcHealth2 --> Store2[Store in aiServices Object]
    CalcHealth3 --> Store3[Store in aiServices Object]
    
    Store1 --> Aggregate[Aggregate All Metrics]
    Store2 --> Aggregate
    Store3 --> Aggregate
    
    Aggregate --> Response[Build Response Object:<br/>totalRequests, successRate,<br/>avgLatency, uptime, aiServices]
    Response --> Send[Send Metrics to Frontend]
    Send --> Update[Update Dashboard Charts & Scores]
    Update --> LocalStore[Store in localStorage<br/>last 500 requests]
    LocalStore --> End([END])
    
    style Start fill:#4ECDC4
    style End fill:#4ECDC4
    style CalcRate fill:#FFE66D
    style CalcHealth1 fill:#FF6B6B
    style CalcHealth2 fill:#FF6B6B
    style CalcHealth3 fill:#FF6B6B
    style Update fill:#95E1D3
```

---

## Procedure 3: Health Score Calculation

### 🎨 AI Prompt for Flowchart Generation

```
Create a flowchart for AI Service Health Score Calculation with a weighted scoring algorithm (40% uptime + 40% success rate + 20% speed). Show:

START
↓
[Input: Service Name (Gemini/Cohere/HuggingFace)]
↓
[Fetch Service Metrics from Backend]
├─ currentUptime (seconds)
├─ successRate (percentage)
├─ avgLatency (milliseconds)
├─ totalRequests
↓
{Decision: Has Service Been Tested?}
├─ No (totalRequests = 0):
│   ↓
│   [Set Health Score = 0]
│   ↓
│   [Set Status = "Not Tested"]
│   ↓
│   [Return Score]
│   ↓
│   END
│
└─ Yes (totalRequests > 0):
    ↓
    [Component 1: Calculate Uptime Score]
    ├─ maxExpectedUptime = currentSessionDuration
    ├─ uptimePercentage = (currentUptime / maxExpectedUptime) × 100
    ├─ uptimeScore = uptimePercentage × 0.40
    ↓
    [Component 2: Calculate Success Score]
    ├─ successScore = successRate × 0.40
    ↓
    [Component 3: Calculate Speed Score]
    ├─ maxAcceptableLatency = 5000ms (benchmark)
    ├─ speedPercentage = ((maxLatency - avgLatency) / maxLatency) × 100
    ├─ speedScore = speedPercentage × 0.20
    ↓
    [Aggregate: Calculate Total Health Score]
    ├─ healthScore = uptimeScore + successScore + speedScore
    ↓
    [Normalize: Ensure Score is 0-100]
    ├─ healthScore = Math.max(0, Math.min(100, healthScore))
    ↓
    {Decision: Categorize Health Level}
    ├─ If healthScore >= 80:
    │   ↓
    │   [Set Status = "Excellent" (Green)]
    │
    ├─ If healthScore >= 60:
    │   ↓
    │   [Set Status = "Good" (Yellow)]
    │
    ├─ If healthScore >= 40:
    │   ↓
    │   [Set Status = "Warning" (Orange)]
    │
    └─ If healthScore < 40:
        ↓
        [Set Status = "Critical" (Red)]
    ↓
    [Update Service Health Badge in Dashboard]
    ↓
    [Update Health Bar Chart]
    ↓
    [Log Health Score to Analytics]
    ↓
    [Return: {healthScore, status, breakdown: {uptime, success, speed}}]
    ↓
    END

Use color-coded status indicators and show the 40-40-20 weighting visually.
Generate Mermaid code.
```

---

### 📊 Mermaid Code (Copy-Paste Ready)

```mermaid
flowchart TD
    Start([START: Health Score Calculation]) --> Input[/"Input: Service Name<br/>(Gemini/Cohere/HuggingFace)"/]
    Input --> Fetch[Fetch Service Metrics:<br/>uptime, successRate, avgLatency]
    
    Fetch --> Check{Has Service<br/>Been Tested?<br/>totalRequests > 0?}
    
    Check -->|No| SetZero[Set Health Score = 0]
    SetZero --> SetNotTested[Set Status = Not Tested]
    SetNotTested --> Return1[Return Score]
    Return1 --> End1([END])
    
    Check -->|Yes| CalcUptime[Component 1: Uptime Score 40%<br/>uptimeScore = uptime / sessionDuration × 40]
    CalcUptime --> CalcSuccess[Component 2: Success Score 40%<br/>successScore = successRate × 0.40]
    CalcSuccess --> CalcSpeed[Component 3: Speed Score 20%<br/>speedScore = 1 - avgLatency/5000 × 20]
    
    CalcSpeed --> Aggregate[Aggregate Total Health Score<br/>healthScore = uptime + success + speed]
    Aggregate --> Normalize[Normalize: 0 ≤ score ≤ 100]
    
    Normalize --> Categorize{Categorize<br/>Health Level}
    
    Categorize -->|score >= 80| Excellent[Status = EXCELLENT<br/>Color: Green]
    Categorize -->|60 <= score < 80| Good[Status = GOOD<br/>Color: Yellow]
    Categorize -->|40 <= score < 60| Warning[Status = WARNING<br/>Color: Orange]
    Categorize -->|score < 40| Critical[Status = CRITICAL<br/>Color: Red]
    
    Excellent --> Update[Update Dashboard Health Badge]
    Good --> Update
    Warning --> Update
    Critical --> Update
    
    Update --> Chart[Update Health Bar Chart]
    Chart --> Log[Log Health Score to Analytics]
    Log --> Return2[/"Return: {healthScore, status,<br/>breakdown: {uptime, success, speed}}"/]
    Return2 --> End2([END])
    
    style Start fill:#A8E6CF
    style End1 fill:#FFD3B6
    style End2 fill:#A8E6CF
    style CalcUptime fill:#FFAAA5
    style CalcSuccess fill:#FF8B94
    style CalcSpeed fill:#FFDAC1
    style Excellent fill:#51CF66
    style Good fill:#FFD93D
    style Warning fill:#FF922B
    style Critical fill:#FF6B6B
```

---

## Procedure 4: Automated Chaos Testing

### 🎨 AI Prompt for Flowchart Generation

```
Create a flowchart for Automated Chaos Testing procedure that continuously tests AI service resilience. Show:

START
↓
[System Initialization]
↓
[Load Configuration]
├─ testInterval = 10 seconds (configurable)
├─ enabledServices = [Gemini, Cohere, HuggingFace]
├─ testPrompts = ["Test prompt 1", "Test prompt 2", ...]
↓
[Start Automated Testing Loop]
↓
[Wait for Next Interval (10 seconds)]
↓
[Select Random Service]
├─ services = [Gemini, Cohere, HuggingFace]
├─ selectedService = random(services)
↓
[Select Random Test Prompt]
├─ prompts = ["Simple test", "Complex query", ...]
├─ testPrompt = random(prompts)
↓
[Record Start Time]
↓
[Generate Request ID (UUID)]
↓
[Check Circuit Breaker State for Selected Service]
↓
{Decision: Circuit Breaker Open?}
├─ Yes:
│   ↓
│   [Skip API Call]
│   ↓
│   [Log: "Request Blocked - Circuit Open"]
│   ↓
│   [Record Failure Metrics]
│   ├─ timestamp
│   ├─ service
│   ├─ status = "blocked"
│   ├─ errorType = "Circuit Breaker Open"
│   ↓
│   [Update Dashboard with Blocked Request]
│   ↓
│   [Go to Next Interval] ───┐
│                            │
└─ No:                       │
    ↓                        │
    [Execute API Request]    │
    ├─ Send POST to /ai endpoint
    ├─ Include: service, prompt
    ↓                        │
    {Decision: Request Successful?}
    │                        │
    ├─ Yes:                  │
    │   ↓                    │
    │   [Record End Time]    │
    │   ↓                    │
    │   [Calculate Latency = endTime - startTime]
    │   ↓                    │
    │   [Extract Response Data]
    │   ├─ responseText     │
    │   ├─ responseSize     │
    │   ↓                    │
    │   [Log Success Metrics]
    │   ├─ timestamp        │
    │   ├─ service          │
    │   ├─ latency (ms)     │
    │   ├─ status = "success"
    │   ├─ responseSize     │
    │   ↓                    │
    │   [Update Success Counter]
    │   ↓                    │
    │   [Update Latency Chart]
    │   ↓                    │
    │   [Update Health Score Dashboard]
    │   ↓                    │
    │   [Store in Request History (last 500)]
    │   ↓                    │
    │   [Go to Next Interval] ─┤
    │                          │
    └─ No (Error/Timeout):     │
        ↓                      │
        [Record End Time]      │
        ↓                      │
        [Calculate Latency]    │
        ↓                      │
        [Extract Error Details]
        ├─ errorType (timeout, 500, rate limit, etc.)
        ├─ errorMessage        │
        ↓                      │
        [Log Failure Metrics]  │
        ├─ timestamp           │
        ├─ service             │
        ├─ latency             │
        ├─ status = "failure"  │
        ├─ errorType           │
        ├─ errorMessage        │
        ↓                      │
        [Update Failure Counter]
        ↓                      │
        [Update Error Leaderboard]
        ↓                      │
        [Trigger Circuit Breaker Logic]
        ↓                      │
        [Update Dashboard with Error]
        ↓                      │
        [Store in Request History]
        ↓                      │
        [Go to Next Interval] ─┘
        ↓
[Check: Continue Testing?]
├─ If autoTesting enabled: Loop back to "Wait for Next Interval"
└─ If stopped: END

Show the continuous loop nature and error handling paths clearly.
Generate Mermaid code.
```

---

### 📊 Mermaid Code (Copy-Paste Ready)

```mermaid
flowchart TD
    Start([START: Automated Chaos Testing]) --> Init[System Initialization]
    Init --> LoadConfig[Load Configuration:<br/>interval=10s, services, prompts]
    LoadConfig --> LoopStart[Start Automated Testing Loop]
    
    LoopStart --> Wait[Wait for Next Interval 10s]
    Wait --> SelectService[Select Random Service<br/>Gemini/Cohere/HuggingFace]
    SelectService --> SelectPrompt[Select Random Test Prompt]
    SelectPrompt --> RecordStart[Record Start Time]
    RecordStart --> GenID[Generate Request ID UUID]
    GenID --> CheckCB{Circuit Breaker<br/>Open?}
    
    CheckCB -->|Yes| Skip[Skip API Call]
    Skip --> LogBlock[Log: Request Blocked - Circuit Open]
    LogBlock --> RecordBlock[Record Failure Metrics:<br/>timestamp, service, status=blocked]
    RecordBlock --> UpdateBlock[Update Dashboard with Blocked]
    UpdateBlock --> Continue1[Go to Next Interval]
    
    CheckCB -->|No| Execute[Execute API Request<br/>POST /ai endpoint]
    Execute --> ReqSuccess{Request<br/>Successful?}
    
    ReqSuccess -->|Yes| RecordEnd1[Record End Time]
    RecordEnd1 --> CalcLatency1[Calculate Latency<br/>endTime - startTime]
    CalcLatency1 --> Extract1[Extract Response Data:<br/>text, size]
    Extract1 --> LogSuccess[Log Success Metrics:<br/>timestamp, service, latency, status]
    LogSuccess --> IncSuccess[Update Success Counter]
    IncSuccess --> UpdateChart1[Update Latency Chart]
    UpdateChart1 --> UpdateHealth1[Update Health Score Dashboard]
    UpdateHealth1 --> Store1[Store in Request History<br/>last 500 requests]
    Store1 --> Continue2[Go to Next Interval]
    
    ReqSuccess -->|No| RecordEnd2[Record End Time]
    RecordEnd2 --> CalcLatency2[Calculate Latency]
    CalcLatency2 --> Extract2[Extract Error Details:<br/>errorType, message]
    Extract2 --> LogFail[Log Failure Metrics:<br/>timestamp, service, latency,<br/>status=failure, errorType]
    LogFail --> IncFail[Update Failure Counter]
    IncFail --> UpdateError[Update Error Leaderboard]
    UpdateError --> TriggerCB[Trigger Circuit Breaker Logic]
    TriggerCB --> UpdateDash2[Update Dashboard with Error]
    UpdateDash2 --> Store2[Store in Request History]
    Store2 --> Continue3[Go to Next Interval]
    
    Continue1 --> CheckContinue{Continue<br/>Testing?}
    Continue2 --> CheckContinue
    Continue3 --> CheckContinue
    
    CheckContinue -->|Enabled| Wait
    CheckContinue -->|Stopped| End([END])
    
    style Start fill:#A8DADC
    style End fill:#A8DADC
    style Execute fill:#457B9D
    style LogSuccess fill:#51CF66
    style LogFail fill:#FF6B6B
    style CheckCB fill:#F1FAEE
    style CheckContinue fill:#F1FAEE
```

---

## Procedure 5: Predictive Failure Detection (ML-Based) - PROPOSED

### 🎨 AI Prompt for Flowchart Generation

```
Create a flowchart for a Machine Learning-based Predictive Failure Detection system using Z-score anomaly detection. Show:

START
↓
[Trigger: New Metrics Received from Backend]
↓
[Fetch Latency Time Series Data]
├─ Get last 50 latency measurements for each service
↓
[Loop: For Each AI Service]
│
├─ [Extract Recent Latency Window]
│   ├─ recentLatencies = last 20 measurements
│   ↓
├─ {Decision: Enough Data Points?}
│   ├─ No (< 20 data points):
│   │   ↓
│   │   [Skip Prediction - Insufficient Data]
│   │   ↓
│   │   [Continue to Next Service]
│   │
│   └─ Yes (>= 20 data points):
│       ↓
│       [Calculate Statistical Features]
│       ├─ mean = average(recentLatencies)
│       ├─ stdDev = standardDeviation(recentLatencies)
│       ├─ currentLatency = latest measurement
│       ↓
│       [Calculate Z-Score]
│       ├─ zScore = (currentLatency - mean) / stdDev
│       ↓
│       {Decision: Anomaly Detected?}
│       │
│       ├─ If |zScore| > 3 (3-sigma rule):
│       │   ↓
│       │   [ANOMALY DETECTED]
│       │   ↓
│       │   [Classify Anomaly Severity]
│       │   ├─ If zScore > 3: "High Latency Spike"
│       │   ├─ If zScore < -3: "Unusual Fast Response"
│       │   ↓
│       │   [Calculate Failure Probability]
│       │   ├─ probability = |zScore| / 5 (normalized)
│       │   ↓
│       │   [Generate Alert]
│       │   ├─ alertType = "Predictive Failure Warning"
│       │   ├─ message = "Service X showing abnormal latency (Z=4.2)"
│       │   ├─ probability = 84%
│       │   ↓
│       │   {Decision: Preemptive Action Required?}
│       │   │
│       │   ├─ If probability > 80% AND trend is degrading:
│       │   │   ↓
│       │   │   [Preemptive Circuit Breaker Open]
│       │   │   ↓
│       │   │   [Send Alert to Dashboard]
│       │   │   ├─ Show warning banner
│       │   │   ├─ Highlight service in red
│       │   │   ↓
│       │   │   [Log Preemptive Action]
│       │   │   ├─ timestamp
│       │   │   ├─ service
│       │   │   ├─ action = "Preemptive CB Open"
│       │   │   ├─ zScore
│       │   │   ├─ probability
│       │   │   ↓
│       │   │   [Continue to Next Service]
│       │   │
│       │   └─ Else (probability < 80%):
│       │       ↓
│       │       [Send Warning Only (No CB Action)]
│       │       ↓
│       │       [Update Dashboard Trend Indicator]
│       │       ├─ Show "Degrading" status
│       │       ↓
│       │       [Continue to Next Service]
│       │
│       └─ If |zScore| <= 3 (Normal):
│           ↓
│           [Calculate Trend Direction]
│           ├─ Compare last 10 vs previous 10 latencies
│           ├─ If improving: trend = "improving"
│           ├─ If stable: trend = "stable"
│           ├─ If degrading: trend = "degrading"
│           ↓
│           [Update Dashboard Trend Indicator]
│           ↓
│           [Continue to Next Service]
↓
[All Services Processed]
↓
[Update ML Model Metrics Dashboard]
├─ Show Z-scores per service
├─ Show trend indicators
├─ Show anomaly count
↓
[Store Predictions in Analytics]
↓
[Schedule Next Prediction Cycle (every 30s)]
↓
END

Include ML-specific elements like feature calculation and model inference.
Generate Mermaid code.
```

---

### 📊 Mermaid Code (Copy-Paste Ready)

```mermaid
flowchart TD
    Start([START: Predictive Failure Detection]) --> Trigger[Trigger: New Metrics Received]
    Trigger --> Fetch[Fetch Latency Time Series<br/>Last 50 measurements per service]
    
    Fetch --> Loop[Loop: For Each AI Service]
    Loop --> Extract[Extract Recent Window<br/>last 20 latency measurements]
    
    Extract --> CheckData{Enough Data?<br/>>= 20 points}
    CheckData -->|No| Skip[Skip Prediction<br/>Insufficient Data]
    Skip --> NextService1[Continue to Next Service]
    
    CheckData -->|Yes| CalcStats[Calculate Statistical Features:<br/>mean, stdDev, currentLatency]
    CalcStats --> CalcZ[Calculate Z-Score<br/>z = current - mean / stdDev]
    
    CalcZ --> CheckAnomaly{Anomaly<br/>Detected?<br/>z > 3}
    
    CheckAnomaly -->|Yes| Detected[ANOMALY DETECTED]
    Detected --> Classify[Classify Severity:<br/>High Spike z>3 OR Fast z<-3]
    Classify --> CalcProb[Calculate Failure Probability<br/>prob = z / 5 normalized]
    CalcProb --> GenAlert[Generate Alert:<br/>Predictive Failure Warning]
    
    GenAlert --> PreemptCheck{Preemptive<br/>Action<br/>Required?<br/>prob > 80%}
    
    PreemptCheck -->|Yes| PreemptCB[Preemptive Circuit Breaker OPEN]
    PreemptCB --> SendAlert[Send Alert to Dashboard:<br/>warning banner, red highlight]
    SendAlert --> LogAction[Log Preemptive Action:<br/>timestamp, service, zScore, prob]
    LogAction --> NextService2[Continue to Next Service]
    
    PreemptCheck -->|No| WarnOnly[Send Warning Only<br/>No Circuit Breaker Action]
    WarnOnly --> UpdateWarn[Update Dashboard:<br/>Show Degrading Status]
    UpdateWarn --> NextService3[Continue to Next Service]
    
    CheckAnomaly -->|No| CalcTrend[Calculate Trend Direction:<br/>Compare last 10 vs prev 10]
    CalcTrend --> UpdateTrend[Update Dashboard Trend:<br/>improving/stable/degrading]
    UpdateTrend --> NextService4[Continue to Next Service]
    
    NextService1 --> AllDone{All Services<br/>Processed?}
    NextService2 --> AllDone
    NextService3 --> AllDone
    NextService4 --> AllDone
    
    AllDone -->|No| Loop
    AllDone -->|Yes| UpdateML[Update ML Metrics Dashboard:<br/>Z-scores, trends, anomaly count]
    UpdateML --> Store[Store Predictions in Analytics]
    Store --> Schedule[Schedule Next Cycle<br/>every 30 seconds]
    Schedule --> End([END])
    
    style Start fill:#E3F2FD
    style End fill:#E3F2FD
    style Detected fill:#FFCDD2
    style PreemptCB fill:#FF6B6B
    style CalcZ fill:#B39DDB
    style CalcTrend fill:#A5D6A7
```

---

## Quick Reference: Flowchart Symbols

### Standard Symbols:
- **Oval (Rounded Rectangle):** START / END
- **Rectangle:** Process / Action
- **Diamond:** Decision / Condition
- **Parallelogram:** Input / Output / Data
- **Cylinder:** Database / Storage
- **Circle:** Connection point
- **Arrow:** Flow direction

### Color Coding:
- 🟢 **Green:** Success paths, positive outcomes
- 🔴 **Red:** Failures, errors, critical states
- 🟡 **Yellow:** Warnings, pending states
- 🔵 **Blue:** Neutral processes, calculations
- 🟠 **Orange:** State transitions, important decisions

---

## Tools for Creating Flowcharts

### **1. Mermaid Live Editor (Recommended)**
- URL: https://mermaid.live/
- Copy Mermaid code from above
- Paste into editor
- Export as PNG/SVG

### **2. Draw.io (Desktop/Web)**
- URL: https://app.diagrams.net/
- Free, powerful, professional
- Manual creation using drag-drop

### **3. Lucidchart**
- URL: https://www.lucidchart.com/
- Professional diagramming tool
- Templates available

### **4. Microsoft PowerPoint**
- Use Insert → Shapes
- SmartArt for quick diagrams
- Export as image

### **5. ChatGPT / Claude**
- Copy prompts above
- Ask for Mermaid code
- Paste into Mermaid Live

---

## Next Steps

1. ✅ **Copy Mermaid code** for each procedure
2. ✅ **Paste into https://mermaid.live/**
3. ✅ **Export as PNG** (300 DPI recommended)
4. ✅ **Insert into documentation**
5. ✅ **Create algorithms & pseudo code** (see next document)

---

**All 4 flowcharts ready to generate! Use the Mermaid code sections for instant results.** 🚀
