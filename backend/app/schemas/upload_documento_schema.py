from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel

class DocumentoUploadInput(BaseModel):

    frente: Optional[UploadFile] = None
    verso: Optional[UploadFile] = None
    arquivo: Optional[UploadFile] = None