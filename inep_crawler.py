# -*- coding: utf-8 -*-
import argparse
import helpers
import sys
import settings
import requests
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", type=str, help="URL para o site de microdados do INEP")

    args = parser.parse_args()
    url = args.url if args.url else settings.INEP_URL

    if url is None:
        print("Nenhuma URL para base do INEP foi definida")
        exit(1)

    helpers.print_init(url)
    req = requests.get(url)

    if req.status_code != 200:
        print(
            f"Ocorreu um erro com código {req.status_code} na requisição para a URL {url}"
        )
        exit(1)

    content = req.content
    soup = BeautifulSoup(content, "html.parser")
    
    title = soup.find("title")
    page_update = soup.find("span", {"class": "page-update"})  # TODO Validate version
    meta_data = soup.find(
        "meta", {"property": "creator.productor"}
    )  # TODO Validate version

    helpers.print_welcome(title = title.text, subtitle = page_update.text)

    sections = helpers.generate_sections(soup.find_all(
        lambda tag: tag.name == "div"
        and tag.get("class")
        and "anchor__content" in tag.get("class")
        and tag.get("data-anchor")
    ))

    for section in sections:
        print(f"{section}")

    #select section
    try:
        print(f"Escolha uma opção entre 0 e {len(sections) - 1}")
        option = int(input("Opção: "))
        if option < 0 or option > len(sections):
            raise ValueError

        selected_section = sections[option]
        print(f"Categoria escolhida: {selected_section}")
    except ValueError:
        print("Opção inválida")
        exit(1)

    download_files = []
    #select subsection
    if selected_section.isDefault():
        print(f"Baixando todos os dados de todas as categorias...")
        for section in sections:
            for subsection in section.subsections():
                download_files.append(subsection.url())
    elif selected_section.subsections:
        subsections = selected_section.subsections()
        for subsection in subsections:
            print(f"{subsection}")

        try:
            print(f"Escolha uma opção entre 0 e {len(subsections) - 1}")
            option = int(input("Opção: "))
            if option < 0 or option > len(subsections):
                raise ValueError
            
            selected_subsection = subsections[option]
        except ValueError:
            print("Opção inválida")
            exit(1)

        print(f"Baixando dados de {selected_section} - {selected_subsection}...")
        download_files.append(selected_subsection.url())

    #TODO Async
    for file in download_files:
        file_name = file.split('/')[::-1][0]
        print(f"Requisitando o arquivo {file_name}")
        req = requests.get(file)

        if req.status_code != 200:
            print(
                f"Ocorreu um erro com código {req.status_code} ao tentar baixar o arquivo {file_name}"
            )
        else:
            #TODO save download info
            open(file_name, 'wb').write(req.content)
            print(
                f"O arquivo {file} foi baixado com sucesso"
            )


if __name__ == "__main__":
    main()
