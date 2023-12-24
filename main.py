from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import json
from rag import RagProcessor


app = FastAPI()

@app.post("/answer")
async def get_answers(
    questions_file: UploadFile = File(..., 
                    description="File containing a list of questions in JSON format"),
    document_file: UploadFile = File(...,
                    description="File containing the document in PDF or JSON format")
):
    # Save reference document
    document_file_path = f"./files/{document_file.filename}"
    with open(document_file_path,"wb") as f:
        document_content = await document_file.read()
        f.write(document_content)
    # Read questions
    questions_content = await questions_file.read()
    
    try:
        rag = RagProcessor(document_file_path)
    except ValueError as e:
        return JSONResponse(content={"error": e}, status_code=400)

    # Extract questions from json
    try:
        questions = json.loads(questions_content.decode("utf-8"))["questions"]
    except:
        return JSONResponse(content={"error": "Invalid questions file"}, status_code=400)

    # Answer questions
    answers = {}
    for item in questions:
        answers[item] = rag.get_answer(item)
    rag.delete_vectorstore()
    return answers

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)