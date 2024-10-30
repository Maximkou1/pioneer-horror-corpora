from flask import Flask
from flask import url_for, render_template, request, redirect
from func import sent_list
import func as f

app = Flask(__name__, static_folder='static')


@app.route('/') #главная страница
def main():
    return render_template('main.html')


@app.route('/search') #страница о правилах поиска
def search():
    return render_template('search.html')


@app.route('/result') #страница результатов поиска
def output():
    if request.args:
        word = request.args['word']
        results = f.search_conllu_by_chain(word, None) #применяем к полученному слову функцию поиска 
        output = [result[2] for result in results] #выводим предложение
        if len(output) == 0: #если ничего не нашлось
            output.append(f'Ужас! Мы ничего не нашли по запросу "{word}" ')
        return render_template('output.html', output=output)
    return redirect(url_for('main'))

@app.route('/authors') #страница об авторах
def authors():
    return render_template('authors.html')

@app.route('/about') #страница о проекте
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
