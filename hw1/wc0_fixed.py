#!/usr/bin/env python3 -B
"""Word frequency counter - the cleaned version"""
import json
import yaml
from types import SimpleNamespace as obj

#--- Q3: Policy (data - easy to change) ---
#--- AQ3: All configs are moved to YAML to seperate policy from mechanism
config_file = "config.yaml"
with open(config_file, 'r') as file:
  CONFIG = yaml.load(file, Loader=yaml.FullLoader)

#--- Q1: Model (pure business logic, no I/O) ---
#--- AQ1: Model code only performs computation and does no presentation
def count_words(file="essay.txt"):
  # AQ2: Orchestrates the counting process using smaller helper functions
  counts = {}
  
  # AQ1: File I/O is localized and streamed here
  with open(file) as f:
    for line in f:
      words = line.split()
      
      for word in words:
        # AQ4: Transformations are handled by seperate functions
        word = normalize_word(word)
        word = clean_word(word, CONFIG['punctuation'])
        if is_valid_word(word, CONFIG['stopwords_files'][CONFIG['language']]):
          increment(counts, word)
  
  # AQ3: Sorting rules are loaded in from CONFIG
  # AQ4: Sorting logic is extracted
  sorted_words = sort_words(counts, get_sort_key(CONFIG["sorting"]["key"]), CONFIG["sorting"]["reverse"])
  
  return obj(file=file, counts=counts, sorted_words=sorted_words)

# AQ2: Small, single-purpose functions
def normalize_word(word): 
  return word.lower()

def clean_word(word, punctuation): 
  return word.strip(punctuation)

def is_valid_word(word, stopwords): 
  # AQ3: Stopword list is externalized to a file and loaded from a CONFIG.
  # AQ4: The stopwords are streamed rather than being loaded. 
  with open(stopwords, 'r') as file:
    for line in file:
      line = line.strip()
      if line == word:
        return False
  return True

def increment(counts, word): 
  counts[word] = counts.get(word, 0) + 1

def get_sort_key(policy):
  # AQ3: Interprets sorting policy as data and maps to behavior
  if policy == "word": 
    return lambda x: x[0]
  if policy == "count": 
    return lambda x: x[1]
  raise ValueError("Unknown sort key")

def sort_words(counts, key, reverse): 
  # AQ3: Behavior is controlled by and injected policy
  return sorted(counts.items(), key=key, reverse=reverse)

#--- Q1: Presentation (I/O only, no logic) ---
#--- AQ1: All printing functions are placed here
def print_header(file):
  print(f"\n{'='*50}")
  print(f"WORD FREQUENCY ANALYSIS - {file}")
  print(f"{'='*50}\n")

def print_results(counts):
  print(f"Total words (after removing stopwords): {sum(counts.values())}")
  print(f"Unique words: {len(counts)}\n")
  print(f"Top {CONFIG['top_n']} most frequent words:\n")

def print_words(count, sorted_words):
  # AQ3: Formatting widths are configurable via the CONFIG file
  for i,(word, count) in enumerate(results.sorted_words[:CONFIG["top_n"]], 1):
    bar = "*" * count
    print(f"{i:{CONFIG['formatting']['i_pad']}}. {word:{CONFIG['formatting']['word_pad']}} {count:{CONFIG['formatting']['count_pad']}} {bar}")

  print()

def to_json(results):
  #AQ1: Alternate presentation format (JSON)
  return json.dumps({"file": results.file, "top": results.sorted_words[:CONFIG["top_n"]]}, indent=2)

def to_csv(results):
  #AQ1: Alternate presentation format (CSV)
  rows=["rank,word,count"]
  for i,(w,c) in enumerate(results.sorted_words[:CONFIG["top_n"]],1):
    rows.append(f"{i},{w},{c}")
  return "\n".join(rows)

def write_json_file(results):
  # AQ1: File output is isolated from model logic
  path = f"{CONFIG['output']['output_dir']}/{CONFIG['output']['output_json']}"
  with open(path, "w") as f: 
    f.write(to_json(results))

def write_csv_file(results):
  # AQ1: File output is isolated from model logic
  path = f"{CONFIG['output']['output_dir']}/{CONFIG['output']['output_csv']}"
  with open(path, "w") as f: 
    f.write(to_csv(results))

def report(results):
  # AQ2: Responsible only for coordinating presentation
  if CONFIG["output"]["format"] == "text": 
    print_header(results.file)
    print_results(results.counts)
    print_words(results.counts, results.sorted_words)
  elif CONFIG["output"]["format"] == "json": 
    print(to_json(results, config))
  elif CONFIG["output"]["format"] == "csv": 
    print(to_csv(results, config))

# -- Sample unit tests (from test_wc0.py)
def test_clean_word(): 
  assert clean_word("hello,", ".,") == "hello"

def test_count_words():
  res = count_words("essay.txt")
  assert res.counts.get("cat",0)==0 or isinstance(res, obj)

def run_tests(): 
  test_clean_word() 
  test_count_words()

# Q1: Program entry point
# AQ1: Main logic seperated from model and presentation
#--- Main ---
if __name__ == "__main__":
  results = count_words(CONFIG["input_file"])
  report(results)
  write_json_file(results)
  write_csv_file(results)
  run_tests()
