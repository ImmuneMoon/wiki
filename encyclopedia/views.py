from django.shortcuts import render

from . import util
import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Generates html for each entry page from markdown files
def entry(request, title):
    # Gets code from .md file that matches the title
    html = convert_md_to_html(title)
    if html != None:
        # If html is not empty the page is rendered
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html": html
        })
    else:
        # Otherwise an error page is thrown
        return render(request, "encyclopedia/error.html", {
            "no_entry": "No such entry."
        })

# Test code for converting markdown to html without the markdown library
'''
import re
# Converts markdown text to HTML
def convert_md_to_html(title):
    # Handles headers
    title = re.sub(r'(?m)^#{1,6}\s+(.+)$', r'<h\1>\g<2></h\1>', title)
    
    # Handles emphasis
    title = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', title)
    title = re.sub(r'\*(.*?)\*', r'<em>\1</em>', title)
    
    # Handles links
    title = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', title)
    
    # Handles paragraphs and line breaks
    title = re.sub(r'\n\n', r'</p><p>', title)
    title = re.sub(r'\n', r'<br>', title)
    title = '<p>' + title + '</p>'
    
    return title
'''

# Converts markdown text to HTML
def convert_md_to_html(title):
    # Gets the tite
    content = util.get_entry(title)
    # Sets up markdown method
    mark_down = markdown.Markdown()
    if content != None:
        # Returns html converted from  markdown file
        return mark_down.convert(content)
    else:
        # If no match, returns none
        return None

# Function for search queries
def search(request):
    # Grabs 'q' value from the search box
    query = request.POST['q']
    # Converts any matching .md files to html
    html = convert_md_to_html(query)
    if html != None:
        # If html has a value, that page is rendered
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "html": html
        })
    # If html is empty but the query isn't
    elif query != None:
        # Creates list of all entries
        entry_list = util.list_entries()
        # Compares query value against list to see if it matches any characters in entry_list items and assigns any that match to results
        results = [item for item in entry_list if query.lower() in item.lower()]

        if results != []:
            # Passes results to be rendered if results isnt empty
            return render(request, "encyclopedia/search.html", {
                "results": results
            })
        else:
            # If the results list is empty, error is thrown
            return render(request, "encyclopedia/error.html", {
                "no_entry": "No such entry."
            })
    else:
        # If both html and query is empty, error is thrown
        return render(request, "encyclopedia/error.html", {
            "no_entry": "No such entry."
        })