# Terraform

This section will cover a few hands-on tutorials using Terraform.

## Prerequisites

To get started make sure you have [terraform](https://www.terraform.io) installed on your local machine.
You can check your installation by running the following command in terminal:

```shell
terraform -v
```

Then create a new [service account](../iam/README.md#create-service-account) on GCP which has the global _Editor_ role so that terraform is able to create and manage resources. Now download the [credentials json](../iam/README.md#create-credentials-json-file) file of that service account so that terraform can be executed on your local machine.

## Create VM instance

In this example you will create a virtual machine instance on GCP using terraform. VM Instances are part of the _Compute Engine_ resource which gives you the possibility to create and manage virtualized hardware resources.

1. Start by creating a terraform script (usually called _main.tf_). The very first thing to do in every terraform script is setting the provider and project.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   provider "<cloud-provider>" {
   credentials = file("path/to/your/credentials.json")
   project     = "<project-id>"
   region      = "<your-region>"
   }
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
   provider "google" {
   credentials = file("credentials.json")
   project     = "propane-nomad-396712"
   region      = "europe-west3"
   }
   ```

   </details>

2. Then you can add your resources that should be created. In this case it will be a vm instance.

   <details>
   <summary>Show general code snippet:</summary>

   ```shell
   resource "<provider>_<product>-<resource>" "<tf-resource-name>" {
   name         = "<name>"
   machine_type = "<machine-type>"
   zone         = "<your-zone>"

   boot_disk {
       initialize_params {
       image = "<image>"
       }
   }

   network_interface {
       network = "default"
       access_config {}
   }
   }
   ```

   </details>

   <details open>
   <summary>Show example code snippet:</summary>

   ```shell
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
   ```

   </details>

   If you set the _allow_stopping_for_update_ flag to _true_ you will allow the vm to automatically stop in order to install updates. If you need uninterrupted uptime on your vm you can set this flag to _false_ but it's recommended to have this feature on.
   The image specifies the operating system used by the VM. You can get a list of all available images via gcloud:

   ```shell
   gcloud compute images list
   ```

   The network part lets you specify the network interface used as well as any kind access configuration. The access_config must be scpecified even if it's empty to ensure the VM is actually reachable via the internet.

3. Once the terraform script is completed open a terminal and navigate to the directory of the _main.tf_ file. Now initialize terraform.

   ```shell
   terraform init
   ```

4. You can check which resources will be created, modified or deleted including all parametes (even those not specified in the script) before deploying it to the cloud.

   ```shell
   terraform plan
   ```

5. If everything looks fine deploy the defined resources on the cloud and confirm by typing _yes_ in the terminal.

   ```shell
   terraform apply
   ```

   **Note:** A VM costs money just by running even if there is no traffic/data on it. Therefore if it's not in use you can stop the VM to prevent being charged. You don't need to delete & redeploy the vm every time.
