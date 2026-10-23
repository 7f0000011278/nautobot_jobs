"""Test job that sleeps for a configurable number of seconds.

Useful for watching/capturing a Kubernetes job pod while it is running.
"""

import time

from nautobot.apps.jobs import IntegerVar, Job, register_jobs

name = "Test Jobs"

class SleepTest(Job):
    seconds = IntegerVar(
        default=30,
        min_value=1,
        max_value=3600,
        description="How long to sleep, in seconds",
    )

    class Meta:
        name = "Sleep Test"
        description = "Sleeps for N seconds, logging progress every 5 seconds"
        # Per-job limits so the global CELERY_TASK_*_TIME_LIMIT (2s/3s) doesn't kill it
        soft_time_limit = 3700
        time_limit = 3800

    def run(self, *, seconds):
        self.logger.info("Starting sleep for %s seconds", seconds)
        elapsed = 0
        while elapsed < seconds:
            step = min(5, seconds - elapsed)
            time.sleep(step)
            elapsed += step
            self.logger.info("Slept %s/%s seconds", elapsed, seconds)
        self.logger.success("Done sleeping %s seconds", seconds)
        return f"Slept {seconds} seconds"


register_jobs(SleepTest)