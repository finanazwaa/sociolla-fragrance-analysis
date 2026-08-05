#!/usr/bin/env python3
import csv
import argparse
from shutil import copyfile


def clean_name(name: str, max_len: int, delimiters):
    if not name:
        return name
    original = name
    for d in delimiters:
        idx = name.find(d)
        if idx > 0:
            name = name[:idx]
            break
    name = name.strip()

    # remove trailing token 'Notes' or 'Note' if present
    tokens = name.split()
    if tokens and tokens[-1].lower() in ('notes', 'note'):
        tokens = tokens[:-1]
        name = ' '.join(tokens).strip()

    # detect marketing/descriptive lines and convert to empty
    lower_orig = original.lower()
    noise_indicators = ['tahan', 'untuk', 'kamu', 'semprot', 'cara pakai', 'cara', 'pakai', 'long-lasting', 'long lasting', 'perfect for', 'tunggu', 'kering', 'cocok buat', 'cocok']
    if any(n in lower_orig for n in noise_indicators):
        # if after truncation the remaining text still looks like a sentence (contains verbs or stop words), null it
        # consider short proper names (<=3 words) as valid
        if len(name.split()) > 3:
            return ''

    if len(name) > max_len:
        return name[:max_len].rstrip() + '...'
    return name


def main():
    parser = argparse.ArgumentParser(description='Clean note_name in notes.csv')
    parser.add_argument('--input', '-i', default='data/notes.csv')
    parser.add_argument('--output', '-o', default='data/notes_fixed.csv')
    parser.add_argument('--backup', '-b', default='data/notes_backup.csv')
    parser.add_argument('--max', '-m', type=int, default=50, help='max length for note_name')
    args = parser.parse_args()

    delimiters = [' Cocok', ' Cocok buat', ' Cara', ' Cara Pakai', ' - ', ' – ', ' — ']

    copyfile(args.input, args.backup)

    modified = 0
    samples = []
    with open(args.input, newline='', encoding='utf-8') as inf, open(args.output, 'w', newline='', encoding='utf-8') as outf:
        reader = csv.DictReader(inf)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            orig = row.get('note_name', '')
            cleaned = clean_name(orig, args.max, delimiters)
            if cleaned != orig:
                modified += 1
                if len(samples) < 10:
                    samples.append((row.get('note_id', ''), orig, cleaned))
            row['note_name'] = cleaned
            writer.writerow(row)

    print(f'Wrote cleaned file: {args.output}')
    print(f'Backup of original created at: {args.backup}')
    print(f'Modified rows: {modified}')
    if samples:
        print('\nSample changes (note_id, before => after):')
        for sid, before, after in samples:
            print(f'{sid}: "{before}" => "{after}"')


if __name__ == '__main__':
    main()
