import omdb
import imdb
import populate_utils
import json

import rdflib
g = rdflib.Graph()
g.parse("movies_project.owl")

iri = "https://schema.org/"


def get_movies(n):
    ids = imdb.get_top250_ids()[:n]
    movies_list = []
    for id in ids:
        movie = json.loads(omdb.get_one_film(id))
        movies_list.append(movie)
    return movies_list

def populate_one_movie(movie_dict, graph):

    movie_title = movie_dict['Title']
    sparql = f"""SELECT ?a 
    WHERE {{ ?a  <{iri}mytitle> \"{movie_title}\" }}"""
    res = graph.query(sparql)
    if len(res) != 0: # Cannot Create a movie that already exists
        return
    
    populate_utils.create_movie(title=movie_dict['Title'], year=int(movie_dict['Year']),poster=movie_dict['Poster'],plot=movie_dict['Plot'],graph=graph)

    movie_id = '_'.join(movie_dict['Title'].lower().split())
    
    # ACTORS
    actors_list = [name.strip() for name in movie_dict['Actors'].split(',')]
    for actor in actors_list:
        # Check if exists
        sparql = f"""SELECT ?a 
        WHERE {{ ?a  <{iri}myname> \"{actor}\" }}"""
        res = g.query(sparql)
        if len(res) == 0:
            # Create
            populate_utils.create_person(actor, graph=graph)


        actor_id = '_'.join(actor.lower().split())
        populate_utils.insert_isActorOf(movie_id=movie_id, actor_id=actor_id, graph=graph)

    # DIRECTORS
    directors_list = [name.strip() for name in movie_dict['Director'].split(',')]
    for director in directors_list:
        # Check if exists
        sparql = f"""SELECT ?a 
        WHERE {{ ?a  <{iri}myname> \"{director}\" }}"""
        res = g.query(sparql)
        if len(res) == 0:
            # Create
            populate_utils.create_person(director, graph=graph)


        director_id = '_'.join(director.lower().split())
        populate_utils.insert_isDirectorOf(movie_id=movie_id, director_id=director_id, graph=graph)

    # WRITERS
    writers_list = [name.strip() for name in movie_dict['Writer'].split(',')]
    for writer in writers_list:
        # Check if exists
        sparql = f"""SELECT ?a 
        WHERE {{ ?a  <{iri}myname> \"{writer}\" }}"""
        res = g.query(sparql)
        if len(res) == 0:
            # Create
            populate_utils.create_person(writer,graph=graph)


        writer_id = '_'.join(writer.lower().split())
        populate_utils.insert_isWriterOf(movie_id=movie_id, writer_id=writer_id,graph=graph)

    # GENRES
    genres_list = [name.strip() for name in movie_dict['Genre'].split(',')]
    for genre in genres_list:
        if genre not in ['Drama', 'Thriller', 'Action', 'Crime', 'Comedy']:
            continue
        populate_utils.insert_hasGenre(movie_id=movie_id, genre=genre,graph=graph)

if __name__ == '__main__':

    N = 250

    movies = get_movies(N)

    for n in range(N):
        print(n)
        populate_one_movie(movies[n], g)

    g.serialize("movies_project.owl", format="xml")