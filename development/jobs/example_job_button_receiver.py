from nautobot.apps.jobs import JobButtonReceiver, register_jobs


class ExampleSimpleJobButtonReceiver(JobButtonReceiver):
    class Meta:
        name = "Example Simple Job Button Receiver"

    def receive_job_button(self, obj):
        self.logger.info("Running Job Button Receiver.", extra={"object": obj})
        # Add job logic here


register_jobs(ExampleSimpleJobButtonReceiver)
