import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999
df = pd.read_excel("data.xlsx")


#######################################################################################################################
st.set_page_config(layout="wide", initial_sidebar_state="expanded", menu_items=None)
st.markdown(
"""
<style>
div.st-emotion-cache-jkfxgf.e1nzilvr5 > p {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True
)

with st.sidebar:
    st.header("Faculty of Mathematical Sciences and Informatics")
    st.write("---")
    level_slider = st.radio(
    "Select the level of students",
    options=[
        "Second",
        "Third",
        "Fourth",
        "Fifth",
        "ALL Levels"
    ],
    index=4,
    )
###########################################
if level_slider == "Second":
    condition = df[df["Level"] == "Second"]
elif level_slider == "Third":
    condition = df[df["Level"] == "Third"]
elif level_slider == "Fourth":
    condition = df[df["Level"] == "Forth"]
elif level_slider == "Fifth":
    condition = df[df["Level"] == "Fifth"]
else:
    condition = df.copy()
##########################################

st.title("Students Distribution")

#### Header 1
st.subheader(":blue[Levels]", divider="rainbow")

levels = df["Level"].value_counts()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Second", levels["Second"])
col2.metric("Third", levels["Third"])
col3.metric("Fourth", levels["Forth"])
col4.metric("Fifth", levels["Fifth"])

#### Header 2
st.subheader(":blue[Locations of Students]", divider="rainbow")

# Function to reshape and display Arabic text
def reshaped_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

countries = condition[condition["Response 2"] == "خارج السودان "]["Response 3"].value_counts().reset_index()
states = condition[condition["Response 2"] == "داخل السودان"]["Response 3"].value_counts().reset_index()

countries["Response 3"] = [reshaped_text(text) for text in countries["Response 3"]]
states["Response 3"] = [reshaped_text(text) for text in states["Response 3"]]

# Function to split category labels into multiple lines
def format_labels(labels):
    return [label.replace(' ', '\n') for label in labels]

countries["Response 3"] = format_labels(countries["Response 3"])
states["Response 3"] = format_labels(states["Response 3"])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 5))
bars1 = ax1.bar(countries["Response 3"], countries["count"], color='#347deb')
bars2 = ax2.bar(states["Response 3"], states["count"], color='#347deb')

# Function to add labels on bars
def add_value_labels(ax, bars):
    for bar in bars:
        height = bar.get_height()
        # Set y position of label
        y_position = height if height != 0 else ax.get_ylim()[0]  # Place zero text at x-axis line
        ax.text(bar.get_x() + bar.get_width() / 2, y_position, f'{height:,}', 
                ha='center', va='bottom', fontsize=9)

ax1.tick_params(axis='x', labelsize=9)
ax2.tick_params(axis='x', labelsize=9)

ax1.tick_params(axis='y', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)

ax1.set_ylabel(reshaped_text('خارج\nالسودان'), rotation=0, labelpad=30, va='center')
ax2.set_ylabel(reshaped_text('داخل\nالسودان'), rotation=0, labelpad=30, va='center')

# Add value labels to each bar chart
add_value_labels(ax1, bars1)
add_value_labels(ax2, bars2)

fig


#### Header =3
