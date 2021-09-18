# This JupyterBook

This Econ-Teach site was made using [JupyterBook](https://jupyterbook.org/intro.html) which leverages the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation system.  All content was written using jupyter notebooks (`.ipynb` extension) which combine markdown text and python code cells and/or with plain markdown files.  

Many of the graphs in the book are interactive because they are either:
- Geogebra Apps (javascript apps that will run immediately in any modern browser). 
- Python interactive widgets (ipywidgets).  These may appear as static images on the website but can be made interactive by running the underlying jupyter notebook, usually just by clicking the Binder or Google Colab button at the top of the page.

A longer description and a few tips and tricks for anyone who wants to build similar pages.

```{contents}
:depth: 3
```

## Concepts

The aim is to write content using easy human-readable markdown syntax and then convert to a nice looking rendered HTML website and/or to other intermediary or final formats such as Latex, PDF, etc. We want to do all this without having to learn (too much) about HTML/CSS or Latex.

Jupyterbook is part of [The Executable Book Project](https://executablebooks.org/en/latest/) and extends the powerful Sphinx Static HTML renderer.

Many Executable Books and Courses are being written using Jupyterbook. See the [Gallery of Jupyter Books](https://executablebooks.org/en/latest/gallery.html).  Some of the peopl behind the [Quantecon](https://quantecon.org/) project were important to the development of Jupyter Book.

Most content is simple markdown syntax but in a few places it is augmented by [MyST Markdown](https://jupyterbook.org/content/myst.html) to add extra 'directives' and 'roles' to allow us to do several 'book writing' tasks such as adding bibliographic citations and bibliographies, numbered equations, cross-references, etc. MyST also gives us more fine control over things such as image size and positioning on a page, figure captioning, etc.

## Setup and Build

See installation instructions on jupyter book page.  Basically we need a `_config.yml` with basic configuration settings and a `_toc.yml` file that basically establishes which files will become pages and the navigation structure you'll to the left of the site.

If you have those files as well as other content in a folder labeled `Econ-Teach` then open up an Anaconda terminal in the parent folder and type

`jb build Econ-Teach/`

And jupyterbook will create a local copy of the website which you can view from a browser.  

I've [setup a github action](https://jupyterbook.org/publish/gh-pages.html#automatically-host-your-book-with-github-actions) so that any new push to the Github repository at [github.com/jhconning/Econ-Teach](https://github.com/jhconning/Econ-Teach) triggers a similar build on a virtual cloud machine that will then produce the jupyterbook site that will be rendered at [jhconning.github.io/Econ-Teach](https://jhconning.github.io/Econ-Teach).  There may be a few minutes delay between new builds and the changes showing up.[^1]


## MyST markdown



[^1]: If setting up your own page, make sure you've enabled Github pages in the settings.  Also make sure that your version of the [book.yml](https://github.com/jhconning/Econ-Teach/blob/master/.github/workflows/book.yml) file points to the right branch (e.g. 'main' or 'master').