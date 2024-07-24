# EasyKYC

EasyKYC is a comprehensive e-KYC (Electronic Know Your Customer) solution designed to simplify and automate the process of customer identification and verification. 
Using OCR (Optical Character Recognition) and image processing techniques, EasyKYC extracts and verifies specific text fields from various documents, ensuring a smooth and efficient storage of documents.

## Features

- **OCR Integration**: Utilizes EasyOCR for accurate text extraction from documents.
- **Image Preprocessing**: Leverages OpenCV for enhanced image processing and text detection.
- **Database Management**: Connects to MySQL for secure and reliable data storage.
- **User-Friendly Interface**: Provides a simple and intuitive interface through Streamlit for users to upload and verify documents.

## Installation


### Clone the Repository

```bash
git clone https://github.com/itsmeherepranetha/EasyKYC.git e_kyc
cd e_kyc
```
### Install the required packages

```bash
pip install -r requirements.txt
```
### Configuring Database
- Create a secrets.toml file inside .streamlit folder(keep it in .gitignore if you are thinking of pushing it to github or deploying it)
- Write the file with the following , according to your details
  ```bash
      [mysql]
      host = "localhost"
      port = "3306"
      database = "ekyc"
      user = "root"
      password = "yourpassword"

### Run the application
```bash
streamlit run app.py
```
- Be ready with your pan card and some face image of yours(preferably looking the camera)


## Improvements that can be done
- Right now the application just accepts PAN card, we can also configure the application to accept other documents like Aadhar card, and Driving License.
- But this needs a separate analysis ,since the text recognition pattern and sequences are different here.
- I have fine tuned in such a way the text recognition is done to the best of my abilities , but if there are more improvements that can be done, I am open to it.
