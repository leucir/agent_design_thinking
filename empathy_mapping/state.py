from typing import TypedDict, List, Dict, Any, Optional

from .entities import (
    ConsentRecord, DataSource, EmpathyMap,
    PIIEntity, RedactedDocument, SupportTicket, UserSegment,
    AnalysisResult, SentimentAnalysis, TopicAnalysis, Quote, ProcessingMetrics
    )


class EmpathyMappingState(TypedDict):
    """State for Empathy Synthesizer agent"""
    
    # Core data
    support_tickets: List[SupportTicket]
    user_segments: List[UserSegment]
    empathy_maps: List[EmpathyMap]
    consent_records: List[ConsentRecord]
    
    # Current processing
    current_segment_id: Optional[str]
    current_document_id: Optional[str]
    processing_queue: List[str]
    
    # Analysis results
    analysis_results: List[AnalysisResult]
    sentiment_analyses: List[SentimentAnalysis]
    topic_analyses: List[TopicAnalysis]
    extracted_quotes: List[Quote]
    
    # PII and consent management
    pii_entities: List[PIIEntity]
    redacted_documents: List[RedactedDocument]
    consent_violations: List[str]
    
    # Quality and validation
    validation_results: List[Dict[str, Any]]
    quality_scores: Dict[str, float]
    bias_checks: List[Dict[str, Any]]
    
    # HITL (Human-in-the-Loop) gates
    pending_approvals: List[Dict[str, Any]]
    approved_items: List[str]
    rejected_items: List[str]
    
    # Processing metrics
    metrics: ProcessingMetrics
    
    # Control flow
    should_continue: bool
    current_phase: str
    errors: List[str]
    warnings: List[str]
    
    # Debugging and monitoring
    processing_history: List[str]
    node_execution_times: Dict[str, float]