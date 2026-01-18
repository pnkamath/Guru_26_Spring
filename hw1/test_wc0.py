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

def test_clean_word():
    assert clean_word("hello,", ".,") == "hello"

def test_count_words():
    tmp_file = "tmp_test.txt"
    with open(tmp_file, "w") as f:
        f.write("the cat and the dog\n")

    tmp_config = CONFIG.copy()
    tmp_config["punctuation"] = ""
    stopwords = {"the"}

    res = count_words(tmp_file, tmp_config, stopwords)
    assert res.counts == {"cat": 1, "and": 1, "dog": 1}

    os.remove(tmp_file)

def test_to_json():
    res = obj(file="x", counts={"a":1}, sorted_words=[("a",1)])
    tmp_config = CONFIG.copy()
    tmp_config["top_n"] = 1

    json_output = to_json(res, tmp_config)
    parsed = json.loads(json_output)

    assert parsed["file"] == "x"
    assert parsed["top"] == [["a", 1]]

def test_to_csv():
    res = obj(file="x", counts={"a":1}, sorted_words=[("a",1)])
    tmp_config = CONFIG.copy()
    tmp_config["top_n"] = 1

    csv_output = to_csv(res, tmp_config)
    assert "rank,word,count" in csv_output
    assert "1,a,1" in csv_output

def test_report_text_output(capsys):
    res = obj(file="x", counts={"a":1}, sorted_words=[("a",1)])
    tmp_config = CONFIG.copy()
    tmp_config["output_format"] = "text"
    tmp_config["top_n"] = 1

    report(res, tmp_config)
    captured = capsys.readouterr()

    assert "WORD FREQUENCY ANALYSIS" in captured.out
    assert "Total words" in captured.out

def test_report_json_output(capsys):
    res = obj(file="x", counts={"a":1}, sorted_words=[("a",1)])
    tmp_config = CONFIG.copy()
    tmp_config["output_format"] = "json"
    tmp_config["top_n"] = 1

    report(res, tmp_config)
    captured = capsys.readouterr()

    assert '"file": "x"' in captured.out

def test_report_csv_output(capsys):
    res = obj(file="x", counts={"a":1}, sorted_words=[("a",1)])
    tmp_config = CONFIG.copy()
    tmp_config["output_format"] = "csv"
    tmp_config["top_n"] = 1

    report(res, tmp_config)
    captured = capsys.readouterr()

    assert "rank,word,count" in captured.out

if __name__ == "__main__":
    test_clean_word()
    test_count_words()
    test_to_json()
    test_to_csv()
    test_report_text_output()
    test_report_json_output()
    test_report_csv_output()
    print("All tests passed!")
