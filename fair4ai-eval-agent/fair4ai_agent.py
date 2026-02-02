"""
FAIR4AI Evaluation Agent

This script automates the evaluation of datasets against the FAIR4AI checklist.
It reads metadata files (JSON, JSON-LD, Markdown, XML), uses an LLM to answer 
evaluation questions, and generates both JSON and CSV outputs.

Usage:
    python fair4ai_agent.py --metadata metadata_downloads/*.json --output neon_evaluation
    python fair4ai_agent.py --url https://dataset-url.com --output evaluation

Supported metadata formats:
    - JSON and JSON-LD (schema.org, croissant)
    - Markdown (.md, .markdown) for natural language metadata
    - XML for structured metadata

Requirements:
    - openai (or anthropic) library for LLM access
    - pandas for data manipulation
    - requests and beautifulsoup4 for URL extraction
    - API key set in environment variable (OPENAI_API_KEY or ANTHROPIC_API_KEY)
"""

import json
import csv
import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import os
import sys
import re
import time
try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Import LLM library (you can switch between OpenAI, Azure OpenAI, or Anthropic)
try:
    from openai import OpenAI, AzureOpenAI
    LLM_PROVIDER = "openai"
except ImportError:
    try:
        from anthropic import Anthropic
        LLM_PROVIDER = "anthropic"
    except ImportError:
        print("Error: Please install either 'openai' or 'anthropic' library")
        print("  pip install openai")
        print("  or")
        print("  pip install anthropic")
        sys.exit(1)


