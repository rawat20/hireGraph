# 📄 hireGraph - Resume Optimizer

An AI-powered resume optimization tool that tailors your **LaTeX/Overleaf resumes** to match specific job descriptions. Using intelligent agents and LLMs, hireGraph automatically identifies missing skills and experiences, rewrites bullet points, and iteratively improves your resume until it achieves maximum alignment with the target job posting.

---

## 🎯 What It Does

hireGraph solves a critical problem in job hunting: **resume-JD misalignment**. Instead of manually tweaking your resume for each job application, hireGraph:

- ✨ **Analyzes** the Job Description (JD) and identifies all key requirements
- 🔄 **Rewrites** your resume to include critical skills and experiences from the JD
- 📊 **Evaluates** the optimized resume against the JD requirements
- 🔁 **Iterates** automatically until your resume achieves maximum keyword alignment (10/10 score)
- 📋 **Preserves** important information (company names, dates, titles)

**Result:** A resume that passes ATS filters and impresses recruiters by demonstrating exact alignment with job requirements.

---

## 🚀 How It Works

### Architecture: Multi-Agent LLM Workflow

hireGraph uses **LangGraph** to orchestrate two specialized AI agents:

```
User Input (JD + LaTeX Resume)
            ↓
        [EDITOR AGENT]
    (Rewrites resume to match JD)
            ↓
      [EVALUATOR AGENT]
    (Scores alignment 1-10)
            ↓
        Score ≥ 10?
         ↙       ↘
       YES       NO
        ↓         ↓
     [END]   [Loop back to EDITOR]
             (Max 3 iterations)
```

### Key Agents

**1. Editor Agent** 🖊️
- Analyzes the Job Description for hard skills and experiences
- Strategically rewrites resume sections to include missing keywords
- Naturally integrates new experiences into existing bullet points
- Adds technical skills to the skills section if needed
- Maintains resume authenticity and structure

**2. Evaluator Agent** 🧐
- Scores the resume 1-10 based on keyword alignment with JD
- Identifies specific missing requirements
- Provides actionable feedback for the next iteration

**3. Router Logic** 🔀
- Automatically loops back to the editor if score < 10
- Stops after 3 iterations or when a perfect score is achieved

---

## 🛠️ Technology Stack

- **LLM:** OpenAI GPT-4o (via LangChain)
- **Orchestration:** LangGraph (for agent workflow)
- **Frontend:** Streamlit (interactive web UI)
- **Language:** Python 3.12+
- **LaTeX Support:** Full Overleaf compatibility

---

## 📋 Requirements

- Python 3.8+
- OpenAI API Key (GPT-4o)
- LaTeX resume (Overleaf format)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hireGraph.git
cd hireGraph
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the project root:
```env
OPENAI_API_KEY="your-openai-api-key-here"
```

Get your free OpenAI API key: https://platform.openai.com/api-keys

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 💻 Usage Guide

### Step 1: Prepare Your Resume
- Export your Overleaf/LaTeX resume as raw LaTeX code
- Make sure it's a valid LaTeX document

### Step 2: Copy the Job Description
- Copy the entire job posting from LinkedIn, Indeed, or the company website
- Include all requirements, responsibilities, and preferred qualifications

### Step 3: Run the Optimizer
1. Open the hireGraph web interface
2. **Left panel:** Paste the Job Description
3. **Right panel:** Paste your LaTeX resume code
4. Click **"✨ Optimize Resume"**

### Step 4: Review Results
- Watch as agents work through iterations
- See draft updates and critique scores in real-time
- View the final optimized LaTeX code
- Copy the optimized code back into Overleaf

---

## 🖼️ Project Screenshots

### Main Interface
![hireGraph Main Interface](screenshots/main_interface.png)

### Optimization in Progress
![Optimization Progress](screenshots/optimize.png)

*Your project in action showing the AI-powered resume optimization workflow.*

---

## 📊 Example Workflow

**Input:**
- JD: "Seeking a DevOps Engineer with Kubernetes and Docker expertise..."
- Resume: Generic software engineer resume without Kubernetes mentions

**Process:**
1. Editor Agent detects missing "Kubernetes" and "Docker"
2. Rewrites: "Optimized deployment pipeline" → "Optimized deployment pipeline using Docker containers and Kubernetes orchestration"
3. Evaluator scores the change (e.g., 8/10)
4. Editor iterates again, adding specific Kubernetes metrics
5. Evaluator confirms 10/10 score
6. Process completes

**Output:**
- Resume now contains exact JD keywords
- Higher chance of passing ATS filters
- Better alignment with recruiter requirements

---

## 🔒 Privacy & Security

- Your resume and job descriptions are processed by OpenAI's API
- No data is stored permanently on our servers
- Ensure your API key is kept confidential
- Review the optimized resume before submitting to ensure accuracy

---

## ⚡ Performance Tips

1. **Shorter JD extracts:** Use the most relevant sections of the JD (not the entire website)
2. **Clean LaTeX:** Ensure your LaTeX code is valid before uploading
3. **API quota:** Monitor your OpenAI API usage to avoid unexpected charges
4. **Iteration limit:** Default is 3 iterations; increase if needed for complex JDs

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "API Key Error" | Verify `OPENAI_API_KEY` is correctly set in `.env` |
| "Invalid LaTeX" | Check LaTeX syntax; test in Overleaf first |
| "No optimization happening" | Ensure both JD and resume fields are filled |
| "Score stuck at 7/10" | Try rephrasing the JD or adding more context |

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 💡 Future Enhancements

- [ ] Support for PDF resumes (auto-convert to LaTeX)
- [ ] Multiple ATS optimization algorithms
- [ ] Cover letter optimization
- [ ] Resume scoring benchmarks
- [ ] Batch processing (optimize for multiple JDs)
- [ ] Integration with LinkedIn job scraper
- [ ] Dark mode UI
- [ ] Resume template suggestions

---

## 📧 Contact & Support

- **GitHub Issues:** Report bugs and request features
- **Email:** your.email@example.com
- **LinkedIn:** [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- Powered by [OpenAI GPT-4o](https://openai.com) for intelligent resume optimization
- UI built with [Streamlit](https://streamlit.io) for rapid prototyping

---

**Made with ❤️ to help you land your dream job!**
