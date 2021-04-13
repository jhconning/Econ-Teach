# This JupyterBook

This Econ-Teach site was made using [JupyterBook](https://jupyterbook.org/intro.html) which is built on top of the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation system. 

The content was written using a combination of markdown files (with `.md` extensions) and jupyter notebooks (with `.ipynb` extensions) with markdown and python code cells.  

Many of the graphs in the book are interactive because they are either:
- Geogebra Apps (javascript apps that will run in any browser) 
- Python interactive widgets.  These may appear as static images on the website but can usually be made interactive by running the underlying jupyter notebook by clicking the Binder or Google Colab button to launch a server.


Below is a brief description and evolving list of tips and tricks used to build these pages.

```{contents}
:depth: 3
```

## Concepts

What we're trying to do is write content using easy human-readable markdown syntax and then regularly convert that to fancy looking rendered HTML and/or other formats such as Latex, PDF, Latex, etc, all without having to learn (too much) of the HTML or Latex that we could have used instead.

Jupyterbook is part of [The Executable Book Project](https://executablebooks.org/en/latest/) and extends the powerful Sphinx Static HTML renderer.

Many Executable Books and Courses are being written using Jupyterbook. See the [Gallery of Jupyter Books](https://executablebooks.org/en/latest/gallery.html).  The [Quantecon](https://quantecon.org/) project has been an important force behind the development of Jupyter Book.

We write most content using simple markdown syntax but augmented in places by [MyST Markdown](https://jupyterbook.org/content/myst.html) extended syntax in order to add 'directives' and 'roles' which allow us to do 'book writing' things citations and bibliographies, numbered equations, cross-references, etc. MyST also gives us more fine control over things such as image size and positioning on a page, figure captioning, etc.

## Setup and Build

See installation instructions on jupyter book page.  Basically we need a `_config.yml` with basic configuration settings and a `_toc.yml` file that basically establishes which files will become pages and the navigation structure you'll to the left of the site.

If you have those files as well as other content in a folder labeled `Econ-Teach` then open up an Anaconda terminal in the parent folder and type

`jb build Econ-Teach/`

And jupyterbook will create a local copy of the website which you can view from a browser.  

I've setup a github action so that any new push to the Github repository at [github.com/jhconning/Econ-Teach](https://github.com/jhconning/Econ-Teach) triggers a similar build on a virtual cloud machine that will then produce the jupyterbook site that will be rendered at [jhconning.github.io/Econ-Teach](https://jhconning.github.io/Econ-Teach).  There may be a few minutes delay between new builds and the changes showing up. 

## MyST markdown

