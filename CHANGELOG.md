# Changelog

All notable changes to Kingfisher will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub repository setup and documentation
- Security improvements for API key handling

## [1.0.0] - 2024-09-18

### Added
- Initial release of Kingfisher
- One-click product photography transformation
- AI-powered background removal using Google Gemini 2.5 Flash
- Intelligent product analysis and creative direction generation
- Batch image generation (1-5 marketing images)
- Support for JPEG and PNG input formats
- Automatic retry logic for rate limits
- Organized output with timestamps
- Command-line interface with Click
- OpenRouter API integration
- Customizable prompt templates
- Example images for testing

### Features
- **Background Removal**: Automatic isolation of products with transparent backgrounds
- **Product Analysis**: AI analyzes product type, category, and style
- **Scene Generation**: Creates targeted marketing scenes based on product analysis
- **Batch Processing**: Generate multiple variations with `--count` parameter
- **Error Handling**: Graceful fallbacks and retry mechanisms
- **Model Validation**: Checks for required AI models before processing

### Technical Details
- Python 3.8+ compatibility
- Uses OpenAI Python client for OpenRouter API
- PIL/Pillow for image processing
- Click for CLI interface
- python-dotenv for environment management

## [0.1.0] - 2024-09-11

### Added
- Initial prototype development
- Basic image processing pipeline
- Project planning documentation

---

## Versioning Guide

- **Major version (X.0.0)**: Incompatible API changes
- **Minor version (0.X.0)**: Backwards-compatible functionality additions
- **Patch version (0.0.X)**: Backwards-compatible bug fixes

## Future Roadmap

### Planned Features
- [ ] Web interface option
- [ ] Batch processing for multiple products
- [ ] Additional AI model support
- [ ] Custom scene templates
- [ ] Export to different formats (WebP, AVIF)
- [ ] Progress indicators
- [ ] Configuration file support
- [ ] Docker support