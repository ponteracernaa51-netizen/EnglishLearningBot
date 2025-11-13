import logging
import json
from typing import Optional
import config
import google.generativeai as genai

logger = logging.getLogger(__name__)

_model: Optional[genai.GenerativeModel] = None


def _init_model() -> Optional[genai.GenerativeModel]:
    global _model
    if _model is not None:
        return _model
    
    if not config.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY не найден в переменных окружения.")
        return None
    
    try:
        genai.configure(api_key=config.GEMINI_API_KEY)
        _model = genai.GenerativeModel('gemini-flash-latest')
        logger.info(f"Модель Gemini '{_model.model_name}' успешно инициализирована.")
        return _model
    except Exception as e:
        logger.error(f"Ошибка при инициализации Gemini: {e}")
        return None


async def check_translation(
    original_phrase: str,
    user_translation: str,
    source_lang: str,
    target_lang: str,
    ui_lang: str,
) -> str:
    model = _init_model()
    if not model:
        return json.dumps({"error": "Сервис AI-проверки временно недоступен."})
    
    lang_map = {'ru': 'Russian', 'uz': 'Uzbek', 'en': 'English'}
    ui_language = lang_map.get(ui_lang, 'English')
    
    prompt = f"""You are an expert language teacher. Evaluate a translation.

Original phrase ({lang_map[source_lang]}): "{original_phrase}"
User's translation to {lang_map[target_lang]}: "{user_translation}"

Analyze the translation and respond ONLY with a valid JSON object.
The JSON must have these keys:
- "score": an integer from 0 to 10.
- "corrected_translation": a string with the ideal translation.
- "explanation": a brief, one-sentence explanation in {ui_language}.

Example:
{{
  "score": 8,
  "corrected_translation": "This is a correct sentence.",
  "explanation": "You used the wrong article, but the rest was perfect."
}}"""
    
    try:
        response = await model.generate_content_async(prompt)
        cleaned = response.text.strip().removeprefix('```json').removesuffix('```').strip()
        
        json.loads(cleaned)  # Validate JSON
        logger.info("Проверка через Gemini API успешно завершена.")
        return cleaned
    except json.JSONDecodeError:
        logger.error(f"Gemini вернул невалидный JSON: {response.text}")
        return json.dumps({"error": "Не удалось обработать ответ от AI."})
    except Exception as e:
        logger.error(f"Ошибка при вызове Gemini API: {e}", exc_info=True)
        return json.dumps({"error": "Произошла ошибка при проверке перевода."})
