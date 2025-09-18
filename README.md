# Kingfisher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-powered product photography tool that transforms a single product photo into professional marketing images automatically.**

Kingfisher automatically transforms a single product photo into multiple professional marketing images ready for e-commerce, social media, and advertising. Simply upload your product image and let AI handle the creative work - from background removal to generating compelling marketing scenes tailored to your product's characteristics.

## Features

- **One-Click Operation**: Upload one photo, get multiple marketing images
- **AI-Powered**: Uses Google Gemini 2.5 Flash for intelligent image generation
- **Smart Background Removal**: Automatic product isolation with transparency
- **Intelligent Analysis**: AI analyzes your product and creates targeted marketing strategies
- **Multiple Scenes**: Generate 1-5 different marketing scenarios
- **Organized Output**: Timestamped folders with all assets

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/))

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/kingfisher.git
cd kingfisher
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up your API key:**
```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

4. **Run Kingfisher:**
```bash
python kingfisher.py your-product.jpg
```

## Usage

### Basic Usage

Generate a single marketing image (default):
```bash
python kingfisher.py product.jpg
```

### Generate Multiple Images

Create multiple marketing variations:
```bash
python kingfisher.py product.jpg --count 3
python kingfisher.py product.jpg -c 5
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--count` | `-c` | Number of images to generate (1-5) | 1 |

### Example with Sample Images

```bash
# Test with included examples
python kingfisher.py examples/book.jpeg --count 2
```

## How It Works

Kingfisher follows a four-step AI workflow:

1. **Upload**: Process your product image
2. **Background Removal**: AI removes background, creates transparent cutout
3. **Analysis**: AI analyzes product and generates creative marketing strategy
4. **Generation**: AI creates professional marketing images based on analysis

## Output Structure

```
output/
└── 2024-01-15_143022/
    ├── original.jpg      # Your original image
    ├── cutout.png        # Product with transparent background
    ├── analysis.json     # AI analysis and creative strategy
    ├── scene1.jpg        # Marketing image 1
    ├── scene2.jpg        # Marketing image 2
    └── scene3.jpg        # Marketing image 3
```

## AI Models Used

Kingfisher leverages OpenRouter to access:

- **Product Analysis**: `google/gemini-2.5-flash`
- **Image Generation**: `google/gemini-2.5-flash-image-preview`

## API Costs

- Each run uses OpenRouter API credits
- Approximate cost: $0.01-0.05 per image generated
- Monitor your usage at [OpenRouter Dashboard](https://openrouter.ai/dashboard)

## Rate Limits

- OpenRouter has rate limits based on your plan
- The tool includes automatic retry logic with 15-second delays
- For heavy usage, consider upgrading your OpenRouter plan

## Troubleshooting

### Common Issues

**"OPENROUTER_API_KEY not found"**
- Ensure your `.env` file exists and contains your API key
- Check that you've copied `.env.example` to `.env`

**Rate limit errors**
- The tool automatically retries after 15 seconds
- Consider spacing out requests or upgrading your plan

**Image generation fallbacks**
- If generation fails, the tool copies the cutout as a fallback
- Check your internet connection and API status

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [OpenRouter](https://openrouter.ai/)
- Powered by Google's Gemini models
- Inspired by the need for accessible product photography

## Support

- [Report bugs](https://github.com/yourusername/kingfisher/issues)
- [Request features](https://github.com/yourusername/kingfisher/issues)
- [Documentation](https://github.com/yourusername/kingfisher/wiki)

---

<p align="center">Made with care by the Kingfisher team</p>