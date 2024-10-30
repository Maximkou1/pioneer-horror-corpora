from io import open
from conllu import parse_incr

import spacy

import re

nlp = spacy.load('ru_core_news_sm')


data_file = open("/Users/polinaegorova/уеба/nlp/pythonProject/conllu_stories.conllu", "r", encoding="utf-8")
sent_list = [tokenlist for tokenlist in parse_incr(data_file)]





def parse_query(query):
    """Разбирает запрос и возвращает список условий для поиска."""
    conditions = []
    query_parts = query.split()
    for part in query_parts:
        if part.startswith('"') and part.endswith('"'):
            # Лемма в кавычках
            form = part.strip('"')
            conditions.append({"form": form})
        elif part.isupper():
            # Часть речи
            upos = part
            conditions.append({"upos": upos})
        elif "+" in part:
            lemma, upos = part.split("+")
            conditions.append({"lemma": lemma, "upos": upos})
        else:
            # Слово в любой форме
            lemma = nlp(part)[0].lemma_
            conditions.append({"lemma": lemma})
    return conditions

def search_conllu_by_chain( query, conllu_text=None):
    conditions = parse_query(query)
    results = []

    for sentence in sent_list:
      text_title, sent_id, text = list(sentence.metadata.values())
      for i in range(len(sentence) - len(conditions) + 1):
          match = True
          for j, condition in enumerate(conditions):
              token = sentence[i + j]

              # Проверяем соответствие каждому условию
              if "lemma" in condition and token.get("lemma") != condition["lemma"]:
                  match = False
                  break
              if "upos" in condition and token.get("upostag") != condition["upos"]:
                  match = False
                  break
              if "form" in condition and token.get("form") != condition["form"]:
                  match = False
                  break

          if match:
              # Сохраняем предложение и слова, соответствующие цепочке
              matched_tokens = [(token.get("form"), token.get("lemma"), token.get("upostag")) for token in sentence[i:i + len(conditions)]]
              results.append((text_title, sent_id, text, matched_tokens))

    return results
query = 'мама'
result = search_conllu_by_chain(query)
print(result)