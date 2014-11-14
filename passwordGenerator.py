from flask import Flask, request, make_response
app = Flask(__name__)
app.debug = True
import random

@app.route('/')
def password_form():
    if 'pwordLength' in request.args:
        return sendPage(request.args)
    else:
        return sendForm()

def sendForm():
    return '''
    <html>
      <body>
         <h2>Create a Password</h2>
          <form method='get'>
              <label for="pwordLength">Password Length Limit</label>
              <input id="pwordLength" type="text" name="pwordLength" value="0" /><br></br>
              <label for="upperLimit">All words are shorter than</label>
              <input id="upperLimit" type="text" name="upperLimit" value="0"/><br></br>
              <label for="lowerLimit">All words are longer than</label>
              <input id="lowerLimit" type="text" name="lowerLimit" value="0"><br></br>
              <label for="optimize">Optimize For Typing Speed</label>
              <input id="optimize" type="checkbox" name="optimize"/><br></br>
              <label for="eSub">Replace "e" with "3"</label>
              <input id="eSub" type="checkbox" name="eSub"/><br></br>
              <label for="oSub">Replace "o" with "0"</label>
              <input id="oSub" type="checkbox" name="oSub"/><br></br>
              <label for="iSub">Replace "i" with "1"</label>
              <input id="iSub" type="checkbox" name="iSub"/><br></br>
              <label for="sSub">Replace "s" with "5"</label>
              <input id="sSub" type="checkbox" name="sSub"/><br></br>
              <label for="cap1">Capitalize First Word</label>
              <input id="cap1" type="checkbox" name="cap1"/><br></br>
              <label for="cap2">Capitalize Second Word</label>
              <input id="cap2" type="checkbox" name="cap2"/><br></br>
              <label for="cap3">Capitalize Third Word</label>
              <input id="cap3" type="checkbox" name="cap3"/><br></br>
              <label for="cap4">Capitalize Fourth Word</label>
              <input id="cap4" type="checkbox" name="cap4"/><br></br>
              <input type="submit">
          </form>
      </body>
    </html>
    '''
def getWord(wordList, currentLength, maxLength, upper, lower, optimize, e, i, o, s):
    word = ""
    random.seed()
    place = random.randrange(0, len(wordList))
    word = wordList[place]
    

    
    while not((len(word) <= upper + 4) and (len(word) >= lower + 4) and ((currentLength + len(word)) <= maxLength)):
        place = random.randrange(0, len(wordList))
        word = wordList[place]

    if e or i or o or s:
        word = replaceLetters(word, e, i, o, s)

    if optimize:
        if speedScore(word) <= (len(word) // 2):
            word = getWord(wordList, currentLength, maxLength, upper, lower, optimize, e, i, o, s)
    
    return word

def speedScore(word):
    left = '1qQAaZz2WwSsXx3EeDdCc4RrFfVv5TtGgBb'
    right = '6YyHhNn7UuJjMm8IiKk9OoLl0Pp'
    score = 0
    
    p = 0
    c = 1
    
    for c in range(1, len(word)):
        prev = word[p]
        curr = word[c]
        
        if (prev in left and curr in right) or (prev in right and curr in left) or (prev == curr):
            score += 1
            if prev == curr:
                score += 1
             
        p = c
        
    return score
        
    
def generatePasswords(length, lower, upper, optimize, cap1, cap2, cap3, cap4, eSub, iSub, oSub, sSub):
    wordFile = open('5000 words.txt', 'r')
    words = []
    numPasswords = 10
    numWords = 4
    password = ""
    passwords = []
    
    for line in wordFile:
        words.append(line)
        
    for i in range(0, numPasswords):
        password = ""
        tempList = []
        for j in range(0, numWords):
            word = getWord(words, len(password), length, upper, lower, optimize, eSub, iSub, oSub, sSub)

            if (j == 0 and cap1 == True) or (j == 1 and cap2 == True) or (j == 2 and cap3 == True) or (j == 3 and cap4 == True):
                word = word.upper()

            else:
                password += word
            j += 1
        passwords.append(password)
        i+= 1

    wordFile.close()
 
    return passwords
    
def replaceLetters(word, eSub, oSub, iSub, sSub):
    if eSub:
        word = word.replace('e', '3')
        word = word.replace('E', '3')
    if oSub:
        word = word.replace('o', '0')
        word = word.replace('O', '0')
    if iSub:
        word = word.replace('i', '1')
        word = word.replace('I', '1')
    if sSub:
        word = word.replace('s', '5')
        word = word.replace('S', '5')
    return word
    
def sendPage(options):
    optimize = underScore = cap1 = cap2 = cap3 = cap4 = eSub = oSub = iSub = sSub = False
    
    if 'optimize' in options:
        optimize = True
        
    if 'cap1' in options:
        cap1 = True
    
    if 'cap2'in options:
        cap2 = True
        
    if 'cap3' in options:
        cap3 = True
        
    if 'cap4' in options:
        cap4 = True
        
    if 'eSub' in options:
        eSub = True
        
    if 'oSub' in options:
        oSub = True
        
    if 'iSub' in options:
        iSub = True
        
    if 'sSub' in options:
        sSub = True
        
    list = generatePasswords(int(options['pwordLength']), int(options['lowerLimit']), int(options['upperLimit']), optimize, cap1, cap2, cap3, cap4, eSub, oSub, iSub, sSub)
    
    return '''
    <html>
      <body>
        <h1>Possible Passwords:</h1>
        <ul><li>{0}</li>
        <li>{1}</li>
        <li>{2}</li>
        <li>{3}</li>
        <li>{4}</li>
        <li>{5}</li>
        <li>{6}</li>
        <li>{7}</li>
        <li>{8}</li>
        <li>{9}</li>
        </ul>
      </body>
    </html>
    '''.format(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9])

if __name__ == '__main__':
   app.run()
