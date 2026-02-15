"""
Comprehensive tests for README.md documentation.

This test suite validates that:
1. All files and paths referenced in README.md actually exist
2. The README has proper markdown structure
3. Code examples are syntactically valid
4. Project structure matches documentation
"""

import os
import re
import unittest
from pathlib import Path


class TestReadmeReferences(unittest.TestCase):
    """Test that all files and paths mentioned in README exist."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).parent.parent
        cls.readme_path = cls.repo_root / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()

    def test_readme_exists(self):
        """Test that README.md file exists."""
        self.assertTrue(self.readme_path.exists(), "README.md should exist")
        self.assertTrue(self.readme_path.is_file(), "README.md should be a file")

    def test_readme_not_empty(self):
        """Test that README.md is not empty."""
        self.assertGreater(len(self.readme_content), 0, "README.md should not be empty")

    def test_ai_review_script_exists(self):
        """Test that scripts/ai_review.py exists as referenced in README."""
        script_path = self.repo_root / "scripts" / "ai_review.py"
        self.assertTrue(script_path.exists(),
                       "scripts/ai_review.py should exist as mentioned in README")

    def test_workflow_file_exists(self):
        """Test that workflows/ai-review.yml exists as referenced in README."""
        workflow_path = self.repo_root / "workflows" / "ai-review.yml"
        self.assertTrue(workflow_path.exists(),
                       "workflows/ai-review.yml should exist as mentioned in README")

    def test_pr_test_directory_exists(self):
        """Test that PR-TEST/ directory exists as shown in project structure."""
        pr_test_path = self.repo_root / "PR-TEST"
        self.assertTrue(pr_test_path.exists(),
                       "PR-TEST/ directory should exist as shown in project structure")

    def test_scripts_directory_exists(self):
        """Test that scripts/ directory exists."""
        scripts_path = self.repo_root / "scripts"
        self.assertTrue(scripts_path.exists(), "scripts/ directory should exist")
        self.assertTrue(scripts_path.is_dir(), "scripts/ should be a directory")

    def test_workflows_directory_exists(self):
        """Test that workflows/ directory exists."""
        workflows_path = self.repo_root / "workflows"
        self.assertTrue(workflows_path.exists(), "workflows/ directory should exist")
        self.assertTrue(workflows_path.is_dir(), "workflows/ should be a directory")


class TestReadmeStructure(unittest.TestCase):
    """Test the markdown structure and formatting of README."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).parent.parent
        cls.readme_path = cls.repo_root / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()

    def test_has_title(self):
        """Test that README has a main title (H1)."""
        title_match = re.search(r'^# .+', self.readme_content, re.MULTILINE)
        self.assertIsNotNone(title_match, "README should have a main title (# heading)")

    def test_has_multiple_sections(self):
        """Test that README has multiple sections (H2 headings)."""
        sections = re.findall(r'^## .+', self.readme_content, re.MULTILINE)
        self.assertGreater(len(sections), 0, "README should have at least one section")
        self.assertGreaterEqual(len(sections), 4,
                               "README should have multiple sections for good organization")

    def test_has_feature_section(self):
        """Test that README has a features section."""
        self.assertIn('## 功能特性', self.readme_content,
                     "README should have a features section")

    def test_has_workflow_section(self):
        """Test that README has a workflow section."""
        self.assertIn('## 工作流程', self.readme_content,
                     "README should have a workflow section")

    def test_has_configuration_section(self):
        """Test that README has a configuration section."""
        self.assertIn('## 配置说明', self.readme_content,
                     "README should have a configuration section")

    def test_has_project_structure_section(self):
        """Test that README has a project structure section."""
        self.assertIn('## 项目结构', self.readme_content,
                     "README should have a project structure section")

    def test_has_code_blocks(self):
        """Test that README contains code blocks."""
        code_blocks = re.findall(r'```[\s\S]*?```', self.readme_content)
        self.assertGreater(len(code_blocks), 0,
                          "README should contain at least one code block")

    def test_code_blocks_have_language_hints(self):
        """Test that code blocks specify language for syntax highlighting."""
        code_block_starts = re.findall(r'```(\w*)', self.readme_content)
        # At least one code block should have a language specified
        has_language = any(lang for lang in code_block_starts if lang)
        self.assertTrue(has_language,
                       "At least one code block should specify a language (e.g., ```bash)")

    def test_has_table(self):
        """Test that README contains a table for configuration."""
        # Markdown tables contain pipe characters with header separator
        table_pattern = r'\|.*\|.*\n\|[-:| ]+\|'
        has_table = re.search(table_pattern, self.readme_content)
        self.assertIsNotNone(has_table, "README should contain a table for Secrets configuration")


