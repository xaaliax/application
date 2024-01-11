# the following need to be imported for the application to work
from flask import Flask, request
import gensim 

app = Flask(__name__)

html_form_with_message = '''
<!DOCTYPE html>
<html>
<head>
<title>Opposite Word App</title>
</head>
<body>
    <h2>Enter Word</h2>
    <form method="post" action="/">
        <label for="text">Text:</label><br>
        <input type="text" name="my_input_value"><br><br>
        <input type="submit" value="Enter">
    </form>
    <p>The opposite word: input_word</p>
</body>
</html>
'''

def opposite(word): # define a function with the previous method for the backend of the application
    model = gensim.models.Word2Vec.load("./model_app") # this model needs go be saved in the local folder to be able to fetch it
    reference_pair = ("good", "bad")

    target_word = str(word)

    result_vector = model.wv[target_word] - model.wv[reference_pair[0]] + model.wv[reference_pair[1]]
    opposite_words = model.wv.similar_by_vector(result_vector)

    return opposite_words[0][0] # only return one of the results, otherwise the app will return and error

@app.route('/', methods=['GET', 'POST'])
def home():
    user_input = ""
    opposite_w = ""
    if request.method == 'POST':
        user_input = request.form['my_input_value']
        opposite_w = opposite(user_input)

    return html_form_with_message.replace("input_word", opposite_w) # print the output and show it to the user

app.run()