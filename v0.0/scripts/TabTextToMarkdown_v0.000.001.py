import sys
import os
import re

def write_h1(text_line, link_name=None):
    markdown_line = f"<h1>{text_line}</h1>"
    if link_name:
        markdown_line += f"<a name={link_name}></a>\n"
    else:
        markdown_line += "\n"
    return markdown_line

def write_img(text_url, alt_text=None, width=None):
    markdown_line = f"<img src=\"{text_url}\" align=\"right\""
    if alt_text:
        markdown_line += f" alt=\"{alt_text}\""
    if width:
        markdown_line += f" width=\"{width}\""
    markdown_line += f"></img>\n"
    return markdown_line

def write_h3(text_line, link_name=None):
    markdown_line = f"<h3>{text_line}</h3>"
    if link_name:
        markdown_line += f"<a name={link_name}></a>\n"
    else:
        markdown_line += "\n"
    return markdown_line

class Details:
    def __init__(self, titel, info, hidden_lines=None):
        self.titel = titel
        self.info = info
        self.hidden_lines = hidden_lines if hidden_lines is not None else []
        self.markdown_text = ""
        self.done = False

    def write_markdown_text(self):
        markdown_text = f"<details>\n"
        markdown_text += f"  <summary><b>{self.titel}</b>:{self.info}</summary>\n\n"
        for hidden_line in self.hidden_lines:
            markdown_text += f"  > {hidden_line}  \n"
        markdown_text += f"</details>\n"
        self.done = True
        return markdown_text

def write_details(details):
    if details is not None:
        markdown += details.write_markdown_text()
        details = None


def text_to_markdown(text_file):
    markdown = ""
    #lines = text.split('\n')
    with open(text_file, 'r') as file:
        details = None
        for line in file:
            print_line = line.lstrip('\t').rstrip('\n')
            if len(print_line) == 0:
                if details is not None:
                    markdown += details.write_markdown_text()
                    details = None
                markdown += "<h2> </h2>\n"
            else:
                tabs_match = re.match(r'^(\t+)', line)
                tabs_count = 0
                if tabs_match:
                    tabs_span = tabs_match.span()
                    tabs_count = tabs_span[1]
                
                if tabs_count == 0:
                    if details is not None:
                        markdown += details.write_markdown_text()
                        details = None
                    markdown += write_h1(print_line)
                elif tabs_count == 1:
                    if details is not None:
                        markdown += details.write_markdown_text()
                        details = None
                    
                    if print_line[0] == '.':
                        split_line = print_line.lstrip('.').split(' ')
                        img_url   = split_line[0]
                        img_width = split_line[1] if len(split_line) > 1 else None
                        markdown += write_img(img_url, width=img_width)
                    else:
                        markdown += write_h3(print_line)
                elif tabs_count == 2:
                    if details is not None:
                        markdown += details.write_markdown_text()
                        details = None
                    
                    split_line = print_line.split(':')
                    titel   = split_line[0]
                    info    = split_line[1] if len(split_line) > 1 else ""
                    details = Details(titel, info)
                elif tabs_count == 3 and details is not None:
                    details.hidden_lines.append(print_line)

        if details is not None:
            if not details.done:
                markdown += details.write_markdown_text()
            details = None

    return markdown


# Get the directory of the Python executable
python_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to file.txt relative to the Python executable
file_path = os.path.join(python_dir, 'MTL_UI.txt')
print(file_path)

markdown_content = text_to_markdown(file_path)
with open('README.md', 'w') as f:
    f.write(markdown_content)


#<br clear="left"/>