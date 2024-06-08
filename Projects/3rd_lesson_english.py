from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set title and subtitle
pdf.set_font("Arial", size=16)
pdf.cell(200, 10, txt="3rd Lesson: Developing Reading Comprehension and Sentence Structure", ln=True, align='C')

pdf.set_font("Arial", size=12)

# Add content
content = """
1. Reading Comprehension:
   - Reading Short Stories:
     - Provide simple, illustrated stories for children to read.
     - Discuss the story together to ensure understanding.
     - Ask questions about the story to check comprehension.
   - Answering Questions:
     - Who, What, When, Where, Why, and How questions related to the story.
     - Encourage children to answer in full sentences.

2. Sentence Structure:
   - Building Simple Sentences:
     - Use word cards to create simple sentences (e.g., "The cat is on the mat.").
     - Teach the structure: Subject + Verb + Object.
   - Expanding Sentences:
     - Introduce adjectives to describe nouns (e.g., "The black cat is on the soft mat.").
     - Add more details to sentences to make them interesting.

3. Grammar Basics:
   - Nouns and Verbs:
     - Teach children to identify and use nouns (people, places, things).
     - Teach children to identify and use verbs (actions).
   - Adjectives and Adverbs:
     - Introduce adjectives (words that describe nouns).
     - Introduce adverbs (words that describe verbs).

4. Writing Practice:
   - Journaling:
     - Encourage children to write a few sentences about their day or a favorite activity.
     - Provide prompts to help them get started.
   - Story Writing:
     - Help children write their own short stories, focusing on beginning, middle, and end.
     - Encourage creativity and use of new vocabulary.

5. Phonics and Word Study:
   - Blends and Digraphs:
     - Teach common blends (e.g., bl, cl, fl) and digraphs (e.g., sh, th, ch).
     - Practice reading and writing words with these blends and digraphs.
   - Sight Words:
     - Continue building a sight word vocabulary.
     - Use flashcards and games to reinforce recognition.

6. Speaking and Listening:
   - Show and Tell:
     - Encourage children to bring an item from home and talk about it.
     - Practice asking and answering questions about the item.
   - Group Discussions:
     - Facilitate group discussions on various topics.
     - Encourage children to listen to others and respond appropriately.

7. Fun Activities:
   - Reading Games:
     - Play games that involve reading and understanding sentences (e.g., matching games, sentence puzzles).
   - Creative Arts:
     - Incorporate drawing and arts and crafts projects related to the stories they read or write.
"""

# Add content to PDF
for line in content.split('\n'):
    pdf.cell(200, 10, txt=line, ln=True)

# Save the PDF to a file
pdf_output = "C:/Users/GM Computer/coding/3rd_Lesson_Developing_Reading_Comprehension_and_Sentence_Structure.pdf"
pdf.output(pdf_output)

print(f"PDF generated and saved to {pdf_output}")
