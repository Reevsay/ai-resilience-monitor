const axios = require('axios');
const NotificationService = require('../src/notificationService');

class AlertMonitor {
  constructor(aiProxyUrl = 'http://localhost:3000') {
    this.aiProxyUrl = aiProxyUrl;
    this.notificationService = new NotificationService();
    this.monitoringInterval = parseInt(process.env.MONITORING_INTERVAL_SEC) || 30; // 30 seconds
    this.isRunning = false;
  }

  async start() {
    if (this.isRunning) {
      console.log('Monitor is already running');
      return;
    }

    this.isRunning = true;
    console.log(`🔍 Starting alert monitor (checking every ${this.monitoringInterval}s)`);
    
    // Send startup notification
    await this.notificationService.sendAlert(
      'Monitoring Started',
      'AI Service alert monitoring has started',
      'info'
    );

    this.intervalId = setInterval(async () => {
      try {
        await this.checkMetricsAndAlert();
      } catch (error) {
        console.error('Error during monitoring check:', error.message);
      }
    }, this.monitoringInterval * 1000);

    // Graceful shutdown
    process.on('SIGINT', () => this.stop());
    process.on('SIGTERM', () => this.stop());
  }

  async stop() {
    if (!this.isRunning) return;

    this.isRunning = false;
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }

    await this.notificationService.sendAlert(
      'Monitoring Stopped',
      'AI Service alert monitoring has stopped',
      'info'
    );

    console.log('🛑 Alert monitor stopped');
    process.exit(0);
  }

  async checkMetricsAndAlert() {
    try {
      // Fetch metrics from AI proxy
      const response = await axios.get(`${this.aiProxyUrl}/metrics`, {
        timeout: 5000
      });

      await this.notificationService.checkMetricsAndAlert(response.data);
      
    } catch (error) {
      console.error('Failed to fetch metrics:', error.message);
      
      // Alert if service is unreachable
      await this.notificationService.sendAlert(
        'Service Unreachable',
        `Cannot fetch metrics from ${this.aiProxyUrl}: ${error.message}`,
        'critical'
      );
    }
  }

  async testNotifications() {
    console.log('🧪 Testing notification systems...');
    
    await this.notificationService.sendAlert(
      'Test Alert',
      'This is a test notification to verify the alert system is working',
      'info'
    );
    
    console.log('✅ Test notifications sent');
  }
}

// CLI interface
if (require.main === module) {
  const monitor = new AlertMonitor();
  
  const command = process.argv[2];
  
  if (command === 'test') {
    monitor.testNotifications().then(() => process.exit(0));
  } else {
    monitor.start();
  }
}

module.exports = AlertMonitor;
