
<p align="center">
  <a href="#">
    <img src="https://thumbs.gfycat.com/CalmKeyEidolonhelvum-max-1mb.gif" alt="Logo">
  </a>

  <h3 align="center">Progressive Web App With Django 3</h3>
  <h5 align="center">Languages and Tools:</h5>
  <p align="center"> <a href="https://getbootstrap.com" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg" alt="bootstrap" width="30" height="30"/> </a> <a href="https://www.w3schools.com/css/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="30" height="30"/> </a> <a href="https://www.djangoproject.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-original.svg" alt="django" width="30" height="30"/> </a> <a href="https://graphql.org" target="_blank"> <img src="https://www.vectorlogo.zone/logos/graphql/graphql-icon.svg" alt="graphql" width="30" height="30"/> </a> <a href="https://heroku.com" target="_blank"> <img src="https://www.vectorlogo.zone/logos/heroku/heroku-icon.svg" alt="heroku" width="30" height="30"/> </a> <a href="https://www.w3.org/html/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="30" height="30"/> </a> <a href="https://postman.com" target="_blank"> <img src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="postman" width="30" height="30"/> </a> </p>

  
  <p  align="center">
  <i>PWA where users can register/login and can post/edit their articles or can share, like and comments.</i>
  </p>
</p>


  <p align="center">
    <a href="https://djangoblogdeployed.herokuapp.com/"  target="_blank">View Demo</a>
    ·
    <a href="https://github.com/Aryavir07/Blogging-PWA-with-Django/issues" target="_blank">Report Bug</a>
    ·
    <a href="https://github.com/Aryavir07/Blogging-PWA-with-Django/issues" target="_blank">Request Feature</a>
  </p>




<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![image](https://user-images.githubusercontent.com/42632417/135388133-1efd40c2-e9f9-4a4b-808e-af596f1a9e84.png)
</br>
![image](https://user-images.githubusercontent.com/42632417/135388269-a9d3d764-bfbe-4754-89a2-acb592aaa18b.png)
</br>
![image](https://user-images.githubusercontent.com/42632417/135388350-5b464aab-5cdb-4602-98b6-78dd84c4d662.png)

#### And many more....

This is a demo project for learning Django framework. The idea was to build some basic blogging webapp that has all features of blogging websites like Medium etc.

It was made using Python 3.8 + Django 3 and database is SQLite. Bootstrap was used for styling.

It allows registration, login, password reset, post like, share and commenting on post functionalities.

User has his own blog page, where he can add new blog posts. 
Every authenticated user can comment on posts made by other users. Home page is paginated list of all posts. 
Non-authenticated users can see all blog posts, but cannot add new posts or like/comment.

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* IDE (eg. vscode, sublime)
* Python 3.8+
* Django 3.0+
* Git

### Installation Instructions

If you want to work with this project or create a version of it make sure to follow the steps below!

0. Make sure to install ` Python 3 `, ` pip ` and ` virtualenv `   
1. Create a project folder
   
    ```bash
        $ mkdir project
        $ cd project
    ```
2. Create a python 3 virtualenv, and activate the environment to install requirements.
    ```bash
        $ python3 -m venv env
        $ source env/bin/activate
    ``` 
3. Install the project dependencies from `requirements.txt`
    ```
        (env)$ pip install -r requirements.txt
    ```
4. Clone the repository
   
    ```bash
        (env)$ git clone https://github.com/Aryavir07/Blogging-PWA-with-Django.git
        (env)$ cd django-blogging-webapp
    ```
    
5. Add ```ckeditor, django_filter, crispy_forms``` and ```rest_framework``` to your ```INSTALLED_APPS``` in ```settings.py```:
    ```
         INSTALLED_APPS = (
            ...
                'django_filters',
                'rest_framework',
                'ckeditor',
                'ckeditor_uploader',
                'crispy_forms',
        )

    ```
    <p>
    
    </p>
  6. Run server:
    ```
        Your server is now live on http://127.0.0.1:8000
    ```
    </br>
You have now successfully set up the project on your environment.

<!-- ROADMAP -->
## Roadmap

<p align="center">
  <a href="#">
    <img src="https://user-images.githubusercontent.com/42632417/135386431-449bf4cf-a2a6-4c17-be51-0e5f30656b2e.png" alt="Logo">
  </a>
<p>Diagram credit: Dragan Savić, Mario Ilić, Jaka Sodnik, Anton Kos, Sara Stančin, Sašo Tomažič</p>
</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/StreamingFeature`)
3. Commit your Changes (`git commit -am 'Adding some new streaming feature '`)
4. Push to the Branch (`git push origin feature/StreamingFeature`)
5. Open a Pull Request


## Features

- Dashboard for Authors
- WYSIWYG Editor
- Account Verification 
- Author Login
- Author Password Reset
- New Category Submission
- Related Articles
- Comments
- Articles Search
- Tag Related Articles
- Markdown Support
- Responsive on all devices
- Pagination

## Technologies
- Font awesome
- CKEditor
- SQLite
- Python 3.8
- Javascript
- Jquery 
- Django 3
- HTML5
- CSS3 
- Bootstrap 4

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Font Awesome](https://fontawesome.com)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
