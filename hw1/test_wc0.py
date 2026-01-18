import os
from wc0_fixed import clean_word, count_words, CONFIG, obj

def test_clean_word():
    assert clean_word("hello,", ".,") == "hello"

def test_count_words():
    # Create a temporary file
    tmp_file = "tmp_test.txt"
    with open(tmp_file, "w") as f:
        f.write("the cat and the dog\n")

    tmp_config = CONFIG.copy()
    tmp_config["punctuation"] = ""

    # stopwords set for this test
    stopwords = {"the"}

    res = count_words(tmp_file, tmp_config, stopwords)

    # Expected result
    assert res.counts == {"cat": 1, "and": 1, "dog": 1}

    # Clean up
    os.remove(tmp_file)

if __name__ == "__main__":
    test_clean_word()
    test_count_words()
    print("All tests passed!")
