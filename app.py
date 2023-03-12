import streamlit as st

import rdflib
g = rdflib.Graph()
g.parse("movies_project.owl")

from streamlit_option_menu import option_menu as om

iri = "http://semanticweb.org/cleme/projet#"


def movie_box(movie):
    cols = st.columns([3,2])

    movie_id = '_'.join(movie.lower().split())
    sparql = f"""SELECT ?a ?n
    WHERE {{ <{iri}{movie_id}> <{iri}hasActor> ?a .
                ?a <{iri}name> ?n }}"""
    res = g.query(sparql)

    with cols[1].container():
        st.markdown('#### Actors')
        for row in res:
            st.write(row.n)

    sparql = f"""SELECT ?a ?n
    WHERE {{ <{iri}{movie_id}> <{iri}hasDirector> ?a .
                ?a <{iri}name> ?n }}"""
    res = g.query(sparql)
    with cols[1].container():
        st.markdown('#### Directors')
        for row in res:
            st.write(row.n)

    sparql = f"""SELECT ?a ?n
    WHERE {{ <{iri}{movie_id}> <{iri}hasWriter> ?a .
                ?a <{iri}name> ?n }}"""
    res = g.query(sparql)
    with cols[1].container():
        st.markdown('#### Writers')
        for row in res:
            st.write(row.n)

    sparql_poster = f"""SELECT ?p
    WHERE {{ <{iri}{movie_id}> <{iri}poster> ?p}}"""
    res2 = g.query(sparql_poster)
    with cols[0].container():
        for r in res2:
            st.image(r.p)

    sparql_poster = f"""SELECT ?p
    WHERE {{ <{iri}{movie_id}> <{iri}plot> ?p}}"""
    res2 = g.query(sparql_poster)
    for r in res2:
        st.write(r.p)

def movie_page():
    with st.form("Movie"):
        movies_list = []
        sparql = f"""SELECT ?t
        WHERE {{ ?movie a <{iri}Movie> .
        ?a <{iri}title> ?t .
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
        WHERE {{ ?movie a <{iri}Person> .
        ?a <{iri}name> ?n .
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
    WHERE {{ <{iri}{name_id}> <{iri}photo> ?pic .
    BIND (datatype(?pic) AS ?string) . }}"""
    res = g.query(sparql)
    if len(res) != 0:
        has_tmdb = True
        for row in res:
            cols[0].image(row.pic)

    sparql = f"""SELECT ?bio
    WHERE {{ <{iri}{name_id}> <{iri}biography> ?bio .
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
        WHERE {{ <{iri}{name_id}> <{iri}isActorOf> ?movie .
        ?movie <{iri}title> ?title .
        BIND (datatype(?title) AS ?string) .
        ?movie <{iri}poster> ?poster .
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
        WHERE {{ <{iri}{name_id}> <{iri}isDirectorOf> ?movie .
        ?movie <{iri}title> ?title .
        BIND (datatype(?title) AS ?string) .
        ?movie <{iri}poster> ?poster .
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
        WHERE {{ <{iri}{name_id}> <{iri}isWriterOf> ?movie .
        ?movie <{iri}title> ?title .
        BIND (datatype(?title) AS ?string) .
        ?movie <{iri}poster> ?poster .
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


with st.sidebar:
    page_type = om("Search",options=['Movie','Person','Graph'],icons=['film','person','map'])
    
import streamlit.components.v1 as components

if page_type == 'Movie':
    movie_page()
if page_type == 'Person':
    person_page()
if page_type == 'Graph':
    HtmlFile = open("whole_graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    #print(source_code)
    st.title("Graph")
    with st.container():
        components.html(source_code,height=600)