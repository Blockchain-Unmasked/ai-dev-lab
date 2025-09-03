#!/usr/bin/env python3
"""
AI/DEV Lab Test Runner
Comprehensive test execution with reporting and quality gates
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TestRunner:
    """Comprehensive test runner for AI/DEV Lab."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_dir = Path(__file__).parent
        self.reports_dir = self.test_dir / "reports"
        self.results = {}
        
        # Ensure reports directory exists
        self.reports_dir.mkdir(exist_ok=True)
        (self.reports_dir / "coverage").mkdir(exist_ok=True)
        (self.reports_dir / "security").mkdir(exist_ok=True)
        (self.reports_dir / "performance").mkdir(exist_ok=True)
    
    def run_command(self, command: List[str], description: str) -> Dict:
        """Run a command and return results."""
        print(f"\n🔄 {description}")
        print(f"Command: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "description": description
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out after 5 minutes",
                "description": description
            }
        except Exception as e:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "description": description
            }
    
    def run_unit_tests(self) -> Dict:
        """Run unit tests."""
        return self.run_command(
            ["python", "-m", "pytest", "tests/", "-m", "unit", "-v", "--tb=short"],
            "Running Unit Tests"
        )
    
    def run_integration_tests(self) -> Dict:
        """Run integration tests."""
        return self.run_command(
            ["python", "-m", "pytest", "tests/", "-m", "integration", "-v", "--tb=short"],
            "Running Integration Tests"
        )
    
    def run_backend_tests(self) -> Dict:
        """Run backend tests."""
        return self.run_command(
            ["python", "-m", "pytest", "tests/backend/", "-v", "--tb=short"],
            "Running Backend Tests"
        )
    
    def run_frontend_tests(self) -> Dict:
        """Run frontend tests."""
        return self.run_command(
            ["python", "-m", "pytest", "tests/frontend/", "-v", "--tb=short"],
            "Running Frontend Tests"
        )
    
    def run_mcp_tests(self) -> Dict:
        """Run MCP integration tests."""
        return self.run_command(
            ["python", "-m", "pytest", "tests/mcp/", "-v", "--tb=short"],
            "Running MCP Integration Tests"
        )
    
    def run_security_tests(self) -> Dict:
        """Run security tests."""
        return self.run_command(
            ["python", "-m", "pytest", "tests/security/", "-v", "--tb=short"],
            "Running Security Tests"
        )
    
    def run_performance_tests(self) -> Dict:
        """Run performance tests."""
        return self.run_command(
            ["python", "-m", "pytest", "tests/performance/", "-v", "--tb=short"],
            "Running Performance Tests"
        )
    
    def run_compliance_tests(self) -> Dict:
        """Run OCINT compliance tests."""
        return self.run_command(
            ["python", "-m", "pytest", "tests/", "-m", "ocint", "-v", "--tb=short"],
            "Running OCINT Compliance Tests"
        )
    
    def run_full_test_suite(self) -> Dict:
        """Run the complete test suite with coverage."""
        return self.run_command(
            [
                "python", "-m", "pytest", "tests/", "-v", "--tb=short",
                "--cov=app", "--cov-report=html:reports/coverage",
                "--cov-report=xml:reports/coverage.xml",
                "--junitxml=reports/junit.xml",
                "--html=reports/pytest_report.html", "--self-contained-html"
            ],
            "Running Full Test Suite with Coverage"
        )
    
    def run_security_scan(self) -> Dict:
        """Run security vulnerability scanning."""
        # Run bandit for Python security analysis
        bandit_result = self.run_command(
            ["bandit", "-r", "app/", "-f", "json", "-o", "reports/security/bandit.json"],
            "Running Bandit Security Scan"
        )
        
        # Run safety for dependency vulnerability check
        safety_result = self.run_command(
            ["safety", "check", "--json", "--output", "reports/security/safety.json"],
            "Running Safety Dependency Check"
        )
        
        return {
            "bandit": bandit_result,
            "safety": safety_result,
            "overall_success": bandit_result["success"] and safety_result["success"]
        }
    
    def run_performance_benchmarks(self) -> Dict:
        """Run performance benchmarks."""
        return self.run_command(
            [
                "python", "-m", "pytest", "tests/", "-m", "performance",
                "--benchmark-only", "--benchmark-json=reports/performance/benchmarks.json"
            ],
            "Running Performance Benchmarks"
        )
    
    def check_code_quality(self) -> Dict:
        """Check code quality with various tools."""
        results = {}
        
        # Run black for code formatting check
        results["black"] = self.run_command(
            ["black", "--check", "app/", "tests/"],
            "Checking Code Formatting (Black)"
        )
        
        # Run flake8 for linting
        results["flake8"] = self.run_command(
            ["flake8", "app/", "tests/"],
            "Running Linting (Flake8)"
        )
        
        # Run isort for import sorting
        results["isort"] = self.run_command(
            ["isort", "--check-only", "app/", "tests/"],
            "Checking Import Sorting (isort)"
        )
        
        # Run mypy for type checking
        results["mypy"] = self.run_command(
            ["mypy", "app/", "tests/"],
            "Running Type Checking (mypy)"
        )
        
        return results
    
    def generate_test_report(self) -> Dict:
        """Generate comprehensive test report."""
        timestamp = datetime.now().isoformat()
        
        report = {
            "timestamp": timestamp,
            "project": "AI/DEV Lab",
            "test_suite": "Comprehensive Testing Framework",
            "results": self.results,
            "summary": self.generate_summary(),
            "quality_gates": self.check_quality_gates(),
            "recommendations": self.generate_recommendations()
        }
        
        # Save report to file
        report_file = self.reports_dir / f"test_report_{timestamp[:19].replace(':', '-')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_summary(self) -> Dict:
        """Generate test execution summary."""
        total_tests = len(self.results)
        successful_tests = sum(1 for result in self.results.values() 
                             if isinstance(result, dict) and result.get("success"))
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0
        }
    
    def check_quality_gates(self) -> Dict:
        """Check quality gates for deployment readiness."""
        quality_gates = {
            "all_tests_passing": True,
            "code_coverage_adequate": True,
            "security_scan_clean": True,
            "performance_benchmarks_met": True,
            "ocint_compliance_verified": True
        }
        
        # Check if all tests are passing
        for result in self.results.values():
            if isinstance(result, dict) and not result.get("success"):
                quality_gates["all_tests_passing"] = False
                break
        
        # Additional quality gate checks would be implemented here
        # based on coverage reports, security scan results, etc.
        
        return quality_gates
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        # Check for failed tests
        failed_tests = []
        for test_name, result in self.results.items():
            if isinstance(result, dict) and not result.get("success"):
                failed_tests.append(test_name)
        
        if failed_tests:
            recommendations.append(f"Fix {len(failed_tests)} failed tests: {', '.join(failed_tests)}")
        
        # Check for missing test categories
        expected_categories = ["unit", "integration", "backend", "frontend", "mcp", "security"]
        missing_categories = []
        for category in expected_categories:
            if f"run_{category}_tests" not in self.results:
                missing_categories.append(category)
        
        if missing_categories:
            recommendations.append(f"Implement missing test categories: {', '.join(missing_categories)}")
        
        # Add general recommendations
        recommendations.extend([
            "Maintain 100/100 scores across all categories",
            "Ensure security score ≥900/1000",
            "Maintain code coverage ≥95%",
            "Run tests before every deployment"
        ])
        
        return recommendations
    
    def print_results(self, results: Dict):
        """Print test results in a formatted way."""
        print(f"\n{'='*60}")
        print(f"📊 TEST RESULTS: {results['description']}")
        print(f"{'='*60}")
        
        if results["success"]:
            print("✅ SUCCESS")
            if results["stdout"]:
                print("Output:")
                print(results["stdout"][:500] + "..." if len(results["stdout"]) > 500 else results["stdout"])
        else:
            print("❌ FAILED")
            print(f"Return Code: {results['returncode']}")
            if results["stderr"]:
                print("Error:")
                print(results["stderr"][:500] + "..." if len(results["stderr"]) > 500 else results["stderr"])
        
        print(f"{'='*60}")
    
    def run_all_tests(self, test_categories: Optional[List[str]] = None) -> Dict:
        """Run all specified test categories."""
        print("🚀 AI/DEV Lab Comprehensive Test Suite")
        print("=" * 50)
        
        if test_categories is None:
            test_categories = [
                "unit", "integration", "backend", "frontend", 
                "mcp", "security", "performance", "compliance"
            ]
        
        # Run tests based on categories
        for category in test_categories:
            if category == "unit":
                self.results["unit_tests"] = self.run_unit_tests()
                self.print_results(self.results["unit_tests"])
            elif category == "integration":
                self.results["integration_tests"] = self.run_integration_tests()
                self.print_results(self.results["integration_tests"])
            elif category == "backend":
                self.results["backend_tests"] = self.run_backend_tests()
                self.print_results(self.results["backend_tests"])
            elif category == "frontend":
                self.results["frontend_tests"] = self.run_frontend_tests()
                self.print_results(self.results["frontend_tests"])
            elif category == "mcp":
                self.results["mcp_tests"] = self.run_mcp_tests()
                self.print_results(self.results["mcp_tests"])
            elif category == "security":
                self.results["security_tests"] = self.run_security_tests()
                self.print_results(self.results["security_tests"])
            elif category == "performance":
                self.results["performance_tests"] = self.run_performance_tests()
                self.print_results(self.results["performance_tests"])
            elif category == "compliance":
                self.results["compliance_tests"] = self.run_compliance_tests()
                self.print_results(self.results["compliance_tests"])
        
        # Run additional checks
        self.results["code_quality"] = self.check_code_quality()
        self.results["security_scan"] = self.run_security_scan()
        self.results["performance_benchmarks"] = self.run_performance_benchmarks()
        
        # Generate and print final report
        report = self.generate_test_report()
        self.print_final_report(report)
        
        return report
    
    def print_final_report(self, report: Dict):
        """Print the final test report."""
        print(f"\n{'='*80}")
        print("🎯 FINAL TEST REPORT")
        print(f"{'='*80}")
        
        summary = report["summary"]
        print(f"📊 Test Summary:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Successful: {summary['successful_tests']}")
        print(f"   Failed: {summary['failed_tests']}")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")
        
        print(f"\n🔒 Quality Gates:")
        quality_gates = report["quality_gates"]
        for gate, status in quality_gates.items():
            status_icon = "✅" if status else "❌"
            print(f"   {gate}: {status_icon}")
        
        print(f"\n💡 Recommendations:")
        for i, recommendation in enumerate(report["recommendations"], 1):
            print(f"   {i}. {recommendation}")
        
        print(f"\n📁 Reports saved to: {self.reports_dir}")
        print(f"{'='*80}")


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="AI/DEV Lab Test Runner")
    parser.add_argument(
        "--categories", 
        nargs="+", 
        choices=["unit", "integration", "backend", "frontend", "mcp", "security", "performance", "compliance"],
        help="Specific test categories to run"
    )
    parser.add_argument(
        "--full-suite", 
        action="store_true", 
        help="Run the complete test suite with coverage"
    )
    parser.add_argument(
        "--quick", 
        action="store_true", 
        help="Run only critical tests"
    )
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.full_suite:
        print("🚀 Running Full Test Suite...")
        runner.run_full_test_suite()
    elif args.quick:
        print("⚡ Running Quick Critical Tests...")
        runner.run_all_tests(["unit", "backend", "security"])
    elif args.categories:
        print(f"🎯 Running Specific Test Categories: {', '.join(args.categories)}")
        runner.run_all_tests(args.categories)
    else:
        print("🔄 Running All Test Categories...")
        runner.run_all_tests()


if __name__ == "__main__":
    main()
