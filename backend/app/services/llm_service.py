"""
LLM Service - Handles AI model integrations
==========================================
Primary: Groq (free tier, fast)
Fallback: Google Gemini (free tier)
"""

import logging
import os

import google.generativeai as genai

logger = logging.getLogger("ai_sdlc_copilot")


class LLMService:
    """Service for interacting with LLM providers."""

    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self._gemini_model = None
        self._groq_client = None

        if self.groq_key:
            from groq import Groq

            self._groq_client = Groq(api_key=self.groq_key)
            logger.info("✅ Groq configured (primary)")
        else:
            logger.warning("⚠️ GROQ_API_KEY not set")

        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self._gemini_model = genai.GenerativeModel("gemini-2.0-flash")
            logger.info("✅ Gemini configured (fallback ready)")
        else:
            logger.warning("⚠️ GEMINI_API_KEY not set (no fallback)")

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text using available LLM.
        Tries Groq first (fast), falls back to Gemini if configured.
        """
        # Try Groq first (primary)
        if self._groq_client:
            try:
                return await self._generate_groq(prompt, system_prompt, max_tokens, temperature)
            except Exception as e:
                logger.error(f"Groq error: {e}")
                if self._gemini_model:
                    logger.info("Falling back to Gemini...")
                    return await self._generate_gemini(
                        prompt, system_prompt, max_tokens, temperature
                    )
                else:
                    raise

        # Fallback to Gemini (if no Groq configured)
        if self._gemini_model:
            return await self._generate_gemini(prompt, system_prompt, max_tokens, temperature)

        raise ValueError("No LLM configured. Set GROQ_API_KEY or GEMINI_API_KEY.")

    async def _generate_gemini(
        self,
        prompt: str,
        system_prompt: str | None,
        max_tokens: int,
        temperature: float = 0.7,
    ) -> str:
        """Generate using Google Gemini."""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = self._gemini_model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
            ),
        )
        return response.text

    async def _generate_groq(
        self,
        prompt: str,
        system_prompt: str | None,
        max_tokens: int,
        temperature: float = 0.7,
    ) -> str:
        """Generate using Groq (Llama 3.3)."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self._groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content


# Singleton instance
_llm_service: LLMService | None = None


def get_llm_service() -> LLMService:
    """Get or create LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
