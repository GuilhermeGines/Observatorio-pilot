from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, PrivateAttr, model_validator
from .catalog import TOPICS

class QueryInput(BaseModel):
    _source_route: dict | None = PrivateAttr(default=None)
    countries: list[Literal['BR','US','CN','RU']] = Field(min_length=1, max_length=4)
    topics: list[str] = []
    keyword: str = Field(default='', max_length=160)
    start: date
    end: date
    mode: Literal['archive','collect'] = 'archive'
    @model_validator(mode='after')
    def valid_range(self):
        if self.end < self.start:
            raise ValueError('A data final deve ser igual ou posterior à inicial.')
        if any(t not in TOPICS for t in self.topics):
            raise ValueError('Tema desconhecido.')
        self.countries = list(dict.fromkeys(self.countries))
        self.keyword = self.keyword.strip()
        return self

class SettingsInput(BaseModel):
    gemini_model: str = Field(default='',max_length=100,pattern=r'^[a-zA-Z0-9._:/-]*$')
    resource_profile: Literal['auto','cpu'] = 'auto'
    memory_reserve_gb: float = Field(default=3,ge=1,le=32)
    codex_model: str = Field(default='',max_length=100,pattern=r'^[a-zA-Z0-9._:/-]*$')
    provider: Literal['openai','ollama','codex','gemini'] = 'openai'
    ollama_model: str = Field(default='qwen3.5:4b', min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9._:/-]+$')
    ollama_context: int = Field(default=16384, ge=8192, le=65536)
    model: str = Field(default='gpt-5.4-mini', min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9._:-]+$')
    allow_ai: bool = False
    max_documents: int = Field(default=12, ge=1, le=40)
    max_chars_per_document: int = Field(default=6000, ge=1000, le=16000)
    max_output_tokens: int = Field(default=6000, ge=1000, le=32768)
    articles_per_source: int = Field(default=3, ge=1, le=10)
    disabled_sources: list[str] = []

class KeyInput(BaseModel):
    key: str = Field(min_length=16, max_length=500)

class Evidence(BaseModel):
    revision_id: int
    quote: str

class Claim(BaseModel):
    country: str
    speaker: str
    statement: str
    period: str
    location: str
    evidence: list[Evidence]

class CountrySummary(BaseModel):
    country: str
    text: str
    evidence: list[Evidence]

class Comparison(BaseModel):
    title: str
    relation: Literal['convergencia','divergencia','hipotese','mudanca_historica']
    observation: str
    inference: str
    alternatives: str
    counterevidence: str
    caveats: str
    evidence: list[Evidence]

class CrossStatement(BaseModel):
    source_country: str
    target_country: str
    speaker: str
    statement: str
    evidence: list[Evidence]

class AnalysisOutput(BaseModel):
    summaries: list[CountrySummary]
    claims: list[Claim]
    comparisons: list[Comparison]
    cross_statements: list[CrossStatement]
    gaps: list[str]
    script: str

class SummaryOutput(BaseModel):
    summaries: list[CountrySummary]
    gaps: list[str]

class CrossingsOutput(BaseModel):
    comparisons: list[Comparison]
    cross_statements: list[CrossStatement]
    gaps: list[str]

class ParagraphPoint(BaseModel):
    country: str
    text: str
    paragraph_ids: list[str] = Field(min_length=1)

class ParagraphSummaryOutput(BaseModel):
    summaries: list[ParagraphPoint]
    gaps: list[str]

def output_model(kind):
    return ParagraphSummaryOutput if kind=='summary' else CrossingsOutput
