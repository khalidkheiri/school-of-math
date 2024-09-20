import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
st.subheader(":blue[Final Exam Date Suggesion]", divider="rainbow")

exam_date = condition["Response 4"].value_counts().reset_index()
exam_date_sum = exam_date["count"].sum()
exam_date["percent"] = exam_date["count"].apply(lambda x: round(x/exam_date_sum * 100, 1))

col1, col2 = st.columns(2)
col1.metric("Early Exam", exam_date.loc[0,"count"], f'{exam_date.loc[0,"percent"]}%', delta_color="off")
col2.metric("Normal Date", exam_date.loc[1,"count"], f'{exam_date.loc[1,"percent"]}%', delta_color="off")


# Example data
date_suggession = condition[condition["Response 2"] == "خارج السودان "]
suggesions = date_suggession.groupby(["Response 3", "Response 4"]).size().reset_index()
suggesions.rename(columns={0:"count"}, inplace=True)

grouped_data = suggesions.pivot(index='Response 3', columns='Response 4', values="count").fillna(0)

grouped_data.rename(columns={
    "أكمال الفصل الدراسي الثاني  بشكل عادي والإنتظار لدورة الإمتحانات التالية التي عادة ما تكون بعد ستة أشهر على الاقل من دورة منتصف إكتوبر":"Normal",
    "تسريع الفصل الدراسي الثاني والإنتهاء منه في منتصف إكتوبر بدلا من نهايته , بحيث تبدأ إمتحانات الكلية في الاول من نوفمبر مما يتيح لك الجلوس للإمتحانات ":"Early Exam"
}, inplace=True)


# Create horizontal bars dynamically
fig, ax = plt.subplots(figsize=(8, 5))

grouped_data.index = grouped_data.index.map(reshaped_text)
# Plot 'أكمال الفصل الدراسي' (No) bars on the left side if available
if 'Normal' in grouped_data.columns:
    normal_values = grouped_data['Normal'].copy()
    normal_values[normal_values == 0] = 1  # Treat zero as -1 for plotting
    bars_no = ax.barh(grouped_data.index, -normal_values, color='green', label='Normal')

# Plot 'تسريع الفصل الدراسي' (Yes) bars on the right side if available
if 'Early Exam' in grouped_data.columns:
    bars_yes = ax.barh(grouped_data.index, grouped_data['Early Exam'], color='red', label='Early Exam')

if 'Normal' in grouped_data.columns:
    labels_no = [f'{abs(int(label))}' for label in grouped_data['Normal']]
    ax.bar_label(bars_no, labels=labels_no, label_type='edge', padding=5, fontsize=10)

if 'Early Exam' in grouped_data.columns:
    labels_yes = [f'{int(label)}' for label in grouped_data['Early Exam']]
    ax.bar_label(bars_yes, labels=labels_yes, label_type='edge', padding=5, fontsize=10)

# Draw a vertical line at x=0
ax.axvline(x=0, color='black', linewidth=1)

# Remove x-axis ticks
ax.set_xticks([])

ax.set_xlim(-130, 130)

# Set title text
title_normal = ax.text(-90, ax.get_ylim()[1] * 1.02, 'Normal', 
                       fontsize=14, fontweight='bold', color='green')

title_exam = ax.text(50, ax.get_ylim()[1] * 1.02, 'Early Exam', 
                     fontsize=14, fontweight='bold', color='red')

# Adjust the axes to provide space for the title
plt.subplots_adjust(top=0.85)


# Show plot
fig
