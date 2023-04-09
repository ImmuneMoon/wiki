from django.shortcuts import render

from . import util
import markdown
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Prototype code for converting markdown to html without the markdown library
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
def md_to_html(title):
    # Gets the entry
    content = util.get_entry(title)
    # Sets up markdown method
    mark_down = markdown.Markdown()
    if content != None:
        # Returns html converted from  markdown file
        return mark_down.convert(content)
    else:
        # If no match, returns none
        return None

# Generates html for each entry page from markdown files
def entry(request, title):
    # Gets code from .md file that matches the title
    html = md_to_html(title)
    if html != None:
        # If html is not empty the page is rendered
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html": html
        })
    else:
        # Otherwise an error page is thrown
        return render(request, "encyclopedia/error.html", {
            "error": "No such page."
        })

# Function for search queries
def search(request):
    # Grabs 'q' value from the search box
    query = request.POST['q']
    # Converts any matching .md files to html
    html = md_to_html(query)
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
        # Compares query value against list to see if it matches any characters in 
        # entry_list items and assigns any that match to results
        results = [item for item in entry_list if query.lower() in item.lower()]

        if results != []:
            # Passes results to be rendered if results isnt empty
            return render(request, "encyclopedia/search.html", {
                "results": results
            })
        else:
            # If the results list is empty, error is thrown
            return render(request, "encyclopedia/error.html", {
                "error": "No matching pages."
            })
    else:
        # If both html and query is empty, error is thrown
        return render(request, "encyclopedia/error.html", {
            "error": "No such page."
        })
    
def create(request):
    # Returns the create page on GET request
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    
    else:
        # Otherwise get title
        title = request.POST['title']
        new_md = request.POST['markdown']
        # Error catchers for empty title or mardown from input
        if title == '' and new_md =='' or title == None and new_md == None:
            return render(request, "encyclopedia/error.html", {
                "error": "No information entered."
            })
        elif title == '' or title == None:
            return render(request, "encyclopedia/error.html", {
                "error": "Please enter a title for your page."
            })
        elif new_md == '' or new_md == None:
            return render(request, "encyclopedia/error.html", {
                "error": "Please enter some info for your page."
            })
        elif util.get_entry(title) != None:
            return render(request, "encyclopedia/error.html", {
                "error": "Page already exists."
            })
        else:
            # Constructs markdown
            mark_down = "# " + title + "\n\n" + new_md
            # Saves to file
            util.save_entry(title, mark_down)
            # Constructs html from file for redirect
            html = md_to_html(title)
            # Redirect render
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "html": html
            })

def edit(request):
    # Gets the page title
    title = request.POST['page_name']
    # Gets the matching markdown file
    mark_down = util.get_entry(title)
    # Find sthe index of the markdown content
    start_index = mark_down.index('#') + 1
    end_index = mark_down.index('\n', start_index)
    # Extracts the markdown content
    content = mark_down[end_index+1:].strip()
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "markdown": content
    })


def save(request):
    # Gets the page title
    title = request.POST['page_name']
    # Constructs the markup file contents
    change = request.POST['markdown']
    # Checks for empty field and returns error if one is found
    if change == '' or change == None:
        return render(request, "encyclopedia/error.html", {
            "error": "Please enter some info."
        })

    else:
        # Otherwise, markdown is constructed
        mark_down = "# " + title + "\n\n" + mark_down
        # Saves to file
        util.save_entry(title, mark_down)
        # Constructs html from file for redirect
        html = md_to_html(title)
        # Redirect render
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html": html
        })


def random_page(request):
    # Gets list of entries 
    entry_list = util.list_entries()
    # Generates a random number between 0 and the last entry index position
    index = random.randint(0, len(entry_list) - 1)
    # Gets the matching page
    page = entry_list[index]
    # Converts to html
    html = md_to_html(page)
    # Render page
    return render(request, "encyclopedia/entry.html", {
        "title": page,
        "html": html
    })