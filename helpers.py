# -*- coding: utf-8 -*-
import settings
from models import *
from parsel import Selector


def generate_sections(data):
    sections = []

    if len(data) > 0:
        sections.append(Section(index=0, title="Todos", subsections=[]))
        for index, element in enumerate(data):
            sel = Selector(text=element)
            title_text = sel.xpath(
                "//h4/text()"
            ).get()  # TODO: checar se esse xpath retorna o child e, caso não retornar, usar só "h4/text()"
            if title_text is not None and title_text != "":
                subsections = generate_subsections(element)
                section = Section(
                    index=index + 1,
                    title=title_text,
                    subsections=subsections,
                    source=data,
                )
                sections.append(section)

    return sections


def generate_subsections(data):
    subsections = []

    sel = Selector(text=data)
    children = sel.xpath("//a").getall()

    if len(children) > 0:
        subsections.append(Subsection(index=0, title="Todos", source=None))
        for index, element in enumerate(children):
            sel = Selector(text=element)
            title_text = sel.xpath("normalize-space(string(//a))").get()
            url = sel.xpath("//a/@href").get()
            if title_text is not None and title_text != "":
                subsections.append(
                    Subsection(index=index + 1, title=title_text, source=data, url=url)
                )

    return subsections


def print_init(url):
    print(
        f"Aguarde um instante enquanto o portal do INEP está sendo acessado ({url})..."
    )


def print_welcome(title, subtitle):
    len_title = len(title)
    len_subtitle = len(subtitle)
    print("".join(str("#") for x in range(len_title * 2 + len_subtitle)))
    print(f"#\t{title}\t#")
    print(f"#\t{subtitle}\t#")
    print("".join(str("#") for x in range(len_title * 2 + len_subtitle)) + "\n")
    print(
        f"Em caso de erro no programa, abra uma issue no link: { settings.OPEN_ISSUE_URL }\n"
    )
