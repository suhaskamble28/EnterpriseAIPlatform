import time
import requests

from prometheus_client import Counter, Histogram, start_http_server


# ---------------------------------------------------------
# Prometheus Metrics
# ---------------------------------------------------------

AI_REQUESTS = Counter(
    "ai_requests_total",
    "Total number of AI/LLM requests",
    ["model", "operation"]
)

AI_ERRORS = Counter(
    "ai_errors_total",
    "Total number of AI/LLM errors",
    ["model", "operation"]
)

AI_REQUEST_DURATION = Histogram(
    "ai_request_duration_seconds",
    "AI/LLM request duration in seconds",
    ["model", "operation"]
)

AI_INPUT_TOKENS = Counter(
    "ai_input_tokens_total",
    "Total input tokens",
    ["model"]
)

AI_OUTPUT_TOKENS = Counter(
    "ai_output_tokens_total",
    "Total output tokens",
    ["model"]
)


# ---------------------------------------------------------
# Ollama Configuration
# ---------------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"


# ---------------------------------------------------------
# AI Request
# ---------------------------------------------------------

def ask_ollama(prompt):

    operation = "llm_generate"

    AI_REQUESTS.labels(
        model=MODEL,
        operation=operation
    ).inc()

    start_time = time.time()

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        response_json = response.json()
        prompt_tokens = response_json.get("prompt_eval_count",0)
        output_tokens = response_json.get("eval_count",0)
        AI_INPUT_TOKENS.labels(model=MODEL).inc(prompt_tokens)
        AI_OUTPUT_TOKENS.labels(model=MODEL).inc(output_tokens)

        return response.json()["response"]

    except Exception:

        AI_ERRORS.labels(
            model=MODEL,
            operation=operation
        ).inc()

        raise

    finally:

        duration = time.time() - start_time

        AI_REQUEST_DURATION.labels(
            model=MODEL,
            operation=operation
        ).observe(duration)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    # Prometheus metrics endpoint
    start_http_server(8000)

    print("AI Observability Service started")
    print("Metrics available at: http://localhost:8000/metrics")

    while True:

        prompt = input("\nEnter your question (or 'exit'): ")

        if prompt.lower() == "exit":
            break

        try:

            start = time.time()

            answer = ask_ollama(prompt)

            total_time = time.time() - start

            print("\nAnswer:")
            print(answer)

            print(f"\nLatency: {total_time:.2f} seconds")

        except Exception as e:

            print(f"\nERROR: {e}")