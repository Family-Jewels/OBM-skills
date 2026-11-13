def chunk(items, n):
    out = []
    i = 0
    while i < len(items):
        out.append(items[i:i + n])
        i += n
    return out
