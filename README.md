ReadMe*

There are both the Python notebook file using Gradio interface and the web application made by me.

Instructions manual:

01. Setting up Environment:

* Ensure you have Python installed on your system.
* Install the required dependencies by running: "pip install -r requirements.txt"
* Make sure you have Docker or any other app that handle containers.

02. Running the API:

* Execute the following command in your terminal: "docker build -t caption-it ."
* Then execute this command next: "docker run --name container_CI -p 8000:8000 caption-it"
* This will start the Flask development server, and you can access the application in your web browser at 'http://127.0.0.1:8000/'

03. Using the Application:

* You have to upload an image in the webpage.
* Click the "Generate Caption" button.
* The application will generate a caption. Easy as that.

04. If by any chance you think my webpage is ugly, then use my Python notebook file which uses the Gradio interface.
