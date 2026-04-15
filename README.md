# 📧 Automated Email assistant

An AI-powered tool to generate personalized follow-up emails for mill partners based on compliance data. Built to streamline partner communication while ensuring consistency, clarity, and actionable insights.

---

## 🚀 Features

- Reads compliance data from Google Sheets  
- Generates personalized emails using AI (Groq API)  
- Classifies partners by performance (High / Moderate / Needs Attention)  
- Allows manual review and editing before sending  
- Creates Gmail draft emails (local environment)  
- Displays summary dashboard for quick insights  

---

## 🧠 How It Works

1. Fetches partner data from Google Sheets  
2. Processes compliance rates and categorizes performance  
3. Uses AI to generate context-aware email drafts  
4. Displays emails in an interactive UI  
5. Allows users to create Gmail drafts 

---

## 🛠️ Tech Stack

- **Frontend:** `Streamlit`  
- **Backend Logic:** `Python`  
- **AI / LLM:** `Groq API` (LLaMA 3.1)  
- **Data Source:** `Google Sheets API` (via `gspread`)  
- **Email Integration:** `Gmail API`  
- **Authentication:** `Google OAuth 2.0`  
- **Environment Management:** `python-dotenv`

---
## 🔄 Pipeline

- Google Sheets
- Data Cleaning & Standardization**  
- Compliance Classification(High / Moderate / Needs Attention)
- AI Email Generation(Groq – LLaMA 3.1)
- Streamlit Dashboard(Review & Edit)
- Gmail Draft Creation (Local Environment)*  
- Final Output (Personalized Email Drafts)*
---

## 📦 Project Structure
```text
automated-email-drafter/
├── app.py            # Streamlit frontend (UI, dashboard, user interaction)
├── main.py           # Backend logic (data processing, AI generation, Gmail drafts)
├── requirements.txt  # Python dependencies
├── .gitignore        # Files to exclude (credentials, tokens, env)

```
---

## ⚙️ Setup (Local)

### 1. Clone the repository
```bash
git clone <your-repo-link>
cd fortify-email-system
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Add environment variables
```bash
GROQ_API_KEY=your_api_key_here
```
### 4. Add Google credentials
- Place credentials.json in the root folder
- Run once to authenticate:
```bash 
python main.py
```
### 5. Run the app
```bash
streamlit run app.py
```
## Limitations
- Not production deployed; runs only locally or in Streamlit preview.
- Gmail draft automation works only in local environment due to OAuth restrictions.

## Future Work
- Deploy as a secure, cloud-ready production application.
- Add scalable database and advanced analytics dashboard.
  
