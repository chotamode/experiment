"""
Image Search Module
Searches for images using various search engines
"""
import os
import time
import random
from typing import List, Dict

try:
    from ddgs import DDGS
except ImportError:
    # Fallback to old package name
    from duckduckgo_search import DDGS


class ImageSearcher:
    """Searches for images using search engines"""

    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def search_duckduckgo(self, query: str, max_results: int = 20, retry_count: int = 3) -> List[Dict]:
        """
        Search for images using DuckDuckGo with retry logic

        Args:
            query: Search query (kanji or any text)
            max_results: Maximum number of results to return
            retry_count: Number of retries on rate limit (default: 3)

        Returns:
            List of image dictionaries with 'url', 'title', 'thumbnail' keys
        """
        results = []

        for attempt in range(retry_count):
            try:
                # Add delay before search to avoid rate limiting
                if attempt > 0:
                    # Exponential backoff on retry
                    delay = (2 ** attempt) + random.uniform(1, 3)
                    print(f"  Rate limited, waiting {delay:.1f}s before retry {attempt + 1}/{retry_count}...")
                    time.sleep(delay)
                else:
                    # Initial delay
                    time.sleep(random.uniform(2, 4))

                with DDGS() as ddgs:
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

                # If we got results, break out of retry loop
                if results:
                    break

            except Exception as e:
                error_msg = str(e)
                if '202' in error_msg or 'Ratelimit' in error_msg:
                    if attempt < retry_count - 1:
                        continue  # Try again
                    else:
                        print(f"Rate limit exceeded for '{query}' after {retry_count} attempts")
                else:
                    print(f"Error searching for '{query}': {e}")
                    break

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
