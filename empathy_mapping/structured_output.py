from pydantic import BaseModel

class ClarificationOutput(BaseModel):
    """
    The clarification response of the problem statement.
    """
    clarified_problem: str




class IngestionOutput(BaseModel):
    """
    The ingestion response of the data.
    """
    ingested_data: str


class SupportTicketIngestionOutput(BaseModel):
    """
    The support ticket ingestion response.
    """
    tickets_ingested: int
    tickets_processed: int
    errors: list
    processing_time: float


class PIIRedactionOutput(BaseModel): 
    """
    The PII redaction response of the data.
    """
    redacted_data: str


class EmpathyMapOutput(BaseModel):
    """
    The empathy map response of the data.
    """
    empathy_map: str


class AnalysisSummaryOutput(BaseModel):
    """
    The analysis summary response of the data.
    """
    total_tickets_processed: int
    total_customers: int
    empathy_maps_generated: int
    average_confidence: float
    top_insights: list
    key_metrics: dict


class ConsentValidationOutput(BaseModel):
    """
    The consent validation response of the data.
    """
    consent_validated: bool
    consent_validation_reason: str


class ConsentRecordOutput(BaseModel):   
    """
    The consent record response of the data.
    """
    consent_record: str