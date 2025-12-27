#!/usr/bin/env python3
"""
Kanji Collage Generator
Creates artistic collages from random kanji-based image searches
"""
import os
import argparse
import random
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

from kanji_generator import KanjiGenerator
from image_search import ImageSearcher
from image_downloader import ImageDownloader
from collage_builder import CollageBuilder
from visual_effects import VisualEffects


console = Console()


class KanjiCollageApp:
    """Main application class"""

    def __init__(self):
        self.kanji_gen = KanjiGenerator()
        self.searcher = ImageSearcher()
        self.downloader = ImageDownloader()
        self.effects = VisualEffects()

    def generate_collage(
        self,
        num_queries: int = 5,
        images_per_query: int = 10,
        max_images: int = 30,
        collage_type: str = 'random',
        output_size: tuple = (2400, 2400),
        apply_effects: bool = True,
        effect_intensity: int = 3,
        kanji_mode: str = 'mixed'
    ):
        """
        Generate a complete collage

        Args:
            num_queries: Number of kanji queries to generate
            images_per_query: Images to fetch per query
            max_images: Maximum images to download
            collage_type: Type of collage (grid, random, mosaic, scattered)
            output_size: Output image size (width, height)
            apply_effects: Whether to apply visual effects
            effect_intensity: Number of effects to apply (1-5)
            kanji_mode: Kanji generation mode (themed, mixed, random, nonsense, auto)
        """
        console.print(Panel.fit(
            "[bold cyan]🎨 Kanji Collage Generator[/bold cyan]\n"
            "[dim]Creating art from the chaos of random kanji[/dim]",
            border_style="cyan"
        ))

        # Step 1: Generate kanji queries
        console.print("\n[bold yellow]🔮 Generating random kanji queries...[/bold yellow]")
        queries = []
        for i in range(num_queries):
            query = self.kanji_gen.generate_query(mode=kanji_mode)
            queries.append(query)
            console.print(f"  {i+1}. [bold magenta]{query}[/bold magenta]")

        # Step 2: Search for images
        console.print(f"\n[bold yellow]🔍 Searching for images...[/bold yellow]")
        all_results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Searching...", total=len(queries))

            for query in queries:
                results = self.searcher.search_duckduckgo(query, max_results=images_per_query)
                all_results.extend(results)
                progress.update(task, advance=1, description=f"[cyan]Searched: {query}")

        console.print(f"  [green]✓[/green] Found {len(all_results)} images total")

        if not all_results:
            console.print("[red]✗ No images found. Try different kanji modes.[/red]")
            return None

        # Step 3: Download images
        console.print(f"\n[bold yellow]⬇️  Downloading images...[/bold yellow]")
        images = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Downloading...", total=min(max_images, len(all_results)))

            for idx, result in enumerate(all_results[:max_images]):
                img = self.downloader.download_image(result['url'])
                if img:
                    images.append(img)
                    progress.update(task, advance=1, description=f"[cyan]Downloaded {len(images)}/{max_images}")

        console.print(f"  [green]✓[/green] Downloaded {len(images)} images")

        if not images:
            console.print("[red]✗ Failed to download any images.[/red]")
            return None

        # Step 4: Create collage
        console.print(f"\n[bold yellow]🖼️  Creating {collage_type} collage...[/bold yellow]")
        builder = CollageBuilder(output_size=output_size)

        if collage_type == 'grid':
            collage = builder.create_grid_collage(images)
        elif collage_type == 'random':
            collage = builder.create_random_collage(images)
        elif collage_type == 'mosaic':
            collage = builder.create_mosaic_collage(images)
        elif collage_type == 'scattered':
            collage = builder.create_scattered_collage(images)
        else:
            collage = builder.create_random_collage(images)

        console.print(f"  [green]✓[/green] Collage created")

        # Step 5: Apply visual effects
        if apply_effects and effect_intensity > 0:
            console.print(f"\n[bold yellow]✨ Applying visual effects (intensity: {effect_intensity})...[/bold yellow]")
            collage = self.effects.apply_random_effects(collage, num_effects=effect_intensity)
            console.print(f"  [green]✓[/green] Effects applied")

        # Step 6: Save output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"kanji_collage_{timestamp}.jpg"
        filepath = self.downloader.save_image(collage, filename, quality=95)

        console.print(f"\n[bold green]✓ Collage saved:[/bold green] [cyan]{filepath}[/cyan]")

        # Show stats
        stats = Table(title="Generation Stats", show_header=False, box=None)
        stats.add_row("Queries generated", str(num_queries))
        stats.add_row("Images found", str(len(all_results)))
        stats.add_row("Images downloaded", str(len(images)))
        stats.add_row("Collage type", collage_type)
        stats.add_row("Output size", f"{output_size[0]}x{output_size[1]}")
        stats.add_row("Effects applied", str(effect_intensity) if apply_effects else "None")

        console.print("\n")
        console.print(stats)

        return filepath


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate artistic collages from random kanji-based image searches",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Generate with default settings
  %(prog)s -q 10 -i 50 -t mosaic    # 10 queries, 50 images, mosaic layout
  %(prog)s -t grid -e 0              # Grid layout, no effects
  %(prog)s -k nonsense -t scattered  # Pure random kanji, scattered layout
  %(prog)s --size 3000 -e 5          # Large output, heavy effects
        """
    )

    parser.add_argument(
        '-q', '--queries',
        type=int,
        default=5,
        help='Number of random kanji queries to generate (default: 5)'
    )

    parser.add_argument(
        '-i', '--images-per-query',
        type=int,
        default=10,
        help='Number of images to fetch per query (default: 10)'
    )

    parser.add_argument(
        '-m', '--max-images',
        type=int,
        default=30,
        help='Maximum total images to download (default: 30)'
    )

    parser.add_argument(
        '-t', '--type',
        choices=['grid', 'random', 'mosaic', 'scattered'],
        default='random',
        help='Collage layout type (default: random)'
    )

    parser.add_argument(
        '-s', '--size',
        type=int,
        default=2400,
        help='Output size in pixels (square) (default: 2400)'
    )

    parser.add_argument(
        '-e', '--effects',
        type=int,
        default=3,
        choices=[0, 1, 2, 3, 4, 5],
        help='Visual effects intensity 0-5 (default: 3, 0=none)'
    )

    parser.add_argument(
        '-k', '--kanji-mode',
        choices=['themed', 'mixed', 'random', 'nonsense', 'auto'],
        default='mixed',
        help='Kanji generation mode (default: mixed)'
    )

    parser.add_argument(
        '--no-effects',
        action='store_true',
        help='Disable visual effects'
    )

    args = parser.parse_args()

    # Create app and generate
    app = KanjiCollageApp()

    try:
        app.generate_collage(
            num_queries=args.queries,
            images_per_query=args.images_per_query,
            max_images=args.max_images,
            collage_type=args.type,
            output_size=(args.size, args.size),
            apply_effects=not args.no_effects and args.effects > 0,
            effect_intensity=args.effects,
            kanji_mode=args.kanji_mode
        )
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠ Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]✗ Error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
