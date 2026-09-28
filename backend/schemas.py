from pydantic import BaseModel, Field, ConfigDict

class DocumentRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    document_type: str = Field(min_length=2, max_length=120)
    parties: str = Field(min_length=3, max_length=5000)
    terms: str = Field(min_length=3, max_length=10000)
    effective_date: str = Field(min_length=2, max_length=100)
    jurisdiction: str = Field(default="Not specified", max_length=200)
    additional_instructions: str = Field(default="", max_length=4000)

class DocumentResponse(BaseModel):
    document: str
    model: str
