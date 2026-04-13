import sys
import json
from features import extract_features
from db import insert_tracks
from db import get_all_tracks
from recommendations import find_similar_tracks
from ml_recommendations import get_ml_recommendations
from db import delete_track


#dodanie tracku: python3 cli.py "nazwa pliku audio"

if len(sys.argv) < 2:
    print("Use: python3 cli.py <audio_file>")
    sys.exit(1)
    
elif sys.argv[1] == "tracks":
        tracks = get_all_tracks()
        for track in tracks:
            print(track)
        
        # reference_track = tracks[0]
        # result = find_similar_tracks(reference_track,tracks)
        # print(result)
elif sys.argv[1] == "similar":
    if len(sys.argv) < 3:
        print("tehers no track name")
        sys.exit(1)
    path = sys.argv[2]
    tracks = get_all_tracks()
    reference_track = None 
    for track in tracks:
        if track["path"] == path:
            reference_track  = track
            break 
    if reference_track is None:
            print("track not found")
            sys.exit(1) 
    
    
    result = find_similar_tracks(reference_track,tracks)
    for item in result:
        a = item["track"]["path"]
        b = item["similarity"]
        print(a,b)
#wywolanie knn 
elif sys.argv[1] == "knn":
    if len(sys.argv) < 3:
        print("tehers no track name")
        sys.exit(1)
    path = sys.argv[2]
    tracks = get_all_tracks()
    reference_track = None 
    for track in tracks:
        if track["path"] == path:
            reference_track  = track
            break
    if reference_track is None:
            print("track not found")
            sys.exit(1) 
    results = get_ml_recommendations(reference_track)
    for i, result in enumerate(results, start=1):
        track = result["track"]
    
        print(f"{i}. Track: {track['path']}")
        print(f"Key: {track['key']}")
        print(f"Score: {result['final_score']:.3f}")
        print()
elif sys.argv[1] == "delete":
    if len(sys.argv) < 3:
        print("tehers no track name")
        sys.exit(1)
    path = sys.argv[2]
    delete_track(path)
else:
    
    path = sys.argv[1]

    result = extract_features(path)
    insert_tracks(path, result)

    print(json.dumps(result, indent=2))

    
