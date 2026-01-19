import os
import json
from wc0_fixed import (
    clean_word,
    count_words,
    to_json,
    to_csv,
    report,
    CONFIG,
    obj
)

class ConfigOverride:
    def __init__(self, **kwargs):
        self.overrides = kwargs
        self.originals = {}

    def __enter__(self):
        for key, value in self.overrides.items():
            self.originals[key] = CONFIG[key]
            CONFIG[key] = value

    def __exit__(self, exc_type, exc, tb):
        for key, value in self.originals.items():
            CONFIG[key] = value


def test_clean_word():
    assert clean_word("hello,", ".,") == "hello"

def test_count_words():
    tmp_file = "tmp_test.txt"
    tmp_stopwords = "tmp_stopwords.txt"

    with open(tmp_file, "w") as f:
        f.write("the cat and the dog\n")

    with open(tmp_stopwords, "w") as f:
        f.write("the\nand\n")

    with ConfigOverride(
        stopwords_files={"english": tmp_stopwords},
        language="english"
    ):
        res = count_words(tmp_file)
        assert res.counts == {"cat": 1, "dog": 1}

    os.remove(tmp_file)
    os.remove(tmp_stopwords)

def test_to_json():
    with ConfigOverride(top_n=1):
        res = obj(file="x", counts={"a": 1}, sorted_words=[("a", 1)])
        json_output = to_json(res)
        parsed = json.loads(json_output)

        assert parsed["file"] == "x"
        assert parsed["top"] == [["a", 1]]

def test_to_csv():
    with ConfigOverride(top_n=1):
        res = obj(file="x", counts={"a": 1}, sorted_words=[("a", 1)])
        csv_output = to_csv(res)

        assert "rank,word,count" in csv_output
        assert "1,a,1" in csv_output

if __name__ == "__main__":
    test_clean_word()
    test_count_words()
    test_to_json()
    test_to_csv()
    print("All tests passed!")

