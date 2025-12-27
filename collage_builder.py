"""
Collage Builder Module
Creates collages from multiple images with various layouts
"""
import random
import math
from PIL import Image
from typing import List, Tuple


class CollageBuilder:
    """Creates image collages with various layouts"""

    def __init__(self, output_size: Tuple[int, int] = (2400, 2400)):
        self.output_size = output_size

    def create_grid_collage(self, images: List[Image.Image], grid_size: Tuple[int, int] = None) -> Image.Image:
        """
        Create a grid-based collage

        Args:
            images: List of PIL Images
            grid_size: (cols, rows) tuple, auto-calculated if None

        Returns:
            Collage image
        """
        if not images:
            raise ValueError("No images provided")

        # Auto-calculate grid size if not provided
        if grid_size is None:
            n = len(images)
            cols = math.ceil(math.sqrt(n))
            rows = math.ceil(n / cols)
            grid_size = (cols, rows)

        cols, rows = grid_size
        cell_width = self.output_size[0] // cols
        cell_height = self.output_size[1] // rows

        # Create blank canvas
        collage = Image.new('RGB', self.output_size, (255, 255, 255))

        # Place images
        for idx, img in enumerate(images[:cols * rows]):
            row = idx // cols
            col = idx % cols

            # Resize image to fit cell
            img_resized = self._resize_to_fill(img, (cell_width, cell_height))

            # Paste into collage
            x = col * cell_width
            y = row * cell_height
            collage.paste(img_resized, (x, y))

        return collage

    def create_random_collage(self, images: List[Image.Image], num_images: int = None) -> Image.Image:
        """
        Create a collage with randomly sized and positioned images

        Args:
            images: List of PIL Images
            num_images: Number of images to use (None for all)

        Returns:
            Collage image
        """
        if not images:
            raise ValueError("No images provided")

        if num_images is None:
            num_images = len(images)

        # Create blank canvas
        collage = Image.new('RGB', self.output_size, (0, 0, 0))

        # Shuffle images
        selected_images = random.sample(images, min(num_images, len(images)))

        for img in selected_images:
            # Random size (20% to 60% of canvas)
            scale = random.uniform(0.2, 0.6)
            width = int(self.output_size[0] * scale)
            height = int(self.output_size[1] * scale)

            # Resize image
            img_resized = self._resize_to_fill(img, (width, height))

            # Random position
            x = random.randint(-width // 3, self.output_size[0] - width // 2)
            y = random.randint(-height // 3, self.output_size[1] - height // 2)

            # Random rotation
            angle = random.randint(-30, 30)
            img_resized = img_resized.rotate(angle, expand=True)

            # Paste with blend
            try:
                collage.paste(img_resized, (x, y))
            except Exception:
                pass  # Skip if paste fails

        return collage

    def create_mosaic_collage(self, images: List[Image.Image], tile_size: int = 200) -> Image.Image:
        """
        Create a mosaic-style collage with varying tile sizes

        Args:
            images: List of PIL Images
            tile_size: Base tile size

        Returns:
            Collage image
        """
        if not images:
            raise ValueError("No images provided")

        collage = Image.new('RGB', self.output_size, (255, 255, 255))

        x, y = 0, 0
        row_height = 0
        img_idx = 0

        while y < self.output_size[1] and img_idx < len(images):
            # Randomize tile size
            size_multiplier = random.choice([0.5, 0.75, 1.0, 1.5, 2.0])
            tile_w = int(tile_size * size_multiplier)
            tile_h = int(tile_size * size_multiplier)

            # Don't exceed canvas
            if x + tile_w > self.output_size[0]:
                x = 0
                y += row_height
                row_height = 0
                continue

            if y + tile_h > self.output_size[1]:
                break

            # Get next image
            img = images[img_idx % len(images)]
            img_idx += 1

            # Resize to tile
            img_resized = self._resize_to_fill(img, (tile_w, tile_h))

            # Paste
            collage.paste(img_resized, (x, y))

            # Update position
            x += tile_w
            row_height = max(row_height, tile_h)

        return collage

    def create_scattered_collage(self, images: List[Image.Image], num_layers: int = 3) -> Image.Image:
        """
        Create a collage with layered, scattered images

        Args:
            images: List of PIL Images
            num_layers: Number of image layers

        Returns:
            Collage image
        """
        if not images:
            raise ValueError("No images provided")

        collage = Image.new('RGB', self.output_size, (20, 20, 20))

        images_per_layer = len(images) // num_layers + 1

        for layer in range(num_layers):
            layer_images = images[layer * images_per_layer:(layer + 1) * images_per_layer]

            for img in layer_images:
                # Size decreases with layer
                scale = random.uniform(0.3, 0.7) * (1 - layer * 0.2)
                width = int(self.output_size[0] * scale)
                height = int(self.output_size[1] * scale)

                # Resize
                img_resized = self._resize_to_fill(img, (width, height))

                # Random position
                x = random.randint(0, max(0, self.output_size[0] - width))
                y = random.randint(0, max(0, self.output_size[1] - height))

                # Random rotation
                angle = random.randint(-20, 20)
                img_resized = img_resized.rotate(angle, expand=True)

                # Apply transparency for layering effect
                if img_resized.mode != 'RGBA':
                    img_resized = img_resized.convert('RGBA')

                alpha = int(255 * random.uniform(0.7, 1.0))
                img_resized.putalpha(alpha)

                # Paste
                try:
                    collage.paste(img_resized, (x, y), img_resized)
                except Exception:
                    pass

        return collage.convert('RGB')

    def _resize_to_fill(self, img: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """Resize image to fill the target size (crop if needed)"""
        target_ratio = size[0] / size[1]
        img_ratio = img.width / img.height

        if img_ratio > target_ratio:
            # Image is wider
            new_height = size[1]
            new_width = int(new_height * img_ratio)
        else:
            # Image is taller
            new_width = size[0]
            new_height = int(new_width / img_ratio)

        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Crop to exact size
        left = (new_width - size[0]) // 2
        top = (new_height - size[1]) // 2
        right = left + size[0]
        bottom = top + size[1]

        return img_resized.crop((left, top, right, bottom))


if __name__ == '__main__':
    # Test with some colored rectangles
    print("=== Collage Builder Test ===\n")

    # Create test images
    test_images = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
              (255, 0, 255), (0, 255, 255), (128, 128, 128)]

    for i, color in enumerate(colors):
        img = Image.new('RGB', (400, 400), color)
        test_images.append(img)

    builder = CollageBuilder(output_size=(1200, 1200))

    print("Creating grid collage...")
    grid = builder.create_grid_collage(test_images)
    grid.save('downloads/test_grid.jpg')

    print("Creating random collage...")
    random_c = builder.create_random_collage(test_images)
    random_c.save('downloads/test_random.jpg')

    print("Creating mosaic collage...")
    mosaic = builder.create_mosaic_collage(test_images)
    mosaic.save('downloads/test_mosaic.jpg')

    print("\nTest collages saved to downloads/")
