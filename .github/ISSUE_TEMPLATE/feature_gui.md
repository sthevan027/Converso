# Interface Gráfica (GUI)

## Descrição

Criar uma interface gráfica para facilitar o uso do conversor, permitindo que usuários sem conhecimento técnico possam converter documentos facilmente.

---

## Etapas de Implementação

### Fase 1: Estrutura Base

- [ ] Escolher framework GUI (Tkinter, PyQt6, ou CustomTkinter)
- [ ] Criar estrutura de pastas para a GUI (gui/)
- [ ] Configurar dependências no requirements.txt

### Fase 2: Tela Principal

- [ ] Criar janela principal com título e ícone
- [ ] Adicionar área de arrastar e soltar (drag and drop) para arquivos
- [ ] Botão "Selecionar Arquivo" com diálogo de seleção
- [ ] Exibir nome e caminho do arquivo selecionado
- [ ] Dropdown para selecionar formato de saída (DOCX, PDF)

### Fase 3: Opções de Configuração

- [ ] Seção expansível "Opções Avançadas"
- [ ] Configuração de cabeçalho/rodapé (keep, remove, convert)
- [ ] Seleção de qualidade (fast, balanced, high)
- [ ] Checkbox para opções (preservar formatação, extrair imagens, etc.)
- [ ] Campos para página inicial e final

### Fase 4: Conversão e Feedback

- [ ] Botão "Converter" com estado habilitado/desabilitado
- [ ] Barra de progresso durante a conversão
- [ ] Log de mensagens em tempo real
- [ ] Notificação de sucesso/erro ao finalizar
- [ ] Botão "Abrir Pasta de Saída"

### Fase 5: Melhorias de UX

- [ ] Tema claro/escuro
- [ ] Salvar preferências do usuário
- [ ] Histórico de conversões recentes
- [ ] Conversão em lote (múltiplos arquivos)
- [ ] Atalhos de teclado

---

## Mockup Sugerido

```text
+-------------------------------------------+
|  Converso - Conversor de Documentos       |
+-------------------------------------------+
|                                           |
|   +-----------------------------------+   |
|   |                                   |   |
|   |   Arraste um arquivo aqui        |   |
|   |   ou clique para selecionar      |   |
|   |                                   |   |
|   +-----------------------------------+   |
|                                           |
|   Arquivo: documento.pdf                  |
|   Converter para: [DOCX v]                |
|                                           |
|   > Opções Avançadas                      |
|                                           |
|   [=========>          ] 45%              |
|                                           |
|          [ Converter ]                    |
|                                           |
+-------------------------------------------+
```

---

## Tecnologias Sugeridas

- **CustomTkinter** - Interface moderna com tema escuro
- **TkinterDnD2** - Drag and drop de arquivos
- **Threading** - Conversão em background sem travar a UI
