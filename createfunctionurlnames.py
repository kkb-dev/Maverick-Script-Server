# convert function names into numerical url

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
           'n','o','p','q','r','s','t','u','v','w','x','y','z']

words = ['killaddmac',
         'killaddssid',
         'killremovemac',
         'killremovessid',
         'launchscripts',
         'getcontmac',
         'getcontssid',
         ]

for word in words:
    numword = ''
    word1 = list(word)
    for letter in word1:
        letter = letters.index(letter)
        numword = str(numword) + str(letter)
    print(word)    
    print((numword[::-1])[0:15])


