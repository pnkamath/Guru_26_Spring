#!/usr/bin/env python3 -B
"""Word frequency counter - the messy version"""
from types import SimpleNamespace as obj

top_n = 10
stopwords = ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "is", "was", "are", "were", "be", "been", "with"]
punctuation = '.,!?;:"()[]'
             
#--- Model (pure business logic, no I/O) ---
def count_words(file="essay.txt"):
  """One big function doing everything"""
  counts = {}

  with open(file) as f:
    for line in f:
      words = line.split()
  
      for word in words:
        word = normalize_word(word)
        word = clean_word(word, punctuation)
        if is_valid_word(word, stopwords):
          increment(counts, word)
  
  # VIOLATION 4: Sort and filter inline
  sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)

  return obj(file=file, counts=counts, sorted_words=sorted_words)

def normalize_word(word):
  return word.lower()

def clean_word(word, punctuation):
  return word.strip(punctuation)

def is_valid_word(word, stopwords):
  return word != "" and word not in stopwords

def increment(counts, word):
    counts[word] = counts.get(word, 0) + 1

#--- Presentation (I/O only, no logic) ---    
def print_header(file):
  # VIOLATION 2: Print mixed with processing
  print(f"\n{'='*50}")
  print(f"WORD FREQUENCY ANALYSIS - {file}")
  print(f"{'='*50}\n")

def print_results(counts):
  # VIOLATION 5: Print results mixed with computation
  print(f"Total words (after removing stopwords): {sum(counts.values())}")
  print(f"Unique words: {len(counts)}\n")
  print(f"Top {top_n} most frequent words:\n")
  
def print_words(count, sorted_words):
  # VIOLATION 6: Hardcoded formatting
  for i, (word, count) in enumerate(sorted_words[:top_n], 1):
    bar = "*" * count
    print(f"{i:2}. {word:15} {count:3} {bar}")
  
  print()

def report(results):
  print_header(results.file)
  print_results(results.counts)
  print_words(results.counts, results.sorted_words)

#--- Main ---
results = count_words("essay.txt")
report(results)
