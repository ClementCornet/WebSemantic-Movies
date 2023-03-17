import streamlit as st

import rdflib
g = rdflib.Graph()
g.parse("movies_project.owl")

from streamlit_option_menu import option_menu as om

iri = "https://schema.org/"


# Currently not workin since update to agraph 2.0 - work in progress
from rdflib import Graph
from streamlit_agraph import TripleStore, agraph
from streamlit_agraph.config import Config, ConfigBuilder
from streamlit_agraph import agraph, Node, Edge, Config



def graph_person(actor_name):

    edges_colors = {
        "actor": "#fcba03",
        "director": "#03fc41",
        "writer": "#7303fc",
    }
    nodes = []
    edges = []

    name_id = '_'.join(actor_name.lower().split())
    #sparql_base_photo = f"""SELECT ?pic
    #        WHERE {{ <{iri}{name_id}> <{iri}myphoto> ?pic .
    #        BIND (datatype(?pic) AS ?string) . }}"""
    #res = g.query(sparql_base_photo)
    #if len(res) != 0:
    #    for row in res:
    #        nodes.append(Node(id=name_id,title=actor_name,size=25,shape="circularImage",image=row.pic))
    #        break
    #else:
    #    nodes.append(Node(id=name_id,title=actor_name,size=25))

    people = [f"{iri}{name_id}"]
    #st.write(f" A LA BASE\t{people[0]}")
    movies_list = []
    actor_in = []
    writer_in = []
    director_in = []

    sparql_actor = f"""SELECT ?movie
        WHERE {{ <{iri}{name_id}> <{iri}isActor> ?movie }}"""
    res = g.query(sparql_actor)
    for row in res:
        actor_in.append(row.movie)
    sparql_writer = f"""SELECT ?movie
        WHERE {{ <{iri}{name_id}> <{iri}isWriter> ?movie }}"""
    res = g.query(sparql_writer)
    for row in res:
        writer_in.append(row.movie)
    sparql_director = f"""SELECT ?movie
        WHERE {{ <{iri}{name_id}> <{iri}isDirector> ?movie }}"""
    res = g.query(sparql_director)
    for row in res:
        director_in.append(row.movie)

    for movie in actor_in:
        sparql_movie = f"""SELECT ?p ?t
            WHERE {{ 
                <{movie}> <{iri}myposter> ?p .
                BIND (datatype(?p) AS ?string) .
                <{movie}> <{iri}mytitle> ?t .
                BIND (datatype(?t) AS ?string)
                }}"""
        #st.write(sparql_movie)
        res = g.query(sparql_movie)
        for row in res:
            #st.write(row)
            movies_list.append(movie)
            nodes.append(Node(id=movie,title=row.t,image=row.p,size=25,shape="image"))
            edges.append(Edge(source=name_id,target=movie,label="Actor",color=edges_colors['actor']))
    for movie in writer_in:
        sparql_movie = f"""SELECT ?p ?t
            WHERE {{ 
                <{movie}> <{iri}myposter> ?p .
                BIND (datatype(?p) AS ?string) .
                <{movie}> <{iri}mytitle> ?t .
                BIND (datatype(?t) AS ?string)
                }}"""
        #st.write(sparql_movie)
        res = g.query(sparql_movie)
        for row in res:
            #st.write(row)
            if movie not in movies_list:
                movies_list.append(movie)
                nodes.append(Node(id=movie,title=row.t,image=row.p,size=25,shape="image"))
            edges.append(Edge(source=name_id,target=movie,label="Writer",color=edges_colors['writer']))
    for movie in director_in:
        sparql_movie = f"""SELECT ?p ?t
            WHERE {{ 
                <{movie}> <{iri}myposter> ?p .
                BIND (datatype(?p) AS ?string) .
                <{movie}> <{iri}mytitle> ?t .
                BIND (datatype(?t) AS ?string)
                }}"""
        #st.write(sparql_movie)
        res = g.query(sparql_movie)
        for row in res:
            #st.write(row)
            if movie not in movies_list:
                movies_list.append(movie)
                nodes.append(Node(id=movie,title=row.t,image=row.p,size=25,shape="image"))
            edges.append(Edge(source=name_id,target=movie,label="Director",color=edges_colors['director']))


    for movie in movies_list:
        # GET ACTORS
        sparql_actor = f"""SELECT ?id ?name ?pic
                    WHERE {{
                        <{movie}> <{iri}hasActor> ?id .
                        ?id <{iri}myname> ?name .
                        OPTIONAL {{ ?id <{iri}myphoto> ?pic }}
                    }}"""
        res = g.query(sparql_actor)
        # FOR EACH ACTOR
        for row in res:
            # IF P NOT IN PEOPLE (la liste) -> CREATE NODE
            if row.id not in people:
                people.append(row.id)
                #st.write(f"iD DANS LA BOUCLE : {row.id}, {people[0] == row.id}")
                if row.pic is not None:
                    nodes.append(Node(id=row.id,label=row.name, shape="circularImage", image=row.pic))
                else:
                    nodes.append(Node(id=row.id,label=row.name))
            # CREATE EDGE
            edges.append(Edge(source=row.id,target=movie,label='Actor',color=edges_colors['actor']))

        # GET DIRECTORS
        sparql_actor = f"""SELECT ?id ?name ?pic
                    WHERE {{
                        <{movie}> <{iri}hasDirector> ?id .
                        ?id <{iri}myname> ?name .
                        OPTIONAL {{ ?id <{iri}myphoto> ?pic }}
                    }}"""
        res = g.query(sparql_actor)
        # FOR EACH DIRECOR
        for row in res:
            # IF P NOT IN PEOPLE (la liste) -> CREATE NODE
            if row.id not in people:
                people.append(row.id)
                #st.write(f"iD DANS LA BOUCLE : {row.id}, {people[0] == row.id}")
                if row.pic is not None:
                    nodes.append(Node(id=row.id,label=row.name, shape="circularImage", image=row.pic))
                else:
                    nodes.append(Node(id=row.id,label=row.name))
            # CREATE EDGE
            edges.append(Edge(source=row.id,target=movie,label='Director',color=edges_colors['director']))

        # GET WRITERS
        sparql_actor = f"""SELECT ?id ?name ?pic
                    WHERE {{
                        <{movie}> <{iri}hasWriter> ?id .
                        ?id <{iri}myname> ?name .
                        OPTIONAL {{ ?id <{iri}myphoto> ?pic }}
                    }}"""
        res = g.query(sparql_actor)
        # FOR EACH WRITER
        for row in res:
            # IF P NOT IN PEOPLE (la liste) -> CREATE NODE
            if row.id not in people:
                people.append(row.id)
                #st.write(f"iD DANS LA BOUCLE : {row.id}, {people[0] == row.id}")
                if row.pic is not None:
                    nodes.append(Node(id=row.id,label=row.name, shape="circularImage", image=row.pic))
                else:
                    nodes.append(Node(id=row.id,label=row.name))
            # CREATE EDGE
            edges.append(Edge(source=row.id,target=movie,label=str('Writer'),color=edges_colors['writer']))
        # GET WRITERS
        # FOR EACH WRITER
            # IF P NOT IN PEOPLE (la liste) -> CREATE NODE
            # CREATE EDGE
        pass


    #config = Config(width=750,height=950,directed=True, physics=True, hierarchical=False)
    config=Config()

    agraph(nodes=nodes, 
                edges=edges, 
                config=config)



