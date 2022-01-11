import streamlit as st
import numpy as np
import pandas as pd
import time

##### SETUP CONFIG
st.set_page_config(page_title="Python Application", page_icon=None, layout='centered', initial_sidebar_state='auto', menu_items={'Get help':None,'Report a Bug':None,'About':None,})


##### ADD A SIDEBAR SELECTION
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)


##### PERCENTAGE BAR
my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)


##### MARKDOWN
st.markdown('Streamlit is **_really_ cool**.')





##### SPINNER
with st.spinner('Wait for it...'):
    time.sleep(5)
    

col1, col2 = st.columns([3, 1])
data = np.random.randn(10, 1)

col1.subheader("A wide column with a chart")
col1.line_chart(data)

col2.subheader("A narrow column with the data")
col2.write(data)

with st.expander("See explanation"):
    st.write("""
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    """)
    st.image("https://static.streamlit.io/examples/dice.jpg")


########## CONFIRMATIONS/NON-CONFIRMATIONS
#####

##### SUCCESS
st.success('Done!')


##### BALLOONS
st.balloons()


##### INFO
st.info('This is a purely informational message')


##### WARNING
st.warning('This is a warning')


##### RUNTIME ERRORS
e = RuntimeError('This is an exception of type RuntimeError')
st.exception(e)


##### ERROR
st.error('This is an error')



########## OTHER
#####

st.help(pd.DataFrame)

#Want to quickly check what datatype is output by a certain function? Try:
x = my_poorly_documented_function()
st.help(x)


##### ADD A SIDEBAR SELECTION
add_select2box = st.sidebar.selectbox(
    "dff would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)




##### CREATE A FORM
with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")


##### creates a callback

def form_callback(form_val):
    st.write(st.session_state.my_checkbox_val)

with st.form(callback=form_callback):
    st.write("Inside the form")
    slider_input = st.slider("Form slider")