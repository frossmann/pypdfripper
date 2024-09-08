# %%
import click

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import RectangleSelector
from pathlib import Path
from PIL import Image
from tqdm import tqdm


def on_select(eclick, erelease):
    """Event handler for RectangleSelector"""
    pass


def draw_rect(on_select, im):
    """Shows an image in pop-up window and prompts used to draw the
    rectangular area used for cropping."""

    fig, ax = plt.subplots()
    ax.imshow(im)
    ax.set_title(f"Select Cropping Region\nPress Q to continue.")
    RS = RectangleSelector(ax, on_select, interactive=True)
    plt.show()

    extent = [int(pt) for pt in RS.extents]

    print(f"{extent} selected.")

    return extent


def crop_image(im, extent):
    """Given a matplotlib.widgets.RectangleSelector extent, crops a
    PIL Image."""
    crop = im.crop((extent[0], extent[2], extent[1], extent[3]))
    return crop


def queue_files(source_folder):
    """Returns  a queue of filenames to load, sorted by page number.
    (Expects the file stem to be named as  'file_XX`)."""

    source_folder = Path(source_folder)

    filenames = [f for f in source_folder.glob("*.png")]

    page_nums = [int(f.stem.split("page_")[-1]) for f in filenames]
    sort_idx = np.argsort(page_nums)

    sorted_filenames = np.array(filenames)[sort_idx]
    return sorted_filenames


def load_images(sorted_filenames):
    """Load images from filenames into a list of PIL Images"""
    images = []
    for filename in tqdm(sorted_filenames):
        images.append(Image.open(filename))

    return images


@click.command()
@click.argument("source_folder")
@click.option("--output_name", "-o", default="MERGED.pdf", show_default=True)
@click.option("--color", "-c", default=False, show_default=True)
def main(source_folder, output_name, color):
    """
    Crops and joins images from the input source folder into a single PDF document.

    Options:
    - output_name: Filename of merged PDF
    - color: Flag, save in color (True) or Black and White (False - default)
    """

    print("Loading images...")
    sorted_filenames = queue_files(source_folder)
    images = load_images(sorted_filenames)

    print("Waiting for cropping coordinates...")
    extent = draw_rect(on_select, images[0])
    plt.close()

    print("Cropping...")
    cropped_images = []
    for image in tqdm(images):
        if color:
            cropped_images.append(crop_image(image, extent))
        else:
            # * convert("L") to B/W
            cropped_images.append(crop_image(image.convert("L"), extent))

    print("Collating and saving...")
    cropped_images[0].save(
        output_name,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=cropped_images[1:],
    )


if __name__ == "__main__":
    main()

# %%
