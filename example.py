#!/usr/bin/env python3
"""
Quick Example Script
Demonstrates using the Kanji Collage Generator as a library
"""

from kanji_generator import KanjiGenerator
from image_search import ImageSearcher
from image_downloader import ImageDownloader
from collage_builder import CollageBuilder
from visual_effects import VisualEffects


def main():
    print("=== Kanji Collage Generator - Library Example ===\n")

    # Step 1: Generate some random kanji queries
    print("1. Generating kanji queries...")
    gen = KanjiGenerator()

    queries = [
        gen.generate_themed_query(),
        gen.generate_mixed_query(),
        gen.generate_nonsense_query()
    ]

    print(f"   Generated queries: {', '.join(queries)}\n")

    # Step 2: Search for images
    print("2. Searching for images...")
    searcher = ImageSearcher()
    results = searcher.search_multiple_queries(queries, images_per_query=5)
    print(f"   Found {len(results)} images\n")

    if not results:
        print("   No images found. Exiting.")
        return

    # Step 3: Download images
    print("3. Downloading images...")
    downloader = ImageDownloader()
    images = downloader.download_from_search_results(results, max_images=15)
    print(f"   Downloaded {len(images)} images\n")

    if not images:
        print("   No images downloaded. Exiting.")
        return

    # Step 4: Create a collage
    print("4. Creating collage...")
    builder = CollageBuilder(output_size=(1800, 1800))
    collage = builder.create_random_collage(images)
    print("   Collage created!\n")

    # Step 5: Apply some visual effects
    print("5. Applying visual effects...")
    effects = VisualEffects()
    collage = effects.apply_random_effects(collage, num_effects=3)
    print("   Effects applied!\n")

    # Step 6: Save the result
    print("6. Saving collage...")
    filepath = downloader.save_image(collage, 'example_collage.jpg', quality=90)
    print(f"   Saved to: {filepath}\n")

    print("✓ Done! Check the downloads folder for your collage.")


if __name__ == '__main__':
    main()
