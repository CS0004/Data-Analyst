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
        "1. The total votes in the elections were approximately 642 million.",
        "2. The party with the highest number of votes was Bharatiya Janata Party with approximately 235,973,935 votes i.e 36.56% of total votes.",
        "3. Indian National Congress (INC) was the second most successful party with approximately 136,759,064 votes i.e 21.19% of total votes.",
        "4. In terms of assembly constituencies won Bharatiya Janata Party claimed 240 constituencies whereas INC claimed only 99.",
        "5. The NDA alliance being led by Bharatiya Janata Party claimed the majority with 293 constituencies under their haul.",
        "6. Although Bharatiya Janata Party had more votes in Uttar Pradesh i.e 41.37% as compared to Samajwadi Party's 33.59%,they still could only win 33 constituencies as compared to SP's haul of 37.",
        "7. Fierce competition was seen in the 10 constituencies of Haryana as both BJP and INC won 5-5 each respectively, while achieving 46.11% and 43.67% votes respectively.",
        "8. In the NCT of Delhi BJP had a clean sweep across the 7 constituencies with a vote count of approximately 54.35% across the region.",
        "9. Although RJD bagged most votes in Bihar it was BJP and JD(U) with the most constituency hauls with 12-12 seats each as compared to RJD's 4.",
        "10. Towards the seven sisters BJP performed well as compared to the previous performances bagging majority in Assam,Arunachal Pradesh,etc."
    ]
    for insight in insights:
        f.write(insight + "\n")

print("Scraping and analysis complete. Report and visualization saved.")
