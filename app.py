from flask import Flask
from flask import url_for, render_template, request, redirect
from func import sent_list
import func as f

app = Flask(__name__, static_folder='static')


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/result')
def output():
    if request.args:
        word = request.args['word']
        results = f.search_conllu_by_chain(word, None)
        output = [result[2] for result in results]
        if len(output) == 0:
            output.append(f'Ужас! Мы ничего не нашли по запросу "{word}" ')
        return render_template('output.html', output=output)
    return redirect(url_for('main'))

@app.route('/authors')
def authors():
    return render_template('authors.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
