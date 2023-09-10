from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from utils.llm_tools import SchoolLLM
import dotenv

dotenv.load_dotenv()
st_callback = StreamlitCallbackHandler(st.container())
with st.sidebar:
    # agent_type = st.selectbox("Agent Type", ["csv", "pandas"])
    agent_type = "csv"

suggested_questions = [
    "How many students enrolled for Biology this year?",
    "What is the median population of counties?",
    "What is the most common age group of students?",
    "What County has the most students who's families each 150k or more? ",
    "What county has the most 12th grade students?",
    "What county has the most 12th grade students by ratio to the population?"
]
school = SchoolLLM(agent_type=agent_type)
with st.sidebar:
    st.markdown('## Welcome to the FooBar School District')
    st.write('Below are some suggested questions to ask. Feel free to check "Use my own questions" to activate the chat feature')
    # st.table(suggested_questions)
    # select_box = st.selectbox("Select a question, or use your own.", suggested_questions + ["use my own"])
    use_my_own = st.checkbox("Use my own questions", value=False)
    st.markdown('---')
    st.markdown('## Advanced Features')
    st.markdown('_Uncheck the box to remove the wrapper and see more under the hood_')
    wrapper_checkbox = st.checkbox("Use Wrapper", value=True, help="Removing the wrapper passes the question directly to "
                                                                   "the inner-agent and bypasses the 'logic' layer. This "
                                                                   "can lead to unexpected errors, so use with caution.")
if not use_my_own:
    cols = st.columns(int(len(suggested_questions)/2))
    buttons = []
    for i, question in enumerate(suggested_questions):
        buttons.append(cols[i%2].button(question, key=f"suggested_question_{i}"))
    if any(buttons):
        st.chat_message("user").write(suggested_questions[buttons.index(True)])
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = school.run(suggested_questions[buttons.index(True)], callbacks=[st_callback])
            st.write(response)

    st.table({
        "Question": suggested_questions,
        "Correct Answers": ['This is not answerable with the data provided',
                            '186,788 (because CA as a whole is listed in the data, the model often says 192,646 instead)',
                            'Kindergarten (followed by 12th grade, going by enrollment, not by sampled demographics)',
                            'Alameda County (as far as our data goes)',
                            'Los Angeles County',
                            "Mono County (~4.5% of the population is 12th grade)"],
    })
else:
    prompt = st.chat_input()
    if prompt:
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = school.run(prompt, callbacks=[st_callback])

        st.write(response)

