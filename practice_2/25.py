words = ["apple","lime","orange", "cherry", "date", "fig"]
for w in words:
    if "a" not in w:
        continue          # skip words without 'a'
    if w.startswith("d"):
        break             # stop if word starts with 'd'
    print(w)