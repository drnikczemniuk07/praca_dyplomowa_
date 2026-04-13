from sklearn.preprocessing import MinMaxScaler
from db import get_all_tracks
from sklearn.neighbors import NearestNeighbors

circle_of_fifths = {
    "C" : 0,
    "G" : 1,
    "D" : 2,
    "A" : 3,
    "E" : 4,
    "B" : 5,
    "F#" : 6,
    "C#" : 7,
    "G#" : 8,
    "D#" : 9,
    "A#" : 10,
    "F" : 11
    
}

def track_to_vector(track):
    return[track["duration_sec"],track["rms_mean"], track["spectral_centroid_mean_hz"], track["spectral_rolloff_mean_hz"], track["tempo_bpm"]]


def prepare_vectors():
    vectors = []
    all_tracks = get_all_tracks()
    
    for track in all_tracks:
        vector = track_to_vector(track)
        vectors.append(vector)
         
        
    scaler = MinMaxScaler()
    normalized_vectors = scaler.fit_transform(vectors)

    return all_tracks, normalized_vectors    
    

        
    
def key_similarity(key_a, key_b):
    
    a = circle_of_fifths[key_a]
    b = circle_of_fifths[key_b]
    
    diff = abs(a -b)
    distance = min(diff, 12 - diff)
    
    score = 1 - (distance/6)
    return score 

def find_similar_tracks_knn(reference_track, all_tracks, normalized_vectors, limit = 5):
    model = NearestNeighbors(n_neighbors = limit + 1, metric = "euclidean" )
    model.fit(normalized_vectors)
    
    
    reference_index = None
    for index, track in enumerate(all_tracks):
        if track["path"] == reference_track["path"]:
            reference_index = index
            break
    if reference_index is None:
        return []
        
    reference_vector = [normalized_vectors[reference_index]]
    distances, indices = model.kneighbors(reference_vector)
    
    indices = indices[0]
    distances = distances[0]
    
    indices = indices[1:]
    distances = distances[1:]
    
    results = []
    for index, distance in zip(indices, distances):
        track = all_tracks[index]
        
        results.append( {
            "track" : track,
            "distance" : distance 
        })
    return results   
        
        
def knn_score(distance):
    score = 1 /( 1 + distance)
    return score 

def final_score(knn_score, key_score):
    final_score = (0.7 * knn_score) + (0.3 * key_score)
    return final_score 

def get_ml_recommendations(reference_track, limit = 5):
    
    all_tracks, normalized_vectors = prepare_vectors()
    
    results = find_similar_tracks_knn(reference_track, all_tracks, normalized_vectors, limit)
    
    final_results = []
    
    for result in results:
        candidate_track = result["track"]
        distance = result["distance"]
        candidate_key = candidate_track["key"]
        reference_key = reference_track["key"]
        key_score = key_similarity(reference_key, candidate_key)
        knn_score_value = knn_score(distance)
        final_score_value = final_score(knn_score_value, key_score)
        
        final_results.append({
            "track" : candidate_track,
            "distance" : distance, 
            "key_score" : key_score,
            "knn_score" : knn_score_value,
            "final_score" : final_score_value
            })
    final_results.sort(key= lambda item: item["final_score"], reverse= True )
    return final_results 