class FAIR4AIAgent:
    """Agent for automated FAIR4AI dataset evaluation."""
    
    def __init__(self, llm_provider: str = "openai", model: str = None, 
                 azure_endpoint: str = None, azure_api_version: str = None):
        """
        Initialize the FAIR4AI agent.
        
        Args:
            llm_provider: "openai", "azure", or "anthropic"
            model: Model name (defaults to gpt-4o-mini or claude-3-5-sonnet-20241022)
            azure_endpoint: Azure OpenAI endpoint URL (overrides env var)
            azure_api_version: Azure API version (defaults to 2024-08-01-preview)
        """
        self.llm_provider = llm_provider
        
        if llm_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            self.client = OpenAI(api_key=api_key)
            self.model = model or "gpt-4o-mini"
        elif llm_provider == "azure":
            # Azure OpenAI configuration
            # Check for OPENAI_SUBSCRIPTION_KEY first (common in Azure), then AZURE_OPENAI_API_KEY
            api_key = os.getenv("OPENAI_SUBSCRIPTION_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
            # Check for OPENAI_ENDPOINT first, then AZURE_OPENAI_ENDPOINT
            endpoint = azure_endpoint or os.getenv("OPENAI_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
            api_version = azure_api_version or os.getenv("OPENAI_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
            
            if not api_key:
                raise ValueError("OPENAI_SUBSCRIPTION_KEY or AZURE_OPENAI_API_KEY environment variable not set")
            if not endpoint:
                raise ValueError("OPENAI_ENDPOINT or AZURE_OPENAI_ENDPOINT environment variable not set or not provided")
            
            self.client = AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
            # For Azure, model should be your deployment name
            self.model = model or os.getenv("OPENAI_DEPLOYMENT") or os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
            self.azure_endpoint = endpoint
            self.azure_api_version = api_version
        else:  # anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self.client = Anthropic(api_key=api_key)
            self.model = model or "claude-3-5-sonnet-20241022"
        
        self.form_questions = None
        self.metadata_content = {}
        
    def load_form_questions(self, form_csv_path: str) -> pd.DataFrame:
        """Load the FAIR4AI form questions from CSV."""
        self.form_questions = pd.read_csv(form_csv_path)
        print(f"Loaded {len(self.form_questions)} questions from form")
        return self.form_questions
    
    def extract_metadata_from_url(self, url: str, output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Extract metadata from a dataset landing page URL."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests and beautifulsoup4 are required for URL extraction. Install with: pip install requests beautifulsoup4")
        
        print(f"Fetching metadata from URL: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            extracted_metadata = {}
            
            # Extract JSON-LD (Schema.org) metadata
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            for idx, script in enumerate(json_ld_scripts):
                try:
                    data = json.loads(script.string)
                    filename = f"extracted_schema_org_{idx}.json"
                    extracted_metadata[filename] = data
                    print(f"  Found JSON-LD metadata: {filename}")
                    
                    # Save to output directory if specified
                    if output_dir:
                        output_path = output_dir / filename
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        print(f"  Saved to: {output_path}")
                except json.JSONDecodeError:
                    continue
            
            # Extract meta tags
            meta_data = {}
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    meta_data[name] = content
            
            if meta_data:
                filename = "extracted_meta_tags.json"
                extracted_metadata[filename] = meta_data
                print(f"  Found meta tags: {filename}")
                
                if output_dir:
                    output_path = output_dir / filename
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(meta_data, f, indent=2, ensure_ascii=False)
                    print(f"  Saved to: {output_path}")
            
            # Look for direct links to metadata files
            metadata_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Search for JSON, JSON-LD, markdown, and XML metadata files
                if any(ext in href.lower() for ext in ['.json', '.jsonld', '.md', '.markdown', '.xml', 'metadata', 'schema', 'readme']):
                    metadata_links.append(href)
            
            # Download linked metadata files
            for idx, link in enumerate(metadata_links[:10]):  # Increased limit to 10 files
                try:
                    # Make absolute URL
                    if link.startswith('/'):
                        from urllib.parse import urljoin
                        link = urljoin(url, link)
                    elif not link.startswith('http'):
                        continue
                    
                    print(f"  Downloading linked metadata: {link}")
                    link_response = requests.get(link, timeout=15)
                    link_response.raise_for_status()
                    
                    # Determine file type and process accordingly
                    content_type = link_response.headers.get('content-type', '').lower()
                    link_lower = link.lower()
                    
                    # Try to parse as JSON first
                    if '.json' in link_lower or 'application/json' in content_type or 'application/ld+json' in content_type:
                        try:
                            data = link_response.json()
                            filename = f"downloaded_metadata_{idx}.json"
                            extracted_metadata[filename] = data
                            
                            if output_dir:
                                output_path = output_dir / filename
                                with open(output_path, 'w', encoding='utf-8') as f:
                                    json.dump(data, f, indent=2, ensure_ascii=False)
                                print(f"  Saved to: {output_path}")
                        except:
                            continue
                    # Handle markdown files
                    elif '.md' in link_lower or 'markdown' in link_lower or 'text/markdown' in content_type:
                        try:
                            text_content = link_response.text
                            filename = f"downloaded_metadata_{idx}.md"
                            extracted_metadata[filename] = text_content
                            
                            if output_dir:
                                output_path = output_dir / filename
                                with open(output_path, 'w', encoding='utf-8') as f:
                                    f.write(text_content)
                                print(f"  Saved to: {output_path}")
                        except:
                            continue
                    # Handle XML files
                    elif '.xml' in link_lower or 'application/xml' in content_type or 'text/xml' in content_type:
                        try:
                            text_content = link_response.text
                            filename = f"downloaded_metadata_{idx}.xml"
                            extracted_metadata[filename] = text_content
                            
                            if output_dir:
                                output_path = output_dir / filename
                                with open(output_path, 'w', encoding='utf-8') as f:
                                    f.write(text_content)
                                print(f"  Saved to: {output_path}")
                        except:
                            continue
                except:
                    continue
            
            # Extract main page content as markdown for dataset landing pages
            # This is especially useful for HuggingFace dataset cards and similar sites
            try:
                # Look for main content areas that typically contain dataset descriptions
                main_content = None
                content_source = None
                
                # Platform-specific handlers for common dataset repositories
                
                # 1. HuggingFace: Fetch raw README.md from repository
                if 'huggingface.co' in url and '/datasets/' in url:
                    dataset_path = url.split('/datasets/')[-1].rstrip('/')
                    readme_url = f"https://huggingface.co/datasets/{dataset_path}/raw/main/README.md"
                    try:
                        readme_response = requests.get(readme_url, timeout=15)
                        if readme_response.status_code == 200:
                            main_content = readme_response.text
                            content_source = "HuggingFace README.md"
                    except:
                        pass
                
                # 2. Zenodo: Extract description and notes from main page
                if not main_content and 'zenodo.org' in url:
                    desc_div = soup.select_one('.record-description, .dataset-description, #description')
                    if desc_div:
                        main_content = desc_div.get_text(separator='\n\n', strip=True)
                        content_source = "Zenodo description"
                
                # 3. Figshare: Extract article/dataset description
                if not main_content and 'figshare.com' in url:
                    desc_div = soup.select_one('.description, .article-description, [data-testid="description"]')
                    if desc_div:
                        main_content = desc_div.get_text(separator='\n\n', strip=True)
                        content_source = "Figshare description"
                
                # 4. NEON Data Portal: Extract product description
                if not main_content and 'data.neonscience.org' in url:
                    desc_areas = soup.select('.product-description, .dataset-description, #description, .abstract')
                    for desc_div in desc_areas:
                        text = desc_div.get_text(separator='\n\n', strip=True)
                        if len(text) > 200:
                            main_content = text
                            content_source = "NEON description"
                            break
                
                # 5. EDI Data Portal: Extract dataset abstract and methods
                if not main_content and ('environmentaldatainitiative.org' in url or 'portal.edirepository.org' in url):
                    # Look for abstract, methods, and additional info sections
                    content_parts = []
                    for selector in ['.abstract', '.methods', '#abstract', '#methods', '.metadata-section']:
                        section = soup.select_one(selector)
                        if section:
                            content_parts.append(section.get_text(separator='\n\n', strip=True))
                    if content_parts:
                        main_content = '\n\n---\n\n'.join(content_parts)
                        content_source = "EDI metadata"
                
                # 6. Dataverse: Extract dataset description and metadata
                if not main_content and 'dataverse' in url.lower():
                    desc_div = soup.select_one('.dataset-description, .description-block, #datasetDescription')
                    if desc_div:
                        main_content = desc_div.get_text(separator='\n\n', strip=True)
                        content_source = "Dataverse description"
                
                # 7. Google Dataset Search: Extract dataset info
                if not main_content and 'datasetsearch.research.google.com' in url:
                    desc_div = soup.select_one('[data-attrid="description"], .dataset-description')
                    if desc_div:
                        main_content = desc_div.get_text(separator='\n\n', strip=True)
                        content_source = "Google Dataset description"
                
                # General fallback: extract text from common content containers
                if not main_content:
                    content_selectors = [
                        'article', 'main', '[role="main"]',
                        '.dataset-card', '.readme', '.markdown-body', '.dataset-description',
                        '.description', '.abstract', '.metadata', '.content',
                        '#readme', '#dataset-card', '#description', '#abstract',
                        '[itemprop="description"]'
                    ]
                    for selector in content_selectors:
                        content_div = soup.select_one(selector)
                        if content_div:
                            main_content = content_div.get_text(separator='\n\n', strip=True)
                            if len(main_content) > 500:  # Only use if substantial content
                                content_source = f"page content (selector: {selector})"
                                break
                
                # Save the main content if found and substantial
                if main_content and len(main_content) > 500:
                    filename = "extracted_page_content.md"
                    extracted_metadata[filename] = main_content
                    print(f"  Found {content_source}")
                    
                    if output_dir:
                        output_path = output_dir / filename
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(main_content)
                        print(f"  Saved to: {output_path}")
            except Exception as e:
                print(f"  Note: Could not extract main page content: {e}")
            
            if not extracted_metadata:
                print("  Warning: No metadata found on page")
                return {}
            
            print(f"Extracted {len(extracted_metadata)} metadata source(s) from URL")
            
            # Add to metadata content
            self.metadata_content.update(extracted_metadata)
            return extracted_metadata
            
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return {}
    
    def load_metadata_files(self, metadata_paths: List[str]) -> Dict[str, Any]:
        """Load metadata files (JSON, markdown, or XML format)."""
        for path in metadata_paths:
            file_path = Path(path)
            if not file_path.exists():
                print(f"Warning: File not found: {path}")
                continue
            
            file_ext = file_path.suffix.lower()
            
            # Handle JSON files
            if file_ext in ['.json', '.jsonld']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        content = json.load(f)
                        self.metadata_content[file_path.name] = content
                        print(f"Loaded JSON metadata: {file_path.name}")
                    except json.JSONDecodeError as e:
                        print(f"Error loading JSON {path}: {e}")
            # Handle markdown files
            elif file_ext in ['.md', '.markdown']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        content = f.read()
                        self.metadata_content[file_path.name] = content
                        print(f"Loaded Markdown metadata: {file_path.name}")
                    except Exception as e:
                        print(f"Error loading Markdown {path}: {e}")
            # Handle XML files
            elif file_ext == '.xml':
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        content = f.read()
                        self.metadata_content[file_path.name] = content
                        print(f"Loaded XML metadata: {file_path.name}")
                    except Exception as e:
                        print(f"Error loading XML {path}: {e}")
            else:
                print(f"Warning: Unsupported file format: {file_path.name} (supported: .json, .jsonld, .md, .markdown, .xml)")
        
        return self.metadata_content
    
    def _build_context_prompt(self) -> str:
        """Build the context prompt with all metadata."""
        context = "# Metadata Files Content\n\n"
        
        for filename, content in self.metadata_content.items():
            context += f"## {filename}\n\n"
            
            # Format based on content type
            if isinstance(content, dict) or isinstance(content, list):
                # JSON content
                context += "```json\n"
                context += json.dumps(content, indent=2)[:10000]  # Limit size
                context += "\n```\n\n"
            elif isinstance(content, str):
                # Text content (markdown or XML)
                if filename.endswith('.md') or filename.endswith('.markdown'):
                    context += "```markdown\n"
                elif filename.endswith('.xml'):
                    context += "```xml\n"
                else:
                    context += "```\n"
                context += content[:10000]  # Limit size
                context += "\n```\n\n"
            else:
                # Fallback for unknown types
                context += "```\n"
                context += str(content)[:10000]
                context += "\n```\n\n"
        
        return context

    def _extract_message_text(self, content: Any) -> str:
        """Normalize LLM message.content into a plain text string.

        Newer models / SDKs may return message.content as a list of content parts
        instead of a single string. This helper flattens those structures so the
        rest of the agent can treat outputs uniformly as text.
        """
        if isinstance(content, str) or content is None:
            return content or ""

        # Handle list-of-parts structures (e.g., [{"type": "text", "text": {...}}, ...])
        if isinstance(content, list):
            parts: List[str] = []
            for part in content:
                if isinstance(part, str):
                    parts.append(part)
                elif isinstance(part, dict):
                    # Prefer explicit text blocks but be liberal about keys
                    text_val = part.get("text") or part.get("value") or part.get("content")
                    if isinstance(text_val, dict):
                        parts.append(str(text_val.get("value", "")))
                    elif isinstance(text_val, str):
                        parts.append(text_val)
            if parts:
                return "\n".join(p for p in parts if p)
            # If we didn't recognize any parts, fall back to a serialized form
            try:
                return json.dumps(content, ensure_ascii=False, default=str)
            except Exception:
                return str(content)

        # Fallback for any other unexpected structure
        try:
            return json.dumps(content, ensure_ascii=False, default=str)
        except Exception:
            return str(content)
    
    def _call_llm(self, system_prompt: str, user_prompt: str, max_retries: int = 5) -> str:
        """Call the LLM with the given prompts, with retry logic for rate limits."""
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                if self.llm_provider in ["openai", "azure"]:
                    # Both OpenAI and Azure use the same API structure with slight parameter differences
                    completion_kwargs = {
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                    }
                    if self.llm_provider == "azure":
                        completion_kwargs["max_completion_tokens"] = 2000
                    else:
                        completion_kwargs["max_tokens"] = 2000
                        completion_kwargs["temperature"] = 0.1

                    response = self.client.chat.completions.create(**completion_kwargs)
                    raw_content = response.choices[0].message.content
                    return self._extract_message_text(raw_content)
                else:  # anthropic
                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=2000,
                        temperature=0.1,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    return response.content[0].text
                    
            except Exception as e:
                last_exception = e
                error_str = str(e)
                
                # Check if it's a rate limit error (429 or RateLimitReached)
                if "429" in error_str or "RateLimitReached" in error_str or "rate_limit" in error_str.lower():
                    # Exponential backoff: wait longer with each retry
                    wait_time = (2 ** attempt) + 1  # 2, 3, 5, 9, 17 seconds
                    print(f"  Rate limit hit. Retrying in {wait_time} seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    # For non-rate-limit errors, fail immediately
                    raise
        
        # If we exhausted all retries, raise the last exception
        raise last_exception
    
    def answer_question(self, question_row: pd.Series, metadata_context: str) -> Dict[str, str]:
        """
        Use LLM to answer a single question based on metadata.
        
        Args:
            question_row: Row from the form questions DataFrame
            metadata_context: Metadata content as context
            
        Returns:
            Dictionary with response, evidence, and notes
        """
        section = question_row.get('section', '')
        title = question_row.get('title', '')
        description = question_row.get('description', '')
        question_type = question_row.get('question_type', '')
        options = question_row.get('options', '')
        
        # Skip section breaks and text items (informational only)
        if question_type in ['SECTION_BREAK', 'textItem']:
            return None
        
        system_prompt = """You are an expert in evaluating datasets for FAIR (Findable, Accessible, Interoperable, Reusable) principles and AI readiness.

Your task is to answer questions about a dataset based solely on the provided metadata files.

For each question, provide:
1. A direct answer (for choice questions, select from provided options; for text questions, provide specific information)
2. Evidence from the metadata that supports your answer (cite specific fields/values)
3. Notes with any caveats or additional context

Be precise and evidence-based. If information is not available in the metadata, state "Not found in metadata" rather than making assumptions.

For choice questions (Yes/No or multiple choice):
- Answer with ONLY the exact option text provided
- If partially present, answer "Partial" if that's an option, otherwise "No" with explanation in notes
- If not applicable, answer "Not applicable"

For text questions:
- Provide specific, factual information found in the metadata
- If not found, state "Not found in metadata"
"""
        
        user_prompt = f"""Based on the following metadata, answer this question:

{metadata_context}

---

Section: {section}
Question: {title}
"""
        
        if description and str(description) != 'nan':
            user_prompt += f"Description: {description}\n"
        
        if question_type == 'choiceQuestion' and options and str(options) != 'nan':
            user_prompt += f"Response Options: {options}\n"
        
        user_prompt += """
Provide your response in the following JSON format:
{
    "response": "your answer here",
    "evidence": "specific evidence from metadata",
    "notes": "any additional context or caveats"
}
"""
        
        try:
            llm_response = self._call_llm(system_prompt, user_prompt)
            
            # Parse JSON response
            # Try to extract JSON if it's wrapped in markdown
            if "```json" in llm_response:
                llm_response = llm_response.split("```json")[1].split("```")[0].strip()
            elif "```" in llm_response:
                llm_response = llm_response.split("```")[1].split("```")[0].strip()
            
            result = json.loads(llm_response)
            
            return {
                "response": result.get("response", ""),
                "evidence": result.get("evidence", ""),
                "notes": result.get("notes", "")
            }
            
        except Exception as e:
            print(f"Error processing question '{title}': {e}")
            return {
                "response": "Error processing",
                "evidence": "",
                "notes": f"Error: {str(e)}"
            }
    
    def process_all_questions(self, batch_size: int = 5, delay_between_calls: float = 0.5) -> List[Dict[str, Any]]:
        """
        Process all questions from the form.
        
        Args:
            batch_size: Process questions in batches (for progress tracking)
            delay_between_calls: Delay in seconds between API calls to avoid rate limits
            
        Returns:
            List of response dictionaries
        """
        if self.form_questions is None:
            raise ValueError("Form questions not loaded. Call load_form_questions() first.")
        
        if not self.metadata_content:
            raise ValueError("No metadata loaded. Call load_metadata_files() first.")
        
        # Build metadata context once
        metadata_context = self._build_context_prompt()
        
        responses = []
        total = len(self.form_questions)
        
        print(f"\nProcessing {total} questions...")
        
        for idx, row in self.form_questions.iterrows():
            # Progress indicator
            if idx % batch_size == 0:
                print(f"Progress: {idx}/{total} questions processed")
            
            result = self.answer_question(row, metadata_context)
            
            # Skip non-question items
            if result is None:
                continue
            
            response_entry = {
                "section": row.get('section', ''),
                "question": row.get('title', ''),
                "response_choices": row.get('options', ''),
                "response": result["response"],
                "evidence": result["evidence"],
                "notes": result["notes"]
            }
            
            responses.append(response_entry)
            
            # Add delay between API calls to avoid rate limits
            if delay_between_calls > 0:
                time.sleep(delay_between_calls)
        
        print(f"Completed: {len(responses)} responses generated\n")
        return responses
    
    def generate_summary(self, responses: List[Dict], dataset_name: str = "Unknown Dataset") -> Dict:
        """Generate overall summary insights from the evaluation responses."""
        print("Generating evaluation summary...")

        summary_prompt = f"""
You are assessing the FAIRness of the dataset "{dataset_name}" based on structured evaluation responses.
Summarize the key strengths and weaknesses, provide an overall assessment paragraph, and estimate FAIR scores.

Provide a JSON object with this structure:
{{
  "strengths": ["..."],
  "weaknesses": ["..."],
  "overall_assessment": "...",
  "fair_score_estimate": {{
    "findable": "score/10 - explanation",
    "accessible": "score/10 - explanation",
    "interoperable": "score/10 - explanation",
    "reusable": "score/10 - explanation"
  }}
}}

Use evidence-based observations. If information is missing, mention it explicitly. Return ONLY the JSON.
"""

        # Append evaluation responses grouped by section for context
        sections: Dict[str, List[str]] = {}
        for item in responses:
            section = item.get("section", "Unknown") or "Unknown"
            sections.setdefault(section, []).append(
                f"Question: {item.get('question', '')}\nResponse: {item.get('response', '')}\nNotes: {item.get('notes', '')}\n"
            )

        for section, entries in sections.items():
            summary_prompt += f"\n### {section}\n" + "\n".join(entries[:10])

        summary_text = ""
        raw_content = None

        try:
            if self.llm_provider in ["openai", "azure"]:
                completion_kwargs = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are an expert in FAIR data evaluation providing JSON summaries."},
                        {"role": "user", "content": summary_prompt}
                    ],
                }
                if self.llm_provider == "azure":
                    completion_kwargs["max_completion_tokens"] = 1500
                else:
                    completion_kwargs["max_tokens"] = 1500
                    completion_kwargs["temperature"] = 0.1

                # For standard OpenAI, request strict JSON; for Azure, avoid
                # response_format to match the working question-answer calls.
                if self.llm_provider == "openai":
                    completion_kwargs["response_format"] = {"type": "json_object"}

                response = self.client.chat.completions.create(**completion_kwargs)
                raw_content = response.choices[0].message.content
                summary_text = self._extract_message_text(raw_content).strip()
            else:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1500,
                    temperature=0.1,
                    system="You are an expert in FAIR data evaluation providing JSON summaries.",
                    messages=[{"role": "user", "content": summary_prompt}]
                )
                summary_text = response.content[0].text.strip()

            # Normalize LLM output to a clean JSON string
            raw = summary_text.strip()

            # Remove markdown fencing if present (```json ... ``` or ``` ... ```)
            if raw.startswith("```"):
                parts = raw.split("```")
                # Take the first non-empty fenced block
                for part in parts[1:]:
                    if part.strip():
                        raw = part.strip()
                        break

            # Drop an optional leading 'json' language tag
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()

            # First attempt: parse as-is
            try:
                summary_data = json.loads(raw)
            except json.JSONDecodeError:
                # Second attempt: extract the first top-level JSON object
                start = raw.find("{")
                end = raw.rfind("}")
                if start != -1 and end != -1 and end > start:
                    candidate = raw[start:end + 1]
                    summary_data = json.loads(candidate)
                else:
                    # Re-raise to be handled by outer except
                    raise

            print("Summary generated")
            return summary_data

        except json.JSONDecodeError as exc:
            # JSON parsing failed – log and fall back to using raw text
            print(f"Warning: Unable to parse summary JSON: {exc}")
            print(f"Raw summary response: {summary_text}")
        except Exception as exc:
            # Any other error during summary generation
            print(f"Error generating summary: {exc}")

        # Fallback summary that still preserves whatever the model returned
        if (summary_text is None or not str(summary_text).strip()) and raw_content is not None:
            # If we never got usable text, show the raw content structure for debugging
            try:
                fallback_text = json.dumps(raw_content, ensure_ascii=False, default=str)
            except Exception:
                fallback_text = str(raw_content)
        else:
            fallback_text = summary_text or "Summary could not be generated due to an error."
        return {
            "strengths": [
                "Automated JSON summary generation failed; see overall_assessment for raw summary text."
            ],
            "weaknesses": [
                "Summary JSON could not be parsed or generated reliably; FAIR sub-scores are set to N/A."
            ],
            "overall_assessment": fallback_text,
            "fair_score_estimate": {
                "findable": "N/A",
                "accessible": "N/A",
                "interoperable": "N/A",
                "reusable": "N/A"
            }
        }

    def save_json_output(self, responses: List[Dict], output_path: str, 
                        dataset_name: str = "Unknown Dataset", output_dir: Optional[Path] = None,
                        summary: Dict = None):
        """Save responses in JSON format following the template structure."""
        output = {
            "metadata": {
                "generated_date": datetime.now().strftime("%Y-%m-%d"),
                "dataset_evaluated": dataset_name,
                "evaluation_method": "Automated analysis using FAIR4AI Agent with LLM",
                "source_files": list(self.metadata_content.keys()),
                "llm_provider": self.llm_provider,
                "llm_model": self.model
            },
            "responses": responses
        }

        if summary:
            output["summary"] = summary
        
        if output_dir:
            json_path = output_dir / f"{Path(output_path).stem}.json"
        else:
            json_path = Path(output_path).with_suffix('.json')
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"JSON output saved to: {json_path}")
        return json_path
    
    def save_csv_output(self, responses: List[Dict], output_path: str, output_dir: Optional[Path] = None):
        """Save responses in CSV format following the template structure."""
        if output_dir:
            csv_path = output_dir / f"{Path(output_path).stem}.csv"
        else:
            csv_path = Path(output_path).with_suffix('.csv')
        
        # Convert to DataFrame and save
        df = pd.DataFrame(responses)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        print(f"CSV output saved to: {csv_path}")
        return csv_path
    
    def run_evaluation(self, form_csv: str, metadata_files: List[str] = None, 
                      output_prefix: str = "evaluation", dataset_name: str = None,
                      dataset_url: str = None, output_dir: str = None) -> tuple:
        """
        Run complete evaluation workflow.
        
        Args:
            form_csv: Path to form questions CSV
            metadata_files: List of metadata file paths
            output_prefix: Prefix for output files
            dataset_name: Name of dataset being evaluated
            
        Returns:
            Tuple of (json_path, csv_path)
        """
        print("=" * 70)
        print("FAIR4AI Automated Dataset Evaluation")
        print("=" * 70)
        print(f"LLM Provider: {self.llm_provider}")
        print(f"Model: {self.model}")
        print()
        
        # Create output directory if specified
        output_directory = None
        if output_dir:
            output_directory = Path(output_dir)
            output_directory.mkdir(parents=True, exist_ok=True)
            print(f"Output directory: {output_directory}")
            print()
        
        # Load data
        self.load_form_questions(form_csv)
        
        # Load metadata from URL or files
        if dataset_url:
            print(f"Loading metadata from URL: {dataset_url}\n")
            self.extract_metadata_from_url(dataset_url, output_directory)
        
        if metadata_files:
            self.load_metadata_files(metadata_files)
        
        if not self.metadata_content:
            raise ValueError("No metadata loaded. Provide either metadata files or a dataset URL.")
        
        # Infer dataset name from metadata if not provided
        if dataset_name is None:
            # Try to extract from schema.org metadata
            for content in self.metadata_content.values():
                if isinstance(content, list) and len(content) > 0:
                    if '@type' in content[0] and content[0]['@type'] == 'Dataset':
                        dataset_name = content[0].get('name', 'Unknown Dataset')
                        break
                elif isinstance(content, dict):
                    if content.get('@type') == 'Dataset':
                        dataset_name = content.get('name', 'Unknown Dataset')
                        break
            
            if dataset_name is None:
                dataset_name = "Unknown Dataset"
        
        print(f"Evaluating: {dataset_name}\n")
        
        # Process questions
        responses = self.process_all_questions()
        
        # Generate summary
        summary = self.generate_summary(responses, dataset_name)
        
        # Save outputs
        json_path = self.save_json_output(responses, output_prefix, dataset_name, output_directory, summary)
        csv_path = self.save_csv_output(responses, output_prefix, output_directory)
        
        print("\n" + "=" * 70)
        print("Evaluation Complete!")
        print("=" * 70)
        
        return json_path, csv_path


def main():
    """Command-line interface for the FAIR4AI agent."""
    parser = argparse.ArgumentParser(
        description="Automated FAIR4AI dataset evaluation using LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate NEON dataset with OpenAI
  python fair4ai_agent.py --metadata metadata_downloads/*.json --output neon_eval
  
  # Use Anthropic Claude instead
  python fair4ai_agent.py --provider anthropic --metadata metadata_downloads/*.json --output neon_eval
  
  # Specify custom model
  python fair4ai_agent.py --model gpt-4o --metadata metadata_downloads/*.json --output neon_eval
"""
    )
    
    parser.add_argument(
        '--form',
        default='form_ai_checklist_automated.csv',
        help='Path to form questions CSV (default: form_ai_checklist_automated.csv)'
    )
    
    parser.add_argument(
        '--metadata',
        nargs='+',
        help='Path(s) to metadata JSON file(s)'
    )
    
    parser.add_argument(
        '--url',
        help='Dataset landing page URL to extract metadata from'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory for all files (results and downloaded metadata)'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Output file prefix (without extension)'
    )
    
    parser.add_argument(
        '--dataset-name',
        help='Name of dataset being evaluated (auto-detected if not provided)'
    )
    
    parser.add_argument(
        '--provider',
        choices=['openai', 'azure', 'anthropic'],
        default='openai',
        help='LLM provider to use (default: openai)'
    )
    
    parser.add_argument(
        '--model',
        help='Specific model to use (default: gpt-4o-mini for OpenAI, claude-3-5-sonnet for Anthropic, or deployment name for Azure)'
    )
    
    parser.add_argument(
        '--azure-endpoint',
        help='Azure OpenAI endpoint URL (e.g., https://your-resource.openai.azure.com/)'
    )
    
    parser.add_argument(
        '--azure-api-version',
        help='Azure OpenAI API version (default: 2024-08-01-preview)'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.metadata and not args.url:
        print("Error: Either --metadata or --url must be provided", file=sys.stderr)
        sys.exit(1)
    
    # Create agent and run evaluation
    agent = FAIR4AIAgent(
        llm_provider=args.provider, 
        model=args.model,
        azure_endpoint=args.azure_endpoint if args.provider == 'azure' else None,
        azure_api_version=args.azure_api_version if args.provider == 'azure' else None
    )
    
    try:
        agent.run_evaluation(
            form_csv=args.form,
            metadata_files=args.metadata,
            output_prefix=args.output,
            dataset_name=args.dataset_name,
            dataset_url=args.url,
            output_dir=args.output_dir
        )
    except Exception as e:
        print(f"\nError during evaluation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
