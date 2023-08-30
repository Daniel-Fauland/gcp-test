provider "google" {
  credentials = file("credentials.json")
  project     = "propane-nomad-396712"
  region      = "europe-west3"
}

resource "google_compute_instance" "vm_instance" {
  name                      = "my-vm"
  machine_type              = "e2-small"
  zone                      = "europe-west3-c"
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}
