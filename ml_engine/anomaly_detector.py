"""Anomaly detection using ML models."""
import numpy as np
import joblib
import os


class AnomalyDetector:
    """Wrapper for anomaly detection models."""
    
    def __init__(self, model_type="isolation_forest"):
        """
        Initialize anomaly detector.
        
        Args:
            model_type: Type of model ('isolation_forest', 'dbscan', 'autoencoder')
        """
        self.model_type = model_type
        self.model = None
        self.is_fitted = False
    
    def load_model(self, model_path):
        """
        Load a pre-trained model from file.
        
        Args:
            model_path: Path to the model file
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        self.model = joblib.load(model_path)
        self.is_fitted = True
        print(f"✅ Model loaded from {model_path}")
    
    def detect(self, X):
        """
        Detect anomalies in feature vectors.
        
        Args:
            X: Feature array (n_samples, n_features)
            
        Returns:
            tuple: (is_anomaly: bool, score: float)
        """
        if self.model is None or not self.is_fitted:
            raise ValueError("Model not loaded or not fitted")
        
        # Predict anomaly
        prediction = self.model.predict(X)
        is_anomaly = prediction[0] == -1  # Isolation Forest: -1 is anomaly
        
        # Get anomaly score
        if hasattr(self.model, 'decision_function'):
            score = self.model.decision_function(X)[0]
        elif hasattr(self.model, 'score_samples'):
            score = self.model.score_samples(X)[0]
        else:
            score = 0.0
        
        # Normalize score (lower is more anomalous)
        normalized_score = abs(score) if is_anomaly else 0.0
        
        return is_anomaly, normalized_score
    
    def detect_batch(self, X):
        """
        Detect anomalies in a batch of feature vectors.
        
        Args:
            X: Feature array (n_samples, n_features)
            
        Returns:
            tuple: (predictions: array, scores: array)
        """
        if self.model is None or not self.is_fitted:
            raise ValueError("Model not loaded or not fitted")
        
        predictions = self.model.predict(X)
        is_anomalies = predictions == -1
        
        if hasattr(self.model, 'decision_function'):
            scores = self.model.decision_function(X)
        elif hasattr(self.model, 'score_samples'):
            scores = self.model.score_samples(X)
        else:
            scores = np.zeros(len(X))
        
        return is_anomalies, scores

