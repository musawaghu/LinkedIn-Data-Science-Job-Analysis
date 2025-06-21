import numpy
import seaborn
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

"""
LinkedIn 2025 Data Science/AI Job Posting Analysis
Questions to be answered:
1.How many total data/AI-related roles are there, and where?
2.What is the distribution between data analyst/scientist/engineer roles?
3.What are the hiring hotspots in the US?
4.Which companies are hiring the most data/AI jobs?
5.When are jobs being posted, and how does job posting look over time?
"""


def categorize_title(title):
    title = title.lower()
    if 'data' and 'scientist' in title:
        return 'Data Scientist'
    elif 'data' and 'engineer' in title:
        return 'Data Engineer'
    elif 'data' and 'analyst' in title:
        return 'Data Analyst'
    elif 'machine learning' or 'ai/ml' or 'ai' or 'ml' in title:
        return 'AI/ML Engineer'
    else:
        return 'Other'


if __name__ == '__main__':
    df = pd.read_csv("clean_jobs.csv")
    # drop null value columns
    df = df.drop(['work_type', 'employment_type'], axis=1)

    """Distribution of data jobs in the US by state and how many jobs in the US"""
    df = pd.read_csv('clean_jobs.csv')
    df['state'] = df['location'].str.extract(r', ([A-Z]{2})')  # Extract state abbreviations
    state_counts = df['state'].value_counts().reset_index()
    state_counts.columns = ['state', 'job_count']
    number_of_jobs = len(df['id'].value_counts())

    fig = px.choropleth(
        state_counts,
        locations='state',
        locationmode='USA-states',
        color='job_count',
        scope='usa',
        title='Job Listings by U.S. State',
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        annotations=[
            dict(
                x=0.5,
                y=-0.1,
                text=f"Number of Data/AI jobs in the USA:{number_of_jobs}",
                font=dict(size=12),
                bgcolor='white',
                bordercolor='black'
            )
        ]
    )
    fig.show()
    fig.write_html("DS Job distribution by state.html")

    """Distribution between data analyst/scientist/engineer and AI/ML engineers"""
    df['role'] = df['title'].apply(categorize_title)
    role_counts = df['role'].value_counts()
    fig = px.pie(
        role_counts,
        values=role_counts.values,
        names=role_counts.index,
        title='Distribution of Data Roles',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()
    fig.write_html("Distribution by job title.html")

    """Visualizing Job Posting over time"""
    date_counts = df['date_posted'].value_counts().reset_index()
    date_counts.columns = ['date', 'count']
    date_counts = date_counts.sort_values('date')

    fig = px.line(date_counts, x='date', y='count', title='Number of Posts Over Time')
    fig.show()
    fig.write_html("Job distribution by time.html")

    """Top companies that are hiring the most"""
    company_counts = df['company'].value_counts().reset_index()
    company_counts.columns = ['company', 'job_count']

    top_companies = company_counts.head(20)

    fig = px.bar(
        top_companies,
        x='company',
        y='job_count',
        title='Top 20 Companies Hiring Data/AI Roles',
        labels={'job_count': 'Number of Jobs', 'company': 'Company'},
        color='job_count',
        color_continuous_scale='Blues'
    )
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()
    fig.write_html("Job distribution by company.html")