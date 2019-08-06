import asyncio
import aiohttp
import argparse
import helpers
import settings
import os

from parsel import Selector


async def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", type=str, help="URL para o site de microdados do INEP")

    args = parser.parse_args()
    url = args.url if args.url else settings.INEP_URL

    if url is None:
        print("Nenhuma URL para base do INEP foi definida")
        return

    helpers.print_init(url)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as req:
            req.raise_for_status()
            content = await req.text()
    
    sel = Selector(text=content)

    title = sel.xpath("//title/text()").get()
    page_update = sel.xpath("//span[@class='page-update']/text()").get()
    meta_data = sel.xpath("//meta[@property='creator.productor']").get()

    helpers.print_welcome(title=title, subtitle=page_update)

    sections = helpers.generate_sections(sel.xpath("//div[contains(@class, 'anchor__content') and @data-anchor)]").getall())

    for section in sections:
        print(section)

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
        return

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
            return

        print(f"Baixando dados de {selected_section} - {selected_subsection}...")
        download_files.append(selected_subsection.url())

    for f in download_files:
        file_name = os.path.basename(f)

        print(f"Requisitando o arquivo {file_name}")

        async with aiohttp.ClientSession() as session:
            async with session.get(file) as req:
                req.raise_for_status()

                with open(file_name, "wb") as output_f:
                    async for chunk in req.content.iter_chunked(256):
                        output_f.write(chunk)

                print(f"O arquivo {f} foi baixado com sucesso!")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
