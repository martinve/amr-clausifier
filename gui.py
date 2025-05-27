import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import extract_info as ei

from contextlib import contextmanager, redirect_stdout
from io import StringIO

def annotate_text(text):
    parse = ei.get_amr_parse(text)
    return parse, ei.decompose_amr(parse)


def output_code(code):
    with stylable_container(
    "codeblock",
    """
    code {
        white-space: pre-wrap !important;
    }
    """,
    ):
        st.code(code)

def save_example():
    st.toast(":blue-background[Saved]")
    with open("cache/examples.txt", "a") as f:
        f.write(passage + "\n")


def run_annotator():

    parse, amr = annotate_text(passage)

    st.write("**AMR Graph**")
    output_code(parse)

    st.write("**Annotated passage**")
    output_code(amr)

    st.button("Save example", on_click=save_example)

    


@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        
        stdout.write = new_write
        yield


st.title("AMR Annotator")
passage = st.text_input("Enter a passage")

st.button("Annotate text",  type="primary", on_click=run_annotator)