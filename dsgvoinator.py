import os
import requests
import json

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
    s = requests.get(url).content
    with open(path + '/' + filename + '.' + filetype, 'wb') as file: 
        file.write(s)
    return filename

print("Please enter the file path to your angular project:")
path = input()

#Using angular.json to find style language (css/scss/sass/less)
print("Determining used styling language...")
angular = open(path + "angular.json")
angular = json.load(angular)
for key in angular['projects']:
    inlineStyleLanguage = angular['projects'][key]['architect']['build']['options']['inlineStyleLanguage']
print(f'Detected {inlineStyleLanguage}.')

#Open files
index = open(path + "src/index.html")
styles = open(path + "src/styles." + inlineStyleLanguage)

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

#search for links in styles
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
    filenames.append(download_stylesheet(link, path + 'font-stylesheets', inlineStyleLanguage))

#Finding font urls in the downloaded stylesheets
font_links = []
search_link_fonts = "https://fonts.gstatic.com"
print("Searching for font file links...")
for name in filenames:
    file = open(path + 'font-stylesheets/' + name + '.' + inlineStyleLanguage)
    lines = file.readlines()
    for row in lines:
        start = row.find(search_link_fonts)
        row = row[start:]
        end = row.find(')')
        if start != -1:
            font_links.append(row[:end])

print(f'Found {len(font_links)} font files.')

#Check if path exists and generate it if it doesnt
if not os.path.exists(path + 'fonts'):
    os.mkdir(path + 'fonts')

#Downloading fonts
print("Downloading fonts...")
for link in font_links:
    download_font(link, path + 'fonts')
#Removing google font links from index.html
new_index_html_array = []
for row in index_lines:
    if row.find(search_link_stylesheets) == -1 and row.find(search_link_fonts) == -1:
        new_index_html_array.append(row)

#Removing google links from stylesheet
new_styles = []
#Determining if angular material is used
angular_material = False
for row in styles_lines:
    if row.find('~@use "angular/material'):
        angular_material = True
if angular_material:
    for row in styles_lines:
        #Only write lines without google links
        if row.find(search_link_stylesheets) == -1 and row.find(search_link_fonts) == -1:
            new_styles.append(row)
            #Write new font imports after the angular material import
            if row.find('@use "~@angular/material" as mat;') != -1:
                for link in stylesheet_links:
                    link_start = link.rindex('family=') + 7
                    link_end = len(link)
                    link_end = link.find('&')
                    link = link[link_start:link_end]
                    new_styles.append(f'@import url("../font-stylesheets/{link}.{inlineStyleLanguage}");\n')
else:
    #Add new links
    for link in stylesheet_links:
        link_start = link.rindex('family=') + 7
        link_end = len(link)
        link_end = link.find('&')
        link = link[link_start:link_end]
        new_styles.append(f'@import url("../font-stylesheets/{link}.{inlineStyleLanguage}");\n')
    #Writing old file contents without google links
    for row in styles_lines:
        if row.find(search_link_stylesheets) == -1 and row.find(search_link_fonts) == -1:
            new_styles.append(row)
                

#Rewriting generated stylesheets for the fonts
for link in stylesheet_links:
    link_start = link.rindex('family=') + 7
    link_end = len(link)
    link_end = link.find('&')
    link = link[link_start:link_end]
    
    style_file = open(path + 'font-stylesheets/' + link + '.' + inlineStyleLanguage)
    new_style_file_array = []

    for row in style_file:
        if row.find(search_link_fonts) == -1:
            new_style_file_array.append(row)
        else:
            for font_link in font_links:
                if not row.find(font_link) == -1:
                    link_start = font_link.rindex('/') + 1
                    font_link = font_link[link_start:]
                    new_style_file_array.append(f'  src: url("../fonts/{font_link}")')
    print(f"Rewriting stylesheet {link}...")
    with open(path + 'font-stylesheets/' + link + '.' + inlineStyleLanguage, 'w') as style_file:
        for row in new_style_file_array:
            style_file.write(row)

    style_file.close()

#Writing index.html
print("Rewriting index.html...")
with open(path + 'src/index.html', 'w') as new_index_html:
    for row in new_index_html_array:
        new_index_html.write(row)

new_index_html.close()

#Writing stylesheet
print("Rewriting main style sheet...")
with open(path + 'src/styles.' + inlineStyleLanguage, 'w') as new_styles_file:
    for row in new_styles:
        new_styles_file.write(row)

new_styles_file.close()

print("DSGVOinator done.")
