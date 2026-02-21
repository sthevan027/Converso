# Melhoria na Lógica de Conversão

## Descrição

Melhorar a lógica de conversão para aumentar a qualidade, performance e confiabilidade do sistema.

---

## Etapas de Implementação

### Fase 1: Melhorias na Detecção de Estrutura (PDF para DOCX)

- [ ] Melhorar algoritmo de detecção de cabeçalhos (usar ML ou heurísticas avançadas)
- [ ] Detectar rodapés com números de página em diferentes formatos (i, ii, 1, 2, A, B)
- [ ] Identificar notas de rodapé vs rodapé da página
- [ ] Melhorar detecção de títulos baseada em contexto (não apenas tamanho de fonte)

### Fase 2: Melhorias na Extração de Texto

- [ ] Implementar OCR para PDFs escaneados (usando Tesseract ou EasyOCR)
- [ ] Melhorar tratamento de texto em múltiplas colunas
- [ ] Detectar e preservar listas numeradas e com marcadores
- [ ] Melhorar mesclagem de parágrafos com análise semântica
- [ ] Tratar textos rotacionados ou em ângulo

### Fase 3: Melhorias em Tabelas

- [ ] Implementar detecção avançada de tabelas (bordas visíveis e invisíveis)
- [ ] Preservar formatação de células (cores, alinhamento)
- [ ] Detectar células mescladas
- [ ] Converter tabelas complexas corretamente

### Fase 4: Melhorias em Imagens

- [ ] Preservar posição relativa das imagens no texto
- [ ] Suportar imagens vetoriais (SVG)
- [ ] Otimizar compressão de imagens
- [ ] Detectar e remover marcas d'água (opcional)

### Fase 5: Melhorias na Conversão DOCX para PDF

- [ ] Preservar hyperlinks
- [ ] Suportar imagens embutidas no DOCX
- [ ] Melhorar renderização de tabelas
- [ ] Preservar cores e estilos de texto
- [ ] Suportar fontes customizadas

### Fase 6: Performance e Otimização

- [ ] Implementar conversão paralela para documentos grandes
- [ ] Cache de análise de fontes
- [ ] Otimizar uso de memória para PDFs grandes
- [ ] Adicionar modo streaming para arquivos muito grandes

### Fase 7: Qualidade e Testes

- [ ] Criar suite de testes automatizados com diferentes tipos de PDFs
- [ ] Implementar métricas de qualidade de conversão
- [ ] Adicionar validação de saída (verificar DOCX/PDF válidos)
- [ ] Testes de regressão para cada release

---

## Prioridades

| Prioridade | Fase | Justificativa |
| ---------- | ---- | ------------- |
| Alta | Fase 2 | OCR expande muito o uso do conversor |
| Alta | Fase 3 | Tabelas são comuns em documentos corporativos |
| Média | Fase 1 | Melhora qualidade geral |
| Média | Fase 5 | Completa ciclo bidirecional |
| Baixa | Fase 4 | Imagens já funcionam basicamente |
| Baixa | Fase 6 | Otimização após funcionalidades |

---

## Dependências Sugeridas

```txt
# OCR
pytesseract>=0.3.10
easyocr>=1.7.0

# Processamento de imagem
Pillow>=10.0.0
opencv-python>=4.8.0

# Detecção de tabelas
camelot-py>=0.11.0
tabula-py>=2.8.0
```
