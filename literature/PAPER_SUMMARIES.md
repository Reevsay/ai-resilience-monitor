# Extended Literature Summaries (8 Core Papers)

This document provides structured, implementation-oriented summaries of eight papers most relevant to the AI Resilience Monitor project. For each: Methodology, Core Contributions, Identified Research Gaps, and Actionable Lessons for our system.

## 1. Chaos Engineering: Building Confidence in System Behavior through Experiments (Basiri et al., 2016)
**Methodology:** Hypothesis-driven controlled experiments on production-like systems; define steady-state metrics, introduce real faults (latency, dependency failure), measure deviation.
**Core Contributions:** Formalizes chaos engineering cycle; emphasizes observability maturity as prerequisite; shifts resilience validation from reactive to proactive.
**Research Gaps:** Limited ML-specific failure patterns; no standardized prioritization for experiment selection; lacks automated experiment outcome scoring.
**Actionable for Project:**
- Implement `/experiments` API (CRUD + run) with stored hypothesis & metrics snapshot.
- Tag metrics with `experiment_id` label during injection window.
- Auto-generate experiment report: steady_state_delta, recovery_time_ms, circuit_open_ratio.
- Add experiment prioritization heuristic (risk_score = (historical_incidents + change_velocity) * blast_radius_estimate).

## 2. The ML Test Score: A Rubric for ML Production Readiness (Breck et al., 2017)
**Methodology:** Qualitative rubric across operational domains (data quality, monitoring, reproducibility, testing, model serving, fairness), encouraging incremental maturity scoring.
**Core Contributions:** Shared readiness vocabulary; drives systematic coverage; highlights monitoring + rollback preparedness.
**Research Gaps:** Subjective weighting; does not quantify cross-provider readiness; minimal guidance on real-time scoring.
**Actionable for Project:**
- Compute `ai_readiness_score` = weighted sum of binary dimension flags (monitoring, alerting, failure injection, regression, config audit, provider fallback).
- Dashboard readiness panel with trend line.
- Emit `ai_readiness_dimension{dimension="X"} 0|1` gauges.
- Alert if score drops >10% within 24h.

## 3. Clipper: A Low-Latency Online Prediction Serving System (Crankshaw et al., 2017)
**Methodology:** Modular serving layer decoupling application from models; adaptive batching, caching, and policy-based model selection.
**Core Contributions:** Separation of concern; multi-model policy abstraction; latency variance reduction under load.
**Research Gaps:** Limited explicit failure resilience (focus on performance); no multi-vendor SLA normalization; no chaos/fault routing logic.
**Actionable for Project:**
- Introduce provider policy interface: `selectProvider(context)` with strategies: round_robin, latency_aware (moving p95), error_aware (EWMA error rate), hybrid.
- Track `ai_provider_efficiency_score{provider}` combining (success_rate * (target_p95 / observed_p95)).
- Dynamic policy switching when efficiency gap > threshold.
- Cache last N successful responses to support graceful degradation (optional).

## 4. Simple Testing Can Prevent Most Critical Failures (Yuan et al., 2014)
**Methodology:** Empirical postmortem analysis of large-scale outages; classification of failure causes emphasizing untested simple error paths.
**Core Contributions:** Demonstrates high payoff of enumerating negative paths (timeouts, null handling, config errors) with simple deterministic tests.
**Research Gaps:** Pre-dates AI model serving complexity; no structured mapping to chaos experimentation; lacks automated recovery SLO metrics.
**Actionable for Project:**
- Enumerate failure modes registry (JSON): id, trigger, expected_breaker_state, max_recovery_ms.
- Regression harness executes all modes nightly; outputs `ai_failure_mode_test_coverage`.
- Capture circuit recovery time histogram (`ai_circuit_recovery_time_ms`).
- Fail build if coverage < target (e.g., 90%).

## 5. Hidden Technical Debt in Machine Learning Systems (Sculley et al., 2015)
**Methodology:** Conceptual taxonomy: configuration debt, glue code, data dependencies, entanglement, undeclared consumers, feedback loops.
**Core Contributions:** Frames ML reliability as long-term debt management; introduces vocabulary enabling proactive architecture choices.
**Research Gaps:** Lacks measurable operationalization; no scoring or automated detection mechanisms.
**Actionable for Project:**
- Emit `ai_config_changes_total` (increment on runtime config mutation endpoint hits).
- Detect & flag unused environment variables (baseline snapshot + runtime scan) → increment `ai_debt_indicators_total`.
- Maintain dependency graph size metric (providers + injectable failure modules).
- Add Debt section to dashboard with warning thresholds.

