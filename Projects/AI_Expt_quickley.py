from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(file_name, content):
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []

    for line in content:
        p = Paragraph(line, styles["Normal"])
        flowables.append(p)

    doc.build(flowables)

if __name__ == "__main__":
    content = [
        "How to Become an AI Expert Quickly",
        "",
        "Step 1: Understand the Basics",
        "1. Learn Python",
        "2. Math Fundamentals",
        "3. Machine Learning Basics",
        "",
        "Step 2: Dive Deeper into AI",
        "1. Advanced Machine Learning",
        "2. Natural Language Processing (NLP)",
        "3. Computer Vision",
        "",
        "Step 3: Gain Practical Experience",
        "1. Projects",
        "2. Competitions",
        "3. Internships",
        "",
        "Step 4: Stay Updated",
        "1. Follow AI Research",
        "2. Online Courses",
        "3. Join AI Communities",
        "",
        "Step 5: Specialize",
        "1. Choose Your Focus",
        "2. Advanced Topics",
        "",
        "Job Opportunities:",
        "1. Machine Learning Engineer",
        "2. Data Scientist",
        "3. AI Research Scientist",
        "4. AI Software Developer",
        "5. AI Consultant",
        "6. AI Product Manager",
        "",
        "Additional Tips:",
        "- Network",
        "- Continuous Learning",
        "- Build a Portfolio"
    ]

    file_name = "AI_Expt_quickley.pdf"
    create_pdf(file_name, content)
    print(f"PDF file '{file_name}' created successfully.")