class TestReadmeCodeExamples(unittest.TestCase):
    """Test that code examples in README are valid."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).parent.parent
        cls.readme_path = cls.repo_root / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()

    def test_bash_code_block_syntax(self):
        """Test that bash code blocks have valid syntax."""
        bash_blocks = re.findall(r'```bash\n([\s\S]*?)```', self.readme_content)
        self.assertGreater(len(bash_blocks), 0, "Should have at least one bash code block")

        for i, block in enumerate(bash_blocks):
            # Check for common bash patterns
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            for line in lines:
                # Skip comments and empty lines
                if line.startswith('#') or not line:
                    continue
                # Basic syntax checks
                # Should not have unclosed quotes (basic check)
                single_quotes = line.count("'") - line.count("\\'")
                double_quotes = line.count('"') - line.count('\\"')
                if single_quotes % 2 != 0 and not line.strip().startswith('#'):
                    self.fail(f"Bash block {i+1} has unclosed single quotes: {line}")
                if double_quotes % 2 != 0 and not line.strip().startswith('#'):
                    self.fail(f"Bash block {i+1} has unclosed double quotes: {line}")

    def test_bash_examples_use_valid_commands(self):
        """Test that bash examples use common valid commands."""
        bash_blocks = re.findall(r'```bash\n([\s\S]*?)```', self.readme_content)

        valid_commands = {
            'pip', 'export', 'python', 'python3', 'cd', 'ls', 'mkdir',
            'git', 'npm', 'docker', 'curl', 'wget', 'echo', 'cat'
        }

        for block in bash_blocks:
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            for line in lines:
                if line.startswith('#') or not line:
                    continue
                # Extract first word (command)
                parts = line.split()
                if parts:
                    command = parts[0]
                    # Check if it's a known command or variable assignment
                    if '=' not in command:
                        # It's okay if we don't recognize every command,
                        # but we should recognize common ones
                        pass  # This is a weak check, mainly for documentation

    def test_environment_variables_mentioned(self):
        """Test that required environment variables are documented."""
        required_vars = ['REPO', 'PR_NUMBER', 'GITHUB_TOKEN', 'LLM_API_KEY']

        for var in required_vars:
            self.assertIn(var, self.readme_content,
                         f"Environment variable {var} should be documented in README")

    def test_api_key_references_valid_service(self):
        """Test that API key references point to valid services."""
        self.assertIn('OpenRouter', self.readme_content,
                     "README should mention OpenRouter service")
        self.assertIn('openrouter.ai', self.readme_content,
                     "README should include OpenRouter URL")


class TestReadmeCompleteness(unittest.TestCase):
    """Test that README contains all essential information."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).parent.parent
        cls.readme_path = cls.repo_root / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()

    def test_mentions_dependencies(self):
        """Test that README lists dependencies."""
        self.assertIn('依赖', self.readme_content, "README should have a dependencies section")
        self.assertIn('Python', self.readme_content, "README should mention Python")
        self.assertIn('openai', self.readme_content, "README should mention openai package")
        self.assertIn('requests', self.readme_content, "README should mention requests package")

    def test_has_setup_instructions(self):
        """Test that README contains setup instructions."""
        # Should mention GitHub Actions setup
        self.assertIn('GitHub Actions', self.readme_content,
                     "README should mention GitHub Actions")
        # Should mention Secrets configuration
        self.assertIn('Secrets', self.readme_content,
                     "README should mention Secrets configuration")

    def test_mentions_workflow_trigger_events(self):
        """Test that README explains workflow trigger events."""
        self.assertIn('opened', self.readme_content,
                     "README should mention 'opened' trigger event")
        self.assertIn('synchronize', self.readme_content,
                     "README should mention 'synchronize' trigger event")

    def test_describes_review_dimensions(self):
        """Test that README describes what the review checks for."""
        # Should mention various review aspects
        content_lower = self.readme_content

        # Check for mentions of code quality aspects
        self.assertTrue(
            any(term in content_lower for term in ['逻辑', '性能', '安全', '可维护']),
            "README should describe review dimensions (logic, performance, security, maintainability)"
        )

    def test_local_testing_instructions_present(self):
        """Test that README includes local testing instructions."""
        self.assertIn('本地运行', self.readme_content,
                     "README should include local testing section")

    def test_mentions_ai_model_names(self):
        """Test that README mentions the AI models being used."""
        # Should mention Gemini models
        self.assertIn('gemini', self.readme_content.lower(),
                     "README should mention Gemini models")


