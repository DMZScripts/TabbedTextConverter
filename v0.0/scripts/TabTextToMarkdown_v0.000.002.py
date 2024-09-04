import os
import re


def write_h1(text_line, link_name=None, align=None):
    h1_align = "" if align is None else " align=\"" + align + "\""
    h1_start = f"<h1{h1_align}>"
    markdown_line = f"<br>\n{h1_start}{text_line}</h1>"
    if link_name:
        markdown_line += f"<a name=\"{link_name}\"></a>\n"
    else:
        markdown_line += "\n"
    return markdown_line


def write_img(text_url, alt_text=None, width=None):
    markdown_line = f"<img src=\"{text_url}\""
    if alt_text:
        markdown_line += f" alt=\"{alt_text}\""
    if width:
        if width == "full-width":
            markdown_line += f" class=\"full-width\""
        else:
            markdown_line += f" align=\"right\" width=\"{width}\""
    else:
        markdown_line += f" align=\"right\""
    markdown_line += f"></img>\n"
    return markdown_line


def write_h3(text_line, link_name=None):
    markdown_line = f"<h3>{text_line}</h3>"
    if link_name:
        markdown_line += f"<a name=\"{link_name}\"></a>\n"
    else:
        markdown_line += "\n"
    return markdown_line


def write_list(text_line, link_name=None):
    markdown_line = f"{text_line}"
    return markdown_line


class Details:
    def __init__(self, titel, info, hidden_lines=None, hide_lines=False):
        self.titel = titel
        self.info = info
        self.hidden_lines = hidden_lines if hidden_lines is not None else []
        self.hide_lines = hide_lines
        self.markdown_text = ""
        self.done = False

    def write_markdown_text(self, open=True):
        open_text   = "" if self.hide_lines else " open"
        titel_text  = "" if self.titel == "" else f"<b>{self.titel}</b>:"
        markdown_text = f"<details{open_text}>\n"
        markdown_text += f"  <summary>{titel_text}{self.info}</summary>\n\n"
        for hidden_line in self.hidden_lines:
            markdown_text += f"  > {hidden_line}  \n"
        markdown_text += f"</details>\n"
        self.done = True
        return markdown_text


class TableOfContent:
    def __init__(self):
        self.pos = -1
        self.h1_items = []
        self.h1_links = []
        self.h1_h2_items = []
        self.h1_h2_links = []


    def add_h1(self, h1_text, h1_link):
        self.h1_items.append(h1_text)
        self.h1_links.append(h1_link)
        self.h1_h2_items.append([])
        self.h1_h2_links.append([])
        h1_index = len(self.h1_items) - 1
        return h1_index


    def add_h2(self, h1_index, h2_text, h2_link):
        self.h1_h2_items[h1_index].append(h2_text)
        self.h1_h2_links[h1_index].append(h2_link)
        h2_index = len(self.h1_h2_items[h1_index]) - 1
        return h2_index


    def write_items(self):
        toc_text = write_h1("Table of contents", align="center")
        markdown_text = f"{toc_text}\n"
        markdown_text = write_h3("Table of contents") + "\n"
        zipped_items = zip(self.h1_items, self.h1_links, self.h1_h2_items, self.h1_h2_links)
        for h1_item, h1_link, h2_items, h2_links in zipped_items:
            markdown_text += f"- [{h1_item}](#{h1_link})\n"
            for h2_item, h2_link in zip(h2_items, h2_links):
                markdown_text += f"\t- [{h2_item}](#{h2_link})\n"
        markdown_text += "\n"
        return markdown_text



