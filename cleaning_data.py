import pandas as pd
import json

# Load the data
print("Loading CSV...")
df = pd.read_csv('github_issues.csv')

# Extract Repo Name
def extract_repo(url):
    try:
        parts = str(url).split('/')
        if len(parts) > 4:
            return f"{parts[3]}/{parts[4]}"
    except:
        return "unknown"
    return "unknown"

df['repo'] = df['issue_url'].apply(extract_repo)

# DIVERSITY FILTERING
print("Filtering for quality data...")
df = df.drop_duplicates(subset=['body'])
df = df[df['body'].str.len() > 100]
df = df[~df['repo'].str.contains('test|demo|tutorial|flow', case=False, na=False)]

# PICK THE REPO
repo_counts = df['repo'].value_counts()
chosen_repo = repo_counts.idxmax()
print(f"Chosen repository: {chosen_repo} (Total valid issues: {len(df[df['repo'] == chosen_repo])})")

# SLICE FIRST (Fix for your error)
# We take the top 100 rows FIRST so the length is predictable
subset = df[df['repo'] == chosen_repo].head(100).copy()

# ADD TIMESTAMPS
# We generate exactly as many timestamps as there are rows in our subset
print(f"Generating timestamps for {len(subset)} rows...")
timestamps = []
for i in range(len(subset)):
    day = (i // 24) + 1  # Increments day every 24 rows
    hour = i % 24        # Loops 0-23
    timestamps.append(f"2023-01-{day:02d} {hour:02d}:00:00")

subset['timestamp'] = timestamps

# FINAL CLEANUP
final_output = subset.rename(columns={
    'issue_url': 'id',
    'issue_title': 'title',
    'body': 'content'
})

# Select columns and save
final_output = final_output[['id', 'repo', 'title', 'content', 'timestamp']]
final_output.to_json('clean_data.json', orient='records', indent=2)

print(f"SUCCESS! Check 'clean_data.json' for 100 diverse issues from {chosen_repo}.")