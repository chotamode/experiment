"""
Image Downloader Module
Downloads and caches images from URLs
"""
import os
import hashlib
import requests
from PIL import Image
from io import BytesIO
from typing import List, Optional
import time
import random


class ImageDownloader:
    """Downloads and manages image files"""

    def __init__(self, download_dir='downloads', cache_dir='cache'):
        self.download_dir = download_dir
        self.cache_dir = cache_dir
        os.makedirs(download_dir, exist_ok=True)
        os.makedirs(cache_dir, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def _get_cache_path(self, url: str) -> str:
        """Generate cache file path from URL"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{url_hash}.jpg")

    def download_image(self, url: str, timeout: int = 10) -> Optional[Image.Image]:
        """
        Download an image from URL

        Args:
            url: Image URL
            timeout: Request timeout in seconds

        Returns:
            PIL Image object or None if failed
        """
        # Check cache first
        cache_path = self._get_cache_path(url)
        if os.path.exists(cache_path):
            try:
                return Image.open(cache_path)
            except Exception:
                pass

        # Download image
        try:
            time.sleep(random.uniform(0.1, 0.5))  # Rate limiting
            response = self.session.get(url, timeout=timeout, stream=True)
            response.raise_for_status()

            # Load image
            img = Image.open(BytesIO(response.content))

            # Convert to RGB if needed
            if img.mode in ('RGBA', 'P', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1])
                    img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Cache the image
            try:
                img.save(cache_path, 'JPEG', quality=85)
            except Exception as e:
                print(f"Warning: Could not cache image: {e}")

            return img

        except Exception as e:
            print(f"Failed to download {url[:60]}...: {e}")
            return None

    def download_multiple(self, urls: List[str], max_images: Optional[int] = None) -> List[Image.Image]:
        """
        Download multiple images

        Args:
            urls: List of image URLs
            max_images: Maximum number of images to download (None for all)

        Returns:
            List of PIL Image objects
        """
        images = []
        count = 0

        for url in urls:
            if max_images and count >= max_images:
                break

            img = self.download_image(url)
            if img:
                images.append(img)
                count += 1
                print(f"Downloaded {count}/{max_images or len(urls)}")

        return images

    def download_from_search_results(self, results: List[dict], max_images: int = 20) -> List[Image.Image]:
        """
        Download images from search results

        Args:
            results: List of search result dictionaries
            max_images: Maximum number of images to download

        Returns:
            List of PIL Image objects
        """
        urls = [r['url'] for r in results if r.get('url')]
        return self.download_multiple(urls, max_images=max_images)

    def save_image(self, image: Image.Image, filename: str, quality: int = 95):
        """Save an image to the download directory"""
        filepath = os.path.join(self.download_dir, filename)
        image.save(filepath, 'JPEG', quality=quality)
        return filepath


if __name__ == '__main__':
    # Test the downloader
    from kanji_generator import KanjiGenerator
    from image_search import ImageSearcher

    gen = KanjiGenerator()
    searcher = ImageSearcher()
    downloader = ImageDownloader()

    print("=== Image Downloader Test ===\n")

    # Generate a query and search
    query = gen.generate_query()
    print(f"Query: {query}\n")

    results = searcher.search_duckduckgo(query, max_results=5)
    print(f"Found {len(results)} images\n")

    if results:
        print("Downloading images...")
        images = downloader.download_from_search_results(results, max_images=3)
        print(f"\nSuccessfully downloaded {len(images)} images")

        for i, img in enumerate(images):
            print(f"  Image {i+1}: {img.size} ({img.mode})")
