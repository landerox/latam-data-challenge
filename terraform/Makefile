.DEFAULT_GOAL := help

# ========== GLOBAL CONFIG ==========
PROJECT_ID      ?= latam-data-challenge
REGION          ?= us-east1
TF_BUCKET_NAME  ?= $(PROJECT_ID)-terraform-state
SA_NAME         ?= sa-terraform
SA_EMAIL        = $(SA_NAME)@$(PROJECT_ID).iam.gserviceaccount.com
SA_KEY_FILE     ?= sa/sa-terraform.json

.PHONY: help

# Show this help message
help:
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-24s\033[0m %s\n", $$1, $$2}'

# Set GCP project for current gcloud session
set-project:
	gcloud config set project $(PROJECT_ID)

# Activate authentication with service account (if key exists)
auth-login:
	@if [ -f $(SA_KEY_FILE) ]; then \
		gcloud auth activate-service-account $(SA_EMAIL) --key-file=$(SA_KEY_FILE); \
	else \
		echo "File $(SA_KEY_FILE) does not exist."; \
	fi

# Enable required APIs for infra, CI/CD, Cloud Run, and dashboards
enable-apis:
	gcloud services enable \
	  storage.googleapis.com \
	  iam.googleapis.com \
	  cloudresourcemanager.googleapis.com \
	  bigquery.googleapis.com \
	  artifactregistry.googleapis.com \
	  run.googleapis.com \
	  cloudbuild.googleapis.com \
	  serviceusage.googleapis.com \
	  monitoring.googleapis.com \
	  logging.googleapis.com

# Create Terraform service account
create-sa:
	gcloud iam service-accounts create $(SA_NAME) \
		--description="Terraform admin SA for infra automation" \
		--display-name="Terraform Admin"

# Assign roles to SA: infra management, Cloud Run, Storage, BigQuery, Logging, Monitoring
add-sa-roles:
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
		--member="serviceAccount:$(SA_EMAIL)" --role="roles/editor"
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
		--member="serviceAccount:$(SA_EMAIL)" --role="roles/storage.admin"
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
		--member="serviceAccount:$(SA_EMAIL)" --role="roles/bigquery.admin"
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
		--member="serviceAccount:$(SA_EMAIL)" --role="roles/run.admin"
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
		--member="serviceAccount:$(SA_EMAIL)" --role="roles/logging.logWriter"
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
		--member="serviceAccount:$(SA_EMAIL)" --role="roles/monitoring.metricWriter"

# Generate SA key (do NOT commit this file!)
create-sa-key:
	mkdir -p sa
	gcloud iam service-accounts keys create $(SA_KEY_FILE) \
		--iam-account=$(SA_EMAIL)

# Create GCS bucket for Terraform state
create-tf-bucket:
	gsutil mb -p $(PROJECT_ID) -l $(REGION) gs://$(TF_BUCKET_NAME)

# Remove generated sensitive files
clean:
	rm -f $(SA_KEY_FILE)
