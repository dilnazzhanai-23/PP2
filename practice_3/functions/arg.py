def func(greeting, *names):
    for name in names:
        print(greeting, name)

func("Hello", "Emil", "Tobias", "Linus") 