# Contributing to Kingfisher

First off, thank you for considering contributing to Kingfisher! It's people like you that make Kingfisher such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Include screenshots if relevant**
- **Describe the behavior you observed and expected**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes**:
   - Add tests if you've added code
   - Ensure the test suite passes
   - Make sure your code follows the existing style
   - Write clear commit messages
3. **Test your changes**:
   ```bash
   python kingfisher.py examples/book.jpeg
   ```
4. **Create a Pull Request**:
   - Fill in the PR template
   - Link any relevant issues
   - Update documentation if needed

## Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/yourusername/kingfisher.git
   cd kingfisher
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment**:
   ```bash
   cp .env.example .env
   # Add your OpenRouter API key to .env
   ```

## Code Style Guidelines

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic
- Use type hints where appropriate

### Example:
```python
def remove_background(image_path: str, output_dir: Path) -> Path:
    """Remove background from product image using AI.
    
    Args:
        image_path: Path to the input image
        output_dir: Directory to save the output
        
    Returns:
        Path to the generated cutout image
    """
    # Implementation here
```

## Testing

Before submitting a PR, ensure:

1. Your code runs without errors
2. Existing functionality still works
3. New features are tested with sample images
4. Error cases are handled gracefully

Run basic tests:
```bash
# Test with single image
python kingfisher.py examples/book.jpeg

# Test with multiple outputs
python kingfisher.py examples/book.jpeg --count 3
```

## Documentation

- Update the README.md if you change functionality
- Add docstrings to new functions
- Update CHANGELOG.md with your changes
- Include examples for new features

## Project Structure

```
kingfisher/
├── kingfisher.py          # Main application file
├── prompts/               # AI prompt templates
├── examples/              # Sample images
├── output/                # Generated images (git-ignored)
└── docs/                  # Additional documentation
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## Recognition

Contributors will be recognized in our README.md and release notes.

Thank you for contributing to Kingfisher! 🐦