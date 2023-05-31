terraform {
  required_providers {
    google = {
      source 	= "hashicorp/google"
      version 	= "4.61.0"
    }
  }
}

provider "google" {
  project 	= "your-project-name"
  region 	= "your-google-region"
  zone 		= "your-google-region-zone"
  credentials 	= file("/path/to/google/credentials/json/file")
}

resource "google_storage_bucket" "data_lake"{
  name 		= "your-bucket-name"
  location 	= "your-google-region"
  force_destroy = true
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

# Optional: set the blobs in the bucket
# to expire in 30 days.

  /*lifecycle_rule {
    action {
      type 	= "Delete"
    }
    condition {
      age 	= 30  // days
    }
  }*/

}


resource "google_bigquery_dataset" "data_warehouse"{
  dataset_id 	= "your_dataset_name"
  description 	= "Collection of data gathered from the Spotify Web API."
  location 	= "your-google-region"
}
