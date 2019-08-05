# -*- coding: utf-8 -*-
import sys
import settings
from models import *


def generate_sections(data):
    sections = []

    if len(data):
        sections.append(Section(index=0, title='Todos', subsections=[]))
        for index in range(len(data)):
            title = data[index].findChildren("h4")
            title_text = title[0].text if title and title[0] and title[0].text else None
            if title_text:
                subsections = generate_subsections(data = data[index])
                section = Section(index=index+1, title=title_text, subsections=subsections, source=data)
                sections.append(section)

    return sections


def generate_subsections(data):
    subsections = []

    children = data.findChildren("a")

    if len(children):
        subsections.append(Subsection(index=0, title='Todos', source=None))
        for index in range(len(children)):
            title_text = children[index].text if children[index] and children[index].text else None
            if title_text:
                subsections.append(Subsection(index=index + 1, title=title_text, source=data))

    return subsections


def print_init(url):
    print(f"Aguarde um instante enquanto o portal do INEP está sendo acessado ({url})...")


def print_welcome(title, subtitle):
    len_title = len(title)
    len_subtitle = len(subtitle)
    print("".join(str("#") for x in range(len_title * 2 + len_subtitle)))
    print(f"#\t{title}\t#")
    print(f"#\t{subtitle}\t#")
    print("".join(str("#") for x in range(len_title * 2 + len_subtitle)))
    print("")
    print(
        f"Em caso de erro no programa, abra uma issue no link: { settings.OPEN_ISSUE_URL }"
    )
    print("")

