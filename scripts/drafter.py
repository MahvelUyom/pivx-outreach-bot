import json
import os
import time
from google import genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file.")
    exit()

# Initialize the new GenAI Client
client = genai.Client(api_key=api_key)

def generate_proposal(repo_name, description):
    prompt = f"""
    You are a technical outreach lead for PIVX, a privacy-focused DAO. 
    Write a professional 3-paragraph collaboration proposal to the maintainers of the GitHub repository: {repo_name}.
    
    Context about the repo: {description}
    
    Your goal: Propose how PIVX's SHIELD technology (based on zk-SNARKs) could enhance their project's privacy or payment capabilities. 
    - Paragraph 1: Mention their specific work and why it's impressive.
    - Paragraph 2: Introduce PIVX SHIELD and the technical benefit of zk-SNARKs for their specific use case.
    - Paragraph 3: Invite them to discuss a potential integration or a DAO grant from PIVX.
    
    Tone: Professional, technical, and peer-to-peer.
    """

    try:
        # Using the current 2026 flagship flash model
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"❌ Error drafting for {repo_name}: {e}")
        return None

def main():
    input_file = 'data/scored_results.json'
    output_file = 'data/proposals.json'

    if not os.path.exists(input_file):
        print("❌ Scored results not found. Run scraper.py and scorer.py first.")
        return

    with open(input_file, 'r') as f:
        repos = json.load(f)

    proposals = []
    top_repos = repos[:10] 
    
    print(f"✍️ Drafting proposals using Gemini 3 for the top {len(top_repos)} repos...")

    for repo in top_repos:
        print(f"📝 Drafting for {repo['name']}...")
        draft = generate_proposal(repo['name'], repo['description'])
        
        if draft:
            repo['proposal_draft'] = draft
            proposals.append(repo)
            # Free tier safety delay
            time.sleep(4)

    with open(output_file, 'w') as f:
        json.dump(proposals, f, indent=4)

    print(f"\n✅ Success! {len(proposals)} drafts saved to {output_file}")

if __name__ == "__main__":
    main()