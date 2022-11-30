import os
import requests

def download_stylesheet(url, path, filetype):
    #Finding font name in link
    filename_start = url.find('family=') + 7
    filename_end = len(url)
    filename_end = url.find('&')

    filename = url[filename_start:filename_end]

    if not os.path.exists(path):
        os.mkdir(path)
    s = requests.get(url).text
    with open(path + '/' + filename + '.' + filetype, 'w') as file: 
        file.write(s)
    return filename

def download_font(url, path):
    #Finding font name in link
    filename_start = url.rindex('/') + 1
    filename_end = url.rindex('.')
    filetype_start = url.rindex('.') + 1
    filetype_end = len(url)
    filetype = url[filetype_start:filetype_end]
    filename = url[filename_start:filename_end]

    if not os.path.exists(path):
        os.mkdir(path)
    s = requests.get(url).text
    with open(path + '/' + filename + '.' + filetype, 'w') as file: 
        file.write(s)
    return filename

#Open files
index = open("src/index.html")
styles = open("src/styles.scss")

#Reading lines
index_lines = index.readlines()
styles_lines = styles.readlines()

#Search for google font links
search_link_stylesheets = 'https://fonts.googleapis.com/'
stylesheet_links = []

#Search for links in index html
print("Searching for google fonts...")
for row in index_lines:
    start = row.find(search_link_stylesheets)
    row = row[start:]
    end = row.find('"')
    if start != -1:
        stylesheet_links.append(row[:end])

#search for links in styles.scss
for row in styles_lines:
    start = row.find(search_link_stylesheets)
    row = row[start:]
    end = row.find('"')
    if start != -1:
        stylesheet_links.append(row[:end])
print(f'Found {len(stylesheet_links)} font links.')
filenames = []

#Downloadind the stylesheets
print("Downloading stylesheets...")
for link in stylesheet_links:
    filenames.append(download_stylesheet(link, 'font-stylesheets', 'scss'))

#Finding font urls in the downloaded stylesheets
font_links = []
search_link_fonts = "https://fonts.gstatic.com"
print("Searching for font file links...")
for name in filenames:
    file = open('font-stylesheets/' + name + '.scss')
    lines = file.readlines()
    for row in lines:
        start = row.find(search_link_fonts)
        row = row[start:]
        end = row.find(')')
        if start != -1:
            font_links.append(row[:end])

print(f'Found {len(font_links)} font files.')

#Check if path exists and generate it if it doesnt
if not os.path.exists('fonts'):
    os.mkdir('fonts')

#Downloading fonts
print("Downloading fonts...")
for link in font_links:
    download_font(link, 'fonts')
#Rewriting index.html
new_index_html_array = []
for row in index_lines:
    if row.find(search_link_stylesheets) == -1 and row.find(search_link_fonts) == -1:
        new_index_html_array.append(row)

new_styles_scss = []
for row in styles_lines:
    if row.find(search_link_stylesheets) == -1 and row.find(search_link_fonts) == -1:
        new_styles_scss.append(row)
        if row.find('@use "~@angular/material" as mat;') != -1:
            for link in stylesheet_links:
                link_start = link.rindex('family=') + 7
                link_end = len(link)
                link_end = link.find('&')
                link = link[link_start:link_end]
                new_styles_scss.append(f'@import url("font-stylesheets/{link}.scss");\n')

for link in stylesheet_links:
    link_start = link.rindex('family=') + 7
    link_end = len(link)
    link_end = link.find('&')
    link = link[link_start:link_end]
    
    scss_file = open('font-stylesheets/' + link + '.scss')
    new_scss_file_array = []

    for row in scss_file:
        if row.find(search_link_fonts) == -1:
            new_scss_file_array.append(row)
        else:
            for font_link in font_links:
                if not row.find(font_link) == -1:
                    link_start = font_link.rindex('/') + 1
                    font_link = font_link[link_start:]
                    new_scss_file_array.append(f'  src: url("../fonts/{font_link}")')
    print(f"Rewriting stylesheet {link}...")
    with open('font-stylesheets/' + link + '.scss', 'w') as scss_file:
        for row in new_scss_file_array:
            scss_file.write(row)

    scss_file.close()

print("Rewriting index.html...")
with open('src/index.html', 'w') as new_index_html:
    for row in new_index_html_array:
        new_index_html.write(row)

new_index_html.close()

print("Rewriting main style sheet...")
with open('src/styles.scss', 'w') as new_styles_scss_file:
    for row in new_styles_scss:
        new_styles_scss_file.write(row)

new_styles_scss_file.close()

print("DSGVOinator done.")
