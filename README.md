# Project

The primary goal is to render a `.ply` file that comes with a texture file from different camera angles. This is crucial for most vision pipelines utilizes pose-estimation with template matching.

## Getting Started

The project is coded in python and should be extremely portable, but I have only tried it on `ubuntu-noetic`.


### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Install the following via pip or any favorite package installer
  ```sh
  pip trimesh
  pip pyrender
  pip matplotlib
  ```

### Installation and Usage

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. Create the folder `imgs/templates` or modify the ``settings.json`` file according to your needs.

3. Usage:
    ```sh
    Python3 src/generate_templates.py
    ```
4. There should now be generated rendered images and their poses located in `imgs/templates`.

<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<!-- CONTACT -->
## Contact

(Daniel Tofte Schøn) - danieltoftesch@hotmail.com

[https://github.com/dscho15](https://github.com/dscho15)

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [pyrender](https://github.com/mmatl/pyrender)
* [Trimesh](https://github.com/mikedh/trimesh)
