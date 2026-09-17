from prometheus_client import Counter, Histogram


llm_requests_total = Counter(
    "resolveai_llm_requests_total",
    "Total number of LLM requests",
    ["model"],
)

llm_errors_total = Counter(
    "resolveai_llm_errors_total",
    "Total number of failed LLM requests",
    ["model"],
)

llm_request_duration_seconds = Histogram(
    "resolveai_llm_request_duration_seconds",
    "LLM request duration in seconds",
    ["model"],
)

llm_input_tokens_total = Counter(
    "resolveai_llm_input_tokens_total",
    "Total number of LLM input tokens",
    ["model"],
)

llm_output_tokens_total = Counter(
    "resolveai_llm_output_tokens_total",
    "Total number of LLM output tokens",
    ["model"],
)