def movie_box(movie):
    cols = st.columns([2,2])

    movie_id = '_'.join(movie.lower().split())
    sparql = f"""SELECT ?a ?n
    WHERE {{ <{iri}{movie_id}> <{iri}hasActor> ?a .
                ?a <{iri}myname> ?n }}"""
    res = g.query(sparql)

    with cols[1].container():
        if len(res) != 0:
            st.markdown('##### Actors')
            actors = ", ".join([str(row.n) for row in res])
            st.write(actors)

    sparql = f"""SELECT ?a ?n
    WHERE {{ <{iri}{movie_id}> <{iri}hasDirector> ?a .
                ?a <{iri}myname> ?n }}"""
    res = g.query(sparql)
    with cols[1].container():
        if len(res) != 0:
            st.markdown('##### Directors')
            directors = ", ".join([str(row.n) for row in res])
            st.write(directors)

    sparql = f"""SELECT ?a ?n
    WHERE {{ <{iri}{movie_id}> <{iri}hasWriter> ?a .
                ?a <{iri}myname> ?n }}"""
    res = g.query(sparql)
    with cols[1].container():
        if len(res) != 0:
            st.markdown('##### Writers')
            writers = ", ".join([str(row.n) for row in res])
            st.write(writers)

    sparql = f"""SELECT ?g
    WHERE {{ <{iri}{movie_id}> <{iri}hasGenre> ?g}}"""
    res = g.query(sparql)
    with cols[1].container():
        if len(res) != 0:
            st.markdown('##### Genres')
            genres = ", ".join([str(row.g).replace(iri,"") for row in res])
            st.write(genres)
    
    sparql = f"""SELECT ?y
        WHERE {{
            <{iri}{movie_id}> <{iri}myyear> ?y .
            BIND (datatype(?y) AS ?string)}}"""
    res = g.query(sparql)
    with cols[1].container():
        if len(res) != 0:
            st.markdown('##### Year')
            years = ", ".join([str(row.y).replace(iri,"") for row in res])
            st.write(years)

    sparql_poster = f"""SELECT ?p
    WHERE {{ <{iri}{movie_id}> <{iri}myposter> ?p}}"""
    res2 = g.query(sparql_poster)
    with cols[0].container():
        for r in res2:
            st.image(r.p)

    sparql_poster = f"""SELECT ?p
    WHERE {{ <{iri}{movie_id}> <{iri}myplot> ?p}}"""
    res2 = g.query(sparql_poster)
    for r in res2:
        st.write(r.p)

