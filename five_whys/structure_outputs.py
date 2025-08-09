from pydantic import BaseModel, Field


class CauseAnalysisOutput(BaseModel):
    """
    This is the output structure for the cause analysis node.
    """
    primary_cause: str = Field(description="The main cause that answers the why question")
    evidence: str = Field(description="Evidence or reasoning supporting this cause")
    alternative_causes: list[str] = Field(description="Alternative causes")
    depth_assessment: str = Field(description="How deep this cause is (surface/intermediate/deep)")
    confidence_level: float = Field(description="0.0 to 1.0")
    actionability: str = Field(description="How actionable this cause is (low/medium/high)")



class ValidationOutput(BaseModel):
    """
    This is the output structure for the validation node.
    """
    chain_validity: float = Field(description="0.0 to 1.0")
    depth_adequacy: float = Field(description="0.0 to 1.0")
    evidence_strength: float = Field(description="0.0 to 1.0")
    actionability: float = Field(description="0.0 to 1.0")
    issues_found: list[str] = Field(description="Issues found in the chain")
    improvement_suggestions: list[str] = Field(description="Improvement suggestions")
    is_root_cause_likely: bool = Field(description="Is the root cause likely?")
    recommended_action: str = Field(description="Recommended action")



class SolutionOutput(BaseModel):
    """
    This is the output structure for the solution node.
    """
    immediate_actions: list[str] = Field(description="Immediate actions to address the root cause")
    preventive_measures: list[str] = Field(description="Preventive measures to avoid recurrence")
    monitoring_strategies: list[str] = Field(description="Monitoring strategies to track effectiveness")
    alternative_approaches: list[str] = Field(description="Alternative approaches if the primary solution fails")
    success_metrics: list[str] = Field(description="Success metrics")
    timeline: str = Field(description="Suggested implementation timeline")



class WebSearchOutput(BaseModel):
    """
    This is the output structure for the web search node.
    """
    search_results: list[str] = Field(description="Search results")
    search_query: str = Field(description="Search query")
    search_time: str = Field(description="Search time")
    search_engine: str = Field(description="Search engine")
    search_url: str = Field(description="Search URL")