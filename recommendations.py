
bpm_max_difference = 20
centroid_max_difference = 3000
rolloff_max_difference = 4000


def compute_similarity(track_a, track_b):
    
    bpm_difference = abs(track_a["tempo_bpm"]- track_b["tempo_bpm"])
    bpm_score = 1 - (bpm_difference/bpm_max_difference)
    bpm_score = max(0, bpm_score)
    
    if track_a["key"] == track_b["key"]:
        key_score = 1
    else:
        key_score = 0 
        
    centroid_difference = abs(track_a["spectral_centroid_mean_hz"]- track_b["spectral_centroid_mean_hz"])
    centroid_score = 1 - (centroid_difference/centroid_max_difference)
    centroid_score = max(0, centroid_score)
    
    rolloff_difference = abs(track_a["spectral_rolloff_mean_hz"]- track_b["spectral_rolloff_mean_hz"])
    rolloff_score = 1 - (rolloff_difference/rolloff_max_difference)
    rolloff_score  = max(0, rolloff_score)
    
    similarity = (bpm_score + key_score + centroid_score + rolloff_score)/ 4
    return similarity

def find_similar_tracks(reference_track, all_tracks, limit=5):

    results = []

    for track in all_tracks:

        if track["path"] == reference_track["path"]:
            continue

        score = compute_similarity(reference_track, track)

        results.append({
            "track": track,
            "similarity": score
        })
    results.sort(key= lambda item: item["similarity"], reverse= True )
    
    return results


              


