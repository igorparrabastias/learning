from pydantic import BaseModel, Field
from typing import Optional


class KnowledgeBase(BaseModel):
    first_name: str = Field(
        'unknown', description="Nombre del usuario del chat")
    last_name: str = Field(
        'unknown', description="Apellido del usuario del chat")
    confirmation: Optional[int] = Field(
        None, description="Número de confirmación de vuelo")
    discussion_summary: str = Field(
        "", description="Resumen de la conversación")
    open_problems: str = Field("", description="Temas aún no resueltos")
    current_goals: str = Field(
        "", description="Objetivo actual que el agente debe abordar")
