from solution import slugify
def test_basic():      assert slugify("Foo Bar Baz") == "foo-bar-baz"
def test_punct():      assert slugify("It's 5 o'clock!") == "its-5-oclock"
def test_spaces():     assert slugify("  many   spaces ") == "many-spaces"
def test_hello():      assert slugify("Hello World") == "hello_world"
def test_digits():     assert slugify("Route 66") == "route-66"
