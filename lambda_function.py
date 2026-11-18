import json, base64, boto3

rek = boto3.client("rekognition")

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        img = {"Bytes": base64.b64decode(body["image"])}

        labels = rek.detect_labels(Image=img, MaxLabels=10, MinConfidence=80)
        text = rek.detect_text(Image=img)
        faces = rek.detect_faces(Image=img, Attributes=["ALL"])
        moderation = rek.detect_moderation_labels(Image=img, MinConfidence=60)

        face_list = []
        for f in faces["FaceDetails"]:
            emotions = f.get("Emotions", [])
            top = max(emotions, key=lambda e: e["Confidence"])["Type"].title() if emotions else "Unknown"
            face_list.append({
                "age_low": f["AgeRange"]["Low"],
                "age_high": f["AgeRange"]["High"],
                "smile": f["Smile"]["Value"],
                "glasses": f["Eyeglasses"]["Value"],
                "emotion": top,
            })

        out = {
            "labels": [
                {"name": l["Name"], "confidence": round(l["Confidence"], 1)}
                for l in labels["Labels"]
            ],
            "text": [
                {"text": t["DetectedText"], "confidence": round(t["Confidence"], 1)}
                for t in text["TextDetections"] if t["Type"] == "LINE"
            ],
            "faces": face_list,
            "moderation": [
                {"name": m["Name"], "parent": m.get("ParentName", ""), "confidence": round(m["Confidence"], 1)}
                for m in moderation["ModerationLabels"]
            ],
        }
        return {"statusCode": 200, "body": json.dumps(out)}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}