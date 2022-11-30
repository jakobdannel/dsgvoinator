# dsgvoinator
A tool that downloads google fonts to an Angular Project and replaces all links in scss files with local links to comply with the DSGVO

## How to use this tool

- Install python
- Copy the file 'dsgvoinator.py' into the source folder of your angular project (not /src!)
- Run `python3 dsgvoinator.py`

This is tool is still experimental and currently only works for .scss files and fonts linked either in `index.html` or `styles.scss`.
