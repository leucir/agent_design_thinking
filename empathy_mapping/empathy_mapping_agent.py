from typing import Dict, List, Optional, Tuple
from datetime import datetime
from langchain.agents import AgentExecutor
from langchain.tools import BaseTool
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
import time
from langchain_core.messages import SystemMessage, HumanMessage
import json

from .prompts import CLARIFICATION_PROMPT
from .structured_output import ClarificationOutput

from .entities import (
    ConsentRecord, DataSource, EmpathyMap, EmpathyMapResponse,
    PIIRedactionResponse, ConsentValidationResponse, AnalysisSummaryResponse,
    SupportTicket
)
from .state import EmpathyMappingState


class EmpathyMappingAgent:
    """Controller for the empathy mapping agent system focused on support ticket analysis"""
    
    def __init__(
        self,
        llm: None,
        debug: bool = False
    ):
        self.llm = llm
        self.debug = debug

    def _build_graph(self):    
        """Build the LangGraph for empathy mapping"""
        
        # Create the graph
        workflow = StateGraph(EmpathyMappingState)

        # Add nodes
        
        
