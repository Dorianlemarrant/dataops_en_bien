provider "google" {
  project = "ensai-2026"
  region  = var.region
  zone    = var.zone
}

resource "google_storage_bucket" "test-bucket" {
  name     = "christophe-bucket-tf-2"
  location = "EU"

  uniform_bucket_level_access = true
  labels = {
    environment = "dev"
  }
}

resource "google_compute_instance" "default" {
  name         = "christophe-instance-tf"
  machine_type = "n2-standard-2"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  // Local SSD disk
  scratch_disk {
    interface = "NVME"
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }
}

output "instance_ip" {
  value = google_compute_instance.default.network_interface[0].access_config[0].nat_ip
}
