import sys, io, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load(path):
    d = {}
    with io.open(path, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.rstrip('\n').split('\t')
            if len(parts) >= 2:
                d[parts[0]] = parts[1].split(' ')[0]
    return d

PH = load(os.path.join(BASE, 'TSPhrases.txt'))
CH = load(os.path.join(BASE, 'TSCharacters.txt'))
KEYS = sorted(PH.keys(), key=len, reverse=True)

def convert(text):
    for k in KEYS:
        if k in text:
            text = text.replace(k, PH[k])
    return ''.join(CH.get(c, c) for c in text)

if __name__ == '__main__':
    s = '雜阿含1經：如是我聞，一時，佛住舍衛國祇樹給孤獨園。爾時，世尊告諸比丘：「當觀色無常，如是觀者則為正觀；正觀者則生厭離；厭離者喜、貪盡；喜、貪盡者說心解脫。」'
    print(convert(s))
