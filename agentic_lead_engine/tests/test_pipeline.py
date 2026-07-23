import unittest
import tempfile
import shutil
import os

from agentic_lead_engine.orchestrator import Orchestrator
from agentic_lead_engine.config import settings


class TestPipeline(unittest.TestCase):
    def test_full_pipeline_runs_without_crashing(self):
        temp_dir = tempfile.mkdtemp(prefix="v2_memory_")
        original_memory_dir = settings.MEMORY_DIR
        try:
            settings.MEMORY_DIR = temp_dir
            orchestrator = Orchestrator()
            summary = orchestrator.run_cycle("gym", "Delhi")

            self.assertIsInstance(summary, dict)
            self.assertIn("leads_generated", summary)
            self.assertTrue(summary["leads_generated"] > 0)
            print("Pipeline summary:", summary)
        finally:
            settings.MEMORY_DIR = original_memory_dir
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
