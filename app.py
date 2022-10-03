import flask
import difflib

import pickle

movies1 = pickle.load(open('movie_list.pkl','rb'))
similarity1 = pickle.load(open('similarity.pkl','rb'))

app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
        list_of_all_titles = movies1['title'].tolist()
        
        

        list_of_all_titles = movies1['title'].tolist()

        find_close_match = difflib.get_close_matches(m_name, list_of_all_titles)

        close_match = find_close_match[0]

        index_of_the_movie = movies1[movies1.title == close_match]['index'].values[0]

        similarity_score = list(enumerate(similarity1[index_of_the_movie]))

        sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

        i = 1
        names = []
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movies1[movies1.index==index]['title'].values[0]
            if (i<10):
                names.append(title_from_index)
            i+=1
        return flask.render_template('found.html',movie_names=names,search_name=m_name)

if __name__ == '__main__':
    app.run()