# pypdfripper

Command line tool to rip documents from PDF viewers. 

## Installation
1. Clone this repository. 
2. Navigate to the repository folder and run: 

```
conda env create -f environment.yml
```
3. Activate the conda environment: 
```
conda activate pypdfripper
``` 

## Workflow

Workflow is intentionally divided into two steps so that code can be modified flexibly.

### 1. Ripping: `rip.py`
This function is designed to work with any PDF viewer that has a text input box that controls which page is rendered. 
It iteratively clicks the page input box, inputting page numbers (in ascending order), and takes a screenshot after a delay. 
The delay should be adjusted to allow the page to render before screenshotting.

1. Adjust the window size to maximize the page size of the target document. Make sure that the entire page is in view and as large as possible. 
2. Note the page numbers to copy (`start` and `stop`).
3. Run `rip.py` from the command line. For help: `python rip.py --help`

Examples:

```
# rip first 10 pages
python rip.py --stop 10
```
```
# or with a custom delay of 2 seconds 
python rip.py --stop 10 --wait 2
```
```
# or rip 10th-20th pages:
python rip.py --start 10 --stop 20 
```



4. Follow the command line prompts. Avoid using the mouse after setting the input box location while the program is running. 

5. Screenshots will be saved to `./screenshots/` and labeled `page_XXX.png`. Note that the screenshots will be of your entire screen, and will need to be cropped and merged (next step).



### 2. Joining: `join.py`
This function crops and merges the screenshots captured by `rip.py` into an output PDF. The outputted file is by default in black and white,

1. Run `join.py` from the command line. For help: `python join.py --help`

Examples: 
```
# saves PDF with default filename MERGED.pdf
python join.py screenshots/
```
```
# or specify the output filename: 
python join.py screenshots --output_filename 'your_filename.pdf'

# short-hand: 
python join.py screenshots -o 'your_filename.pdf'
```
```
# request color output:
python join.py screenshots --color True
```


2. After the files have been loaded, you will be asked to identify the rectangular area over which to crop all images. Press `Q` when finished. 

3. Screenshots generated from `rip.py` will be cropped, merged and saved into an output PDF in the current folder. 

