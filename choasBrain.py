import tensorflow
import string
from random import randint
from numpy import array
from pickle import dump, load 
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.preprocessing.sequence import pad_sequences

def readText(filename):
    file = open(filename, "r")
    text = file.read()
    file.close()
    return text

def cleanText(text):
    text = text.replace('--',' ')
    text = text.replace('-', '')     
    comments = text.split('\n')
    table = str.maketrans('', '', string.punctuation)
    comments = [c.translate(table) for c in comments]     
    comments = [c.lower() for c in comments]
    comments = comments[:10000]
    return comments

def makeInputLines(comment, sequence):
    words = comment.split()
    length = 8
    if (len(words) > 9):
        for i in range(length, len(words) + 1):
            seq = words[i-length:i]
            line = ' '.join(seq)
            sequence.append(line)    
    return

def trainModel(input):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(input)
    intInputLines = tokenizer.texts_to_sequences(input)
    
    vocab_size = len(tokenizer.word_index) + 1
    
    intInputLines = array(intInputLines)
    x, y = intInputLines[:,:-1], intInputLines[:,-1]
    y = to_categorical(y, num_classes=vocab_size)
    input_length = x.shape[1]
    
    # define model
    model = Sequential()
    model.add(Embedding(vocab_size, 50, input_length=input_length))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(vocab_size, activation='softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x, y, batch_size=128, epochs=100)
    
    model.save('model.h5')
    dump(tokenizer, open('tokenizer.pkl', 'wb'))
    return
          
def predictText(sequence, predictionLength):
    model = load_model('model.h5')
    tokenizer = load(open('tokenizer.pkl', 'rb'))
    seq_length = len(sequence[0].split()) - 1
    
    seed_text = sequence[randint(0, len(sequence))]
    print(seed_text + '\n')
    
    result = list()
    for _ in range(predictionLength):
        encoded = tokenizer.texts_to_sequences([seed_text])[0]
        encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
        yhat = model.predict_classes(encoded, verbose=0)
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
            
        seed_text += ' ' + out_word
        result.append(out_word)
     
    generated = ' '.join(result)
    print(generated + '\n')


def main():    
    comments = cleanText(readText('master.txt'))
    
    inputLines = list()
    
    for comment in comments:
        makeInputLines(comment, inputLines)

    trainModel(inputLines)
    #predictText(inputLines, 30)
 
main()
