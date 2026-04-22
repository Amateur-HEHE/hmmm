import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import sys
import contextlib

# Page configuration
st.set_page_config(
    page_title="PandasLab — Master DataFrames",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
/* Import fonts */
@import url('[fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;500;600;700;800&display=swap)');

/* Root variables */
:root {
    --accent: #00e5a0;
    --accent2: #7c6aff;
    --accent3: #ff6a5e;
    --bg-dark: #0a0d14;
    --bg-card: rgba(255,255,255,0.04);
}

/* Global styles */
.stApp {
    font-family: 'Outfit', sans-serif;
}

/* Header styling */
.main-header {
    background: linear-gradient(135deg, rgba(0,229,160,0.1), rgba(124,106,255,0.1));
    padding: 2rem 2rem 1.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
}

.main-header h1 {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #e8eaf0, #00e5a0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.main-header p {
    color: #8892b0;
    font-size: 1.1rem;
}

/* Badge styling */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.badge-chapter {
    background: rgba(0,229,160,0.12);
    color: #00e5a0;
    border: 1px solid rgba(0,229,160,0.3);
}

.badge-interactive {
    background: rgba(124,106,255,0.12);
    color: #7c6aff;
    border: 1px solid rgba(124,106,255,0.3);
}

/* Card styling */
.custom-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.custom-card:hover {
    border-color: rgba(0,229,160,0.3);
    box-shadow: 0 8px 30px rgba(0,229,160,0.1);
    transform: translateY(-2px);
}

.custom-card h3 {
    color: #e8eaf0;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.custom-card p {
    color: #8892b0;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* Info boxes */
.info-box {
    padding: 1rem 1.25rem;
    border-radius: 12px;
    margin: 1rem 0;
    display: flex;
    gap: 12px;
    align-items: flex-start;
}

.info-note {
    background: rgba(0,229,160,0.08);
    border-left: 3px solid #00e5a0;
}

.info-tip {
    background: rgba(124,106,255,0.08);
    border-left: 3px solid #7c6aff;
}

.info-warn {
    background: rgba(255,106,94,0.08);
    border-left: 3px solid #ff6a5e;
}

/* Code block styling */
.code-block {
    background: #1a1f2e;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    overflow: hidden;
    margin: 1rem 0;
}

.code-header {
    display: flex;
    align-items: center;
    padding: 10px 16px;
    background: rgba(255,255,255,0.04);
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.code-dots {
    display: flex;
    gap: 6px;
}

.code-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.code-dot-red { background: #ff5f57; }
.code-dot-yellow { background: #febc2e; }
.code-dot-green { background: #28c840; }

/* Section title */
.section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2rem 0 1rem;
    font-size: 1.2rem;
    font-weight: 700;
    color: #e8eaf0;
}

.section-number {
    width: 28px;
    height: 28px;
    background: linear-gradient(135deg, #00e5a0, #7c6aff);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 800;
    color: #000;
}

/* Stats cards */
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-card:hover {
    border-color: #00e5a0;
    box-shadow: 0 4px 20px rgba(0,229,160,0.15);
}

.stat-value {
    font-size: 2rem;
    font-weight: 800;
    font-family: 'Space Mono', monospace;
    color: #00e5a0;
}

.stat-label {
    font-size: 0.8rem;
    color: #8892b0;
    margin-top: 4px;
}

/* Quiz styling */
.quiz-option {
    padding: 12px 18px;
    border-radius: 10px;
    border: 1.5px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.02);
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.quiz-option:hover {
    border-color: #7c6aff;
    background: rgba(124,106,255,0.08);
}

.quiz-correct {
    border-color: #00e5a0 !important;
    background: rgba(0,229,160,0.12) !important;
}

.quiz-wrong {
    border-color: #ff6a5e !important;
    background: rgba(255,106,94,0.1) !important;
}

/* Progress bar */
.progress-container {
    background: rgba(255,255,255,0.04);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
}

.progress-bar {
    height: 6px;
    background: rgba(255,255,255,0.08);
    border-radius: 3px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #00e5a0, #7c6aff);
    border-radius: 3px;
    transition: width 0.5s ease;
}

/* Difficulty badges */
.diff-easy {
    background: rgba(0,229,160,0.12);
    color: #00e5a0;
    border: 1px solid rgba(0,229,160,0.3);
    padding: 3px 10px;
    border-radius: 10px;
    font-size: 0.72rem;
    font-weight: 700;
}

.diff-medium {
    background: rgba(254,188,46,0.12);
    color: #febc2e;
    border: 1px solid rgba(254,188,46,0.3);
    padding: 3px 10px;
    border-radius: 10px;
    font-size: 0.72rem;
    font-weight: 700;
}

.diff-hard {
    background: rgba(255,106,94,0.12);
    color: #ff6a5e;
    border: 1px solid rgba(255,106,94,0.3);
    padding: 3px 10px;
    border-radius: 10px;
    font-size: 0.72rem;
    font-weight: 700;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: #10141f;
}

section[data-testid="stSidebar"] .stRadio > label {
    color: #8892b0;
    font-size: 0.85rem;
}

/* Table styling */
.dataframe {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* Button styling override */
.stButton > button {
    background: linear-gradient(135deg, #00e5a0, #00c77a);
    color: #000;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,229,160,0.4);
}

/* Expander styling */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Ticker animation */
@keyframes ticker {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

.ticker {
    display: flex;
    gap: 40px;
    animation: ticker 30s linear infinite;
    white-space: nowrap;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace;
    color: #00e5a0;
}
</style>
""", unsafe_allow_html=True)

# Data structures
CHAPTERS = {
    "🏠 Home": "home",
    "📖 Introduction to Pandas": "intro",
    "📊 DataFrame Basics": "basics",
    "🏗️ Creating DataFrames": "creating",
    "🔍 Data Inspection": "inspection",
    "📌 Indexing & Selection": "indexing",
    "✂️ Slicing": "slicing",
    "🧹 Data Cleaning": "cleaning",
    "❓ Handling Missing Data": "missing",
    "⚙️ Operations": "operations",
    "🔧 Functions & Methods": "functions",
    "🗂️ GroupBy & Aggregation": "groupby",
    "🔗 Merge, Join, Concat": "merge",
    "🔃 Sorting & Filtering": "sorting",
    "📈 Visualization": "viz",
    "🌍 Real-life Examples": "reallife",
    "💪 Practice Exercises": "exercises",
    "🧠 Quiz": "quiz"
}

QUIZ_DATA = [
    {"q": "Which method shows the first 5 rows of a DataFrame?", "opts": ["df.top()", "df.head()", "df.first()", "df.start()"], "ans": 1, "exp": "df.head(n) returns the first n rows (default 5)."},
    {"q": "What does df.shape return?", "opts": ["Number of rows", "Number of columns", "(rows, columns) tuple", "List of column names"], "ans": 2, "exp": "df.shape returns a tuple (rows, columns)."},
    {"q": "What is the difference between loc and iloc?", "opts": ["No difference", "loc uses integer positions, iloc uses labels", "loc uses labels, iloc uses integer positions", "loc is for columns, iloc is for rows"], "ans": 2, "exp": "loc is label-based; iloc is integer position-based."},
    {"q": "Which method is used to fill NaN values?", "opts": ["df.replace()", "df.fillna()", "df.fill()", "df.nan_fill()"], "ans": 1, "exp": "df.fillna(value) fills NaN values with the given value."},
    {"q": "How do you select multiple columns from a DataFrame?", "opts": ['df("A","B")', 'df["A","B"]', 'df[["A","B"]]', 'df.select("A","B")'], "ans": 2, "exp": 'Use double brackets df[["A","B"]] to select multiple columns.'},
    {"q": "What does df.dropna() do by default?", "opts": ["Drops columns with any NaN", "Drops rows with any NaN", "Drops rows where all values are NaN", "Fills NaN with 0"], "ans": 1, "exp": "By default, df.dropna() drops any row that has at least one NaN."},
    {"q": "Which parameter in pd.merge() controls the join type?", "opts": ["join", "type", "how", "method"], "ans": 2, "exp": 'The "how" parameter controls join type: inner, left, right, outer.'},
    {"q": "How do you sort a DataFrame by column 'Score' descending?", "opts": ["df.sort('Score',False)", "df.sort_values('Score', ascending=False)", "df.order_by('Score', desc=True)", "df.arrange('Score', asc=False)"], "ans": 1, "exp": 'Use df.sort_values("Score", ascending=False) to sort descending.'},
    {"q": 'What does df.groupby("Dept")["Salary"].mean() return?', "opts": ["Overall mean salary", "Mean salary per department", "List of departments", "Error"], "ans": 1, "exp": "It groups rows by Dept, then computes mean Salary for each group."},
    {"q": "Which is the correct boolean operator for combining conditions in pandas?", "opts": ["and", "or", "& and |", "+ and -"], "ans": 2, "exp": 'Use & for AND and | for OR with pandas boolean indexing.'},
    {"q": "What does df.info() display?", "opts": ["Statistical summary", "Column names, dtypes, and non-null counts", "First 5 rows", "Index values only"], "ans": 1, "exp": "df.info() shows column names, data types, non-null counts, and memory usage."},
    {"q": "How do you rename a column in pandas?", "opts": ["df.rename(columns={'old':'new'})", 'df.rename("old","new")', 'df.columns.rename("old","new")', 'df["old"].rename("new")'], "ans": 0, "exp": 'Use df.rename(columns={"old_name":"new_name"}).'},
    {"q": "What is the default join type in pd.merge()?", "opts": ["left", "right", "outer", "inner"], "ans": 3, "exp": 'The default how parameter in pd.merge() is "inner".'},
    {"q": "Which method stacks multiple DataFrames vertically?", "opts": ["pd.merge()", "pd.join()", "pd.concat()", "pd.combine()"], "ans": 2, "exp": "pd.concat([df1, df2]) stacks DataFrames vertically."},
    {"q": "What does iloc use for selection?", "opts": ["Column names", "Row labels", "Integer positions", "Boolean masks"], "ans": 2, "exp": "iloc selects by integer position (0, 1, 2...)."},
    {"q": "How do you check the number of unique values per column?", "opts": ["df.unique()", "df.count_unique()", "df.nunique()", "df.distinct()"], "ans": 2, "exp": "df.nunique() returns the count of unique values for each column."},
    {"q": "What does df.apply(func, axis=1) do?", "opts": ["Applies func to each column", "Applies func to each row", "Applies func to each cell", "Raises an error"], "ans": 1, "exp": "axis=1 means apply function across columns (row-by-row)."},
]

EXERCISES = [
    {"title": "Create a Student DataFrame", "difficulty": "easy", "task": "Create a DataFrame with columns: Name, Age, Score for 5 students. Print its shape and dtypes.", "hint": 'Use pd.DataFrame({"Name":[...], "Age":[...], "Score":[...]})'},
    {"title": "Filter High Scorers", "difficulty": "easy", "task": "From the student DataFrame, filter rows where Score > 80.", "hint": 'Use df[df["Score"] > 80]'},
    {"title": "Add a Grade Column", "difficulty": "easy", "task": "Add a 'Grade' column: A if Score≥90, B if ≥75, C otherwise.", "hint": 'Use df["Score"].apply(lambda x: "A" if x>=90 else "B" if x>=75 else "C")'},
    {"title": "Handle Missing Values", "difficulty": "medium", "task": "Create a DataFrame with some NaN values. Fill numeric NaNs with column mean.", "hint": 'Use df.fillna(df.mean())'},
    {"title": "GroupBy Analysis", "difficulty": "medium", "task": "From an employee DataFrame with Dept and Salary, find the average salary per department.", "hint": 'Use df.groupby("Dept")["Salary"].mean()'},
    {"title": "Merge Two DataFrames", "difficulty": "medium", "task": "Create two DataFrames and merge them using a left join.", "hint": 'Use pd.merge(df1, df2, on="key", how="left")'},
    {"title": "Find Top N Per Group", "difficulty": "hard", "task": "Find the top 2 highest-paid employees per department.", "hint": 'Use df.groupby("Dept").apply(lambda x: x.nlargest(2,"Salary"))'},
    {"title": "Reshape: Pivot Table", "difficulty": "hard", "task": "Create a pivot table showing total Sales per Product per Month.", "hint": 'Use pd.pivot_table(df, values="Sales", index="Month", columns="Product", aggfunc="sum")'},
]

# Initialize session state
if 'completed_chapters' not in st.session_state:
    st.session_state.completed_chapters = set()
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'current_quiz_idx' not in st.session_state:
    st.session_state.current_quiz_idx = 0

# Helper functions
def run_python_code(code):
    """Execute Python code and capture output"""
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    try:
        exec(code, {'pd': pd, 'np': np, 'print': print})
        output = redirected_output.getvalue()
    except Exception as e:
        output = f"Error: {str(e)}"
    finally:
        sys.stdout = old_stdout
    return output

def display_code_block(code, language="python"):
    """Display a styled code block"""
    st.code(code, language=language)

def info_box(content, box_type="note"):
    """Display an info box"""
    icons = {"note": "💡", "tip": "🎯", "warn": "⚠️"}
    colors = {
        "note": ("rgba(0,229,160,0.08)", "#00e5a0"),
        "tip": ("rgba(124,106,255,0.08)", "#7c6aff"),
        "warn": ("rgba(255,106,94,0.08)", "#ff6a5e")
    }
    bg, border = colors.get(box_type, colors["note"])
    st.markdown(f"""
    <div style="background:{bg}; border-left:3px solid {border}; padding:1rem 1.25rem; border-radius:12px; margin:1rem 0;">
        <span style="font-size:1.2rem">{icons.get(box_type, '💡')}</span>&nbsp;&nbsp;{content}
    </div>
    """, unsafe_allow_html=True)

def section_title(number, title):
    """Display a section title with number"""
    st.markdown(f"""
    <div class="section-title">
        <div class="section-number">{number}</div>
        <span>{title}</span>
    </div>
    """, unsafe_allow_html=True)

def chapter_badge(chapter_num, title="Chapter"):
    """Display a chapter badge"""
    st.markdown(f"""
    <div class="badge badge-chapter">
        📖 {title} {chapter_num}
    </div>
    """, unsafe_allow_html=True)

def interactive_badge():
    """Display an interactive badge"""
    st.markdown("""
    <div class="badge badge-interactive">
        ⚡ Interactive
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:1.5rem;">
        <div style="width:40px; height:40px; background:linear-gradient(135deg, #00e5a0, #7c6aff); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.5rem;">🐼</div>
        <div>
            <div style="font-family:'Space Mono',monospace; font-weight:700; color:#00e5a0;">Pandas<span style="color:#7c6aff">Lab</span></div>
            <div style="font-size:0.7rem; color:#8892b0;">Master DataFrames</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress
    progress = len(st.session_state.completed_chapters) / (len(CHAPTERS) - 3) * 100  # Exclude home, exercises, quiz
    st.markdown(f"""
    <div class="progress-container">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.8rem; color:#8892b0;">
            <span>Progress</span>
            <span>{progress:.0f}%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width:{progress}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    selected_chapter = st.radio(
        "Navigation",
        list(CHAPTERS.keys()),
        label_visibility="collapsed"
    )

# Main content based on selection
page = CHAPTERS[selected_chapter]

# ==================== HOME ====================
if page == "home":
    st.markdown("""
    <div class="main-header">
        <div class="badge badge-chapter">🐼 Interactive Learning Platform</div>
        <h1>Master Pandas DataFrames</h1>
        <p>The ultimate interactive guide to pandas DataFrames — from zero to hero. Crisp notes, live code, quizzes, and real-world examples.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">16</div>
            <div class="stat-label">Chapters</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">17</div>
            <div class="stat-label">Quiz Questions</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">40+</div>
            <div class="stat-label">Code Examples</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(st.session_state.completed_chapters)}</div>
            <div class="stat-label">Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Commands Ticker
    st.markdown("### 🚀 Essential Commands")
    commands = [
        ("df.head()", "First 5 rows"),
        ("df.info()", "Column types"),
        ("df.describe()", "Stats summary"),
        ("df.loc[]", "Label-based"),
        ("df.iloc[]", "Index-based"),
        ("df.dropna()", "Drop missing"),
        ("df.fillna()", "Fill missing"),
        ("df.groupby()", "Group data"),
        ("df.merge()", "Combine DFs"),
        ("df.sort_values()", "Sort data"),
    ]
    
    cols = st.columns(5)
    for i, (cmd, desc) in enumerate(commands):
        with cols[i % 5]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px; margin-bottom:10px; text-align:center;">
                <div style="font-family:'Space Mono',monospace; color:#00e5a0; font-size:0.85rem; margin-bottom:4px;">{cmd}</div>
                <div style="color:#8892b0; font-size:0.75rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Topics grid
    st.markdown("### 📚 All Topics")
    topics = list(CHAPTERS.items())[1:-2]  # Exclude home, exercises, quiz
    cols = st.columns(4)
    for i, (name, key) in enumerate(topics):
        with cols[i % 4]:
            completed = "✅" if key in st.session_state.completed_chapters else ""
            st.markdown(f"""
            <div class="custom-card">
                <h3>{name} {completed}</h3>
                <p>{'Completed' if completed else 'Click to learn'}</p>
            </div>
            """, unsafe_allow_html=True)

# ==================== INTRO ====================
elif page == "intro":
    chapter_badge(1)
    st.title("Introduction to Pandas")
    st.markdown("Pandas is the foundational library for data manipulation and analysis in Python.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_intro"):
            st.session_state.completed_chapters.add("intro")
            st.success("Chapter completed!")
    
    section_title(1, "What is Pandas?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3>🐼 Pandas</h3>
            <p>An open-source Python library providing data structures (Series & DataFrame) and tools for data analysis.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3>📅 Created in 2008</h3>
            <p>Wes McKinney developed pandas for financial data analysis at AQR Capital Management.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="custom-card">
            <h3>🏗️ Built on NumPy</h3>
            <p>Pandas uses NumPy arrays internally, gaining speed and rich mathematical operations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    section_title(2, "Installing Pandas")
    st.code("""pip install pandas
pip install numpy  # dependency""", language="bash")
    
    section_title(3, "Importing Pandas")
    st.code("""import pandas as pd     # standard alias
import numpy as np      # usually imported together

print(pd.__version__)   # check version""", language="python")
    
    info_box("By convention, pandas is always imported as <code>pd</code>. Using this alias makes your code consistent with thousands of tutorials and projects.", "note")
    
    section_title(4, "Core Data Structures")
    
    st.markdown("""
    | Structure | Dimensions | Description | Analogy |
    |-----------|------------|-------------|---------|
    | `Series` | 1D | Array with labels (index) | Single column |
    | `DataFrame` | 2D | Table of Series columns | Excel spreadsheet |
    """)
    
    st.code("""# Series — 1D labeled array
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s)

# DataFrame — 2D table
df = pd.DataFrame({'Name': ['Alice', 'Bob'],
                   'Age': [25, 30]})
print(df)""", language="python")
    
    # Interactive section
    st.markdown("---")
    interactive_badge()
    st.markdown("### ⚡ Try It Yourself")
    
    default_code = """import pandas as pd

# Create a Series
s = pd.Series([10, 20, 30, 40], index=['a','b','c','d'])
print("Series:")
print(s)
print()

# Create a DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['Delhi', 'Mumbai', 'Bangalore']
})
print("DataFrame:")
print(df)"""
    
    code = st.text_area("Edit code:", default_code, height=300, key="code_intro")
    
    if st.button("▶ Run Code", key="run_intro"):
        output = run_python_code(code)
        st.code(output, language="text")

# ==================== BASICS ====================
elif page == "basics":
    chapter_badge(2)
    st.title("DataFrame Basics")
    st.markdown("Understand the anatomy of a DataFrame — its structure, attributes, and fundamental properties.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_basics"):
            st.session_state.completed_chapters.add("basics")
            st.success("Chapter completed!")
    
    section_title(1, "DataFrame Anatomy")
    
    info_box("A DataFrame is like a 2D table with <strong>rows</strong> (observations) and <strong>columns</strong> (features/variables). Each column is a <code>Series</code>.", "note")
    
    st.code("""df = pd.DataFrame({
    'Name':   ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Age':    [25, 30, 35, 28],
    'Salary': [50000, 60000, 75000, 55000],
    'City':   ['Delhi', 'Mumbai', 'Chennai', 'Pune']
})

# Key attributes
print(df.shape)       # (4, 4) — rows, columns
print(df.columns)     # Index(['Name','Age','Salary','City'])
print(df.index)       # RangeIndex(start=0,stop=4,step=1)
print(df.dtypes)      # data type of each column""", language="python")
    
    section_title(2, "Key Attributes Quick Reference")
    
    st.markdown("""
    | Attribute | Returns | Example |
    |-----------|---------|---------|
    | `df.shape` | Tuple (rows, cols) | (100, 5) |
    | `df.columns` | Column names | Index(['A','B','C']) |
    | `df.index` | Row labels | RangeIndex(0..99) |
    | `df.dtypes` | Column data types | int64, object, float64 |
    | `df.size` | Total elements | 500 |
    | `df.ndim` | Number of dimensions | 2 |
    | `df.values` | Numpy ndarray | array([[...]]) |
    | `df.T` | Transposed DataFrame | Rows↔Columns swapped |
    """)
    
    section_title(3, "Interactive DataFrame Explorer")
    
    # Sample DataFrame
    df_sample = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'Dept': ['HR', 'Tech', 'Tech', 'HR', 'Finance'],
        'Salary': [50000, 90000, 75000, 60000, 80000],
        'Age': [25, 30, 28, 35, 29],
        'Score': [85, 92, 78, 88, 95]
    })
    
    st.dataframe(df_sample, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", df_sample.shape[0])
    with col2:
        st.metric("Columns", df_sample.shape[1])
    with col3:
        st.metric("Total Elements", df_sample.size)
    
    # Operations
    operation = st.selectbox("Select Operation:", [
        "Show Original",
        "Sort by Name ↑",
        "Sort by Salary ↓",
        "Filter: Dept = Tech",
        "Filter: Salary > 70k",
    ])
    
    if operation == "Sort by Name ↑":
        st.dataframe(df_sample.sort_values('Name'), use_container_width=True)
    elif operation == "Sort by Salary ↓":
        st.dataframe(df_sample.sort_values('Salary', ascending=False), use_container_width=True)
    elif operation == "Filter: Dept = Tech":
        st.dataframe(df_sample[df_sample['Dept'] == 'Tech'], use_container_width=True)
    elif operation == "Filter: Salary > 70k":
        st.dataframe(df_sample[df_sample['Salary'] > 70000], use_container_width=True)
    else:
        st.dataframe(df_sample, use_container_width=True)

# ==================== CREATING ====================
elif page == "creating":
    chapter_badge(3)
    st.title("Creating DataFrames")
    st.markdown("Multiple ways to create DataFrames — from dicts, lists, CSV files, and more.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_creating"):
            st.session_state.completed_chapters.add("creating")
            st.success("Chapter completed!")
    
    section_title(1, "From Dictionary")
    st.code("""# Keys = column names, Values = list of column data
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35]
}
df = pd.DataFrame(data)""", language="python")
    
    section_title(2, "From List of Dicts")
    st.code("""# Each dict = one row
rows = [
    {'Name': 'Alice', 'Age': 25, 'City': 'Delhi'},
    {'Name': 'Bob',   'Age': 30, 'City': 'Mumbai'},
    {'Name': 'Charlie', 'Age': 35}     # missing City → NaN
]
df = pd.DataFrame(rows)""", language="python")
    
    section_title(3, "From CSV / Excel / JSON")
    st.code("""# CSV file
df = pd.read_csv('data.csv')

# Excel file
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# JSON file
df = pd.read_json('data.json')

# From URL
df = pd.read_csv('[example.com](https://example.com/data.csv)')""", language="python")
    
    section_title(4, "From NumPy Array")
    st.code("""import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df = pd.DataFrame(arr, 
    columns=['A', 'B', 'C'],
    index=['r1', 'r2', 'r3'])""", language="python")
    
    # Interactive
    st.markdown("---")
    interactive_badge()
    st.markdown("### ⚡ Try It Yourself")
    
    creation_method = st.radio("Select creation method:", ["From Dictionary", "From List of Dicts", "From NumPy Array"])
    
    if creation_method == "From Dictionary":
        code = """import pandas as pd

df = pd.DataFrame({
    'Product': ['Laptop', 'Phone', 'Tablet'],
    'Price': [80000, 25000, 35000],
    'Stock': [50, 200, 100]
})
print(df)"""
    elif creation_method == "From List of Dicts":
        code = """import pandas as pd

rows = [
    {'name': 'Alice', 'score': 85},
    {'name': 'Bob', 'score': 92},
    {'name': 'Charlie', 'score': 78}
]
df = pd.DataFrame(rows)
print(df)"""
    else:
        code = """import pandas as pd
import numpy as np

arr = np.random.randint(1, 100, (5, 3))
df = pd.DataFrame(arr, columns=['A', 'B', 'C'])
print(df)"""
    
    st.code(code, language="python")
    if st.button("▶ Run", key="run_creating"):
        output = run_python_code(code)
        st.code(output, language="text")

# ==================== INSPECTION ====================
elif page == "inspection":
    chapter_badge(4)
    st.title("Data Inspection")
    st.markdown("Essential methods to explore and understand your dataset quickly.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_inspection"):
            st.session_state.completed_chapters.add("inspection")
            st.success("Chapter completed!")
    
    section_title(1, "Quick Look Methods")
    
    st.markdown("""
    | Method | Description |
    |--------|-------------|
    | `df.head(n)` | First n rows (default 5) |
    | `df.tail(n)` | Last n rows (default 5) |
    | `df.sample(n)` | n random rows |
    | `df.info()` | Column types, non-null counts, memory |
    | `df.describe()` | Stats: count, mean, std, min, max, quartiles |
    | `df.shape` | Tuple (rows, columns) |
    | `df.dtypes` | Data type of each column |
    | `df.columns` | List of column names |
    | `df.isnull().sum()` | Count of NaN per column |
    | `df.nunique()` | Unique values per column |
    """)
    
    st.code("""df = pd.read_csv('employees.csv')

df.head(3)           # first 3 rows
df.tail(3)           # last 3 rows
df.info()            # summary: dtype, non-null count
df.describe()        # statistical summary

# Missing data
df.isnull().sum()    # NaN count per column

# Unique values
df['Gender'].unique()       # array of unique values
df['Gender'].nunique()      # count
df['City'].value_counts()   # frequency table""", language="python")
    
    # Interactive demo
    st.markdown("---")
    interactive_badge()
    
    df_demo = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'Dept': ['HR', 'Tech', 'Tech', 'HR', 'Finance'],
        'Salary': [50000, 80000, 90000, 55000, 70000],
        'Score': [85, 92, np.nan, 78, 88]
    })
    
    method = st.selectbox("Select inspection method:", [
        "head(3)", "tail(2)", "info()", "describe()", "isnull().sum()", "nunique()", "dtypes"
    ])
    
    st.markdown("**Result:**")
    if method == "head(3)":
        st.dataframe(df_demo.head(3))
    elif method == "tail(2)":
        st.dataframe(df_demo.tail(2))
    elif method == "info()":
        buffer = StringIO()
        df_demo.info(buf=buffer)
        st.text(buffer.getvalue())
    elif method == "describe()":
        st.dataframe(df_demo.describe())
    elif method == "isnull().sum()":
        st.dataframe(df_demo.isnull().sum())
    elif method == "nunique()":
        st.dataframe(df_demo.nunique())
    else:
        st.dataframe(df_demo.dtypes)

# ==================== INDEXING ====================
elif page == "indexing":
    chapter_badge(5)
    st.title("Indexing & Selection")
    st.markdown("Master loc, iloc, and column selection — the most critical pandas skills.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_indexing"):
            st.session_state.completed_chapters.add("indexing")
            st.success("Chapter completed!")
    
    info_box("<strong>loc</strong> = Label-based (use column names and row labels). <strong>iloc</strong> = Integer position-based (use row/column numbers starting at 0).", "tip")
    
    section_title(1, "Column Selection")
    st.code("""df['A']            # Single column → Series
df[['A', 'C']]     # Multiple columns → DataFrame
df['D'] = df['A'] + df['B']  # Add new column""", language="python")
    
    section_title(2, "loc — Label Based")
    st.code("""df.loc['a']           # row with label 'a'
df.loc['a':'b']       # rows 'a' to 'b' (INCLUSIVE!)
df.loc['b', 'Name']   # cell at row 'b', col 'Name'
df.loc[:, 'Age']      # all rows, 'Age' column
df.loc[df['Age'] > 25]  # boolean indexing""", language="python")
    
    section_title(3, "iloc — Integer Based")
    st.code("""df.iloc[0]            # first row
df.iloc[-1]           # last row
df.iloc[0:2]          # rows 0,1 (END exclusive!)
df.iloc[1, 2]         # row 1, col 2 (cell)
df.iloc[:, 1]         # all rows, col index 1""", language="python")
    
    info_box("<strong>loc slice</strong> is inclusive on both ends. <strong>iloc slice</strong> is exclusive on the end — like Python lists. This is a common source of bugs!", "warn")
    
    # Interactive
    st.markdown("---")
    interactive_badge()
    
    df_idx = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Score': [85, 92, 78, 95],
        'Grade': ['B', 'A', 'C', 'A']
    }, index=['r1', 'r2', 'r3', 'r4'])
    
    st.markdown("**Sample DataFrame:**")
    st.dataframe(df_idx)
    
    idx_method = st.selectbox("Select indexing:", [
        "loc['r1']", "loc['r1':'r2']", "loc[df['Score']>85]",
        "iloc[0]", "iloc[0:2]", "iloc[:, 0:2]"
    ])
    
    st.markdown("**Result:**")
    if idx_method == "loc['r1']":
        st.write(df_idx.loc['r1'])
    elif idx_method == "loc['r1':'r2']":
        st.dataframe(df_idx.loc['r1':'r2'])
    elif idx_method == "loc[df['Score']>85]":
        st.dataframe(df_idx.loc[df_idx['Score'] > 85])
    elif idx_method == "iloc[0]":
        st.write(df_idx.iloc[0])
    elif idx_method == "iloc[0:2]":
        st.dataframe(df_idx.iloc[0:2])
    else:
        st.dataframe(df_idx.iloc[:, 0:2])

# ==================== SLICING ====================
elif page == "slicing":
    chapter_badge(6)
    st.title("Slicing")
    st.markdown("Extract subsets of DataFrames using powerful slicing syntax and boolean masks.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_slicing"):
            st.session_state.completed_chapters.add("slicing")
            st.success("Chapter completed!")
    
    section_title(1, "Row Slicing")
    st.code("""df[1:4]      # rows 1,2,3 (integer slice, exclusive end)
df[:3]       # first 3 rows
df[::2]      # every 2nd row
df[::-1]     # reverse all rows""", language="python")
    
    section_title(2, "Boolean Masking")
    st.code("""# Single condition
df[df['Age'] > 25]

# Multiple conditions (use & | ~, NOT and/or/not)
df[(df['Age'] > 25) & (df['City'] == 'Delhi')]
df[(df['Salary'] > 50000) | (df['Age'] < 30)]
df[~(df['Dept'] == 'HR')]   # NOT HR

# isin — membership test
df[df['City'].isin(['Delhi', 'Mumbai'])]

# between — range check
df[df['Age'].between(25, 35)]

# String methods
df[df['Name'].str.startswith('A')]
df[df['Name'].str.contains('li', case=False)]""", language="python")
    
    info_box("Always use <code>&</code>, <code>|</code>, <code>~</code> for element-wise boolean ops — never Python's <code>and</code> / <code>or</code> / <code>not</code> with pandas!", "note")

# ==================== CLEANING ====================
elif page == "cleaning":
    chapter_badge(7)
    st.title("Data Cleaning")
    st.markdown("Real data is messy. Learn to rename, retype, remove duplicates, and standardize your data.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_cleaning"):
            st.session_state.completed_chapters.add("cleaning")
            st.success("Chapter completed!")
    
    section_title(1, "Rename Columns")
    st.code("""df.rename(columns={'old_name': 'new_name'}, inplace=True)
df.columns = df.columns.str.lower().str.replace(' ', '_')""", language="python")
    
    section_title(2, "Change Data Types")
    st.code("""df['Age'] = df['Age'].astype(int)
df['Price'] = df['Price'].astype(float)
df['Date'] = pd.to_datetime(df['Date'])
df['col'] = pd.to_numeric(df['col'], errors='coerce')  # bad → NaN""", language="python")
    
    section_title(3, "Remove Duplicates")
    st.code("""df.duplicated().sum()                    # count of dupes
df.drop_duplicates(inplace=True)         # remove all dupes
df.drop_duplicates(subset=['Name'])      # dupes by column""", language="python")
    
    section_title(4, "String Cleaning")
    st.code("""df['Name'] = df['Name'].str.strip()      # remove whitespace
df['Name'] = df['Name'].str.lower()      # lowercase
df['Name'] = df['Name'].str.title()      # Title Case""", language="python")

# ==================== MISSING ====================
elif page == "missing":
    chapter_badge(8)
    st.title("Handling Missing Data")
    st.markdown("Detect, handle, and impute missing values — a crucial step in every data pipeline.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_missing"):
            st.session_state.completed_chapters.add("missing")
            st.success("Chapter completed!")
    
    section_title(1, "Detecting Missing Values")
    st.code("""df.isnull()              # True where NaN
df.notnull()             # True where not NaN
df.isnull().sum()        # count NaN per column""", language="python")
    
    section_title(2, "Dropping Missing Values")
    st.code("""df.dropna()                        # drop rows with ANY NaN
df.dropna(axis=1)                  # drop columns with ANY NaN
df.dropna(how='all')               # drop only if ALL values NaN
df.dropna(thresh=3)                # keep rows with at least 3 non-NaN""", language="python")
    
    section_title(3, "Filling Missing Values")
    st.code("""df.fillna(0)                        # fill all NaN with 0
df['Age'].fillna(df['Age'].mean())  # fill with mean
df['City'].fillna('Unknown')        # fill with string
df.fillna(method='ffill')           # forward fill
df.fillna(method='bfill')           # backward fill""", language="python")
    
    # Interactive demo
    st.markdown("---")
    interactive_badge()
    
    df_missing = pd.DataFrame({
        'Name': ['Alice', 'Bob', None, 'Diana'],
        'Age': [25, None, 35, 28],
        'Score': [85, 90, None, 78]
    })
    
    st.markdown("**Before:**")
    st.dataframe(df_missing)
    
    fill_method = st.selectbox("Select fill method:", [
        "No fill", "Fill with 0", "Fill with mean", "Forward fill", "Drop NaN"
    ])
    
    st.markdown("**After:**")
    if fill_method == "Fill with 0":
        st.dataframe(df_missing.fillna(0))
    elif fill_method == "Fill with mean":
        df_filled = df_missing.copy()
        df_filled['Age'] = df_filled['Age'].fillna(df_filled['Age'].mean())
        df_filled['Score'] = df_filled['Score'].fillna(df_filled['Score'].mean())
        st.dataframe(df_filled)
    elif fill_method == "Forward fill":
        st.dataframe(df_missing.ffill())
    elif fill_method == "Drop NaN":
        st.dataframe(df_missing.dropna())
    else:
        st.dataframe(df_missing)

# ==================== OPERATIONS ====================
elif page == "operations":
    chapter_badge(9)
    st.title("Operations on DataFrame")
    st.markdown("Arithmetic, comparison, apply, and vectorized operations on DataFrames.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_operations"):
            st.session_state.completed_chapters.add("operations")
            st.success("Chapter completed!")
    
    st.code("""# Arithmetic (element-wise)
df['Tax'] = df['Salary'] * 0.3
df['Total'] = df['Price'] * df['Qty']

# apply — custom function
df['Name_len'] = df['Name'].apply(len)
df['Grade'] = df['Score'].apply(lambda x: 'A' if x>=90 else 'B' if x>=75 else 'C')

# Aggregation
df['Salary'].sum()
df['Score'].mean()
df['Age'].max()

# Multiple aggregations
df[['Salary','Score']].agg(['mean', 'std', 'min', 'max'])""", language="python")

# ==================== FUNCTIONS ====================
elif page == "functions":
    chapter_badge(10)
    st.title("Functions & Methods")
    st.markdown("Comprehensive overview of the most useful pandas DataFrame methods.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_functions"):
            st.session_state.completed_chapters.add("functions")
            st.success("Chapter completed!")
    
    st.markdown("""
    | Method | Description |
    |--------|-------------|
    | `df.copy()` | Create independent copy |
    | `df.reset_index()` | Reset index to 0,1,2... |
    | `df.set_index('col')` | Set column as index |
    | `df.sort_values('col')` | Sort by column |
    | `df.sort_index()` | Sort by index |
    | `df.rename(cols)` | Rename columns/index |
    | `df.drop('col',axis=1)` | Remove column |
    | `df.query('expr')` | SQL-style filter |
    | `df.melt()` | Wide → Long format |
    | `df.pivot()` | Long → Wide format |
    | `df.pivot_table()` | Summarize with aggregation |
    | `df.to_csv('f.csv')` | Save to CSV |
    | `df.to_excel('f.xlsx')` | Save to Excel |
    """)
    
    section_title(1, "Query & Eval")
    st.code("""# query — readable boolean filter
df.query('Age > 25 and City == "Delhi"')
df.query('Salary > @min_sal')  # use Python variable with @

# eval — column operations as string
df.eval('Net = Salary - Tax')""", language="python")

# ==================== GROUPBY ====================
elif page == "groupby":
    chapter_badge(11)
    st.title("GroupBy & Aggregation")
    st.markdown("Split data into groups, apply functions, and combine results.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_groupby"):
            st.session_state.completed_chapters.add("groupby")
            st.success("Chapter completed!")
    
    info_box("<strong>Split-Apply-Combine:</strong> Split data by group → Apply a function (sum, mean, etc.) → Combine results into a new DataFrame.", "tip")
    
    st.code("""# Basic groupby
df.groupby('Dept')['Salary'].mean()       # avg salary per dept
df.groupby('Dept')['Salary'].sum()        # total salary per dept
df.groupby('Dept').size()                 # count per dept

# agg — multiple functions at once
df.groupby('Dept')['Salary'].agg(['mean','std','min','max'])

# Named aggregation
df.groupby('Dept').agg(
    avg_salary=('Salary', 'mean'),
    total_salary=('Salary', 'sum'),
    headcount=('Name', 'count')
)

# Transform — returns same-shape df
df['dept_avg'] = df.groupby('Dept')['Salary'].transform('mean')""", language="python")
    
    # Interactive demo
    st.markdown("---")
    interactive_badge()
    
    df_group = pd.DataFrame({
        'Dept': ['HR', 'Tech', 'HR', 'Tech', 'Finance', 'Tech'],
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
        'Salary': [50000, 90000, 55000, 85000, 70000, 95000],
        'Score': [80, 95, 75, 90, 88, 92]
    })
    
    st.dataframe(df_group)
    
    agg_func = st.selectbox("Select aggregation:", ["mean", "sum", "count", "max", "min"])
    
    st.markdown(f"**Result of groupby('Dept')['Salary'].{agg_func}():**")
    result = getattr(df_group.groupby('Dept')['Salary'], agg_func)()
    st.dataframe(result)
    
    # Visualization
    fig = px.bar(result.reset_index(), x='Dept', y='Salary', 
                 color='Dept', title=f'Salary {agg_func.title()} by Department')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ==================== MERGE ====================
elif page == "merge":
    chapter_badge(12)
    st.title("Merge, Join & Concatenate")
    st.markdown("Combine multiple DataFrames — like SQL JOINs but in Python.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_merge"):
            st.session_state.completed_chapters.add("merge")
            st.success("Chapter completed!")
    
    section_title(1, "pd.merge (SQL-style JOIN)")
    st.code("""pd.merge(df1, df2, on='Key', how='inner')  # common rows
pd.merge(df1, df2, on='Key', how='left')   # all left + matching right
pd.merge(df1, df2, on='Key', how='right')  # all right + matching left
pd.merge(df1, df2, on='Key', how='outer')  # all rows""", language="python")
    
    section_title(2, "pd.concat (Stack DataFrames)")
    st.code("""pd.concat([df1, df2])               # stack vertically
pd.concat([df1, df2], ignore_index=True)  # reset index
pd.concat([df1, df2], axis=1)       # stack horizontally""", language="python")
    
    st.markdown("""
    | how | SQL equivalent | Result |
    |-----|----------------|--------|
    | inner | INNER JOIN | Only matching rows |
    | left | LEFT JOIN | All left + matching right |
    | right | RIGHT JOIN | All right + matching left |
    | outer | FULL OUTER JOIN | All rows from both |
    """)
    
    # Interactive demo
    st.markdown("---")
    interactive_badge()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Employees:**")
        emp = pd.DataFrame({'EmpID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']})
        st.dataframe(emp)
    with col2:
        st.markdown("**Salaries:**")
        sal = pd.DataFrame({'EmpID': [1, 2, 4], 'Salary': [50000, 60000, 70000]})
        st.dataframe(sal)
    
    join_type = st.selectbox("Select join type:", ["inner", "left", "right", "outer"])
    
    st.markdown(f"**Result of merge (how='{join_type}'):**")
    result = pd.merge(emp, sal, on='EmpID', how=join_type)
    st.dataframe(result)

# ==================== SORTING ====================
elif page == "sorting":
    chapter_badge(13)
    st.title("Sorting & Filtering")
    st.markdown("Sort by values or index, filter rows with conditions, and rank your data.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_sorting"):
            st.session_state.completed_chapters.add("sorting")
            st.success("Chapter completed!")
    
    section_title(1, "Sorting")
    st.code("""df.sort_values('Salary')                           # ascending
df.sort_values('Salary', ascending=False)          # descending
df.sort_values(['Dept','Salary'], ascending=[True,False])  # multi-col

# Rank
df['Salary_rank'] = df['Salary'].rank(ascending=False)

# nlargest / nsmallest
df.nlargest(5, 'Salary')      # top 5 by salary
df.nsmallest(3, 'Age')        # bottom 3 by age""", language="python")
    
    section_title(2, "Filtering & Masking")
    st.code("""# where — keeps structure, replaces False with NaN
df['Salary'].where(df['Salary'] > 50000)

# clip — bound values to range
df['Score'].clip(lower=0, upper=100)

# query (SQL-like)
df.query('Salary > 60000 and Dept == "Tech"')""", language="python")

# ==================== VIZ ====================
elif page == "viz":
    chapter_badge(14)
    st.title("Visualization")
    st.markdown("Create quick plots directly from DataFrames.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_viz"):
            st.session_state.completed_chapters.add("viz")
            st.success("Chapter completed!")
    
    section_title(1, "Built-in Plot Types")
    st.code("""df['Salary'].plot(kind='line')           # line chart
df['Salary'].plot(kind='bar')            # bar chart
df['Salary'].plot(kind='hist', bins=10)  # histogram
df['Salary'].plot(kind='box')            # boxplot

# Scatter
df.plot(x='Age', y='Salary', kind='scatter')""", language="python")
    
    # Interactive demo
    st.markdown("---")
    interactive_badge()
    
    df_viz = pd.DataFrame({
        'Dept': ['HR', 'Tech', 'Finance', 'Sales', 'Ops'],
        'Avg_Salary': [55000, 88000, 73000, 62000, 58000],
        'Headcount': [15, 45, 12, 30, 20]
    })
    
    chart_type = st.selectbox("Select chart type:", ["Bar Chart", "Pie Chart", "Scatter Plot", "Line Chart"])
    
    if chart_type == "Bar Chart":
        fig = px.bar(df_viz, x='Dept', y='Avg_Salary', color='Dept',
                     title='Average Salary by Department')
    elif chart_type == "Pie Chart":
        fig = px.pie(df_viz, values='Headcount', names='Dept',
                     title='Headcount Distribution')
    elif chart_type == "Scatter Plot":
        fig = px.scatter(df_viz, x='Headcount', y='Avg_Salary', color='Dept',
                        size='Headcount', title='Salary vs Headcount')
    else:
        fig = px.line(df_viz, x='Dept', y='Avg_Salary', markers=True,
                     title='Average Salary Trend')
    
    st.plotly_chart(fig, use_container_width=True)
    
    info_box("For production visualizations, use <strong>Matplotlib</strong>, <strong>Seaborn</strong>, or <strong>Plotly</strong> for richer, more customizable charts.", "note")

# ==================== REAL LIFE ====================
elif page == "reallife":
    chapter_badge(15)
    st.title("Real-Life Examples")
    st.markdown("Complete end-to-end data analysis scenarios with real-world flavor.")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark Complete", key="complete_reallife"):
            st.session_state.completed_chapters.add("reallife")
            st.success("Chapter completed!")
    
    section_title(1, "Sales Analysis Report")
    st.code("""import pandas as pd

df = pd.read_csv('sales.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month_name()
df['Revenue'] = df['Units'] * df['Price']

# KPIs
total_revenue = df['Revenue'].sum()
top_product = df.groupby('Product')['Revenue'].sum().idxmax()
best_month = df.groupby('Month')['Revenue'].sum().idxmax()

print(f"Total Revenue: ₹{total_revenue:,.0f}")
print(f"Top Product: {top_product}")
print(f"Best Month: {best_month}")""", language="python")
    
    section_title(2, "Student Grade Analysis")
    
    # Interactive demo
    st.markdown("---")
    interactive_badge()
    
    np.random.seed(42)
    n = 20
    df_students = pd.DataFrame({
        'Student': [f'S{i:02d}' for i in range(1, n+1)],
        'Math': np.random.randint(40, 100, n),
        'Science': np.random.randint(40, 100, n),
        'English': np.random.randint(40, 100, n),
    })
    df_students['Average'] = df_students[['Math', 'Science', 'English']].mean(axis=1).round(1)
    df_students['Grade'] = pd.cut(df_students['Average'],
                                   bins=[0, 49, 59, 74, 89, 100],
                                   labels=['F', 'D', 'C', 'B', 'A'])
    
    st.dataframe(df_students.head(10))
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Grade Distribution:**")
        grade_dist = df_students['Grade'].value_counts().sort_index()
        fig = px.bar(x=grade_dist.index, y=grade_dist.values,
                     labels={'x': 'Grade', 'y': 'Count'},
                     color=grade_dist.index)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Top 5 Students:**")
        st.dataframe(df_students.nlargest(5, 'Average')[['Student', 'Average', 'Grade']])

# ==================== EXERCISES ====================
elif page == "exercises":
    st.title("💪 Practice Exercises")
    st.markdown("Apply what you've learned with hands-on exercises of varying difficulty.")
    
    for i, ex in enumerate(EXERCISES):
        with st.expander(f"Exercise {i+1}: {ex['title']}", expanded=i==0):
            # Difficulty badge
            diff_class = ex['difficulty']
            st.markdown(f"""
            <span class="diff-{diff_class}">{ex['difficulty'].upper()}</span>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Task:** {ex['task']}")
            
            if st.button(f"💡 Show Hint", key=f"hint_{i}"):
                info_box(ex['hint'], "tip")
            
            # Code editor
            code = st.text_area("Your code:", height=150, key=f"ex_code_{i}")
            
            if st.button("▶ Run", key=f"run_ex_{i}"):
                if code.strip():
                    output = run_python_code(code)
                    st.code(output, language="text")
                else:
                    st.warning("Please write some code first!")

# ==================== QUIZ ====================
elif page == "quiz":
    st.title("🧠 Test Your Knowledge")
    st.markdown("17 multiple-choice questions covering all pandas DataFrame topics.")
    
    # Progress bar
    progress = (st.session_state.current_quiz_idx / len(QUIZ_DATA)) * 100
    st.markdown(f"""
    <div class="progress-bar" style="margin-bottom:2rem">
        <div class="progress-fill" style="width:{progress}%"></div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.current_quiz_idx >= len(QUIZ_DATA):
        # Show results
        correct = sum(1 for i, ans in st.session_state.quiz_answers.items() 
                     if ans == QUIZ_DATA[i]['ans'])
        total = len(QUIZ_DATA)
        pct = (correct / total) * 100
        
        emoji = "🏆" if pct >= 90 else "🎉" if pct >= 70 else "👍" if pct >= 50 else "📚"
        
        st.markdown(f"""
        <div style="text-align:center; padding:3rem; background:rgba(255,255,255,0.04); border-radius:20px; border:1px solid rgba(255,255,255,0.08);">
            <div style="font-size:4rem; margin-bottom:1rem">{emoji}</div>
            <div style="font-size:4rem; font-weight:800; font-family:'Space Mono',monospace; color:#00e5a0">{pct:.0f}%</div>
            <div style="color:#8892b0; margin-top:0.5rem">
                {'Outstanding!' if pct >= 90 else 'Great job!' if pct >= 70 else 'Good effort!' if pct >= 50 else 'Keep studying!'}
            </div>
            <div style="display:flex; justify-content:center; gap:3rem; margin-top:2rem">
                <div style="text-align:center">
                    <div style="font-size:2rem; font-weight:700; color:#00e5a0">{correct}</div>
                    <div style="font-size:0.8rem; color:#8892b0">Correct</div>
                </div>
                <div style="text-align:center">
                    <div style="font-size:2rem; font-weight:700; color:#ff6a5e">{total - correct}</div>
                    <div style="font-size:0.8rem; color:#8892b0">Wrong</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Try Again"):
            st.session_state.quiz_answers = {}
            st.session_state.current_quiz_idx = 0
            st.session_state.quiz_submitted = False
            st.rerun()
    else:
        # Show current question
        idx = st.session_state.current_quiz_idx
        q = QUIZ_DATA[idx]
        
        st.markdown(f"**Question {idx + 1} of {len(QUIZ_DATA)}**")
        st.markdown(f"### {q['q']}")
        
        answered = idx in st.session_state.quiz_answers
        selected = st.session_state.quiz_answers.get(idx)
        
        for i, opt in enumerate(q['opts']):
            letter = 'ABCD'[i]
            
            # Determine styling
            if answered:
                if i == q['ans']:
                    style = "border-color:#00e5a0; background:rgba(0,229,160,0.12);"
                elif i == selected and selected != q['ans']:
                    style = "border-color:#ff6a5e; background:rgba(255,106,94,0.1);"
                else:
                    style = ""
            else:
                style = ""
            
            if st.button(f"{letter}. {opt}", key=f"opt_{idx}_{i}", 
                        disabled=answered,
                        use_container_width=True):
                st.session_state.quiz_answers[idx] = i
                st.rerun()
        
        if answered:
            is_correct = selected == q['ans']
            if is_correct:
                st.success(f"✅ Correct! {q['exp']}")
            else:
                st.error(f"❌ Incorrect. {q['exp']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if idx > 0:
                    if st.button("← Previous"):
                        st.session_state.current_quiz_idx -= 1
                        st.rerun()
            with col2:
                if st.button("Next →" if idx < len(QUIZ_DATA) - 1 else "🏆 See Results"):
                    st.session_state.current_quiz_idx += 1
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#8892b0; font-size:0.85rem; padding:1rem 0;">
    Made with ❤️ for Data Science learners | <a href="#" style="color:#00e5a0;">PandasLab</a>
</div>
""", unsafe_allow_html=True)
