# Mobick Logbook (formerly SeedSigner)

### Build an offline, airgapped BTCMobick signing device for less than $50!

![Mobick Logbook Device](docs/img/Mini_Pill_Main_Photo.jpg) 
*(Image placeholder: You can replace this with your own Mobick Logbook photo later)*

---------------

* [Project Summary](#project-summary)
* [Shopping List](#shopping-list)
* [Software Installation](#software-installation)
  * [Verifying your download](#verifying-your-download)
* [Enclosure Designs](#enclosure-designs)
* [SeedQR Printable Templates](#seedqr-printable-templates)
* [Build from Source](#build-from-source)
* [Developer Local Build Instructions](#developer-local-build-instructions)


---------------

# Project Summary

**Mobick Logbook** is a specialized fork of the [SeedSigner](https://github.com/SeedSigner/seedsigner) project, tailored specifically for the **BTCMobick** ecosystem.

The goal of Mobick Logbook is to lower the cost and complexity of BTCMobick multisignature wallet use. It offers anyone the opportunity to build a verifiably air-gapped, stateless signing device using inexpensive, publicly available hardware components (usually < $50).

# Key Changes & Features

### 🇰🇷 Specialized for Mobick & Korea
* **Korean Language Support (한글화):**
  * Fully localized Korean interface added.
  * Select "Korean" (한국어) in the Settings menu.
* **BTCMobick Ecosystem:**
  * Native support for the **BTCMobick** network and unit (`bick`).
* **Custom Branding:**
  * "Mobick Logbook" boot logo and UI rebranding.
  * **Custom Toast Messages:** Special signature "Forged by HoguSea" confirmation toasts upon boot/SD card insertion.

### Standard Features (Inherited from SeedSigner)
* **Stateless, air-gapped operation:**
  * Temporarily stores seeds in memory while the device is powered; all memory is wiped when power is removed.
  * No WiFi or Bluetooth hardware onboard.
  * Can only receive data via reading QR codes with its camera.
  * Can only send data by displaying QR codes on its screen.
* **Trustless, auditable:**
  * Completely FOSS code, MIT license.
  * Reproducible builds.

### Credits
This project is based on **SeedSigner**. Huge respect and credit to the original SeedSigner team for their incredible work.
* Original Project: [SeedSigner.com](https://seedsigner.com)
* Original Repo: [github.com/SeedSigner/seedsigner](https://github.com/SeedSigner/seedsigner)

---------------

# Shopping List

To build a Mobick Logbook, you will need the same hardware as a standard SeedSigner:

* **Raspberry Pi Zero** (v1.3, W, or 2W)
  * Recommended: Raspberry Pi Zero 2 W (with headers)
* **Waveshare 1.3" 240x240 LCD HAT** (Must be 240x240 resolution, IPS version recommended)
* **Pi Zero-compatible Camera** (OV5647 Sensor with Zero cable)
* **MicroSD Card** (4GB or larger)

---------------

# Software Installation

## Downloading the Software

Download the latest **Mobick Logbook** release image (v1.0.0) from the [Releases Page](https://github.com/hogusea/seedsigner/releases).

| Board | Download Image Link |
| :--- | :--- |
| **Raspberry Pi Zero 1.3 / W / 2W** | [Check Releases Page](https://github.com/hogusea/seedsigner/releases) |
| Raspberry Pi 4 | [Check Releases Page](https://github.com/hogusea/seedsigner/releases) |

**Note:** Since this is a custom fork, please ensure you are downloading the `mobick` tagged images.

## Verifying your download
(Verification steps are identical to original SeedSigner, but using the SHA256 sums provided in our release page.)

## Writing the software onto your MicroSD card
You can use **Balena Etcher** or **Raspberry Pi Imager** to flash the `.img` file onto your SD card.

1. Insert MicroSD card into your computer.
2. Open Balena Etcher.
3. Select the `mobick_logbook_os.img` file.
4. Select your SD card target.
5. Click **Flash!**

---------------

# Enclosure Designs

You can use any standard SeedSigner case (Open Pill, Orange Pill) for your Mobick Logbook.

* [Open Pill Design](https://github.com/SeedSigner/seedsigner/tree/main/enclosures/open_pill)
* [Orange Pill Design](https://github.com/SeedSigner/seedsigner/tree/main/enclosures/orange_pill)

*(Future Update: Custom Mobick Logbook cases will be added here)*

---------------

# SeedQR Printable Templates
Mobick Logbook supports the standard SeedQR format for air-gapped seed backups.

* [12-word SeedQR template](docs/seed_qr/printable_templates/dots_25x25.pdf)
* [24-word SeedQR template](docs/seed_qr/printable_templates/dots_29x29.pdf)

[More information about SeedQRs](docs/seed_qr/README.md)

---------------

# Build from Source

If you prefer to build the OS image yourself from source code:

1. Clone this repository:
   ```bash
   git clone [https://github.com/hogusea/seedsigner.git](https://github.com/hogusea/seedsigner.git)

   Follow the build instructions in the seedsigner-os repository (or use the provided build scripts if available).

2. Update Submodules (Important)
This fork uses a custom translation repository. You must update the pointers correctly.

```bash
git submodule update --init --recursive
# Note: The 'seedsigner-screenshots' submodule has been removed in this fork to prevent build errors.
```

3. Build with Docker
Navigate to the seedsigner-os directory (you may need to clone the OS repo separately or use the provided build scripts).

Recommended Build Command:
Use this command to ensure the builder pulls the correct Korean translation files from the hogusea fork:

```bash
./build.sh --pi0 --dev --app-repo=[https://github.com/hogusea/seedsigner.git](https://github.com/hogusea/seedsigner.git) --app-branch=dev
```

Localization
Korean Translation (Contributor Note)
Translation files are located in src/seedsigner/resources/seedsigner-translations/l10n/ko/.

Important: .mo files (compiled binary) are ignored by git by default. If you update the translation, you must force add the compiled file:

```bash
# Example for updating Korean translation
git add -f l10n/ko/LC_MESSAGES/messages.mo
git commit -m "feat: update Korean translation"
```

# SeedQR Printable Templates
Mobick Logbook supports the standard SeedQR format for air-gapped seed backups.

* [12-word SeedQR template](docs/seed_qr/printable_templates/dots_25x25.pdf)
* [24-word SeedQR template](docs/seed_qr/printable_templates/dots_29x29.pdf)

[More information about SeedQRs](docs/seed_qr/README.md)

