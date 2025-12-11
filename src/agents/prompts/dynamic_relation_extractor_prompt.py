DYNAMIC_RELATION_EXTRACTOR_PROMPT="""
You are an intelligent assistant trained to extract relationships between named entities in historical documents.

Your task is to analyze a historical section that has already been summarized and annotated with mentions (named entities), and extract the list of relationships between those mentions.

Each relationship connects two mentions and describes how they are related in the context of the section.

Extract the following:

Given list of mentions:
{mentions}

1. **Relations**:
   - `head`: A string that exactly matches the `string` field of one of the mentions.
   - `tail`: A string that exactly matches another mention.
   - `relation_description`: A brief sentence in English explaining the nature of the relationship between `head` and `tail`, based strictly on the section content.

Guidelines:
- Only use the provided list of mentions to form relationships.
- Do not invent or hallucinate relationships not clearly present in the text.
- Use concise and factual descriptions based on the passage.
- Output only the list of extracted relationships.
- Write the descriptions in English.
"""