# dsgvoinator
A tool that downloads google fonts to an Angular Project and replaces all links in css/scss/sass/less files with local links to comply with the DSGVO

## How to use this tool

- Install python
- Clone this repository with `git clone git@github.com:jakobdannel/dsgvoinator.git`
- Run `python3 dsgvoinator.py`
- Enter the filepath to your angular project root folder when prompted

This is tool is still experimental and currently only works for fonts linked either in `index.html` or `styles.css/scss/sass/less`.