def text_to_markdown(text_file):
    markdown = ""
    #lines = text.split('\n')
    with open(text_file, 'r') as file:
        details = None
        in_list = False
        in_numbered = False
        TOC = TableOfContent()
        TOC_index = -1

        for line in file:
            print_line = line.lstrip('\t').rstrip('\n')
            if len(print_line) == 0:
                if details is not None:
                    markdown += details.write_markdown_text()
                    details = None
                if in_list:
                    markdown += "\n"
                    in_list = False
                if in_numbered:
                    markdown += "\n"
                    in_numbered = False
                markdown += "<h2> </h2>\n"
            else:
                if line == "TOC\n":
                    print(line)
                    TOC.pos = len(markdown)
                else:
                    tabs_match = re.match(r'^(\t+)', line)
                    tabs_count = 0
                    if tabs_match:
                        tabs_span = tabs_match.span()
                        tabs_count = tabs_span[1]

                    if tabs_count == 0:
                        in_list = False
                        if details is not None:
                            markdown += details.write_markdown_text()
                            details = None
                        if print_line.startswith('.'):
                            split_line = print_line.lstrip('.').split(' ')
                            img_url   = split_line[0]
                            markdown += write_img(img_url, width="full-width")
                        else:
                            split_lines = print_line.split(' #')
                            text_line = split_lines[0]
                            link_name = split_lines[1] if len(split_lines) > 1 else None
                            align = split_lines[2] if len(split_lines) > 2 else None
                            markdown += write_h1(text_line, link_name=link_name, align=align)
                            if link_name:
                                TOC_index = TOC.add_h1(text_line, link_name)
                    elif tabs_count == 1:
                        in_list = False
                        if details is not None:
                            markdown += details.write_markdown_text()
                            details = None
                        if print_line[0] == '.':
                            split_line = print_line.lstrip('.').split(' ')
                            img_url   = split_line[0]
                            img_width = split_line[1] if len(split_line) > 1 else None
                            markdown += write_img(img_url, width=img_width)
                        else:
                            split_lines = print_line.split(' #')
                            text_line = split_lines[0]
                            link_name = split_lines[1] if len(split_lines) > 1 else None
                            markdown += write_h3(text_line, link_name=link_name)
                            if TOC_index > -1:
                                TOC.add_h2(TOC_index, text_line, link_name)
                    elif tabs_count == 2:
                        if details is not None:
                            markdown += details.write_markdown_text()
                            details = None
                        if ':' in print_line:
                            split_line = print_line.split(':')
                            titel   = split_line[0]
                            info    = split_line[1] if len(split_line) > 1 else ""
                            hide    = titel == ""
                            details = Details(titel, info, hide_lines=hide)
                        elif print_line.startswith('-'):
                            if not in_list:
                                markdown += "\n"
                            in_list = True
                            markdown += print_line + "\n"
                        elif print_line[0].isdigit():
                            if not in_numbered:
                                markdown += "\n"
                            in_numbered = True
                            markdown += print_line + "\n"
                        else:
                            markdown += print_line + "\n"
                    elif tabs_count == 3 and details is not None:
                        details.hidden_lines.append(print_line)

        if details is not None:
            if not details.done:
                markdown += details.write_markdown_text()
            details = None

        if len(TOC.h1_items) > 0:
            TOC_text = TOC.write_items()
            markdown = markdown[:TOC.pos] + TOC_text + markdown[TOC.pos:]

    return markdown


# directories
python_dir  = os.path.dirname(os.path.abspath(__file__))
develop_dir = "d:\\work\\Script Development\\"
tabtext_dir = develop_dir + "TabbedTextConverter\\"
mtl_dir     = develop_dir + "MaterialTextureLoader\\"
sbx_dir     = develop_dir + "ScriptBox\\"

# text files
mtl_text = mtl_dir + "dev\\documents\\mtl_ui_description_002.txt"
sbx_text = sbx_dir + "dev\\documents\\sbx_ui_description_002.txt"

#output file
mtl_readme = mtl_dir + "public\\README.md"
sbx_readme = sbx_dir + "public\\README.md"

#file_path = os.path.join(python_dir, 'mtl_ui_description_002.txt')
#print(file_path)

# create markdown file
markdown_content = text_to_markdown(mtl_text)
with open(mtl_readme, 'w') as f:
    f.write(markdown_content)


#<br clear="left"/>