from solution import slugify
def test_hello_spec(): assert slugify("Hello World") == "hello-world"
def test_more(): assert slugify("Good Morning All") == "good-morning-all"
