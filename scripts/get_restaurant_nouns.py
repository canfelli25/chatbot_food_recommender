import nltk
from polyglot.text import Text
from polyglot.detect import Detector
import json

FILE = 'static/resto-reviews-{}.json'
STOPS = ['sih', 'yang', 'gue', 'enak', 'the', 'and', 'dan', 'also', 'duh', 'yng', 'gak', 'ngak', 'nggak',
    'oke', 'okay', 'all', 'semua', 'mas', 'mba', 'mbak', 'pak', 'ibu', 'bu', 'bapak', 'aja', 'saja',
    'bgt', 'banget', 'bngt', 'nya', 'dia', 'wah', 'waah', 'wahh', 'way', 'worth', 'gitu', 'zomato', 'zomayo', 
    'sini', 'dah', 'deh', 'doi', 'sana', 'situ', 'apa', 'kapan', 'lagi', 'mau', 'nak', 'yah', 'yak', 'yam',
    'yummy', 'enakk', 'delicious', 'recommended', 'recomended', 'bagus', 'rekomendasi', 'duh',
    'pesan', 'pesen', 'girl', 'boy', 'guys', 'him', 'her', 'them', 'our', 'kita', 'kami', 'aku', 'gua']

def get_chunk_parser():
    grammar = r'''
    NP: {<NUM|DET>* <NOUN|PROPN|PRON>* <.*>* <NOUN|PROPN|PRON>}
        {<NOUN|PROPN|PRON> <NOUN|PROPN|PRON>}
        {<NOUN|PROPN|PRON>* <ADJ>}
        {<NUM|DET>* <NOUN|PROPN|PRON>* <PP>}
        {<NOUN|PROPN|PRON>}
    PP: {<ADP><NOUN|PROPN|PRON>*}
    '''
    chunk_parser = nltk.RegexpParser(grammar)
    return chunk_parser

def get_chunks(text):
    try:
        detector = Detector(text)
        hint = 'en' if detector.language.name == 'English' else 'id'
    except:
        hint = 'id'
    temp_text = Text(text, hint_language_code=hint)
    temp_pos_tag = temp_text.pos_tags
    chunk_parser = get_chunk_parser()
    temp_chunks = chunk_parser.parse(temp_pos_tag)
    return (temp_pos_tag, temp_chunks)


zones = [74001, 74002, 74003, 74004, 74005]

for zone in zones:
    with open(FILE.format(zone)) as f:
        all_data = []
        data = json.loads(f.read())
        for id, resto in data.items():
            keywords = resto.get('highlights')
            keywords.extend(resto.get('cuisines').split(', '))
            keywords.extend(resto.get('location').get('locality').split(' '))
            print(keywords)
            reviews = resto.get('reviews')
            for r in reviews:
                review = r.get('review_text')
                if not review:
                    continue
                pos, chunk = get_chunks(review)
                for p in pos:
                    word, pos = p
                    word_ok = len(word) > 2 and word.isalpha() and ',' not in word and\
                    '.' not in word and word.lower() not in STOPS
                    if pos in ['PROPN', 'NOUN'] and word_ok:
                        print(word)
                        keywords.append(word)
            keywords = [k.lower() for k in keywords]
            all_data.append({
                'res_id': int(id),
                'score': sorted(set(keywords))
            })
    with open('static/resto-score-{}.json'.format(zone), 'w') as h:
        h.write(json.dumps(all_data))
