from django.shortcuts import render

from . import util
import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html = convert_md_to_html(title)
    if html != None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html": html
        })
    else:
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
        # Returns con
        return mark_down.convert(content)
    else:
        return None

def search(request):
    search = request.POST['q']
    html = convert_md_to_html(search)
    if html != None:
        return render(request, "encyclopedia/entry.html", {
            "title": search,
            "html": html
        })
    else:
        if search != None:
            entry_list =  util.list_entries()
            results = []
            for i in entry_list:
                if search in entry_list[i]:
                    results.append(entry_list[i])
                    return render(request, "encyclopedia/results.html", {
                        "results": results
                    })
        
        else:
            return render(request, "encyclopedia/error.html", {
                "no_entry": "No such entry."
            })