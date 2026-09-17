import time

import ollama
from langsmith import traceable

from observability.llm_metrics import (
    llm_requests_total,
    llm_errors_total,
    llm_request_duration_seconds,
    llm_input_tokens_total,
    llm_output_tokens_total,
)


class LLMService:

    def __init__(self, model: str = "qwen2.5:3b"):
        self.model = model

    @traceable(
        name="llm.diagnosis",
        run_type="llm",
        process_outputs=lambda result: {
            "model": result["model"],
            "input_tokens": result["input_tokens"],
            "output_tokens": result["output_tokens"],
            "total_tokens": result["total_tokens"],
            "latency_ms": result["latency_ms"],
            "success": result["success"],
        },
    )
    def diagnose(self, evidence) -> dict:

        # Convert Pydantic model to dictionary when necessary
        if hasattr(evidence, "model_dump"):
            evidence = evidence.model_dump()

        prompt = f"""
You are an enterprise incident diagnosis assistant.

Analyze the following transaction evidence.

Transaction ID: {evidence.get("transaction_id")}
Service: {evidence.get("service")}
Business Outcome: {evidence.get("business_outcome")}
Failure Category: {evidence.get("failure_category")}
Failure Type: {evidence.get("failure_type")}
Dependency: {evidence.get("dependency_name")}
Dependency Type: {evidence.get("dependency_type")}
Message: {evidence.get("message")}

Provide a concise diagnosis with:
1. Root Cause
2. Business Impact
3. Recommended Next Step

Do not invent facts that are not present in the evidence.
"""

        # Count the LLM request
        llm_requests_total.labels(
            model=self.model
        ).inc()

        start_time = time.perf_counter()

        try:

            # Measure actual application-observed LLM latency
            with llm_request_duration_seconds.labels(
                model=self.model
            ).time():

                response = ollama.chat(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                )

            latency_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            # Extract token usage
            input_tokens = response.get(
                "prompt_eval_count",
                0,
            )

            output_tokens = response.get(
                "eval_count",
                0,
            )

            # Record token metrics
            llm_input_tokens_total.labels(
                model=self.model
            ).inc(input_tokens)

            llm_output_tokens_total.labels(
                model=self.model
            ).inc(output_tokens)

            return {
                "model": self.model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "latency_ms": latency_ms,
                "success": True,
                "diagnosis": response["message"]["content"],
            }

        except Exception:

            # Record failed LLM request
            llm_errors_total.labels(
                model=self.model
            ).inc()

            latency_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            return {
                "model": self.model,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "latency_ms": latency_ms,
                "success": False,
                "diagnosis": "LLM diagnosis failed",
            }