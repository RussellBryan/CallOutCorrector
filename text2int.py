def text2int(textnum, numwords={}):
    if not numwords:
        units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                 "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                 "sixteen", "seventeen", "eighteen", "nineteen"]

        tens = ["", "", "twenty", "thirty", "forty",
                "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = count = 0
    end = ''
    for word in textnum.split():
        if 'percent' in textnum.split():
            end = ' %'
        elif 'feet' in textnum.split():
            end = ' ft'

        count += 1
        if word in numwords:
            scale, increment = numwords[word]
            if count != len(textnum.split()):  # If there is a next word
                nextword = textnum.split()[count]
                if nextword in numwords:  # And its a number
                    nextscale, nextincrement = numwords[nextword]
                    # is it larger than the first number
                    if nextincrement > 10 and nextincrement != 0:
                        increment = increment * 100

            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
    return str(result + current) + end
