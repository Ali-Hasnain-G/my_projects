from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set title and subtitle
pdf.set_font("Arial", size=16)
pdf.cell(200, 10, txt="Next Lesson After Learning the Alphabet", ln=True, align='C')

pdf.set_font("Arial", size=12)

# Add content
content = """
1. Phonics and Letter Sounds:
   - Teach the sounds each letter makes (phonemic awareness).
   - Practice recognizing the beginning sounds of words.
   - Use flashcards, songs, and games to reinforce letter sounds.

2. Letter Formation and Handwriting:
   - Practice writing each letter, both uppercase and lowercase.
   - Focus on proper pencil grip and letter formation.
   - Use tracing worksheets, sand trays, or whiteboards for practice.

3. Simple Word Recognition:
   - Introduce basic CVC (consonant-vowel-consonant) words like cat, dog, bat.
   - Use pictures and words together to enhance recognition.
   - Start with simple sight words such as "a," "the," "is," "in."

4. Reading Simple Sentences:
   - Combine simple words into short sentences.
   - Practice reading aloud to build confidence and fluency.
   - Use picture books and early readers with repetitive text.

5. Rhyming and Word Families:
   - Teach rhyming words to help with phonemic awareness.
   - Introduce word families (e.g., -at family: cat, hat, mat).
   - Play rhyming games and activities to reinforce learning.

6. Listening and Speaking Skills:
   - Engage in storytelling and retelling activities.
   - Encourage children to describe pictures or events in their own words.
   - Practice following simple instructions and answering questions.

7. Vocabulary Building:
   - Introduce new words through stories, songs, and conversations.
   - Use visual aids and real-life objects to explain meanings.
   - Encourage children to use new words in sentences.
"""

# Add content to PDF
for line in content.split('\n'):
    pdf.cell(200, 10, txt=line, ln=True)

# Save the PDF to a file
pdf_output = "C:/Users/GM Computer/coding/Next_Lesson_After_Learning_Alphabet.pdf"
pdf.output(pdf_output)

print(f"PDF generated and saved to {pdf_output}")
