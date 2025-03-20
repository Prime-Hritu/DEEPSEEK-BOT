from enum import Enum


class MODELS(Enum):
    DEEPSEEKV3 = "deepseek-ai/DeepSeek-V3"
    DEEPSEEKR1 = "deepseek-ai/DeepSeek-R1"
    DEEPSEEKR1DISTILLQWEN14B = "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
    DEEPSEEKR1DISTILLQWEN15B = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    NONE = None
