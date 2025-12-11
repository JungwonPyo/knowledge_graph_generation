from enum import Enum

class AgentName(Enum):
    single_distiller_agent: str = "single_distiller_agent"
    doc_parser_agent: str = "doc_parser_agent"
    section_distiller_agent: str = "section_distiller_agent"
