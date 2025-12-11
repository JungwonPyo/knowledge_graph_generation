from pydantic import BaseModel, Field, create_model
from dataclasses import dataclass
from typing import Literal, List, Optional, Any, Type


class Mention(BaseModel):
    type: Literal["LOCATION", "TIME", "PERSON", "EVENT", "ORGANIZATION"]
    string: str = Field(...,
                        description="The exact string of a named entity (e.g., place, time, person, or event) as it appears in the original text.")


class Relation(BaseModel):
    head: str = Field(..., description="The mentioned entity.")
    tail: str = Field(..., description="The mentioned entity.")
    relation_description: str = Field(...,
                                      description="A brief description of the relationship between head and tail mention entities.")


class Section(BaseModel):
    title: str = Field(..., description="The title of the section")
    summary: str = Field(...,
                         description="A brief summary (150–300 words) highlighting the key points covered in this section.")
    mentions: List[Mention] = Field(...,
                                    description="A comprehensive list of mentions (entities) found in the section.")
    relations: Optional[List[Any]] = None

# class Section(BaseModel):
#     title: str = Field(..., description="The title of the section")
#     summary: str = Field(...,
#                          description="A brief summary (150–300 words) highlighting the key points covered in this section.")
#     mentions: List[Mention] = Field(...,
#                                     description="A comprehensive list of mentions (entities) found in the section.")
#     relations: List[Relation] = Field(..., description="A comprehensive list of relations between mentions found in the section.")

class SectionContent(BaseModel):
    title: str = Field(..., description="The title of the section")
    content: str = Field(..., description="The section content")

class Unit(BaseModel):
    title: str = Field(..., description="Title of the unit")
    summary: str = Field(..., description="A concise summary of the unit's content, between 150 and 300 words.")
    sections: List[SectionContent] = Field(..., description="A list of `SectionContent` (in order) contained in the unit's content")

@dataclass
class DistilledUnit:
    title: str = Field(..., description="Title of the unit")
    summary: str = Field(..., description="A concise summary of the unit's content, between 150 and 300 words.")
    sections: List[Section] = Field(..., description="A list of `Section` contained in the unit's content")

def build_dynamic_relation_model(mention_strings: List[str]) -> BaseModel:
    mention_literals = Literal[tuple(mention_strings)]

    DynamicRelation = create_model(
        "DynamicRelation",
        head=(mention_literals,  Field(..., description="The mentioned entity (head) must match upper/lower case.")),
        tail=(mention_literals,  Field(..., description="The mentioned entity (tail) must match upper/lower case. ")),
        relation_description=(str,  Field(..., description="A brief description of the relationship between head and tail entities.")),
    )

    return DynamicRelation