## 6. Lineage-Driven Fault Injection (Alvaro et al., 2015)
**Methodology:** Uses data lineage to systematically target fault injection points that maximize state-space exploration; selective injection guided by provenance.
**Core Contributions:** Efficiency: fewer injections yield higher coverage; formalizes targeting vs random injection.
**Research Gaps:** Focused on data-intensive systems, not AI API multi-provider context; needs adaptation for request/response service layer.
**Actionable for Project:**
- Maintain lightweight request lineage metadata: provider → latency bucket → outcome → fallback_used.
- Rank failure injection targets by (unseen_state_frequency * impact_score).
- Implement adaptive injector selecting least-tested state combination first.
- Track `ai_injection_state_coverage` (% unique state tuples exercised).

## 7. The Tail at Scale (Dean & Barroso, 2013)
**Methodology:** Analyzes latency tail amplification in large fan-out systems; introduces techniques: hedged requests, micro-replication, timeouts, prioritization.
**Core Contributions:** Emphasis on p99+ latency as reliability dimension; strategies to dampen tail amplification.
**Research Gaps:** Not specialized for paid external AI APIs with quota; no integration with circuit breaker states.
**Actionable for Project:**
- Track `ai_request_latency_ms` histogram percentiles (already) + compute rolling p99 gap vs SLO.
- Hedge optional duplicate request when latency > p95 threshold and circuit closed; cancel slower response.
- Metric: `ai_hedged_requests_total` + `ai_hedge_wins_total`.
- Add tail latency alert condition (p99 > SLO for N intervals).

## 8. AIOps: Real-World Challenges and Research Innovations (Dang et al., 2019)
**Methodology:** Field study of enterprise operational pain points; categorizes challenges (noise reduction, root cause inference, anomaly detection). Suggests ML-enhanced ops workflows.
**Core Contributions:** Identifies gap between raw telemetry and actionable insights; highlights need for feedback loops and adaptive thresholds.
**Research Gaps:** Limited concrete architectures for multi-provider AI reliability; minimal bridging of chaos outputs with anomaly models.
**Actionable for Project:**
- Introduce adaptive alert threshold prototype (EWMA baseline + sigma bands) for failure rate.
- Add anomaly flag metric `ai_failure_rate_anomaly{provider}`.
- Feed chaos experiment outcomes into a feature store for future automated anomaly model.
- Implement basic root-cause tag heuristic (highest error-contributing provider last 5 min).

---
## Cross-Paper Synthesis → Unified Enhancement Plan
1. Experimentation Backbone (Basiri + Alvaro): Structured experiments with lineage-aware injection ordering.
2. Readiness & Debt Scoring (Breck + Sculley): Continuous maturity + debt dashboards.
3. Adaptive Routing & Tail Mitigation (Clipper + Tail at Scale): Policy engine + hedged requests for high quantiles.
4. Reliability Regression (Yuan): Nightly failure suite ensuring breaker SLO adherence.
5. Intelligent Ops Layer (Dang): Adaptive thresholds & early anomaly flags.

## Metrics Additions Summary
- ai_experiment_active, ai_experiment_latency_delta_ms
- ai_readiness_score, ai_readiness_dimension{dimension=""}
- ai_config_changes_total, ai_debt_indicators_total, ai_dependency_graph_size
- ai_injection_state_coverage
- ai_provider_efficiency_score{provider}
- ai_circuit_recovery_time_ms
- ai_hedged_requests_total, ai_hedge_wins_total
- ai_failure_rate_anomaly{provider}

## Implementation Phasing (Effort vs Impact)
Phase 1 (Low Effort / High Impact): readiness score, config changes counter, circuit recovery histogram.
Phase 2: /experiments API + experiment tagging + report generation.
Phase 3: Unified provider policy engine + efficiency score + tail latency hedge.
Phase 4: Lineage-aware adaptive injector + state coverage metric.
Phase 5: Regression harness & nightly failure coverage gating.
Phase 6: Adaptive alert thresholds & anomaly flags.

## Research Gaps Your Project Can Fill
- Standard metric schema for multi-provider AI resilience.
- Practical lineage abstraction for API-level (non-dataflow) fault targeting.
- Integrated resilience maturity + debt scoring in a single dashboard.
- Chaos-to-anomaly feedback loop operationalization.

## Summary
These eight works collectively justify an architecture that is observability-first, experiment-driven, policy-adaptive, and debt-aware. Implementing the actionable items yields a demonstrable, research-aligned reference platform for resilient multi-provider AI service orchestration.
