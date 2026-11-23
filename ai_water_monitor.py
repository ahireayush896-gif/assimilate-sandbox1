"""
AI Water & Resource Consumption Monitoring Module.
Tracks and mitigates water footprints and resource utilization for AI model inference and training.
"""

from typing import Dict, Any, Optional

class AIWaterMonitor:
    """Monitors water consumption (cooling, electricity generation, etc.) for AI models."""
    
    # Average liters of water consumed per kWh / inference / generation tier
    DEFAULT_WATER_INTENSITY_LITERS_PER_KWH = 1.8
    
    def __init__(self, model_name: str = "DefaultAIModel"):
        self.model_name = model_name
        self.total_queries = 0
        self.total_tokens_processed = 0
        self.total_water_consumed_ml = 0.0

    def estimate_inference_water(self, tokens_count: int, water_intensity_per_token_ml: float = 0.5) -> Dict[str, Any]:
        """
        Estimates the water consumption (in milliliters) for processing a given number of tokens.
        """
        if tokens_count < 0:
            tokens_count = 0
            
        water_ml = tokens_count * water_intensity_per_token_ml
        self.total_queries += 1
        self.total_tokens_processed += tokens_count
        self.total_water_consumed_ml += water_ml
        
        return {
            "model_name": self.model_name,
            "tokens_processed": tokens_count,
            "water_consumed_ml": round(water_ml, 2),
            "water_consumed_liters": round(water_ml / 1000.0, 4),
            "total_cumulative_water_ml": round(self.total_water_consumed_ml, 2),
            "message": f"AI model '{self.model_name}' consumed ~{water_ml:.2f} ml of water for {tokens_count} tokens."
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Returns aggregate water footprint statistics for the model session."""
        return {
            "model_name": self.model_name,
            "total_queries": self.total_queries,
            "total_tokens_processed": self.total_tokens_processed,
            "total_water_consumed_ml": round(self.total_water_consumed_ml, 2),
            "total_water_consumed_liters": round(self.total_water_consumed_ml / 1000.0, 4)
        }


def report_ai_water_footprint(model_name: str, tokens: int) -> Dict[str, Any]:
    """Helper function to quickly generate an AI water consumption report."""
    monitor = AIWaterMonitor(model_name)
    return monitor.estimate_inference_water(tokens)
