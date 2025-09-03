const nodemailer = require('nodemailer');
const { IncomingWebhook } = require('@slack/webhook');

class NotificationService {
  constructor() {
    this.slackWebhook = process.env.SLACK_WEBHOOK_URL ? new IncomingWebhook(process.env.SLACK_WEBHOOK_URL) : null;
    this.emailTransporter = this.createEmailTransporter();
    this.alertThresholds = {
      failureRate: parseFloat(process.env.ALERT_FAILURE_RATE) || 0.5, // 50%
      fallbackRate: parseFloat(process.env.ALERT_FALLBACK_RATE) || 0.8, // 80%
      avgLatency: parseInt(process.env.ALERT_AVG_LATENCY_MS) || 5000, // 5s
      circuitOpenDuration: parseInt(process.env.ALERT_CIRCUIT_OPEN_DURATION_SEC) || 300 // 5 min
    };
    this.alertState = {
      lastFailureAlert: 0,
      lastFallbackAlert: 0,
      lastLatencyAlert: 0,
      circuitOpenTime: null
    };
  }

  createEmailTransporter() {
    if (!process.env.EMAIL_HOST) return null;
    
    return nodemailer.createTransporter({
      host: process.env.EMAIL_HOST,
      port: parseInt(process.env.EMAIL_PORT) || 587,
      secure: process.env.EMAIL_SECURE === 'true',
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
      }
    });
  }

  async sendSlackNotification(message, severity = 'warning') {
    if (!this.slackWebhook) {
      console.log('Slack webhook not configured, skipping notification');
      return;
    }

    const colors = {
      info: '#36a64f',
      warning: '#ff9500',
      error: '#ff0000',
      critical: '#8b0000'
    };

    const payload = {
      attachments: [{
        color: colors[severity] || colors.warning,
        title: '🚨 AI Service Alert',
        text: message,
        timestamp: Math.floor(Date.now() / 1000),
        fields: [
          {
            title: 'Service',
            value: 'AI Proxy',
            short: true
          },
          {
            title: 'Severity',
            value: severity.toUpperCase(),
            short: true
          }
        ]
      }]
    };

    try {
      await this.slackWebhook.send(payload);
      console.log('✅ Slack notification sent');
    } catch (error) {
      console.error('❌ Failed to send Slack notification:', error.message);
    }
  }

  async sendEmailNotification(subject, message, severity = 'warning') {
    if (!this.emailTransporter) {
      console.log('Email not configured, skipping notification');
      return;
    }

    const to = process.env.ALERT_EMAIL_TO || 'admin@example.com';
    const from = process.env.ALERT_EMAIL_FROM || 'alerts@ai-proxy.com';

    const mailOptions = {
      from,
      to,
      subject: `[${severity.toUpperCase()}] ${subject}`,
      html: `
        <h2>🚨 AI Service Alert</h2>
        <p><strong>Service:</strong> AI Proxy</p>
        <p><strong>Severity:</strong> ${severity.toUpperCase()}</p>
        <p><strong>Time:</strong> ${new Date().toISOString()}</p>
        <hr>
        <p>${message}</p>
        <hr>
        <p><em>This is an automated alert from your AI Service monitoring system.</em></p>
      `
    };

    try {
      await this.emailTransporter.sendMail(mailOptions);
      console.log('✅ Email notification sent');
    } catch (error) {
      console.error('❌ Failed to send email notification:', error.message);
    }
  }

  async checkMetricsAndAlert(metrics) {
    if (!metrics) return;

    const now = Date.now();
    const cooldownPeriod = 300000; // 5 minutes between same alert types

    // Parse metrics from Prometheus format
    const parsedMetrics = this.parsePrometheusMetrics(metrics);

    // Check failure rate
    const totalRequests = parsedMetrics.ai_request_latency_ms_count || 1;
    const failures = parsedMetrics.ai_failures_total || 0;
    const failureRate = failures / totalRequests;

    if (failureRate > this.alertThresholds.failureRate && 
        now - this.alertState.lastFailureAlert > cooldownPeriod) {
      await this.sendAlert(
        'High Failure Rate Detected',
        `Failure rate is ${(failureRate * 100).toFixed(1)}% (${failures}/${totalRequests} requests)`,
        'error'
      );
      this.alertState.lastFailureAlert = now;
    }

    // Check fallback rate
    const fallbacks = parsedMetrics.ai_fallbacks_total || 0;
    const fallbackRate = fallbacks / totalRequests;

    if (fallbackRate > this.alertThresholds.fallbackRate && 
        now - this.alertState.lastFallbackAlert > cooldownPeriod) {
      await this.sendAlert(
        'High Fallback Rate Detected',
        `Fallback rate is ${(fallbackRate * 100).toFixed(1)}% (${fallbacks}/${totalRequests} requests)`,
        'warning'
      );
      this.alertState.lastFallbackAlert = now;
    }

    // Check average latency
    const latencySum = parsedMetrics.ai_request_latency_ms_sum || 0;
    const avgLatency = totalRequests > 0 ? latencySum / totalRequests : 0;

    if (avgLatency > this.alertThresholds.avgLatency && 
        now - this.alertState.lastLatencyAlert > cooldownPeriod) {
      await this.sendAlert(
        'High Latency Detected',
        `Average latency is ${avgLatency.toFixed(2)}ms`,
        'warning'
      );
      this.alertState.lastLatencyAlert = now;
    }

    // Check circuit breaker state
    const circuitState = parsedMetrics.ai_circuit_state;
    if (circuitState === 1) { // Open
      if (!this.alertState.circuitOpenTime) {
        this.alertState.circuitOpenTime = now;
      } else if (now - this.alertState.circuitOpenTime > this.alertThresholds.circuitOpenDuration * 1000) {
        await this.sendAlert(
          'Circuit Breaker Stuck Open',
          `Circuit breaker has been open for ${Math.round((now - this.alertState.circuitOpenTime) / 1000)} seconds`,
          'critical'
        );
        this.alertState.circuitOpenTime = now; // Reset to avoid spam
      }
    } else {
      this.alertState.circuitOpenTime = null;
    }
  }

  parsePrometheusMetrics(metricsText) {
    const metrics = {};
    const lines = metricsText.split('\n');
    
    for (const line of lines) {
      if (line.startsWith('#') || !line.trim()) continue;
      
      const parts = line.split(' ');
      if (parts.length >= 2) {
        const metricName = parts[0];
        const value = parseFloat(parts[1]);
        if (!isNaN(value)) {
          metrics[metricName] = value;
        }
      }
    }
    
    return metrics;
  }

  async sendAlert(subject, message, severity = 'warning') {
    console.log(`🚨 ALERT [${severity.toUpperCase()}]: ${subject} - ${message}`);
    
    // Send to both Slack and email if configured
    await Promise.all([
      this.sendSlackNotification(`${subject}\n${message}`, severity),
      this.sendEmailNotification(subject, message, severity)
    ]);
  }

  // Health check notification
  async sendHealthCheck() {
    const message = 'AI Service monitoring is operational';
    await this.sendAlert('Health Check', message, 'info');
  }
}

module.exports = NotificationService;
