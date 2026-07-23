import time
import schedule
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os
import signal
import sys
from pathlib import Path

from agentic_lead_engine.integration.integration_manager import IntegrationManager
from agentic_lead_engine.integration.payment_processor import PaymentProcessor
from agentic_lead_engine.config import settings
from agentic_lead_engine.utils.logger import Logger


class AutonomousRunner:
    """
    Makes the system work 24/7 while you sleep.
    Handles automated lead processing, follow-ups, payments, and monitoring.
    """

    def __init__(self):
        self.logger = Logger("AutonomousRunner")
        self.integration = IntegrationManager()
        self.payments = PaymentProcessor()

        self.running = False
        self.threads = []

        # Operation schedules
        self.schedules = {
            'lead_processing': {'interval': 30, 'unit': 'minutes'},  # Every 30 minutes
            'followup_check': {'interval': 1, 'unit': 'hours'},      # Every hour
            'analytics_update': {'interval': 6, 'unit': 'hours'},    # Every 6 hours
            'payment_check': {'interval': 24, 'unit': 'hours'},      # Daily
            'health_check': {'interval': 1, 'unit': 'hours'},        # Every hour
            'market_validation': {'interval': 24, 'unit': 'hours'}   # Daily
        }

    def start_autonomous_mode(self):
        """
        Start the autonomous operation system.
        """
        self.logger.info("🚀 Starting autonomous revenue generation mode")
        self.running = True

        # Handle graceful shutdown
        signal.signal(signal.SIGINT, self._shutdown_handler)
        signal.signal(signal.SIGTERM, self._shutdown_handler)

        # Start monitoring thread
        monitoring_thread = threading.Thread(target=self._run_monitoring_loop, daemon=True)
        monitoring_thread.start()
        self.threads.append(monitoring_thread)

        # Schedule automated tasks
        self._schedule_tasks()

        # Start the scheduler
        scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()
        self.threads.append(scheduler_thread)

        # Initial operations
        self._perform_initial_operations()

        self.logger.info("✅ Autonomous mode active - system will work while you sleep")

        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self._shutdown_handler()

    def _schedule_tasks(self):
        """Schedule all automated tasks."""
        self.logger.info("📅 Scheduling automated tasks")

        # Lead processing - every 30 minutes
        schedule.every(self.schedules['lead_processing']['interval']).minutes.do(
            self._automated_lead_processing
        )

        # Follow-up checks - every hour
        schedule.every(self.schedules['followup_check']['interval']).hours.do(
            self._automated_followup_processing
        )

        # Analytics updates - every 6 hours
        schedule.every(self.schedules['analytics_update']['interval']).hours.do(
            self._update_analytics
        )

        # Payment processing - daily
        schedule.every(self.schedules['payment_check']['interval']).hours.do(
            self._process_payments
        )

        # Health checks - every hour
        schedule.every(self.schedules['health_check']['interval']).hours.do(
            self._health_check
        )

        # Market validation - daily
        schedule.every(self.schedules['market_validation']['interval']).hours.do(
            self._market_validation_cycle
        )

    def _run_scheduler(self):
        """Run the task scheduler."""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                self.logger.error(f"Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes on error

    def _run_monitoring_loop(self):
        """Continuous monitoring and status updates."""
        while self.running:
            try:
                status = self._get_system_status()
                self._log_status_summary(status)

                # Alert if issues detected
                self._check_for_alerts(status)

                time.sleep(3600)  # Update every hour
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(300)

    def _perform_initial_operations(self):
        """Perform initial setup operations."""
        self.logger.info("🔄 Performing initial autonomous operations")

        # Validate market demand for configured niches
        niches = ['real_estate', 'gym', 'restaurant']
        locations = ['Meerut', 'Delhi', 'Noida']

        for niche in niches:
            for location in locations:
                try:
                    validation = self.integration.validate_market_demand(niche, location)
                    if validation['market_readiness'] == 'High':
                        self.logger.info(f"🎯 High-demand opportunity: {niche} in {location}")
                except Exception as e:
                    self.logger.warn(f"Market validation failed for {niche} in {location}: {e}")

        # Tune messages for best conversion
        try:
            message_tuning = self.integration.tune_messages_for_conversion('real_estate', 'Meerut')
            self.logger.info(f"📝 Best converting message found: {message_tuning['conversion_rate']:.1%} rate")
        except Exception as e:
            self.logger.warn(f"Message tuning failed: {e}")

    def _automated_lead_processing(self):
        """Automatically process new leads."""
        try:
            self.logger.info("🔄 Processing new leads automatically")

            # Get leads for configured niches
            niches = [('real_estate', 'Meerut'), ('gym', 'Meerut'), ('restaurant', 'Meerut')]

            total_processed = 0
            total_converted = 0

            for niche, location in niches:
                leads = self.integration.lead_source.fetch_leads(niche, location, limit=settings.LEAD_BATCH_SIZE)

                for lead in leads:
                    result = self.integration.process_lead_autonomously(lead)
                    total_processed += 1

                    if result.get('status') == 'processed':
                        total_converted += 1

            self.logger.info(f"✅ Processed {total_processed} leads, {total_converted} qualified for outreach")

        except Exception as e:
            self.logger.error(f"Automated lead processing failed: {e}")

    def _automated_followup_processing(self):
        """Automatically handle follow-ups and replies."""
        try:
            self.logger.info("📞 Processing follow-ups and replies")

            # Get pending follow-ups
            pending_followups = self.integration.memory.get_pending_followups()

            for followup in pending_followups:
                if datetime.now() >= datetime.fromisoformat(followup['due_time']):
                    self._execute_followup(followup)

            # Check for new incoming messages (in real implementation, this would poll WhatsApp API)
            # For now, simulate checking for replies
            self._check_incoming_messages()

        except Exception as e:
            self.logger.error(f"Follow-up processing failed: {e}")

    def _execute_followup(self, followup: Dict):
        """Execute a scheduled follow-up."""
        try:
            lead = self.integration.memory.get_lead(followup['lead_id'])

            if lead:
                # Generate follow-up message
                followup_message = self.integration.ai_client.generate_followup_message(lead, followup)

                # Send follow-up
                send_result = self.integration.messenger.send_message(lead['phone'], followup_message)

                # Record follow-up
                self.integration.memory.record_followup(followup['lead_id'], followup_message, send_result)

                self.logger.info(f"📤 Follow-up sent to {lead.get('name', 'Unknown')}")

        except Exception as e:
            self.logger.error(f"Follow-up execution failed: {e}")

    def _check_incoming_messages(self):
        """Check for incoming WhatsApp messages."""
        # In real implementation, this would poll the WhatsApp Business API
        # For now, this is a placeholder
        pass

    def _update_analytics(self):
        """Update system analytics."""
        try:
            self.logger.info("📊 Updating analytics")

            status = self.integration.get_autonomous_operations_status()

            # Log key metrics
            analytics = status['analytics']
            self.logger.info(f"📈 Revenue: ₹{analytics['revenue']:,.0f} | Conversions: {analytics['conversions']} | Processed: {analytics['leads_processed']}")

            # Performance by niche
            for niche, perf in analytics['niche_performance'].items():
                if perf['processed'] > 0:
                    rate = perf['converted'] / perf['processed']
                    self.logger.info(f"🎯 {niche}: {rate:.1%} conversion rate ({perf['converted']}/{perf['processed']})")

        except Exception as e:
            self.logger.error(f"Analytics update failed: {e}")

    def _process_payments(self):
        """Process payment-related tasks."""
        try:
            self.logger.info("💰 Processing payments and subscriptions")

            # Check subscription statuses
            active_leads = self.integration.memory.get_active_leads()

            for lead in active_leads:
                if lead.get('subscription_id'):
                    status = self.payments.get_subscription_status(lead['id'])
                    if status['status'] != 'active':
                        self.logger.warn(f"⚠️ Subscription issue for {lead.get('name')}: {status['status']}")

            # Get revenue analytics
            revenue_stats = self.payments.get_revenue_analytics()
            self.logger.info(f"💵 Monthly Recurring Revenue: ₹{revenue_stats['monthly_recurring']:,.0f}")

        except Exception as e:
            self.logger.error(f"Payment processing failed: {e}")

    def _health_check(self):
        """Perform system health check."""
        try:
            self.logger.info("🏥 Running system health check")

            health_status = {
                'lead_source': self._check_lead_source_health(),
                'ai_client': self._check_ai_client_health(),
                'messenger': self._check_messenger_health(),
                'memory': self._check_memory_health(),
                'payments': self._check_payments_health()
            }

            healthy_components = sum(1 for status in health_status.values() if status)
            total_components = len(health_status)

            if healthy_components == total_components:
                self.logger.info("✅ All systems healthy")
            else:
                self.logger.warn(f"⚠️ {total_components - healthy_components}/{total_components} components unhealthy")

        except Exception as e:
            self.logger.error(f"Health check failed: {e}")

    def _market_validation_cycle(self):
        """Run market validation cycle."""
        try:
            self.logger.info("🎯 Running market validation cycle")

            # Re-validate high-priority markets
            high_value_niches = ['real_estate', 'restaurant']
            locations = ['Meerut', 'Delhi', 'Noida']

            opportunities = []
            for niche in high_value_niches:
                for location in locations:
                    validation = self.integration.validate_market_demand(niche, location)
                    if validation['market_readiness'] in ['High', 'Medium']:
                        opportunities.append(validation)

            if opportunities:
                self.logger.info(f"💡 Found {len(opportunities)} market opportunities")

        except Exception as e:
            self.logger.error(f"Market validation cycle failed: {e}")

    def _get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'timestamp': datetime.now().isoformat(),
            'autonomous_mode': self.running,
            'integration_status': self.integration.get_autonomous_operations_status(),
            'payment_status': self.payments.get_revenue_analytics(),
            'uptime': str(datetime.now() - datetime.fromisoformat(self._get_start_time()))
        }

    def _log_status_summary(self, status: Dict):
        """Log a summary of system status."""
        integration = status['integration_status']
        payments = status['payment_status']

        self.logger.info("📊 System Status Summary:")
        self.logger.info(f"   Leads Processed: {integration['analytics']['leads_processed']}")
        self.logger.info(f"   Conversions: {integration['analytics']['conversions']}")
        self.logger.info(f"   Revenue: ₹{integration['analytics']['revenue']:,.0f}")
        self.logger.info(f"   Pending Follow-ups: {integration['pending_followups']}")
        self.logger.info(f"   MRR: ₹{payments['monthly_recurring']:,.0f}")

    def _check_for_alerts(self, status: Dict):
        """Check for system alerts."""
        integration = status['integration_status']

        # Alert if no leads processed recently
        if integration['analytics']['leads_processed'] == 0:
            self.logger.warn("⚠️ ALERT: No leads processed yet - check lead sources")

        # Alert if conversion rate is low
        total_processed = integration['analytics']['leads_processed']
        conversions = integration['analytics']['conversions']
        if total_processed > 10 and (conversions / total_processed) < 0.05:
            self.logger.warn("⚠️ ALERT: Conversion rate below 5% - review messaging")

        # Alert if follow-ups are backing up
        if integration['pending_followups'] > 50:
            self.logger.warn("⚠️ ALERT: High follow-up backlog - check message processing")

    def _shutdown_handler(self, signum=None, frame=None):
        """Handle graceful shutdown."""
        self.logger.info("🛑 Shutdown signal received - stopping autonomous mode")
        self.running = False

        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=10)

        self.logger.info("✅ Autonomous mode stopped gracefully")
        sys.exit(0)

    # Health check methods
    def _check_lead_source_health(self) -> bool:
        try:
            leads = self.integration.lead_source.fetch_leads('real_estate', 'Meerut', limit=1)
            return len(leads) > 0
        except:
            return False

    def _check_ai_client_health(self) -> bool:
        try:
            # Simple health check - try to qualify a test lead
            test_lead = {'name': 'Test Business', 'niche': 'real_estate'}
            result = self.integration.ai_client.qualify_lead(test_lead)
            return isinstance(result, dict)
        except:
            return False

    def _check_messenger_health(self) -> bool:
        try:
            # Check if WhatsApp credentials are configured
            return bool(settings.WHATSAPP_API_URL and settings.WHATSAPP_API_TOKEN)
        except:
            return False

    def _check_memory_health(self) -> bool:
        try:
            # Check if memory operations work
            test_lead = {'id': 'health_check', 'name': 'Health Check'}
            self.integration.memory.record_contact(test_lead, 'test', {'success': True})
            return True
        except:
            return False

    def _check_payments_health(self) -> bool:
        try:
            # Check if payment gateway is configured
            gateway_config = self.payments.gateways[self.payments.default_gateway]
            return bool(gateway_config.get('api_key', ''))
        except:
            return False

    def _get_start_time(self) -> str:
        """Get system start time."""
        # In a real implementation, this would track actual start time
        return (datetime.now() - timedelta(hours=1)).isoformat()

    def quick_service_mode(self, lead: Dict):
        """
        Quick service mode for immediate customer handling.
        """
        self.logger.info(f"🚀 Activating quick service mode for {lead.get('name')}")

        # Immediate qualification and response
        classification = self.integration.ai_client.classify_lead(lead)
        qualified = classification in ['HOT', 'WARM']  # HOT and WARM leads are qualified

        if qualified:
            # Send immediate response
            message = self.integration.ai_client.generate_outreach_message(lead, {'classification': classification})
            self.integration.messenger.send_message(lead['phone'], message)

            # Start onboarding
            self.integration.quick_service_onboarding(lead)

            # Create payment link
            payment_link = self.payments.create_payment_link(lead)

            return {
                'status': 'quick_service_activated',
                'classification': classification,
                'message_sent': True,
                'onboarding_started': True,
                'payment_link': payment_link
            }

        return {'status': 'not_qualified', 'classification': classification}