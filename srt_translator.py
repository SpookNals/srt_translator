import os
import re
import argparse
from tqdm import tqdm

import torch
from transformers import MarianMTModel, MarianTokenizer

INPUT_DIR = "./srt_en"
OUTPUT_DIR = "./srt_nl"
MODEL_NAME = "Helsinki-NLP/opus-mt-en-nl"

def load_translator(model_name):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return tokenizer, model, device

def batch_translate(text_list, tokenizer, model, device):
    batch = tokenizer(text_list, return_tensors="pt", padding=True, truncation=True)
    batch = {k: v.to(device) for k, v in batch.items()}
    with torch.no_grad():
        generated = model.generate(**batch)
    return tokenizer.batch_decode(generated, skip_special_tokens=True)

def extract_blocks(lines):
    blocks = []
    current_block = []
    indexes = []

    for line in lines:
        if re.match(r"^\d+$", line):
            indexes.append(line.strip())
            if current_block:
                blocks.append(current_block)
                current_block = []
        elif re.match(r"^\d{2}:\d{2}:\d{2},\d{3} -->", line):
            current_block.append(line.strip())
        elif line.strip():
            current_block.append(line.strip())
        else:
            if current_block:
                blocks.append(current_block)
                current_block = []
            indexes.append("")

    if current_block:
        blocks.append(current_block)

    return blocks, indexes

def translate_and_fix_srt(input_file, output_file, tokenizer, model, device):
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    blocks, indexes = extract_blocks(lines)
    subtitles = [" ".join(block[1:]) for block in blocks]
    translations = []

    for i in tqdm(range(0, len(subtitles), 16), desc=f"Vertalen {os.path.basename(input_file)}"):
        batch = subtitles[i:i + 16]
        translations.extend(batch_translate(batch, tokenizer, model, device))

    translated_lines = []
    for i, block in enumerate(blocks):
        if indexes[i] != "":
            translated_lines.append(indexes[i] + "\n")
        translated_lines.append(block[0] + "\n")  # timestamp
        translated_lines.append(translations[i] + "\n")
        translated_lines.append("\n")

    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(translated_lines)

def process_all_srts():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    tokenizer, model, device = load_translator(model_name=MODEL_NAME)

    srt_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".srt")]

    for srt_file in srt_files:
        input_path = os.path.join(INPUT_DIR, srt_file)
        output_path = os.path.join(OUTPUT_DIR, srt_file)
        translate_and_fix_srt(input_path, output_path, tokenizer, model, device)

if __name__ == '__main__':

    process_all_srts()
