from data.greetings import say_hello_to

def test_say_hello_appends_name():
    assert say_hello_to("world") == "hello world"