#!/usr/bin/env python3
"""
Mangolint Test Runner
Runs all tests and generates a comprehensive report
"""
import unittest
import sys
import os
from datetime import datetime
from io import StringIO

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class TestReport:
    """Generate formatted test report"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.results = None
    
    def run_tests(self):
        """Run all tests and capture results"""
        self.start_time = datetime.now()
        
        # Discover and run tests
        loader = unittest.TestLoader()
        start_dir = 'tests'
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        # Run tests with detailed output
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=2)
        self.results = runner.run(suite)
        
        self.end_time = datetime.now()
        
        return stream.getvalue()
    
    def generate_report(self, test_output):
        """Generate comprehensive test report"""
        duration = (self.end_time - self.start_time).total_seconds()
        
        report = []
        report.append("=" * 80)
        report.append("MANGOLINT TEST REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Duration: {duration:.2f} seconds")
        report.append("")
        
        # Summary
        report.append("SUMMARY")
        report.append("-" * 80)
        report.append(f"Tests Run: {self.results.testsRun}")
        report.append(f"Successes: {self.results.testsRun - len(self.results.failures) - len(self.results.errors)}")
        report.append(f"Failures: {len(self.results.failures)}")
        report.append(f"Errors: {len(self.results.errors)}")
        report.append(f"Skipped: {len(self.results.skipped)}")
        report.append("")
        
        # Status
        if self.results.wasSuccessful():
            report.append("STATUS: ✅ ALL TESTS PASSED")
        else:
            report.append("STATUS: ❌ SOME TESTS FAILED")
        report.append("")
        
        # Detailed output
        report.append("DETAILED OUTPUT")
        report.append("-" * 80)
        report.append(test_output)
        report.append("")
        
        # Failures
        if self.results.failures:
            report.append("FAILURES")
            report.append("-" * 80)
            for test, traceback in self.results.failures:
                report.append(f"\n{test}:")
                report.append(traceback)
            report.append("")
        
        # Errors
        if self.results.errors:
            report.append("ERRORS")
            report.append("-" * 80)
            for test, traceback in self.results.errors:
                report.append(f"\n{test}:")
                report.append(traceback)
            report.append("")
        
        # Test Coverage
        report.append("TEST COVERAGE")
        report.append("-" * 80)
        report.append("✓ Unit Tests (linter.py)")
        report.append("  - Initialization")
        report.append("  - Prompt construction")
        report.append("  - Empty text handling")
        report.append("  - Mocked Bedrock analysis")
        report.append("  - Model info retrieval")
        report.append("")
        report.append("✓ Integration Tests (app.py)")
        report.append("  - Index route")
        report.append("  - Health endpoint")
        report.append("  - Model info endpoint")
        report.append("  - Lint endpoint (empty, short text)")
        report.append("  - Analyze endpoint validation")
        report.append("  - Invalid JSON handling")
        report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 80)
        if self.results.wasSuccessful():
            report.append("✓ All tests passing - ready for deployment")
            report.append("✓ Consider adding end-to-end tests with real Bedrock API")
            report.append("✓ Add performance benchmarks for analysis speed")
        else:
            report.append("⚠ Fix failing tests before deployment")
            report.append("⚠ Review error logs for root causes")
        report.append("")
        
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_report(self, report, filename='test_report.txt'):
        """Save report to file"""
        with open(filename, 'w') as f:
            f.write(report)
        print(f"\n📄 Report saved to: {filename}")


def main():
    """Main test runner"""
    print("🧪 Running Mangolint Test Suite...\n")
    
    reporter = TestReport()
    test_output = reporter.run_tests()
    report = reporter.generate_report(test_output)
    
    # Print to console
    print("\n" + report)
    
    # Save to file
    reporter.save_report(report)
    
    # Exit with appropriate code
    sys.exit(0 if reporter.results.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
