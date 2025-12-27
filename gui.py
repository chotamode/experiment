#!/usr/bin/env python3
"""
Kanji Collage Generator - GUI Application
Beautiful graphical interface for creating collages
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import os
from datetime import datetime
from PIL import Image, ImageTk

from kanji_generator import KanjiGenerator
from image_search import ImageSearcher
from image_downloader import ImageDownloader
from collage_builder import CollageBuilder
from visual_effects import VisualEffects


class KanjiCollageGUI:
    """GUI Application for Kanji Collage Generator"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Kanji Collage Generator")
        self.root.geometry("800x900")
        self.root.resizable(True, True)

        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Queue for thread communication
        self.message_queue = queue.Queue()
        self.is_generating = False

        # Initialize components
        self.kanji_gen = KanjiGenerator()
        self.searcher = ImageSearcher()
        self.downloader = ImageDownloader()
        self.effects = VisualEffects()

        self.setup_ui()
        self.check_message_queue()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="🎨 Kanji Collage Generator",
            font=('Arial', 20, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        subtitle_label = ttk.Label(
            main_frame,
            text="Create surreal art from random Japanese kanji searches",
            font=('Arial', 10)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        current_row = 0

        # Number of queries
        ttk.Label(options_frame, text="Number of Queries:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.queries_var = tk.IntVar(value=5)
        queries_spinbox = ttk.Spinbox(
            options_frame,
            from_=1,
            to=20,
            textvariable=self.queries_var,
            width=10
        )
        queries_spinbox.grid(row=current_row, column=1, sticky=tk.W, padx=5)
        current_row += 1

        # Images per query
        ttk.Label(options_frame, text="Images per Query:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.images_per_query_var = tk.IntVar(value=10)
        ttk.Spinbox(
            options_frame,
            from_=5,
            to=50,
            textvariable=self.images_per_query_var,
            width=10
        ).grid(row=current_row, column=1, sticky=tk.W, padx=5)
        current_row += 1

        # Max images
        ttk.Label(options_frame, text="Max Images to Download:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.max_images_var = tk.IntVar(value=30)
        ttk.Spinbox(
            options_frame,
            from_=10,
            to=100,
            textvariable=self.max_images_var,
            width=10
        ).grid(row=current_row, column=1, sticky=tk.W, padx=5)
        current_row += 1

        # Kanji mode
        ttk.Label(options_frame, text="Kanji Mode:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.kanji_mode_var = tk.StringVar(value="mixed")
        kanji_mode_combo = ttk.Combobox(
            options_frame,
            textvariable=self.kanji_mode_var,
            values=["themed", "mixed", "random", "nonsense", "auto"],
            state="readonly",
            width=15
        )
        kanji_mode_combo.grid(row=current_row, column=1, sticky=tk.W, padx=5)
        current_row += 1

        # Collage type
        ttk.Label(options_frame, text="Collage Layout:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.collage_type_var = tk.StringVar(value="random")
        collage_type_combo = ttk.Combobox(
            options_frame,
            textvariable=self.collage_type_var,
            values=["grid", "random", "mosaic", "scattered"],
            state="readonly",
            width=15
        )
        collage_type_combo.grid(row=current_row, column=1, sticky=tk.W, padx=5)
        current_row += 1

        # Output size
        ttk.Label(options_frame, text="Output Size (px):").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.output_size_var = tk.IntVar(value=2400)
        size_combo = ttk.Combobox(
            options_frame,
            textvariable=self.output_size_var,
            values=[1200, 1800, 2400, 3000, 4000],
            state="readonly",
            width=15
        )
        size_combo.grid(row=current_row, column=1, sticky=tk.W, padx=5)
        current_row += 1

        # Effects intensity
        ttk.Label(options_frame, text="Visual Effects:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.effects_var = tk.IntVar(value=3)
        effects_scale = ttk.Scale(
            options_frame,
            from_=0,
            to=5,
            orient=tk.HORIZONTAL,
            variable=self.effects_var,
            length=150
        )
        effects_scale.grid(row=current_row, column=1, sticky=tk.W, padx=5)
        self.effects_label = ttk.Label(options_frame, text="Moderate (3)")
        self.effects_label.grid(row=current_row, column=2, sticky=tk.W, padx=5)
        effects_scale.config(command=self.update_effects_label)
        current_row += 1

        # Quick presets
        presets_frame = ttk.LabelFrame(main_frame, text="Quick Presets", padding="10")
        presets_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(
            presets_frame,
            text="⚡ Quick Test",
            command=self.preset_quick_test
        ).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(
            presets_frame,
            text="🎨 Chaos Mode",
            command=self.preset_chaos
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(
            presets_frame,
            text="🖼️ Clean Grid",
            command=self.preset_clean_grid
        ).grid(row=0, column=2, padx=5, pady=5)

        ttk.Button(
            presets_frame,
            text="🌈 Large Wallpaper",
            command=self.preset_wallpaper
        ).grid(row=0, column=3, padx=5, pady=5)

        # Generate button
        self.generate_button = ttk.Button(
            main_frame,
            text="🚀 Generate Collage",
            command=self.start_generation,
            style='Accent.TButton'
        )
        self.generate_button.grid(row=4, column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            variable=self.progress_var,
            length=400
        )
        self.progress_bar.grid(row=5, column=0, columnspan=2, pady=10)

        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready to generate!",
            font=('Arial', 10)
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)

        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Generation Log", padding="5")
        log_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        main_frame.rowconfigure(7, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            wrap=tk.WORD,
            font=('Consolas', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Bottom buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        ttk.Button(
            button_frame,
            text="📁 Open Downloads Folder",
            command=self.open_downloads
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="🗑️ Clear Cache",
            command=self.clear_cache
        ).grid(row=0, column=1, padx=5)

    def update_effects_label(self, value):
        """Update effects intensity label"""
        intensity = int(float(value))
        labels = {0: "None (0)", 1: "Light (1)", 2: "Light (2)",
                  3: "Moderate (3)", 4: "Heavy (4)", 5: "Extreme (5)"}
        self.effects_label.config(text=labels.get(intensity, f"({intensity})"))

    def preset_quick_test(self):
        """Quick test preset"""
        self.queries_var.set(3)
        self.max_images_var.set(10)
        self.output_size_var.set(1200)
        self.effects_var.set(2)
        self.log("Preset: Quick Test loaded")

    def preset_chaos(self):
        """Chaos mode preset"""
        self.queries_var.set(10)
        self.kanji_mode_var.set("nonsense")
        self.collage_type_var.set("scattered")
        self.effects_var.set(5)
        self.max_images_var.set(40)
        self.log("Preset: Chaos Mode loaded")

    def preset_clean_grid(self):
        """Clean grid preset"""
        self.collage_type_var.set("grid")
        self.effects_var.set(0)
        self.kanji_mode_var.set("themed")
        self.log("Preset: Clean Grid loaded")

    def preset_wallpaper(self):
        """Large wallpaper preset"""
        self.queries_var.set(10)
        self.max_images_var.set(80)
        self.output_size_var.set(3000)
        self.collage_type_var.set("mosaic")
        self.effects_var.set(3)
        self.log("Preset: Large Wallpaper loaded")

    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.update()

    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)

    def start_generation(self):
        """Start generation in background thread"""
        if self.is_generating:
            messagebox.showwarning("Already Running", "A collage is already being generated!")
            return

        self.is_generating = True
        self.generate_button.config(state='disabled')
        self.progress_bar.start()
        self.log_text.delete(1.0, tk.END)
        self.log("Starting generation...")

        # Start generation thread
        thread = threading.Thread(target=self.generate_collage_thread)
        thread.daemon = True
        thread.start()

    def generate_collage_thread(self):
        """Generate collage in background thread"""
        try:
            # Get parameters
            num_queries = self.queries_var.get()
            images_per_query = self.images_per_query_var.get()
            max_images = self.max_images_var.get()
            kanji_mode = self.kanji_mode_var.get()
            collage_type = self.collage_type_var.get()
            output_size = self.output_size_var.get()
            effects_intensity = self.effects_var.get()

            # Step 1: Generate queries
            self.message_queue.put(('status', 'Generating kanji queries...'))
            queries = []
            for i in range(num_queries):
                query = self.kanji_gen.generate_query(mode=kanji_mode)
                queries.append(query)
                self.message_queue.put(('log', f"Query {i+1}: {query}"))

            # Step 2: Search
            self.message_queue.put(('status', 'Searching for images...'))
            all_results = []
            for i, query in enumerate(queries):
                self.message_queue.put(('log', f"Searching: {query}"))
                results = self.searcher.search_duckduckgo(query, max_results=images_per_query)
                all_results.extend(results)
                self.message_queue.put(('log', f"  Found {len(results)} images"))

            if not all_results:
                self.message_queue.put(('error', 'No images found!'))
                return

            self.message_queue.put(('log', f"Total images found: {len(all_results)}"))

            # Step 3: Download
            self.message_queue.put(('status', 'Downloading images...'))
            images = []
            for idx, result in enumerate(all_results[:max_images]):
                img = self.downloader.download_image(result['url'])
                if img:
                    images.append(img)
                    self.message_queue.put(('log', f"Downloaded {len(images)}/{max_images}"))

            if not images:
                self.message_queue.put(('error', 'Failed to download images!'))
                return

            self.message_queue.put(('log', f"Successfully downloaded {len(images)} images"))

            # Step 4: Create collage
            self.message_queue.put(('status', f'Creating {collage_type} collage...'))
            builder = CollageBuilder(output_size=(output_size, output_size))

            if collage_type == 'grid':
                collage = builder.create_grid_collage(images)
            elif collage_type == 'random':
                collage = builder.create_random_collage(images)
            elif collage_type == 'mosaic':
                collage = builder.create_mosaic_collage(images)
            else:  # scattered
                collage = builder.create_scattered_collage(images)

            self.message_queue.put(('log', 'Collage created!'))

            # Step 5: Effects
            if effects_intensity > 0:
                self.message_queue.put(('status', 'Applying visual effects...'))
                collage = self.effects.apply_random_effects(collage, num_effects=effects_intensity)
                self.message_queue.put(('log', f'Applied {effects_intensity} effects'))

            # Step 6: Save
            self.message_queue.put(('status', 'Saving collage...'))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kanji_collage_{timestamp}.jpg"
            filepath = self.downloader.save_image(collage, filename, quality=95)

            self.message_queue.put(('success', filepath))

        except Exception as e:
            self.message_queue.put(('error', str(e)))

    def check_message_queue(self):
        """Check for messages from generation thread"""
        try:
            while True:
                msg_type, msg_data = self.message_queue.get_nowait()

                if msg_type == 'log':
                    self.log(msg_data)
                elif msg_type == 'status':
                    self.update_status(msg_data)
                elif msg_type == 'success':
                    self.progress_bar.stop()
                    self.is_generating = False
                    self.generate_button.config(state='normal')
                    self.update_status("✅ Generation complete!")
                    self.log(f"SUCCESS! Saved to: {msg_data}")
                    messagebox.showinfo(
                        "Success!",
                        f"Collage generated successfully!\n\nSaved to:\n{msg_data}"
                    )
                elif msg_type == 'error':
                    self.progress_bar.stop()
                    self.is_generating = False
                    self.generate_button.config(state='normal')
                    self.update_status("❌ Generation failed!")
                    self.log(f"ERROR: {msg_data}")
                    messagebox.showerror("Error", f"Generation failed:\n{msg_data}")

        except queue.Empty:
            pass

        # Schedule next check
        self.root.after(100, self.check_message_queue)

    def open_downloads(self):
        """Open downloads folder"""
        import subprocess
        import platform

        downloads_dir = os.path.abspath('downloads')
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)

        system = platform.system()
        try:
            if system == 'Windows':
                os.startfile(downloads_dir)
            elif system == 'Darwin':  # macOS
                subprocess.Popen(['open', downloads_dir])
            else:  # Linux
                subprocess.Popen(['xdg-open', downloads_dir])
            self.log("Opened downloads folder")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")

    def clear_cache(self):
        """Clear image cache"""
        result = messagebox.askyesno(
            "Clear Cache",
            "This will delete all cached images.\nAre you sure?"
        )
        if result:
            try:
                import shutil
                cache_dir = 'cache'
                if os.path.exists(cache_dir):
                    shutil.rmtree(cache_dir)
                    os.makedirs(cache_dir)
                self.log("Cache cleared!")
                messagebox.showinfo("Success", "Cache cleared successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not clear cache: {e}")


def main():
    """Run the GUI application"""
    root = tk.Tk()
    app = KanjiCollageGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
