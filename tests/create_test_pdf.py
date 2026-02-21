"""Script para criar PDF de teste para o conversor."""
import fitz  # PyMuPDF


def create_test_pdf(output_path: str = "tests/test_document.pdf") -> None:
    """Cria um PDF de teste com cabeçalho, rodapé, títulos e texto."""
    doc = fitz.open()

    for page_num in range(1, 4):
        page = doc.new_page(width=595, height=842)  # A4

        # Cabeçalho
        header_rect = fitz.Rect(50, 30, 545, 60)
        page.insert_textbox(
            header_rect,
            "Empresa ABC - Documento de Teste",
            fontsize=10,
            align=fitz.TEXT_ALIGN_CENTER,
        )

        # Linha separadora do cabeçalho
        page.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), width=0.5)

        # Título principal (apenas na primeira página)
        if page_num == 1:
            title_rect = fitz.Rect(50, 80, 545, 120)
            page.insert_textbox(
                title_rect,
                "Relatório de Testes do Conversor PDF",
                fontsize=18,
                align=fitz.TEXT_ALIGN_CENTER,
            )
            y_start = 140
        else:
            y_start = 80

        # Subtítulo
        subtitle_rect = fitz.Rect(50, y_start, 545, y_start + 30)
        page.insert_textbox(
            subtitle_rect,
            f"Capítulo {page_num}: Seção de Teste",
            fontsize=14,
            align=fitz.TEXT_ALIGN_LEFT,
        )

        # Corpo do texto
        body_text = """
Este é um parágrafo de teste para verificar a conversão de PDF para Word. 
O texto deve ser extraído corretamente, mantendo a formatação e estrutura 
do documento original.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod 
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim 
veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
commodo consequat.

Características importantes do conversor:
- Detecção automática de cabeçalhos
- Identificação de rodapés
- Preservação de formatação
- Extração de imagens
- Mesclagem de parágrafos

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum 
dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non 
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""
        body_rect = fitz.Rect(50, y_start + 40, 545, 750)
        page.insert_textbox(
            body_rect,
            body_text.strip(),
            fontsize=11,
            align=fitz.TEXT_ALIGN_JUSTIFY,
        )

        # Linha separadora do rodapé
        page.draw_line(fitz.Point(50, 780), fitz.Point(545, 780), width=0.5)

        # Rodapé
        footer_rect = fitz.Rect(50, 790, 545, 820)
        page.insert_textbox(
            footer_rect,
            f"Página {page_num} de 3 | Confidencial",
            fontsize=9,
            align=fitz.TEXT_ALIGN_CENTER,
        )

    doc.save(output_path)
    doc.close()
    print(f"PDF de teste criado: {output_path}")


if __name__ == "__main__":
    create_test_pdf()
