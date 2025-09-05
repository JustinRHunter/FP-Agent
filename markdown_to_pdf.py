#!/usr/bin/env python3
"""
Clean Markdown to PDF Converter
Uses markdown2 and WeasyPrint to convert markdown files to well-formatted PDFs
with modern styling, proper typography, and orphan prevention.
"""

import argparse
import sys
from pathlib import Path
import markdown2
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


def get_css_styles():
    """Return CSS styles for the PDF with modern typography and color accents."""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    * {
        box-sizing: border-box;
    }
    
    @page {
        size: A4;
        margin: 2.5cm 2cm;
        @bottom-center {
            content: counter(page);
            font-family: 'Inter', sans-serif;
            font-size: 10pt;
            color: #666;
        }
    }
    
    body {
        font-family: 'Inter', sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #2d3748;
        max-width: none;
        margin: 0;
        padding: 0;
    }
    
    /* Prevent orphaned headings */
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
        page-break-inside: avoid;
        orphans: 3;
        widows: 3;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        font-weight: 600;
    }
    
    h1 {
        font-size: 2.2em;
        color: #1a365d;
        border-bottom: 3px solid #3182ce;
        padding-bottom: 0.3em;
        margin-top: 0;
    }
    
    h2 {
        font-size: 1.8em;
        color: #2c5282;
        border-bottom: 2px solid #63b3ed;
        padding-bottom: 0.2em;
    }
    
    h3 {
        font-size: 1.4em;
        color: #2a4365;
    }
    
    h4 {
        font-size: 1.2em;
        color: #2d3748;
    }
    
    h5, h6 {
        font-size: 1.1em;
        color: #4a5568;
    }
    
    /* Ensure content follows headings */
    h1 + *, h2 + *, h3 + *, h4 + *, h5 + *, h6 + * {
        page-break-before: avoid;
    }
    
    p {
        margin: 0.8em 0;
        orphans: 3;
        widows: 3;
        text-align: justify;
        hyphens: auto;
    }
    
    /* Code styling */
    code {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9em;
        background-color: #f7fafc;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        border: 1px solid #e2e8f0;
        color: #e53e3e;
    }
    
    pre {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85em;
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3182ce;
        border-radius: 4px;
        padding: 1em;
        margin: 1em 0;
        overflow-x: auto;
        page-break-inside: avoid;
    }
    
    pre code {
        background: none;
        border: none;
        padding: 0;
        color: #2d3748;
    }
    
    /* Lists */
    ul, ol {
        margin: 0.8em 0;
        padding-left: 1.5em;
    }
    
    li {
        margin: 0.3em 0;
        orphans: 2;
        widows: 2;
    }
    
    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
        page-break-inside: avoid;
    }
    
    th, td {
        border: 1px solid #e2e8f0;
        padding: 0.5em;
        text-align: left;
    }
    
    th {
        background-color: #edf2f7;
        font-weight: 600;
        color: #2d3748;
    }
    
    tr:nth-child(even) {
        background-color: #f7fafc;
    }
    
    /* Blockquotes */
    blockquote {
        border-left: 4px solid #38b2ac;
        background-color: #f0fff4;
        margin: 1em 0;
        padding: 0.8em 1.2em;
        font-style: italic;
        page-break-inside: avoid;
    }
    
    blockquote p {
        margin: 0.5em 0;
    }
    
    /* Links */
    a {
        color: #3182ce;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    /* Images */
    img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 1em auto;
        page-break-inside: avoid;
    }
    
    /* Horizontal rules */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #3182ce, #63b3ed, #3182ce);
        margin: 2em 0;
    }
    
    /* Print optimizations */
    @media print {
        body {
            font-size: 10pt;
        }
        
        h1 { font-size: 18pt; }
        h2 { font-size: 16pt; }
        h3 { font-size: 14pt; }
        h4 { font-size: 12pt; }
        h5, h6 { font-size: 11pt; }
    }
    """


def convert_markdown_to_pdf(markdown_file, output_file=None, css_file=None):
    """Convert a markdown file to PDF."""
    
    # Read markdown file
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        print(f"Error: Markdown file '{markdown_file}' not found.")
        return False
    except Exception as e:
        print(f"Error reading markdown file: {e}")
        return False
    
    # Convert markdown to HTML
    try:
        html_content = markdown2.markdown(
            markdown_content,
            extras=[
                'fenced-code-blocks',
                'tables',
                'strike',
                'task_list',
                'code-friendly',
                'footnotes',
                'header-ids',
                'toc'
            ]
        )
    except Exception as e:
        print(f"Error converting markdown to HTML: {e}")
        return False
    
    # Wrap in HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Determine output filename
    if output_file is None:
        markdown_path = Path(markdown_file)
        output_file = markdown_path.with_suffix('.pdf')
    
    # Get CSS styles
    if css_file and Path(css_file).exists():
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
        except Exception as e:
            print(f"Error reading CSS file: {e}")
            css_content = get_css_styles()
    else:
        css_content = get_css_styles()
    
    # Convert to PDF
    try:
        font_config = FontConfiguration()
        html_doc = HTML(string=full_html)
        css_doc = CSS(string=css_content, font_config=font_config)
        
        html_doc.write_pdf(
            output_file,
            stylesheets=[css_doc],
            font_config=font_config
        )
        
        print(f"Successfully converted '{markdown_file}' to '{output_file}'")
        return True
        
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to well-formatted PDFs'
    )
    parser.add_argument(
        'input_file',
        help='Input Markdown file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output PDF file (default: same name as input with .pdf extension)'
    )
    parser.add_argument(
        '-c', '--css',
        help='Custom CSS file for styling'
    )
    
    args = parser.parse_args()
    
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    
    success = convert_markdown_to_pdf(
        args.input_file,
        args.output,
        args.css
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
