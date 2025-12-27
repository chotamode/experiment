"""
Image Search Module
Searches for images using various search engines
"""
import os
import time
import random
from typing import List, Dict
from duckduckgo_search import DDGS


class ImageSearcher:
    """Searches for images using search engines"""

    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def search_duckduckgo(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Search for images using DuckDuckGo

        Args:
            query: Search query (kanji or any text)
            max_results: Maximum number of results to return

        Returns:
            List of image dictionaries with 'url', 'title', 'thumbnail' keys
        """
        results = []

        try:
            with DDGS() as ddgs:
                # Add small delay to be respectful
                time.sleep(random.uniform(0.5, 1.5))

                images = ddgs.images(
                    keywords=query,
                    max_results=max_results,
                    safesearch='off'  # Get more varied results
                )

                for img in images:
                    results.append({
                        'url': img.get('image', ''),
                        'title': img.get('title', ''),
                        'thumbnail': img.get('thumbnail', ''),
                        'source': img.get('source', ''),
                        'width': img.get('width', 0),
                        'height': img.get('height', 0)
                    })

        except Exception as e:
            print(f"Error searching for '{query}': {e}")

        return results

    def search_multiple_queries(self, queries: List[str], images_per_query: int = 10) -> List[Dict]:
        """
        Search multiple queries and combine results

        Args:
            queries: List of search queries
            images_per_query: Number of images to fetch per query

        Returns:
            Combined list of image results
        """
        all_results = []

        for query in queries:
            print(f"Searching for: {query}")
            results = self.search_duckduckgo(query, max_results=images_per_query)
            print(f"  Found {len(results)} images")

            # Add query info to results
            for result in results:
                result['query'] = query

            all_results.extend(results)

            # Be respectful with rate limiting
            time.sleep(random.uniform(1, 2))

        return all_results


if __name__ == '__main__':
    # Test the image searcher
    from kanji_generator import KanjiGenerator

    gen = KanjiGenerator()
    searcher = ImageSearcher()

    print("=== Image Search Test ===\n")

    # Generate some queries
    queries = [gen.generate_query() for _ in range(3)]
    print(f"Generated queries: {queries}\n")

    # Search for images
    results = searcher.search_multiple_queries(queries, images_per_query=5)

    print(f"\nTotal images found: {len(results)}")
    if results:
        print("\nSample results:")
        for i, result in enumerate(results[:5]):
            print(f"{i+1}. Query: {result.get('query', 'N/A')}")
            print(f"   Title: {result.get('title', 'N/A')}")
            print(f"   URL: {result.get('url', 'N/A')[:80]}...")
            print()