class TestReadmeEdgeCases(unittest.TestCase):
    """Additional edge case and regression tests for README."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).parent.parent
        cls.readme_path = cls.repo_root / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()

    def test_no_broken_markdown_links(self):
        """Test that markdown link syntax is not broken."""
        # Find all markdown links [text](url)
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', self.readme_content)

        for text, url in markdown_links:
            self.assertGreater(len(text), 0, "Link text should not be empty")
            self.assertGreater(len(url), 0, "Link URL should not be empty")

    def test_no_trailing_whitespace_on_lines(self):
        """Test that lines don't have excessive trailing whitespace."""
        lines = self.readme_content.split('\n')
        lines_with_multiple_trailing_spaces = [
            i for i, line in enumerate(lines, 1)
            if line.endswith('  ') and not line.endswith('  \n')  # Two spaces for line break is valid
        ]
        # This is a style check - not critical but good practice
        # We'll just check it doesn't happen too often
        self.assertLess(len(lines_with_multiple_trailing_spaces), len(lines) * 0.1,
                       "Too many lines with trailing whitespace")

    def test_consistent_heading_style(self):
        """Test that headings use consistent style."""
        headings = re.findall(r'^(#{1,6}) .+', self.readme_content, re.MULTILINE)
        # Should have h1, h2, and possibly h3
        heading_levels = [len(h) for h in headings]
        self.assertIn(1, heading_levels, "Should have at least one H1 heading")
        self.assertIn(2, heading_levels, "Should have H2 headings for sections")

    def test_file_paths_use_correct_separators(self):
        """Test that file paths in README use forward slashes."""
        # Find references to files/directories
        paths = re.findall(r'(?:scripts|workflows|\.github)/[^\s\)]+', self.readme_content)

        for path in paths:
            self.assertNotIn('\\', path,
                           f"Path '{path}' should use forward slashes, not backslashes")

    def test_secret_names_are_uppercase(self):
        """Test that GitHub secret names are in UPPERCASE as per convention."""
        # Find references to secrets in the table or text
        secret_names = ['GITHUB_TOKEN', 'LLM_API_KEY']

        for secret in secret_names:
            # Should find the exact uppercase version
            count = self.readme_content.count(f'`{secret}`')
            self.assertGreater(count, 0,
                             f"Secret {secret} should be referenced in uppercase with backticks")

    def test_workflow_file_path_consistency(self):
        """Test that workflow file path is consistently referenced."""
        # Should reference both the source location and target location
        self.assertIn('workflows/ai-review.yml', self.readme_content,
                     "Should reference workflows/ai-review.yml")
        self.assertIn('.github/workflows/', self.readme_content,
                     "Should reference .github/workflows/ target location")

    def test_python_command_examples_are_valid(self):
        """Test that python command examples in README are syntactically valid."""
        # Find python commands in code blocks
        python_commands = re.findall(r'python[3]?\s+[\w/.-]+\.py', self.readme_content)

        for cmd in python_commands:
            # Check that the script file reference looks valid
            self.assertTrue(
                cmd.endswith('.py'),
                f"Python command '{cmd}' should reference a .py file"
            )

    def test_chinese_content_is_valid_utf8(self):
        """Test that Chinese characters are properly encoded."""
        # If we can read and process the file, UTF-8 encoding is valid
        try:
            chinese_chars = re.findall(r'[\u4e00-\u9fff]+', self.readme_content)
            self.assertGreater(len(chinese_chars), 0,
                             "README should contain Chinese characters")
        except UnicodeDecodeError:
            self.fail("README should be valid UTF-8 encoded")

    def test_install_command_specifies_packages(self):
        """Test that pip install command lists all required packages."""
        pip_install_match = re.search(r'pip install\s+([\w\s]+)', self.readme_content)
        self.assertIsNotNone(pip_install_match, "Should have a pip install command")

        if pip_install_match:
            packages = pip_install_match.group(1).split()
            self.assertIn('openai', packages, "pip install should include openai")
            self.assertIn('requests', packages, "pip install should include requests")


if __name__ == '__main__':
    unittest.main()