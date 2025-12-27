"""
Visual Effects Module
Applies various visual effects and filters to images
"""
import random
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
from typing import List, Tuple


class VisualEffects:
    """Applies visual effects to images"""

    @staticmethod
    def apply_glitch(img: Image.Image, intensity: float = 0.5) -> Image.Image:
        """Apply glitch effect by shuffling pixel rows"""
        img_array = np.array(img)
        height = img_array.shape[0]

        # Number of glitch lines based on intensity
        num_glitches = int(height * intensity * 0.3)

        for _ in range(num_glitches):
            y = random.randint(0, height - 1)
            shift = random.randint(-50, 50)

            if shift != 0:
                img_array[y] = np.roll(img_array[y], shift, axis=0)

        return Image.fromarray(img_array)

    @staticmethod
    def apply_color_shift(img: Image.Image, shift_amount: int = 30) -> Image.Image:
        """Shift color channels randomly"""
        r, g, b = img.split()

        # Shift each channel
        r_array = np.array(r)
        g_array = np.array(g)
        b_array = np.array(b)

        r_shift = random.randint(-shift_amount, shift_amount)
        g_shift = random.randint(-shift_amount, shift_amount)
        b_shift = random.randint(-shift_amount, shift_amount)

        r_array = np.clip(r_array + r_shift, 0, 255).astype(np.uint8)
        g_array = np.clip(g_array + g_shift, 0, 255).astype(np.uint8)
        b_array = np.clip(b_array + b_shift, 0, 255).astype(np.uint8)

        return Image.merge('RGB', (Image.fromarray(r_array), Image.fromarray(g_array), Image.fromarray(b_array)))

    @staticmethod
    def apply_vhs(img: Image.Image) -> Image.Image:
        """Apply VHS/retro effect"""
        # Blur slightly
        img = img.filter(ImageFilter.GaussianBlur(radius=1))

        # Color shift
        img = VisualEffects.apply_color_shift(img, shift_amount=20)

        # Add scanlines
        draw = ImageDraw.Draw(img)
        for y in range(0, img.height, 4):
            draw.line([(0, y), (img.width, y)], fill=(0, 0, 0, 30))

        return img

    @staticmethod
    def apply_posterize(img: Image.Image, bits: int = 3) -> Image.Image:
        """Reduce color depth for posterize effect"""
        return ImageOps.posterize(img, bits)

    @staticmethod
    def apply_solarize(img: Image.Image, threshold: int = 128) -> Image.Image:
        """Apply solarize effect"""
        return ImageOps.solarize(img, threshold)

    @staticmethod
    def apply_color_invert(img: Image.Image) -> Image.Image:
        """Invert colors"""
        return ImageOps.invert(img)

    @staticmethod
    def apply_contrast(img: Image.Image, factor: float = None) -> Image.Image:
        """Adjust contrast"""
        if factor is None:
            factor = random.uniform(0.5, 2.0)
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(factor)

    @staticmethod
    def apply_saturation(img: Image.Image, factor: float = None) -> Image.Image:
        """Adjust color saturation"""
        if factor is None:
            factor = random.uniform(0.5, 2.5)
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(factor)

    @staticmethod
    def apply_brightness(img: Image.Image, factor: float = None) -> Image.Image:
        """Adjust brightness"""
        if factor is None:
            factor = random.uniform(0.7, 1.5)
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(factor)

    @staticmethod
    def apply_blur(img: Image.Image, radius: int = None) -> Image.Image:
        """Apply blur"""
        if radius is None:
            radius = random.randint(2, 10)
        return img.filter(ImageFilter.GaussianBlur(radius))

    @staticmethod
    def apply_sharpen(img: Image.Image, factor: float = 2.0) -> Image.Image:
        """Apply sharpening"""
        enhancer = ImageEnhance.Sharpness(img)
        return enhancer.enhance(factor)

    @staticmethod
    def apply_edge_enhance(img: Image.Image) -> Image.Image:
        """Enhance edges"""
        return img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    @staticmethod
    def apply_emboss(img: Image.Image) -> Image.Image:
        """Apply emboss effect"""
        return img.filter(ImageFilter.EMBOSS)

    @staticmethod
    def apply_pixelate(img: Image.Image, pixel_size: int = None) -> Image.Image:
        """Apply pixelation effect"""
        if pixel_size is None:
            pixel_size = random.randint(10, 40)

        # Resize down
        small = img.resize(
            (img.width // pixel_size, img.height // pixel_size),
            Image.Resampling.NEAREST
        )

        # Resize back up
        return small.resize(img.size, Image.Resampling.NEAREST)

    @staticmethod
    def apply_chromatic_aberration(img: Image.Image, offset: int = 5) -> Image.Image:
        """Apply chromatic aberration effect"""
        r, g, b = img.split()

        # Shift red channel
        r_array = np.array(r)
        r_array = np.roll(r_array, offset, axis=1)

        # Shift blue channel
        b_array = np.array(b)
        b_array = np.roll(b_array, -offset, axis=1)

        return Image.merge('RGB', (Image.fromarray(r_array), g, Image.fromarray(b_array)))

    @staticmethod
    def apply_noise(img: Image.Image, intensity: float = 0.1) -> Image.Image:
        """Add random noise"""
        img_array = np.array(img, dtype=np.float32)

        noise = np.random.normal(0, intensity * 50, img_array.shape)
        img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)

        return Image.fromarray(img_array)

    @staticmethod
    def apply_gradient_map(img: Image.Image, colors: List[Tuple[int, int, int]] = None) -> Image.Image:
        """Apply gradient color mapping"""
        if colors is None:
            colors = [
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            ]

        # Convert to grayscale
        gray = img.convert('L')
        gray_array = np.array(gray)

        # Create gradient
        gradient = np.zeros((*gray_array.shape, 3), dtype=np.uint8)

        for i in range(3):  # RGB channels
            gradient[:, :, i] = np.interp(
                gray_array,
                [0, 255],
                [colors[0][i], colors[1][i]]
            )

        return Image.fromarray(gradient)

    @staticmethod
    def apply_random_effects(img: Image.Image, num_effects: int = None) -> Image.Image:
        """Apply random combination of effects"""
        if num_effects is None:
            num_effects = random.randint(2, 5)

        effects = [
            lambda x: VisualEffects.apply_glitch(x, random.uniform(0.1, 0.5)),
            lambda x: VisualEffects.apply_color_shift(x, random.randint(10, 50)),
            lambda x: VisualEffects.apply_posterize(x, random.randint(2, 5)),
            lambda x: VisualEffects.apply_solarize(x, random.randint(50, 200)),
            lambda x: VisualEffects.apply_contrast(x, random.uniform(0.8, 2.0)),
            lambda x: VisualEffects.apply_saturation(x, random.uniform(0.5, 3.0)),
            lambda x: VisualEffects.apply_brightness(x, random.uniform(0.8, 1.3)),
            lambda x: VisualEffects.apply_blur(x, random.randint(1, 5)),
            lambda x: VisualEffects.apply_sharpen(x, random.uniform(1.5, 3.0)),
            lambda x: VisualEffects.apply_pixelate(x, random.randint(5, 20)),
            lambda x: VisualEffects.apply_chromatic_aberration(x, random.randint(2, 8)),
            lambda x: VisualEffects.apply_noise(x, random.uniform(0.05, 0.15)),
        ]

        selected_effects = random.sample(effects, min(num_effects, len(effects)))

        result = img
        for effect in selected_effects:
            try:
                result = effect(result)
            except Exception as e:
                print(f"Effect failed: {e}")

        return result


if __name__ == '__main__':
    # Test effects
    print("=== Visual Effects Test ===\n")

    # Create a test image
    test_img = Image.new('RGB', (800, 800), (100, 150, 200))
    draw = ImageDraw.Draw(test_img)

    # Draw some shapes
    for _ in range(10):
        x1, y1 = random.randint(0, 800), random.randint(0, 800)
        x2, y2 = random.randint(0, 800), random.randint(0, 800)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.rectangle([x1, y1, x2, y2], fill=color)

    # Apply random effects
    print("Applying random effects...")
    result = VisualEffects.apply_random_effects(test_img, num_effects=5)

    # Save
    result.save('downloads/test_effects.jpg')
    print("Saved to downloads/test_effects.jpg")
