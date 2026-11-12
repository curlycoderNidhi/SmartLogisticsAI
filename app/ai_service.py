class LogisticsAIService:
    @staticmethod
    def analyze_shipment(distance_km: float, weather: str, status: str):
        risk_score = 10.0  # Base risk
        reasons = []

        # 1. Distance Factor
        if distance_km > 1000:
            risk_score += 30.0
            reasons.append("Long-haul route (>1000km)")
        elif distance_km > 500:
            risk_score += 15.0

        # 2. Weather Impact Analysis
        weather_risks = {
            "Storm": (45.0, "Severe storm alert"),
            "Fog": (25.0, "Low visibility fog"),
            "Rain": (15.0, "Wet road conditions"),
            "Clear": (0.0, "")
        }
        w_score, w_reason = weather_risks.get(weather, (10.0, "Unverified weather"))
        risk_score += w_score
        if w_reason:
            reasons.append(w_reason)

        # Cap risk at 100
        risk_score = min(risk_score, 100.0)

        # 3. Automated Actionable Recommendation
        if status == "Delivered":
            recommendation = "COMPLETED: Shipment delivered safely. Archive record."
        elif risk_score >= 60:
            recommendation = f"HIGH RISK ({risk_score}%): {', '.join(reasons)}. Action: Trigger proactive customer delay notice & reroute."
        elif risk_score >= 35:
            recommendation = f"MODERATE RISK ({risk_score}%): {', '.join(reasons)}. Action: Monitor GPS checkpoints closely."
        else:
            recommendation = f"LOW RISK ({risk_score}%): Optimal transit conditions. On schedule."

        return risk_score, recommendation