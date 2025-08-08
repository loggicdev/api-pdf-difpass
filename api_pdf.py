import fitz # PyMuPDF
import os
import io
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
from PIL import Image, ImageDraw

app = FastAPI(
    title="PDF Shell Generator API",
    description="API to create a PDF 'shell' with custom header elements and insert a PDF document into it."
)

def create_pdf_shell_and_insert_content_core(
    input_pdf_path: str,
    icon_image_path: str,
    dif_image_path: str,
    title_text: str = "CRUZEIRO"
) -> io.BytesIO:
    """
    Core function to create a new PDF (a "shell") with header elements only
    and insert each page of the input PDF into a frame within that shell.

    Args:
        input_pdf_path (str): The path to the input PDF file.
        icon_image_path (str): The path to the icon image file (PNG).
        dif_image_path (str): The path to the DIFPASS logo image file (PNG).
        title_text (str): The title text to be included in the header.

    Returns:
        io.BytesIO: An in-memory byte stream of the generated PDF.
    """
    try:
        input_doc = fitz.open(input_pdf_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error opening input PDF: {e}")

    output_doc = fitz.open()

    margin_x = 40
    margin_y_bottom = 40

    icon_size = 40
    dif_logo_width = 100
    dif_logo_height = 40
    title_font_size = 20

    # Altura do cabeçalho COM gradiente
    bar_height = 50  # Altura da barra do gradiente
    spacing_before_bar = 20  # Espaçamento antes da barra
    header_height = max(icon_size, dif_logo_height, title_font_size) + spacing_before_bar + bar_height + 5

    border_color = (0.85, 0.85, 0.85)
    border_width = 0.5  # Reduzido de 1 para 0.5 para ficar mais sutil

    for page_num in range(len(input_doc)):
        input_page = input_doc[page_num] # Acessa a página usando indexação
        new_page = output_doc.new_page(width=input_page.rect.width, height=input_page.rect.height)

        print(f"🏗️ === PÁGINA {page_num + 1} ===")
        print(f"📏 Dimensões da página: {new_page.rect.width}x{new_page.rect.height}")

        # --- CRIAR APENAS CABEÇALHO (SEM GRADIENTE) ---
        # Posição do ícone (canto superior esquerdo)
        icon_rect = fitz.Rect(margin_x, margin_x, margin_x + icon_size, margin_x + icon_size)
        try:
            new_page.insert_image(icon_rect, filename=icon_image_path)
            print(f"✅ Ícone inserido")
        except Exception as e:
            print(f"⚠️ Erro no ícone: {e}")

        # Posição do logo DIFPASS (canto superior direito)
        dif_logo_x = new_page.rect.width - margin_x - dif_logo_width
        dif_logo_rect = fitz.Rect(dif_logo_x, margin_x, dif_logo_x + dif_logo_width, margin_x + dif_logo_height)
        try:
            new_page.insert_image(dif_logo_rect, filename=dif_image_path)
            print(f"✅ Logo DIFPASS inserido")
        except Exception as e:
            print(f"⚠️ Erro no logo DIFPASS: {e}")

        # Posição do título "CRUZEIRO"
        title_x = margin_x + icon_size + 15
        title_y = margin_x + (icon_size + title_font_size) / 2
        new_page.insert_text((title_x, title_y), title_text, fontsize=title_font_size, color=(0, 0, 0))
        print(f"✅ Título inserido")

        # --- CRIAR GRADIENTE APÓS O CABEÇALHO ---
        top_content_bottom_y = margin_x + max(icon_size, dif_logo_height, title_font_size)
        bar_y_position = top_content_bottom_y + spacing_before_bar
        inner_left = margin_x
        inner_right = new_page.rect.width - margin_x
        bar_rect = fitz.Rect(inner_left, bar_y_position, inner_right, bar_y_position + bar_height)

        print(f"🎯 bar_y_position: {bar_y_position}")
        print(f"🎯 bar_rect: {bar_rect}")

        # FUNÇÃO DE GRADIENTE SIMPLES
        def create_gradient_bar(page, rect):
            print(f"🎨 === CRIANDO GRADIENTE ===")
            width = int(rect.width)
            height = int(rect.height)
            
            if width <= 0 or height <= 0:
                print(f"❌ Dimensões inválidas: {width}x{height}")
                return
            
            # Cores do gradiente
            blue_color = (4, 67, 111)      # #04436F
            orange_color = (197, 81, 23)   # #C55117
            
            # Criar imagem gradiente com bordas arredondadas
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Raio das bordas arredondadas
            corner_radius = min(height // 4, 15)  # Máximo 15px ou 1/4 da altura
            print(f"🔄 Raio das bordas: {corner_radius}px")
            
            # Gradiente horizontal
            for x in range(width):
                ratio = x / (width - 1) if width > 1 else 0
                r = int(blue_color[0] + (orange_color[0] - blue_color[0]) * ratio)
                g = int(blue_color[1] + (orange_color[1] - blue_color[1]) * ratio)
                b = int(blue_color[2] + (orange_color[2] - blue_color[2]) * ratio)
                draw.line([(x, 0), (x, height-1)], fill=(r, g, b, 255))
            
            # Cria máscara para bordas arredondadas APENAS NA PARTE SUPERIOR
            mask = Image.new('L', (width, height), 255)  # Fundo branco (opaco) para evitar transparência
            mask_draw = ImageDraw.Draw(mask)
            
            # Mascara as bordas superiores para criar arredondamento
            # Canto superior esquerdo
            mask_draw.rectangle([(0, 0), (corner_radius, corner_radius)], fill=0)
            mask_draw.pieslice([(0, 0), (corner_radius*2, corner_radius*2)], 180, 270, fill=255)
            
            # Canto superior direito  
            mask_draw.rectangle([(width-corner_radius, 0), (width-1, corner_radius)], fill=0)
            mask_draw.pieslice([(width-corner_radius*2, 0), (width, corner_radius*2)], 270, 360, fill=255)
            
            # Aplica a máscara ao gradiente
            img.putalpha(mask)
            
            # Salvar temporariamente
            temp_img_path = f"/tmp/gradient_{os.getpid()}.png"
            img.save(temp_img_path, "PNG")
            print(f"💾 Gradiente salvo em: {temp_img_path}")
            
            try:
                # Inserir gradiente
                page.insert_image(rect, filename=temp_img_path, overlay=True)
                print(f"✅ GRADIENTE INSERIDO!")
                
                # Texto sobre o gradiente
                text_x = rect.x0 + 50
                text_y = rect.y0 + (rect.height * 0.6)
                page.insert_text((text_x, text_y), "Dados do documento", fontsize=14, color=(1, 1, 1))
                print(f"✅ TEXTO INSERIDO!")
                
                # Ícone da barra (Group 5.png) - menor
                bar_icon_path = os.path.join(os.path.dirname(__file__), "assets", "Group (5).png")
                if os.path.exists(bar_icon_path):
                    icon_bar_size = min(rect.height - 15, 18)  # Menor: 18px máximo
                    icon_bar_x = rect.x0 + 15
                    icon_bar_y = rect.y0 + (rect.height - icon_bar_size) / 2
                    icon_bar_rect = fitz.Rect(icon_bar_x, icon_bar_y, icon_bar_x + icon_bar_size, icon_bar_y + icon_bar_size)
                    page.insert_image(icon_bar_rect, filename=bar_icon_path)
                    print(f"📄 Ícone Group (5).png inserido!")
                else:
                    print(f"⚠️ Ícone Group (5).png não encontrado em: {bar_icon_path}")
                
            finally:
                try:
                    os.remove(temp_img_path)
                    print(f"🗑️ Arquivo temporário removido")
                except:
                    pass

        # CRIAR GRADIENTE
        if bar_rect.width > 0 and bar_rect.height > 0:
            print(f"🎨 === CRIANDO GRADIENTE APÓS CABEÇALHO! ===")
            create_gradient_bar(new_page, bar_rect)
            print(f"✅ Gradiente criado sem borda")
        else:
            print(f"❌ Dimensões da barra inválidas!")

        # Calcula o retângulo onde o conteúdo do PDF original será inserido
        content_start_y = bar_y_position + bar_height
        inner_rect = fitz.Rect(margin_x, content_start_y, new_page.rect.width - margin_x, new_page.rect.height - margin_y_bottom)

        print(f"📄 === INSERINDO CONTEÚDO DO PDF ORIGINAL ===")
        print(f"📍 Conteúdo começa em Y={content_start_y} (APÓS o gradiente)")
        print(f"📍 Gradiente termina em Y={bar_y_position + bar_height}")

        # Desenha a borda cinza clara
        new_page.draw_rect(inner_rect, color=border_color, width=border_width)
        print(f"🔲 Borda desenhada: {inner_rect}")

        # Insere a página do PDF original no retângulo calculado
        new_page.show_pdf_page(inner_rect, input_doc, page_num)
        print(f"✅ Conteúdo da página {page_num + 1} inserido")

    pdf_buffer = io.BytesIO()
    try:
        output_doc.save(pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving modified PDF: {e}")
    finally:
        output_doc.close()
        input_doc.close()


@app.post("/generate-pdf/")
async def generate_pdf_shell(
    title: str = Form("CRUZEIRO"),
    icon_image: UploadFile = File(...),
    dif_image: UploadFile = File(...),
    input_pdf: UploadFile = File(...)
):
    """
    Generates a PDF document with header elements only and inserts an existing PDF's content.

    Args:
        title (str): The title text to display in the header (e.g., "CRUZEIRO").
        icon_image (UploadFile): The icon image file (PNG).
        dif_image (UploadFile): The DIFPASS logo image file (PNG).
        input_pdf (UploadFile): The PDF document to be inserted into the shell.

    Returns:
        StreamingResponse: The generated PDF file.
    """
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()

        icon_path = os.path.join(temp_dir, icon_image.filename)
        with open(icon_path, "wb") as buffer:
            shutil.copyfileobj(icon_image.file, buffer)

        dif_path = os.path.join(temp_dir, dif_image.filename)
        with open(dif_path, "wb") as buffer:
            shutil.copyfileobj(dif_image.file, buffer)

        input_pdf_path = os.path.join(temp_dir, input_pdf.filename)
        with open(input_pdf_path, "wb") as buffer:
            shutil.copyfileobj(input_pdf.file, buffer)

        pdf_buffer = create_pdf_shell_and_insert_content_core(
            input_pdf_path, icon_path, dif_path, title
        )

        return StreamingResponse(pdf_buffer, media_type="application/pdf",
                                 headers={"Content-Disposition": f"attachment; filename=ticket_with_shell.pdf"})

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    import uvicorn
    import socket
    
    def find_free_port():
        """Encontra uma porta livre para o servidor"""
        for port in [8000, 8001, 8002, 8003, 8004]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('0.0.0.0', port))
                    return port
                except OSError:
                    continue
        return 8000  # fallback
    
    port = find_free_port()
    print(f"🚀 Iniciando servidor na porta {port}")
    print(f"📝 Documentação: http://localhost:{port}/docs")
    print(f"🔄 ReDoc: http://localhost:{port}/redoc")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
