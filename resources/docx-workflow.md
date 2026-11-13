# DOCX Workflow Reference

## Choose an approach

| Request | Recommended approach |
|---|---|
| Create a Word document | Outline, build with python-docx, render and review |
| Edit an existing file | Inspect first, make targeted changes, preserve styles |
| Extract text | Read paragraphs and tables in document order |
| Reformat | Identify layout issues, define styles, apply consistently |
| Create a template | Use semantic styles, placeholders, and controlled tables |
| Review | Separate factual, structural, language, and visual findings |
| Compare versions | Extract text and structure, then report meaningful changes |

## Suggested working layout

~~~text
work/
  source.docx
  output.docx
  rendered/
    page-1.png
    page-2.png
~~~

Keep source and output separate. Do not overwrite the source unless asked.

## python-docx inspection
Useful objects include Document(path), document.paragraphs, document.tables, document.sections, paragraph.style, paragraph.runs, table.rows, section.header, and section.footer.

Important: document.paragraphs and document.tables are separate collections. Iterating them separately does not preserve their interleaved order. For order-sensitive extraction, walk the underlying document body XML and process paragraph and table elements sequentially.

## Editing discipline
1. Load the original.
2. Record page setup and key styles.
3. Locate exact paragraphs or tables to change.
4. Change only requested content.
5. Save to a new file.
6. Reopen the saved file.
7. Render and inspect when layout matters.

Rebuilding an entire document for a small edit can lose fields, comments, tracked changes, custom XML, or other Word features not fully preserved by python-docx.

## Tables and page layout
- Set explicit column widths when predictable layout matters.
- Use clear header rows and repeat them across pages where possible.
- Keep total table width within usable page width.
- Avoid unnecessary nested tables.
- Use page breaks for intentional new pages, not stacks of blank paragraphs.
- Use section breaks only when page layout changes.

## Rendering
Visual rendering is especially important for documents with tables, images, headers, footers, mixed orientations, page-number fields, strict page limits, or template matching. Word and LibreOffice may paginate differently. Disclose when rendering tools are unavailable.