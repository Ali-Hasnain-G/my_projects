from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(file_name, content):
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []

    for item in content:
        text = f"{item[0]}\t{item[1]}"
        p = Paragraph(text, styles["Normal"])
        flowables.append(p)

    doc.build(flowables)

if __name__ == "__main__":
    content = [
        ("1",   "Mission     24/7"),
        ("2",   "Zikr        24/7"),
        ("3",   "AI expert   24/7"),
        ("4",   "Job         24/7")
    ]

    file_name = "Goal_setup.pdf"
    create_pdf(file_name, content)
    print(f"PDF file '{file_name}' created successfully.")
