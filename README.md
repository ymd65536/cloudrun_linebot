# cloudrun_linebot

CloudRunでLINE botを作る

## コマンド

```bash
gcloud config set project $gcp_project
docker push gcr.io/$gcp_project/linebot-sample:latest
gcloud run deploy cloudrun-test --image gcr.io/$gcp_project/linebot-sample:latest --region asia-northeasat1 --platform managed
$gcp_project
```
