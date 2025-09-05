from typing import TypedDict, List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from dataclasses import dataclass


class ConsentStatus(str, Enum):
    """Consent status for user data processing"""
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    EXPIRED = "expired"
    REVOKED = "revoked"


class DataSource(str, Enum):
    """Types of data sources for user research"""
    SUPPORT_TICKET = "support_ticket"


class PIILevel(str, Enum):
    """Levels of PII sensitivity"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SentimentType(str, Enum):
    """Types of sentiment analysis"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


@dataclass
class ConsentRecord:
    """Record of user consent for data processing"""
    consent_id: str
    user_id: str
    data_source: DataSource
    consent_scope: List[str]
    consent_status: ConsentStatus
    granted_at: datetime
    expires_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None
    consent_artifact_id: Optional[str] = None


@dataclass
class PIIEntity:
    """Personally Identifiable Information entity"""
    entity_type: str  # email, phone, name, address, etc.
    original_text: str
    redacted_text: str
    confidence: float
    pii_level: PIILevel
    start_position: int
    end_position: int


@dataclass
class RedactedDocument:
    """Document with PII redaction applied"""
    original_content: str
    redacted_content: str
    pii_entities: List[PIIEntity]
    redaction_timestamp: datetime
    redaction_confidence: float


@dataclass
class UserSegment:
    """Definition of a user segment"""
    segment_id: str
    segment_name: str
    description: str
    criteria: List[str]
    ticket_count: int
    created_at: datetime


@dataclass
class EmpathyMapQuadrant:
    """One quadrant of an empathy map (Say, Think, Do, Feel)"""
    quadrant_type: str  # "say", "think", "do", "feel"
    insights: List[str]
    quotes: List[str]
    confidence_score: float


@dataclass
class EmpathyMap:
    """Complete empathy map for a user segment"""
    map_id: str
    segment_id: str
    created_at: datetime
    updated_at: datetime
    
    # Empathy map quadrants
    say_quadrant: EmpathyMapQuadrant
    think_quadrant: EmpathyMapQuadrant
    do_quadrant: EmpathyMapQuadrant
    feel_quadrant: EmpathyMapQuadrant
    
    # Additional insights
    goals: List[str]
    pains: List[str]
    gains: List[str]
    latent_needs: List[str]
    
    # Metadata
    data_sources_used: List[DataSource]
    ticket_count: int
    total_analysis_time: float
    confidence_score: float


@dataclass
class SentimentAnalysis:
    """Sentiment analysis results"""
    sentiment_type: SentimentType
    confidence: float
    positive_score: float
    negative_score: float
    neutral_score: float
    emotions: Dict[str, float]  # emotion: intensity


@dataclass
class TopicAnalysis:
    """Topic modeling results"""
    topic_id: str
    topic_name: str
    keywords: List[str]
    frequency: int
    relevance_score: float
    sentiment: SentimentAnalysis


@dataclass
class Quote:
    """Extracted quote from user research"""
    quote_id: str
    original_text: str
    speaker: Optional[str]
    timestamp: Optional[datetime]
    sentiment: SentimentAnalysis
    topics: List[str]
    relevance_score: float
    source_document: str


@dataclass
class SupportTicket:
    """Base class for support ticket data"""
    ticket_id: str
    source_type: DataSource
    title: str
    description: str
    category: str
    priority: str
    status: str
    customer_id: str
    created_at: datetime
    metadata: Dict[str, Any]
    consent_record: Optional[ConsentRecord] = None
    redacted_version: Optional[RedactedDocument] = None


# SupportTicketDocument removed - using SupportTicket instead


@dataclass
class AnalysisResult:
    """Results from empathy map analysis"""
    analysis_id: str
    segment_id: str
    empathy_map: EmpathyMap
    sentiment_summary: SentimentAnalysis
    top_topics: List[TopicAnalysis]
    key_quotes: List[Quote]
    insights_summary: str
    recommendations: List[str]
    created_at: datetime


@dataclass
class ProcessingMetrics:
    """Metrics for processing performance"""
    total_tickets_processed: int
    total_customers: int
    processing_time_seconds: float
    pii_redaction_count: int
    consent_validation_count: int
    empathy_maps_generated: int
    average_confidence_score: float


class EmpathySynthesizerState(TypedDict):
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


# Pydantic models for API responses and structured outputs
class EmpathyMapResponse(BaseModel):
    """API response for empathy map generation"""
    success: bool
    empathy_map: Optional[EmpathyMap] = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    processing_time: float = 0.0


class ConsentValidationResponse(BaseModel):
    """API response for consent validation"""
    valid: bool
    consent_record: Optional[ConsentRecord] = None
    violations: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class PIIRedactionResponse(BaseModel):
    """API response for PII redaction"""
    redacted_content: str
    pii_entities_found: List[PIIEntity] = Field(default_factory=list)
    redaction_confidence: float
    processing_time: float


class AnalysisSummaryResponse(BaseModel):
    """API response for analysis summary"""
    total_segments: int
    total_customers: int
    empathy_maps_generated: int
    average_confidence: float
    top_insights: List[str]
    key_metrics: ProcessingMetrics
