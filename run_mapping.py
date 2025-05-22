import os
import sys
import json
import argparse
import tkinter as tk
from tkinter import filedialog
import PyPDF2
from docx import Document
from sentence_transformers import SentenceTransformer
import torch
from torch.nn.functional import cosine_similarity

# --- Text Extraction ---
def extract_text_from_pdf(path):
    lines = []
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            raw = page.extract_text() or ''
            for ln in raw.splitlines():
                text = ln.strip()
                if len(text) > 30:
                    lines.append(text)
    return lines


def extract_text_from_docx(path):
    doc = Document(path)
    return [p.text.strip() for p in doc.paragraphs if len(p.text.strip()) > 30]


def load_clauses(path):
    if path.lower().endswith('.pdf'):
        return extract_text_from_pdf(path)
    if path.lower().endswith('.docx'):
        return extract_text_from_docx(path)
    raise ValueError('Unsupported file type: ' + path)


# --- Command-line or GUI selection ---

def select_file(prompt):
    print(prompt)
    root = tk.Tk(); root.withdraw()
    path = filedialog.askopenfilename(filetypes=[('PDF','*.pdf'),('DOCX','*.docx')])
    if not path:
        sys.exit('No file selected, exiting.')
    print('Selected:', path)
    return path


def main():
    parser = argparse.ArgumentParser(description='Map SOP to ISO clauses')
    parser.add_argument('--sop', help='Path to SOP PDF/DOCX')
    parser.add_argument('--output', default='sop_iso_mapping.json', help='Output JSON file')
    args = parser.parse_args()

    # # Load ISO standards from embedded JSON
    # iso_json = os.path.join(os.path.dirname(__file__), 'ISO_IEC_27002.json')
    # with open(iso_json, 'r', encoding='utf8') as f:
    #     iso_data = json.load(f)
    # iso_ids = [item['code'] for item in iso_data['values']]
    # iso_texts = [item['label'] for item in iso_data['values']]

    # Determine SOP path and load clauses
    sop_path = args.sop or select_file('Select SOP document:')
    sop_texts = load_clauses(sop_path)
    sop_ids = [f'SOP-{i+1}' for i in range(len(sop_texts))]

    # Embedding
    # print('Loading embedding model...')
    # model = SentenceTransformer('all-roberta-large-v1')
    # iso_emb = model.encode(iso_texts, convert_to_tensor=True)
    # sop_emb = model.encode(sop_texts, convert_to_tensor=True)

    # Mapping
    print('Computing mappings...')
    mappings = {}
    for i, sop_id in enumerate(sop_ids):
        # sims = cosine_similarity(sop_emb[i].unsqueeze(0), iso_emb)
        # best = torch.argmax(sims).item()
        mappings[sop_id] = {
            'sop_text': sop_texts[i]
            # 'iso_id': iso_ids[best],
            # 'iso_text': iso_texts[best],
            # 'similarity': float(sims[best])
        }

    # Save
    with open(args.output, 'w', encoding='utf8') as f:
        json.dump(mappings, f, indent=2)
    # print(f'Mapping saved to {args.output}')


if __name__ == '__main__':
    main()
