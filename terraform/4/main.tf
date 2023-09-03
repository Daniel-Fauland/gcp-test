provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
}

resource "google_compute_instance" "vm_instance" {
  name                      = "my-vm"
  machine_type              = var.vm_instance[0]
  zone                      = var.vm_instance[1]
  allow_stopping_for_update = var.vm_instance[2]

  boot_disk {
    initialize_params {
      image = var.vm_disk.image
      size  = var.vm_disk.size
    }
  }

  network_interface {
    network    = google_compute_network.terraform_network.self_link
    subnetwork = google_compute_subnetwork.terraform_subnet.self_link
    access_config {}
  }
}

resource "google_compute_network" "terraform_network" {
  name                    = "terraform-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "terraform_subnet" {
  name          = "terraform-subnetwork"
  ip_cidr_range = "10.20.0.0/16"
  region        = "europe-west3"
  network       = google_compute_network.terraform_network.id
}

