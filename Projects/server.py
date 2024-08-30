import http.server
import socketserver
import socket
import logging
import cgi
import openpyxl
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Server Configuration
PORT = 8000
EXCEL_FILE = 'data.xlsx'

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/form':
                self._handle_form()
            else:
                super().do_GET()
        except ConnectionAbortedError:
            logging.warning("Connection was aborted by the client.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def do_POST(self):
        try:
            # Parse the form data
            form = cgi.FieldStorage(fp=self.rfile, environ=self.environ, headers=self.headers, max_size=1024*1024*10)  # Handle up to 10 MB file uploads
            
            # Extract form data
            name = form.getfirst('name', '')
            email = form.getfirst('email', '')
            location = form.getfirst('location', '')
            age = form.getfirst('age', '')
            education = form.getfirst('education', '')
            married = form.getfirst('married', '')
            cnic = form.getfirst('cnic', '')
            
            # Handle file upload
            file_item = form['profile_picture']
            if file_item.filename:
                file_data = file_item.file.read()  # You can save or process the file data here if needed

            # Save to Excel
            self._save_to_excel(name, email, location, age, education, married, cnic)

            # Respond with a success message
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h2>Data saved successfully!</h2>")
        except Exception as e:
            logging.error(f"An error occurred while processing POST request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h2>Internal server error</h2>")

    def _handle_form(self):
        """Handles the /form path and serves the HTML form."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # HTML content with styled form
        html_content = """
        <html>
        <head>
            <title>Submit Your Data</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                .popup { background-color: #fff; color: #333; padding: 20px; border-radius: 8px; box-shadow: 0 0 15px rgba(0, 0, 0, 0.2); width: 300px; text-align: center; }
                .popup h2 { margin-bottom: 20px; }
                .popup input[type="text"], .popup input[type="email"], .popup input[type="number"], .popup select, .popup input[type="file"] { width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 4px; border: 1px solid #ccc; }
                .popup input[type="submit"] { background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer; }
                .popup input[type="submit"]:hover { background-color: #45a049; }
            </style>
        </head>
        <body>
            <div class="popup">
                <h2>Submit Your Data</h2>
                <form method="post" action="/form" enctype="multipart/form-data">
                    <input type="text" name="name" placeholder="Your Name" required><br>
                    <input type="email" name="email" placeholder="Your Email" required><br>
                    <input type="text" name="location" placeholder="Location" required><br>
                    <input type="number" name="age" placeholder="Age" required><br>
                    <input type="text" name="education" placeholder="Education" required><br>
                    <select name="married" required>
                        <option value="" disabled selected>Married or Not</option>
                        <option value="yes">Yes</option>
                        <option value="no">No</option>
                    </select><br>
                    <input type="file" name="profile_picture" accept="image/*" required><br>
                    <input type="text" name="cnic" placeholder="CNIC" required><br>
                    <input type="submit" value="Submit">
                </form>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    def _save_to_excel(self, name, email, location, age, education, married, cnic):
        """Saves the form data to an Excel file."""
        try:
            # Load or create the Excel file
            try:
                wb = openpyxl.load_workbook(EXCEL_FILE)
                ws = wb.active
            except FileNotFoundError:
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.append(['Name', 'Email', 'Location', 'Age', 'Education', 'Married', 'CNIC'])  # Add headers

            # Append the new data
            ws.append([name, email, location, age, education, married, cnic])
            wb.save(EXCEL_FILE)
            logging.info(f"Data saved to {EXCEL_FILE}: {name}, {email}, {location}, {age}, {education}, {married}, {cnic}")
        except Exception as e:
            logging.error(f"Failed to save data to Excel: {e}")

# Get the local IP address
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Starting the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    logging.info(f"Serving at http://{local_ip}:{PORT}/form")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server is shutting down.")
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        httpd.server_close()
        logging.info("Server closed.")