def movie_page():
    with st.form("Movie"):
        movies_list = []
        sparql = f"""SELECT ?t
        WHERE {{ ?movie a <{iri}myMovie> .
        ?a <{iri}mytitle> ?t .
        BIND (datatype(?t) AS ?string)}}"""
        res = g.query(sparql)
        for row in res:
            #st.write(row)
            movies_list.append(row.t)
        movies_list = list(set(movies_list))
        movie_title = st.selectbox("Title",movies_list)
        submitted = st.form_submit_button("Submit")
        if submitted:
            movie_box(movie_title)

def person_page():
    with st.form("Person"):
        p_list = []
        sparql = f"""SELECT ?n
        WHERE {{ ?movie a <{iri}myPerson> .
        ?a <{iri}myname> ?n .
        BIND (datatype(?n) AS ?string)}}"""
        res = g.query(sparql)
        for row in res:
            p_list.append(row.n)
        p_list = list(set(p_list))
        p_name = st.selectbox("Name",p_list)
        submitted = st.form_submit_button("Submit")
        if submitted:
            person_box(p_name)

def person_box(name):
    #temp = "https://m.media-amazon.com/images/M/MV5BYWQxYzdhMDMtNjAyZC00NzE0LWFjYmQtYjk0YzMyYjA5NzZkXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg"
    #st.image([temp, temp],width=100)
    name_id = '_'.join(name.lower().split())

    cols = st.columns([2,3])

    has_tmdb = False


    sparql = f"""SELECT ?pic
    WHERE {{ <{iri}{name_id}> <{iri}myphoto> ?pic .
    BIND (datatype(?pic) AS ?string) . }}"""
    res = g.query(sparql)
    if len(res) != 0:
        has_tmdb = True
        for row in res:
            cols[0].image(row.pic)

    sparql = f"""SELECT ?bio
    WHERE {{ <{iri}{name_id}> <{iri}mybiography> ?bio .
    BIND (datatype(?bio) AS ?string) . }}"""
    res = g.query(sparql)
    if len(res) != 0:
        with st.container():
            st.markdown("##### Biography")
            for row in res:
                st.write(row.bio)

    posters_containers = st
    if has_tmdb:
        posters_containers = cols[1]

    with posters_containers.container():
        sparql = f"""SELECT ?title ?poster
        WHERE {{ <{iri}{name_id}> <{iri}isActor> ?movie .
        ?movie <{iri}mytitle> ?title .
        BIND (datatype(?title) AS ?string) .
        ?movie <{iri}myposter> ?poster .
        }}"""
        res = g.query(sparql)
    
        if len(res) != 0:
            st.markdown("##### Actor Of :")
            titles = []
            posters = []
            for row in res:
                titles.append(row.title)
                posters.append(row.poster)
            st.image(posters,width=70) # 133

        sparql = f"""SELECT ?title ?poster
        WHERE {{ <{iri}{name_id}> <{iri}isDirector> ?movie .
        ?movie <{iri}mytitle> ?title .
        BIND (datatype(?title) AS ?string) .
        ?movie <{iri}myposter> ?poster .
        }}"""
        res = g.query(sparql)
        if len(res) != 0:
            st.markdown("##### Director Of :")
            titles = []
            posters = []
            for row in res:
                titles.append(row.title)
                posters.append(row.poster)
            st.image(posters,width=70) # 133

        

        sparql = f"""SELECT ?title ?poster
        WHERE {{ <{iri}{name_id}> <{iri}isWriter> ?movie .
        ?movie <{iri}mytitle> ?title .
        BIND (datatype(?title) AS ?string) .
        ?movie <{iri}myposter> ?poster .
        }}"""
        res = g.query(sparql)
        if len(res) != 0:
            st.markdown("##### Writer Of :")
            titles = []
            posters = []
            for row in res:
                titles.append(row.title)
                posters.append(row.poster)
            st.image(posters,width=70) # 133

        sparql = f"""SELECT ?bday ?age
        WHERE {{<{iri}{name_id}> <{iri}mybirthday> ?bday .
                <{iri}{name_id}> <{iri}myage> ?age .
                BIND (datatype(?bday) AS ?string) .
                BIND (datatype(?age) AS ?string) . }}"""
        res_bday = g.query(sparql)
        sparql = f"""SELECT ?dday
        WHERE {{<{iri}{name_id}> <{iri}mydeathday> ?dday .
                BIND (datatype(?dday) AS ?string) .}}"""
        res_dday = g.query(sparql)
        if len(res_dday) != 0: # If dead
            bday = ""
            dday = ""
            for row in res_bday:
                #st.write(row)
                bday = row.bday
            for row in res_dday:
                #st.write(row)
                dday = row.dday
            st.markdown(f"**Dates :** {bday} to {dday}")
        elif len(res_bday) != 0:
            bday = ""
            age = ""
            for row in res_bday:
                #st.write(row)
                bday = row.bday
                age = row.age
            st.markdown(f"**Born :** {bday}  ({age})")



def graph_page():
    with st.form("Person"):
        p_list = []
        sparql = f"""SELECT ?n
        WHERE {{ ?movie a <{iri}myPerson> .
        ?a <{iri}myname> ?n .
        BIND (datatype(?n) AS ?string)}}"""
        res = g.query(sparql)
        for row in res:
            p_list.append(row.n)
        p_list = list(set(p_list))
        p_name = st.selectbox("Name",p_list)
        submitted = st.form_submit_button("Submit")
        if submitted:
            graph_person(p_name)
            
                

with st.sidebar:
    page_type = om("Search",options=['Movie','Person','Graph'],icons=['film','person','map'])
    
import streamlit.components.v1 as components

if page_type == 'Movie':
    movie_page()
if page_type == 'Person':
    person_page()
if page_type == 'Graph':
    graph_page()
    #HtmlFile = open("whole_graph.html", 'r', encoding='utf-8')
    #source_code = HtmlFile.read() 
    ##print(source_code)
    #st.title("Graph")
    #with st.container():
    #    components.html(source_code,height=600)



#graph_person("Clint Eastwood")