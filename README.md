1. **Environment Variables**

Create a `.env` file in the root directory of the project and add the following keys:

```plaintext
OPENAI_API_KEY=[Your-OpenAI-API-Key]
ANTHROPIC_API_KEY=[Your-Anthropic-API-Key]
```

2. **Install required library**

In the terminal, run the following command to install the required libraries:

```plaintext
pip install -r requirements.txt
```

3. **Run Application**

To run the application, execute the following command in the terminal. Alternatively, you can run the application directly from Visual Studio Code.

```plaintext
python app.py
```


I have stored the embeddings for 3 pdf that are availblae in the data folder which are
```aya-at-a-glance.pdf
monopoly.pdf
ticket_to_ride.pdf
```



**Methodology followed for Phase1:**

I have used the Factory pattern to manage the consumption of the LLM, which allows customization based on the user's selection at the frontend. By using the Factory Pattern, I will be able to add additional models in the future and consume them easily.

**Methodology followed for Phase2:**

I have implemented the Adaptive RAG by initially querying the Chroma DB to retrieve data relevant to a given user prompt. Upon successfully retrieving data,
I employ an LLM model to assess its relevance in relation to the user prompt.
If the content is deemed relevant, I integrate both the user prompt and the relevant document content to generate a response.
Conversely, if the retrieved data lacks sufficient relevance, I bypass the integration step and feed the user prompt directly into the LLM to generate the response


Workflow : 
![image](https://github.com/P-AshishKumar/Adaptive-RAG-System/assets/56246104/98337134-027d-4ce3-b2e6-5d514098afbd)

**Test1: Asking how to create an EC2 instance. The answer for this prompt is coming directly from the LLM**
![image](https://github.com/P-AshishKumar/Adaptive-RAG-System/assets/56246104/ea0dceee-9b60-4da3-a131-1b64589c7753)

**Test2: Asking about AYA, which is not available on the internet; this data is coming from the RAG.**
![image](https://github.com/P-AshishKumar/Adaptive-RAG-System/assets/56246104/37fda01e-5b83-4e00-8b1c-3c6a44b004ec)

**Test3: Asking about who is partnered with AYA.**
![image](https://github.com/P-AshishKumar/Adaptive-RAG-System/assets/56246104/8adf2758-d649-46bf-9483-20f1b4e4cd80)



