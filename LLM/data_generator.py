import json

# Load JSON from file
with open("/content/ego4d_data/v1/annotations/narration.json", 'r') as f:
    dataLoaded = json.load(f)

with open("/content/ego4d_data/v1/annotations/narrationV8.json", "w") as f:
    data = {}
    ancientIUD = next(iter(dataLoaded))
    diff = 0
    for i, (video_uid, narration_pass) in enumerate(dataLoaded.items()):
        if ancientIUD != video_uid:
            diff = i
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
            data = {}
        #print(" fvzcjhbxq \n\n", narration_pass.keys(), "\n\n --- \n\n", i, "\n")
        if len(narration_pass.keys()) == 1 :
          continue
        narrs = narration_pass["narration_pass_"+str(i+1-diff)]["narrations"]
        clips = []
        if len(narrs) == 0:
          continue
        if i == 500:
          break
        tmp = {}
        ann = [{}]
        tmp["clip_uid"] = narrs[0]["annotation_uid"]
        tmp["video_start_sec"] = narrs[0]["timestamp_sec"]
        tmp["video_end_sec"] = narrs[-1]["timestamp_sec"]
        ann[0]["language_query"] = []
        lang_query = []
        for j in range(int(len(narrs)/5)):
            lang_query.append({})
            lang_query[j]["clip_start_sec"] = narrs[j*5]["timestamp_sec"]
            lang_query[j]["clip_end_sec"] = narrs[j*5+4]["timestamp_sec"]
            lang_query[j]["descriptions"] = [ narrs[j*5+l]["narration_text"] for l in range(5)]
            ann[0]["language_query"].append(lang_query)
        tmp["annotations"] = ann
        clips.append(tmp)
            
        data["video_uid"] = str(video_uid)
        data["clips"] = clips

        ancientIUD = video_uid