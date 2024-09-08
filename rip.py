# %%
import click
import pynput
import time

import numpy as np

from pathlib import Path
from PIL import ImageGrab
from tqdm import tqdm


@click.command()
@click.option("--start", default=1, show_default=True)
@click.option("--stop")
@click.option("--wait", default=5, show_default=True)
def main(start, stop, wait):
    """
    Function to rip pages from eTextbook readers by iteratively clicking
    the page input box, inputting page numbers (in ascending order), and
    taking a screenshot after a 5 second startup_delay.

    Screenshots are labeled `page_XXX` and can be cropped and merged using `join.py`.
    """

    print("Initializing...")
    # preliminaries:
    startup_delay = 10
    page_nums = np.arange(int(start), int(stop) + 1, 1)

    # make a folder for screenshots:
    output_folder = Path("./screenshots")
    output_folder.mkdir(parents=True, exist_ok=True)

    # initiate new controls
    mouse = pynput.mouse.Controller()
    keyboard = pynput.keyboard.Controller()

    # identify input box position:
    print("Place mouse over input box.")
    print(f"Process starting in {startup_delay} seconds.")

    for i in tqdm(range(startup_delay)):
        time.sleep(1)
        # grab the mouse position at end of countdown:
        if i == (startup_delay - 1):
            box_position = mouse.position

    # click into the target window:
    mouse.click(pynput.mouse.Button.left)

    # double-click into the input box:
    mouse.click(pynput.mouse.Button.left, 2)

    print("Copying...")
    for page_num in tqdm(page_nums):

        # ensure the mouse hasn't moved from the box:
        if mouse.position != box_position:
            mouse.position = box_position

        # double-click into the box:
        mouse.click(pynput.mouse.Button.left, 2)

        # type the page number and enter:
        keyboard.type(str(page_num))
        keyboard.press(pynput.keyboard.Key.enter)

        # wait 5 seconds for the page to load:
        time.sleep(wait)

        # take a screenshot and save it:
        screenshot = ImageGrab.grab()
        screenshot.save(f"screenshots/page_{page_num}.png")

    print("Done!")


if __name__ == "__main__":
    main()
# %%
