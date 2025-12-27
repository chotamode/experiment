# 🎨 Kanji Collage Generator

**Create surreal artistic collages from random Japanese kanji-based image searches**

This application generates random Japanese kanji combinations to search for obscure, unexpected, and often surreal images from the internet, then creates artistic collages with various visual effects.

## ⚡ Super Fast Start

**Want to run immediately without manual setup?**

### 🖼️ **GUI Mode** (Recommended - Easy & Visual):

> **Linux users:** Install `python3-tk` first: `sudo apt install python3-tk` (Ubuntu/Debian)

**Linux/Mac:**
```bash
./run-gui.sh
```

**Windows:**
```batch
run-gui.bat
```

### 💻 **Command Line Mode:**

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```batch
run.bat
```

**First run**: Auto-installs everything (~30 seconds, or **2-3 seconds with uv**!)
**After that**: Instant startup! ⚡

See [QUICKSTART.md](QUICKSTART.md) for more options and uv installation guide.

---

## 🖼️ GUI Features

The graphical interface provides a comfortable, visual way to create collages:

- **Easy Settings**: Sliders, dropdowns, and spinboxes for all options
- **Quick Presets**: One-click presets for common use cases
  - ⚡ Quick Test (fast, small output)
  - 🎨 Chaos Mode (pure random, heavy effects)
  - 🖼️ Clean Grid (organized, no effects)
  - 🌈 Large Wallpaper (3000px, many images)
- **Real-Time Progress**: See exactly what's happening during generation
- **Live Logs**: Detailed generation logs with timestamps
- **Folder Integration**: Open downloads folder with one click
- **Cache Management**: Clear cache easily from the GUI

**No command-line knowledge required!** Perfect for artists and casual users.

---

## ✨ Core Features

- 🔮 **Random Kanji Generation**: Multiple modes for generating kanji queries
  - **Themed**: Uses curated kanji from categories (nature, mystical, abstract, etc.)
  - **Mixed**: Combines themed kanji with completely random Unicode kanji
  - **Nonsense**: Pure random kanji from Unicode ranges
  - **Auto**: Randomly selects between modes

- 🔍 **Image Search**: Uses DuckDuckGo to find images using the random kanji queries
  - Search engines often "hallucinate" and return unexpected, artistic results
  - No API keys required

- 🖼️ **Multiple Collage Layouts**:
  - **Grid**: Organized grid layout
  - **Random**: Randomly positioned and rotated images
  - **Mosaic**: Varying tile sizes in a mosaic pattern
  - **Scattered**: Layered, overlapping images with transparency

- ✨ **Visual Effects Engine**:
  - Glitch effects
  - Color shifting and chromatic aberration
  - VHS/retro effects
  - Posterize, solarize, invert
  - Blur, sharpen, pixelate
  - Noise and distortion
  - Contrast, saturation, brightness adjustments
  - And many more!

- 💾 **Smart Caching**: Downloaded images are cached to avoid re-downloading

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. Clone or download this repository

2. Install dependencies:

```bash
pip install -r requirements.txt
```

That's it! No API keys or additional configuration needed.

## 📖 Usage

### Basic Usage

Generate a collage with default settings:

```bash
python main.py
```

This will:
- Generate 5 random kanji queries
- Search for ~10 images per query
- Download up to 30 images
- Create a random-layout collage (2400x2400px)
- Apply 3 random visual effects
- Save to `downloads/kanji_collage_TIMESTAMP.jpg`

### Command Line Options

```bash
python main.py [OPTIONS]
```

#### Options:

- `-q, --queries N`: Number of random kanji queries (default: 5)
- `-i, --images-per-query N`: Images to fetch per query (default: 10)
- `-m, --max-images N`: Maximum images to download (default: 30)
- `-t, --type TYPE`: Collage layout type
  - Choices: `grid`, `random`, `mosaic`, `scattered`
  - Default: `random`
- `-s, --size PIXELS`: Output size in pixels (square) (default: 2400)
- `-e, --effects N`: Visual effects intensity 0-5 (default: 3)
  - 0: No effects
  - 1-2: Light effects
  - 3-4: Moderate effects
  - 5: Heavy effects
- `-k, --kanji-mode MODE`: Kanji generation mode
  - Choices: `themed`, `mixed`, `random`, `nonsense`, `auto`
  - Default: `mixed`
- `--no-effects`: Disable all visual effects

### Examples

**Create a large mosaic with many images:**
```bash
python main.py -q 10 -i 50 -m 100 -t mosaic -s 3000
```

**Grid layout with no effects (clean collage):**
```bash
python main.py -t grid --no-effects
```

**Extreme chaos mode (pure random kanji, scattered layout, heavy effects):**
```bash
python main.py -k nonsense -t scattered -e 5 -q 15
```

**Themed kanji with light effects:**
```bash
python main.py -k themed -e 1
```

**Quick test (few images, small size):**
```bash
python main.py -q 3 -m 10 -s 1200 -e 2
```

## 🎭 Kanji Modes Explained

### Themed
Uses curated kanji from thematic categories:
- 🌲 Nature: 森 (forest), 山 (mountain), 海 (sea), etc.
- 🌙 Abstract: 夢 (dream), 影 (shadow), 幻 (illusion), etc.
- 🎨 Colors: 赤 (red), 青 (blue), 虚 (void), etc.
- 🐉 Creatures: 龍 (dragon), 鳥 (bird), 鬼 (demon), etc.
- ✨ Mystical: 神 (god), 魔 (magic), 霊 (spirit), etc.
- ⏰ Time: 永 (eternity), 刹那 (moment), etc.

Example queries: `森影龍`, `夢虚神`, `海闇月`

