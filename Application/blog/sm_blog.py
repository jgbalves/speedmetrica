
# Connector DB Functions
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Blog DB Functions

def create_table():
    '''Creating a db table inside the sqlite'''
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,text TEXT,postdate DATE)')

def add_data(author,title,text,postdate):
    '''Add data to the db table'''
    c.execute('INSERT INTO blogtable(author,title,text,postdate) VALUES (?,?,?,?)',(author,title,text,postdate))
    conn.commit()

def view_all_notes():
    '''To view all blog notes'''
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data

def view_all_titles():
    '''To view all blog titles'''
    c.execute('SELECT DISTINCT title FROM blogtable')
    data = c.fetchall()
    return data


# Blog Layout Templates

html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">Simple Blog </h1>
</div>
"""
title_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
<h6>Author:{}</h6>
<br/>
<br/> 
<p style="text-align:justify">{}</p>
</div>
"""
article_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>Author:{}</h6> 
<h6>Post Date: {}</h6>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""
head_message_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
<h6>Author:{}</h6> 
<h6>Post Date: {}</h6> 
</div>
"""
full_message_temp ="""
<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""



        # --- Blog Test ---
        with st.container():
            st.write("---")
            st.header("Blog Results:")
            st.write("##")
            result = view_all_notes()
            # st.write(result)
            for i in result:
                b_author = i[0]
                b_title = i[1]
                b_article = i[2]
                b_post_date = i[3]
                st.markdown(title_temp.format(b_title, b_author, b_article, b_post_date), unsafe_allow_html=True)





    # --- Blog Page ---
    elif selected_page == 'Blog':
        st.subheader('Blog')

        postlist = st.sidebar.selectbox('View posts',['Post 1', 'Post 2'])

    # --- Add Post ---
    elif selected_page == 'Add Post':
        st.subheader('Add Post')
        create_table()
        blog_author = st.text_input('Enter Author Name', max_chars=50)
        blog_title = st.text_input('Enter Post Title')
        blog_text = st.text_area('Post Article Here', height=200)
        blog_post_date = st.date_input('Date')
        if st.button('Add'):
            add_data(blog_author, blog_title, blog_text, blog_post_date)
            st.success('Post:{} saved'.format(blog_title))


    # --- Search ---
    elif selected_page == 'Search':
        st.subheader('Search')

    # --- Manage ---
    elif selected_page == 'Manage':
        st.subheader('Manage')
