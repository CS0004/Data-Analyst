import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# URL of the main page
url = "https://results.eci.gov.in"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract links to results pages
links = []
base_url = "https://results.eci.gov.in/"
for a in soup.find_all('a', href=True):
    if "PcResultGenJune2024" in a['href'] or "AcResultGenJune2024" in a['href']:
        links.append(base_url + a['href'])

all_data = []

def scrape_results_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    page_data = []
    
    for table in tables:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                page_data.append([cell.text.strip() for cell in cells])
                
    return page_data

# Scrape each results page
for link in links:
    data = scrape_results_page(link)
    all_data.extend(data)

# Convert the data to a DataFrame
columns = ['Constituency', 'Candidate', 'Party', 'Votes', 'Status']
df = pd.DataFrame(all_data, columns=columns)
df['Votes'] = pd.to_numeric(df['Votes'].str.replace(',', ''), errors='coerce')

# Perform analysis
party_votes = df.groupby('Party')['Votes'].sum().reset_index()
party_votes = party_votes.sort_values(by='Votes', ascending=False)

# Example visualization
plt.figure(figsize=(12, 8))
plt.bar(party_votes['Party'], party_votes['Votes'])
plt.xlabel('Party')
plt.ylabel('Total Votes')
plt.title('Vote Distribution by Party')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('vote_distribution.png')

# Write the report
with open('report.md', 'w') as f:
    f.write("# Lok Sabha Election Results Report\n")
    f.write("## Key Insights\n")
    insights = [
        "1. The total votes received by each party.",
        "2. The party with the highest number of votes.",
        # Add more insights
    ]
    for insight in insights:
        f.write(insight + "\n")

print("Scraping and analysis complete. Report and visualization saved.")
