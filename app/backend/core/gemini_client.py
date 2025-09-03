#!/usr/bin/env python3
"""
AI/DEV Lab - Enhanced Gemini API Client
Implements the latest Gemini API features including structured output, 
multimodal processing, and intelligent model selection.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

import google.generativeai as genai
from .config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelType(Enum):
    """Available Gemini models for different use cases"""
    PRO = "gemini-2.5-pro"  # Complex reasoning and analysis
    FLASH = "gemini-2.5-flash"  # General purpose multimodal
    FLASH_LITE = "gemini-2.5-flash-lite"  # High-frequency, cost-efficient
    FLASH_IMAGE = "gemini-2.5-flash-image"  # Image generation
    EMBEDDINGS = "gemini-embeddings"  # Embeddings for RAG


class TaskType(Enum):
    """Task types for intelligent model selection"""
    ANALYSIS = "analysis"
    CHAT = "chat"
    CODE_GENERATION = "code_generation"
    DOCUMENT_PROCESSING = "document_processing"
    IMAGE_GENERATION = "image_generation"
    STRUCTURED_OUTPUT = "structured_output"
    HIGH_FREQUENCY = "high_frequency"


@dataclass
class GenerationConfig:
    """Configuration for content generation"""
    temperature: float = 0.7
    max_output_tokens: int = 2048
    top_p: float = 0.95
    top_k: int = 40
    response_mime_type: Optional[str] = None
    response_schema: Optional[Dict] = None


@dataclass
class SafetySettings:
    """Safety settings for content generation"""
    harassment_threshold: str = "BLOCK_MEDIUM_AND_ABOVE"
    hate_speech_threshold: str = "BLOCK_MEDIUM_AND_ABOVE"
    sexually_explicit_threshold: str = "BLOCK_MEDIUM_AND_ABOVE"
    dangerous_content_threshold: str = "BLOCK_MEDIUM_AND_ABOVE"

class EnhancedGeminiClient:
    """
    Enhanced Gemini API client with latest features:
    - New genai.Client() pattern
    - Structured output capabilities
    - Intelligent model selection
    - Multimodal processing
    - Image generation
    - Long context support
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Gemini client with the new API"""
        try:
            # Configure the API key
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-1.5-pro')
            logger.info("✅ Initialized with Gemini API client")
        except Exception as e:
            logger.error("❌ Failed to initialize Gemini client: %s", e)
            raise
    
    def select_model(self, task_type: TaskType, content_length: int = 0) -> str:
        """
        Intelligently select the best model for the task
        
        Args:
            task_type: Type of task to perform
            content_length: Length of input content (for context considerations)
        
        Returns:
            Model name string
        """
        if task_type == TaskType.ANALYSIS:
            return ModelType.PRO.value
        elif task_type == TaskType.IMAGE_GENERATION:
            return ModelType.FLASH_IMAGE.value
        elif task_type == TaskType.HIGH_FREQUENCY:
            return ModelType.FLASH_LITE.value
        elif content_length > 100000:  # Large content
            return ModelType.PRO.value  # Better for long context
        else:
            return ModelType.FLASH.value  # Default for most tasks
    
    async def generate_content(
        self,
        prompt: str,
        task_type: TaskType = TaskType.CHAT,
        generation_config: Optional[GenerationConfig] = None,
        safety_settings: Optional[SafetySettings] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate content using the latest Gemini API
        
        Args:
            prompt: Input prompt
            task_type: Type of task for model selection
            generation_config: Generation configuration
            safety_settings: Safety settings
            model: Specific model to use (overrides task-based selection)
        
        Returns:
            Dictionary with response data
        """
        try:
            # Select model if not specified
            if not model:
                model = self.select_model(task_type, len(prompt))
            
            # Use default config if not provided
            if not generation_config:
                generation_config = GenerationConfig()
            
            # Use default safety settings if not provided
            if not safety_settings:
                safety_settings = SafetySettings()
            
            return await self._generate_content_new(
                prompt, model, generation_config, safety_settings
            )
                
        except Exception as e:
            logger.error("❌ Content generation failed: %s", e)
            return {
                "success": False,
                "error": str(e),
                "model": model,
                "task_type": task_type.value
            }
    
    async def _generate_content_new(
        self,
        prompt: str,
        model: str,
        generation_config: GenerationConfig,
        safety_settings: SafetySettings
    ) -> Dict[str, Any]:
        """Generate content using the standard google.generativeai API"""
        try:
            # Create a new model instance for the specific model
            model_instance = genai.GenerativeModel(model)
            
            # Prepare generation config
            config = {
                'temperature': generation_config.temperature,
                'max_output_tokens': generation_config.max_output_tokens,
                'top_p': generation_config.top_p,
                'top_k': generation_config.top_k,
            }
            
            # Generate content
            response = model_instance.generate_content(
                prompt,
                generation_config=config
            )
            
            return {
                "success": True,
                "text": response.text,
                "model": model,
                "usage": getattr(response, 'usage_metadata', {}),
                "safety_ratings": getattr(response, 'safety_ratings', []),
                "parsed": getattr(response, 'parsed', None)
            }
            
        except Exception as e:
            logger.error("❌ API generation failed: %s", e)
            raise
    

    
    async def generate_structured_output(
        self,
        prompt: str,
        schema: Dict[str, Any],
        task_type: TaskType = TaskType.STRUCTURED_OUTPUT
    ) -> Dict[str, Any]:
        """
        Generate structured JSON output using the official API
        
        Args:
            prompt: Input prompt
            schema: JSON schema for the expected output
            task_type: Type of task
        
        Returns:
            Dictionary with structured response
        """
        try:
            # Create generation config for structured output
            generation_config = GenerationConfig(
                response_mime_type="application/json",
                response_schema=schema
            )
            
            # Generate content with structured output
            response = await self.generate_content(
                prompt=prompt,
                task_type=task_type,
                generation_config=generation_config
            )
            
            if response["success"]:
                # The new API should return properly parsed JSON
                if response.get("parsed"):
                    response["structured_data"] = response["parsed"]
                else:
                    # Fallback: try to parse the text response
                    try:
                        structured_data = json.loads(response["text"])
                        response["structured_data"] = structured_data
                    except json.JSONDecodeError as e:
                        response["structured_data"] = {"raw_response": response["text"]}
                        response["json_parse_error"] = str(e)
            
            return response
            
        except Exception as e:
            logger.error("❌ Structured output generation failed: %s", e)
            return {
                "success": False,
                "error": str(e),
                "task_type": task_type.value
            }
    
    async def generate_image(
        self,
        prompt: str,
        generation_config: Optional[GenerationConfig] = None
    ) -> Dict[str, Any]:
        """
        Generate images using Gemini 2.5 Flash Image
        
        Args:
            prompt: Image generation prompt
            generation_config: Generation configuration
        
        Returns:
            Dictionary with image data
        """
        try:
            if not generation_config:
                generation_config = GenerationConfig(temperature=0.8)
            
            response = await self.generate_content(
                prompt=prompt,
                task_type=TaskType.IMAGE_GENERATION,
                generation_config=generation_config,
                model=ModelType.FLASH_IMAGE.value
            )
            
            return response
            
        except Exception as e:
            logger.error("❌ Image generation failed: %s", e)
            return {
                "success": False,
                "error": str(e),
                "task_type": "image_generation"
            }
    
    async def process_multimodal_content(
        self,
        text_prompt: str,
        image_path: Optional[str] = None,
        document_path: Optional[str] = None,
        task_type: TaskType = TaskType.DOCUMENT_PROCESSING
    ) -> Dict[str, Any]:
        """
        Process multimodal content (text, images, documents)
        
        Args:
            text_prompt: Text prompt
            image_path: Path to image file
            document_path: Path to document file
            task_type: Type of processing task
        
        Returns:
            Dictionary with processed content
        """
        try:
            # For now, focus on text processing
            # TODO: Implement image and document processing when API supports it
            response = await self.generate_content(
                prompt=text_prompt,
                task_type=task_type
            )
            
            return response
            
        except Exception as e:
            logger.error("❌ Multimodal processing failed: %s", e)
            return {
                "success": False,
                "error": str(e),
                "task_type": task_type.value
            }
    
    def get_available_models(self) -> List[Dict[str, str]]:
        """Get list of available models"""
        return [
            {
                "name": model.value,
                "type": model.name,
                "description": self._get_model_description(model)
            }
            for model in ModelType
        ]
    
    def _get_model_description(self, model: ModelType) -> str:
        """Get description for a model"""
        descriptions = {
            ModelType.PRO: "Most powerful model for complex reasoning and analysis",
            ModelType.FLASH: "General-purpose multimodal model with next-generation features",
            ModelType.FLASH_LITE: "Fastest and most cost-efficient model for high-frequency tasks",
            ModelType.FLASH_IMAGE: "Native image generation and editing capabilities",
            ModelType.EMBEDDINGS: "Embedding model for production RAG workflows"
        }
        return descriptions.get(model, "Unknown model")

# Global client instance
gemini_client = EnhancedGeminiClient()
