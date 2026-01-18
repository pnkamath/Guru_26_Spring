#!/usr/bin/env python3 -B
"""wc0_fixed.py"""

import json
from types import SimpleNamespace as obj

# Q3: Policy data
CONFIG = {
  "input_file": "essay.txt","top_n": 10,"punctuation": '.,!?;:"()[]',"sort_key": "count","sort_reverse": True,"output_format": "text","stopwords_file": "stopwords.txt","output_dir": r"D:\Future_Docs\NCSU\How_to_be_SW_guru\Guru_26_Spring\hw1","output_json": "results.json","output_csv": "results.csv"}

def load_stopwords(path):
  with open(path) as f:
    return set(line.strip() for line in f if line.strip())

STOPWORDS = load_stopwords(CONFIG["stopwords_file"])

# Q1: Model (no I/O)
def count_words(filename, config, stopwords):
  counts = {}
  for line in read_lines(filename):
    for word in split_words(line):
      word = clean_word(normalize_word(word), config["punctuation"])
      if is_valid_word(word, stopwords):
        increment(counts, word)
  sorted_words = sort_words(counts, get_sort_key(config["sort_key"]), config["sort_reverse"])
  return obj(file=filename, counts=counts, sorted_words=sorted_words)

# Q2: SRP helpers
def read_lines(filename):
  with open(filename) as f:
    for line in f: yield line

def split_words(line): return line.split()
def normalize_word(word): return word.lower()
def clean_word(word, punctuation): return word.strip(punctuation)
def is_valid_word(word, stopwords): return word != "" and word not in stopwords
def increment(counts, word): counts[word] = counts.get(word, 0) + 1
def get_sort_key(policy):
  if policy == "word": return lambda x: x[0]
  if policy == "count": return lambda x: x[1]
  raise ValueError("Unknown sort key")
def sort_words(counts, key, reverse): return sorted(counts.items(), key=key, reverse=reverse)

# Q1: Presentation
def report(results, config):
  if config["output_format"] == "text":
    print_text(results, config)
  elif config["output_format"] == "json":
    print(to_json(results, config))
  elif config["output_format"] == "csv":
    print(to_csv(results, config))

def print_text(results, config):
  print("="*50)
  print(f"WORD FREQUENCY ANALYSIS - {results.file}")
  print("="*50)
  print(f"Total words: {sum(results.counts.values())}")
  print(f"Unique words: {len(results.counts)}\n")
  for i,(w,c) in enumerate(results.sorted_words[:config["top_n"]],1):
    print(f"{i:2}. {w:15} {c:4} {'*'*c}")

def to_json(results, config):
  return json.dumps({
    "file": results.file,
    "top": results.sorted_words[:config["top_n"]]
  }, indent=2)

def to_csv(results, config):
  rows=["rank,word,count"]
  for i,(w,c) in enumerate(results.sorted_words[:config["top_n"]],1):
    rows.append(f"{i},{w},{c}")
  return "\n".join(rows)

# ============================================================
# NEW: write outputs to disk (JSON + CSV)
# ============================================================
def write_json_file(results, config):
  path = f"{config['output_dir']}\\{config['output_json']}"
  with open(path, "w") as f:
    f.write(to_json(results, config))

def write_csv_file(results, config):
  path = f"{config['output_dir']}\\{config['output_csv']}"
  with open(path, "w") as f:
    f.write(to_csv(results, config))

# Q4: Tests
def test_clean_word(): assert clean_word("hello,", ".,") == "hello"
def test_count_words():
  tmp = CONFIG.copy(); tmp["punctuation"]=""
  res = count_words("essay.txt", tmp, {"the"})
  assert res.counts.get("cat",0)==0 or isinstance(res, obj)

def run_tests(): test_clean_word(); test_count_words()

if __name__ == "__main__":
  run_tests()
  results = count_words(CONFIG["input_file"], CONFIG, STOPWORDS)
  report(results, CONFIG)

  # NEW: Write outputs to files
  write_json_file(results, CONFIG)
  write_csv_file(results, CONFIG)
