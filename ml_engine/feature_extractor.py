"""Feature extraction from network flow data."""
import numpy as np


class FeatureExtractor:
    """Extracts numerical features from network flow events."""
    
    def __init__(self):
        # Protocol encoding
        self.protocol_map = {"TCP": 0, "UDP": 1, "ICMP": 2}
    
    def extract(self, flow):
        """
        Extract feature vector from a network flow.
        
        Args:
            flow: Dictionary containing flow data
            
        Returns:
            numpy array of features or None if extraction fails
        """
        try:
            features = []
            
            # Basic features
            features.append(float(flow.get("bytes", 0)))
            features.append(float(flow.get("packets", 0)))
            features.append(float(flow.get("duration", 0)))
            
            # Protocol encoding
            protocol = flow.get("protocol", "TCP")
            protocol_val = self.protocol_map.get(protocol, 0)
            features.append(float(protocol_val))
            
            # Derived features
            bytes_per_packet = flow.get("bytes", 0) / max(flow.get("packets", 1), 1)
            features.append(bytes_per_packet)
            
            # Port features (normalized)
            src_port = flow.get("src_port", 0)
            dst_port = flow.get("dst_port", 0)
            features.append(src_port / 65535.0)
            features.append(dst_port / 65535.0)
            
            # Flow rate (bytes per second)
            duration = flow.get("duration", 0.1)
            flow_rate = flow.get("bytes", 0) / max(duration, 0.1)
            features.append(flow_rate)
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def extract_batch(self, flows):
        """
        Extract features from multiple flows.
        
        Args:
            flows: List of flow dictionaries
            
        Returns:
            numpy array of features (n_samples, n_features)
        """
        feature_list = []
        for flow in flows:
            features = self.extract(flow)
            if features is not None:
                feature_list.append(features[0])
        
        if len(feature_list) > 0:
            return np.array(feature_list)
        return None

