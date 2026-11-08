# Contributing to Industrial AI Assistant Framework

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Industrial AI Assistant Framework.

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize safety in all industrial automation discussions
- Respect intellectual property and confidentiality

## How to Contribute

### Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the issue
2. **Environment**: OS, Python version, DCS type (if applicable)
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Expected Behavior**: What you expected to happen
5. **Actual Behavior**: What actually happened
6. **Logs**: Relevant log output (sanitized of sensitive data)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

1. Check if the enhancement has already been suggested
2. Provide a clear use case
3. Explain the benefits for industrial applications
4. Consider safety implications

### Pull Requests

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

#### PR Guidelines

- Keep changes focused and atomic
- Update documentation as needed
- Add tests for new functionality
- Ensure all tests pass
- Follow the existing code style

## Development Setup

### Prerequisites

```bash
# Python 3.9+
python --version

# Git
git --version
```

> MCP 组件使用 Python SDK（``pip install mcp``），无需 Node.js。

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/industrial-ai-assistant.git
cd industrial-ai-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (核心框架无必需第三方依赖)
pip install -e .
```

### Running Tests

> 测试套件尚在建设中。目前可通过运行示例验证核心功能：

```bash
# 生成分析报告（验证分析链路）
python examples/chemical_process/demo.py --report
```

## Project Structure

```
industrial-ai-assistant/
├── src/
│   └── industrial_ai/          # Main package
│       ├── __init__.py
│       ├── models.py           # Unified data models
│       ├── mcp_server/         # MCP server implementation
│       ├── knowledge_base/     # Knowledge base structures
│       ├── analyzers/          # Analysis engines
│       └── adapters/           # Protocol adapters
├── docs/                       # Documentation
├── examples/                   # Example implementations
├── pyproject.toml
└── requirements.txt
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Example of preferred style
class PressureAnalyzer:
    """
    Analyze pressure systems using heuristic rules.

    This class implements heuristic rules
    for industrial pressure system analysis.
    """

    def __init__(self, config: dict) -> None:
        """
        Initialize the analyzer.

        Args:
            config: Configuration dictionary containing
                   threshold values and expert rules.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

    def analyze(
        self,
        upstream_pressure: float,
        downstream_pressure: float
    ) -> AnalysisResult:
        """
        Analyze pressure differential.

        Args:
            upstream_pressure: Pressure at system inlet (MPa)
            downstream_pressure: Pressure at system outlet (MPa)

        Returns:
            AnalysisResult containing status and recommendations

        Raises:
            ValueError: If pressure values are negative
        """
        if upstream_pressure < 0 or downstream_pressure < 0:
            raise ValueError("Pressure values must be non-negative")

        # Implementation...
```

### Documentation

- All public classes and methods must have docstrings
- Use Google-style docstrings
- Include type hints where appropriate
- Update README.md for user-facing changes

### Testing

测试套件尚在建设中，欢迎贡献测试。分析函数应覆盖正常、预警、严重三类场景（可用 `examples/chemical_process/demo.py --report` 作为参考输入）。

## Safety Considerations

When contributing code that may be used in industrial settings:

### ✅ Do

- Implement read-only access by default
- Add human confirmation for any control recommendations
- Include comprehensive error handling
- Document safety considerations
- Add appropriate warnings and disclaimers

### ❌ Don't

- Implement direct control commands to industrial systems
- Bypass safety checks or interlocks
- Include hardcoded credentials or sensitive data
- Suggest modifications to safety-critical systems without warnings

## Documentation Contributions

### Improving Documentation

Documentation improvements are highly valued:

1. Fix typos and grammar
2. Clarify confusing explanations
3. Add examples where helpful
4. Update outdated information
5. Translate to other languages

### Documentation Structure

```
docs/
├── architecture.md       # System architecture
├── security.md          # Security guidelines
├── mcp-integration.md   # MCP integration guide
├── expert-knowledge.md  # Knowledge embedding guide
├── api-reference.md     # API documentation
└── examples/            # Usage examples
```

## Domain Knowledge Contributions

Contributing domain expertise is one of the most valuable ways to help:

### Expert Patterns

Share industrial domain knowledge:

```yaml
# examples/your_industry/expert_patterns.yaml
expert_patterns:
  your_pattern_name:
    description: "Clear description of the pattern"
    applicable_to: ["equipment_type_1", "equipment_type_2"]
    rules:
      - "Rule 1 with explanation"
      - "Rule 2 with explanation"
    examples:
      - scenario: "Description of scenario"
        data:
          param1: value1
          param2: value2
        analysis: "Expected analysis result"
        recommendation: "Recommended action"
```

### Equipment Templates

```yaml
# examples/your_industry/equipment_templates.yaml
equipment_types:
  your_equipment_type:
    description: "General description"
    common_parameters:
      - name: parameter_name
        unit: unit_of_measurement
        normal_range: [min, max]
        critical_threshold: value
    common_issues:
      - name: issue_name
        symptoms: ["symptom1", "symptom2"]
        possible_causes: ["cause1", "cause2"]
        diagnostic_steps:
          - "Step 1"
          - "Step 2"
```

## Review Process

### PR Review Criteria

Maintainers will review PRs based on:

1. **Correctness**: Does the code work as intended?
2. **Safety**: Are there any safety concerns?
3. **Tests**: Are there adequate tests?
4. **Documentation**: Is documentation updated?
5. **Style**: Does it follow coding standards?
6. **Scope**: Is the change focused and appropriate?

### Review Timeline

- Initial review: Within 3 business days
- Follow-up reviews: Within 1 business day
- Merge after: 2 maintainer approvals

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions and reviews

### Recognition

Contributors will be recognized in:

- RELEASE_NOTES.md for significant contributions
- CONTRIBUTORS.md file
- Project documentation acknowledgments

## Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search closed issues and PRs
3. Open a GitHub Discussion
4. Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to safer, more intelligent industrial systems!
