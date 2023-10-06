# cloudrun_linebot

CloudRunでLINE botを作る

## コマンド

```bash
gcloud config set project $gcp_project
gcloud auth login
gcloud auth configure-docker
gcloud artifacts repositories create linebot-sample --location=asia-northeast1 --repository-format=docker --project=$gcp_project
docker build -t gcr.io/$gcp_project/linebot-sample . --platform linux/amd64

docker push gcr.io/$gcp_project/linebot-sample:latest
gcloud run deploy --image gcr.io/$gcp_project/linebot-sample:latest --region asia-northeast1 --platform managed
gcloud components update
```