### Mixed
Combines themed kanji with completely random Unicode kanji from the CJK ranges. Creates interesting combinations of recognizable and obscure characters.

Example queries: `森㐀龍`, `夢䶮影㸗`, `海𠀀星`

### Random/Nonsense
Pure random selection from Unicode CJK Unified Ideographs ranges. Often produces completely nonsensical combinations that make search engines return the most unexpected results.

Example queries: `㗊䶮㸗𠀀`, `𩸽䀀㐀㗊`, `䷀𠀀㐀`

### Auto
Randomly selects between themed, mixed, and nonsense modes for each query.

## 🖼️ Collage Types Explained

### Grid
Organized grid layout where images fill cells evenly. Clean and structured.

### Random
Images are randomly sized (20-60% of canvas), positioned (can overlap edges), and rotated (-30° to +30°). Creates dynamic, chaotic compositions.

### Mosaic
Variable-sized rectangular tiles fill the canvas like a mosaic. Tiles are 0.5x to 2x the base size.

### Scattered
Multiple layers of images with transparency, random positions, and rotations. Creates depth and overlay effects.

## 🎨 Visual Effects

The effects engine can apply combinations of:

- **Glitch**: Pixel row shifting
- **Color Shift**: Random RGB channel adjustments
- **VHS**: Retro video effect with scanlines
- **Posterize**: Reduced color depth
- **Solarize**: Inverted colors above threshold
- **Chromatic Aberration**: RGB channel separation
- **Pixelate**: Retro pixel art effect
- **Blur/Sharpen**: Focus adjustments
- **Noise**: Random pixel noise
- **Contrast/Saturation/Brightness**: Color adjustments

Effects are randomly selected and applied in random order.

## 📁 Project Structure

```
kanji-collage-generator/
├── main.py                 # CLI application entry point
├── kanji_generator.py      # Random kanji generation
├── image_search.py         # DuckDuckGo image search
├── image_downloader.py     # Image downloading and caching
├── collage_builder.py      # Collage layout engine
├── visual_effects.py       # Visual effects and filters
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── downloads/             # Output collages (created automatically)
└── cache/                 # Cached images (created automatically)
```

## 🔧 Advanced Usage

### Using as a Library

You can import and use the modules in your own Python code:

```python
from kanji_generator import KanjiGenerator
from image_search import ImageSearcher
from image_downloader import ImageDownloader
from collage_builder import CollageBuilder
from visual_effects import VisualEffects

# Generate kanji
gen = KanjiGenerator()
queries = [gen.generate_query('mixed') for _ in range(5)]

# Search for images
searcher = ImageSearcher()
results = searcher.search_multiple_queries(queries, images_per_query=10)

# Download images
downloader = ImageDownloader()
images = downloader.download_from_search_results(results, max_images=20)

# Create collage
builder = CollageBuilder(output_size=(2000, 2000))
collage = builder.create_random_collage(images)

# Apply effects
effects = VisualEffects()
collage = effects.apply_random_effects(collage, num_effects=3)

# Save
collage.save('my_collage.jpg', quality=95)
```

### Testing Individual Modules

Each module has test code at the bottom. Run individually:

```bash
python kanji_generator.py     # Test kanji generation
python image_search.py        # Test image search
python image_downloader.py    # Test downloading
python collage_builder.py     # Test collage layouts
python visual_effects.py      # Test effects
```

## 🎯 Tips for Best Results

1. **More queries, more variety**: Use `-q 10` or more for diverse images
2. **Experiment with kanji modes**: `nonsense` mode often gives the weirdest results
3. **Try different layouts**: Each collage type creates a unique aesthetic
4. **Effects make it art**: Don't skip effects! `-e 3` to `-e 5` recommended
5. **Large outputs**: Use `-s 3000` or higher for wallpaper-quality images
6. **Be patient**: Downloading 50+ images takes a few minutes

## ⚠️ Notes

- **Rate Limiting**: The app includes delays between requests to be respectful to search engines
- **Image Availability**: Some image URLs may fail to download (404, timeouts, etc.)
- **Internet Required**: This app requires an active internet connection
- **Disk Space**: Cached images accumulate in `cache/` directory
- **Random Results**: Output is intentionally random and unpredictable!

## 🧹 Maintenance

Clear the cache to free up space:
```bash
rm -rf cache/
```

Clear old outputs:
```bash
rm -rf downloads/
```

## 🐛 Troubleshooting

**No images found:**
- Try different kanji modes (`-k auto` or `-k mixed`)
- Increase queries (`-q 10`)

**Download failures:**
- Some image URLs expire or block downloads
- The app will skip failed downloads automatically
- Increase `--max-images` to compensate

**Out of memory:**
- Reduce `--max-images`
- Reduce `--size`

**Slow generation:**
- Reduce number of queries and images
- Check internet connection

## 📜 License

This project is open source and available for personal and educational use.

## 🙏 Acknowledgments

- Uses DuckDuckGo for image search (no API key required)
- Built with Pillow (PIL) for image manipulation
- Rich library for beautiful CLI output

## 🎨 Gallery Ideas

Try these presets for different artistic styles:

**Vaporwave Aesthetic:**
```bash
python main.py -k themed -t scattered -e 4 -q 8
```

**Glitch Art:**
```bash
python main.py -k nonsense -t random -e 5 -q 10
```

**Clean Gallery:**
```bash
python main.py -k themed -t grid --no-effects -m 16
```

**Surreal Dreams:**
```bash
python main.py -k mixed -t scattered -e 3 -q 12 -s 3000
```

---

**Have fun creating surreal art from the chaos of random kanji! 🎨✨**
