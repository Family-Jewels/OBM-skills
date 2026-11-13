from slug import slugify

def test_lower(): assert slugify("Hello") == "hello"
def test_spaces(): assert slugify("a  b") == "a-b"
def test_punct(): assert slugify("a, b & c!") == "a-b-c"
def test_edges(): assert slugify("  --Hi--  ") == "hi"
def test_empty(): assert slugify("") == ""
