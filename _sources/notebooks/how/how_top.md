# This JupyterBook

```{contents}
:depth: 3
```

This Econ-Teach site was made using [JupyterBook](https://jupyterbook.org/intro.html) which, in turn, leverages the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation system.  These tools take content written in jupyter notebook (`.ipynb` extension) and markdown text files (`.md` extension) to transform text, math input, and python code, into the nicely rendered HTML code of this website.  Some of the notebooks that embed code can then be run on a jupyter notebook server on the users' personal computer, or in the cloud, to make some of the visualizations and simulations interactive.

Some pages contain [geogebra applets](https://geogebra.org) that are immediately interactive in any modern browser.   Other pages which have been created as jupyter notebooks with embedded  python code will display as static pages but can be modified and made interactive by running the the jupyter notebook on a server.  This can be accomplished by clicking the Binder or Google Colab button at the top of the page, or by cloning the [Econ-Teach github repository](https://github.com/jhconning/Econ-Teach) to your local computer and then running them on a local jupyter notebook server.  Here is one [guide](https://www.dataquest.io/blog/jupyter-notebook-tutorial/) to getting started. 

 Most users can interact with the content without having to learn how the entire 'book/website' was built. What follows are a few pointers and tips only for those who might be curious about how to build a similar site.


## Concepts

The aim is to create content using easy human-readable [markdown](https://www.markdownguide.org/getting-started/) in combination with python (or other coding languages) to explore ideas and create scientific content with simulations and visualizations and to then convert this via a nice looking rendered website and/or to other intermediary or final formats such as Latex, PDF, etc.  In short, we want to get a nice looking website and 'book' content for sharing reproducible research without having to learn (too much) HTML/CSS, Latex or other technical content.

[Jupyter notebooks](https://jupyter.org/) already accomplish much of this goal by themselves by providing a 'front end' for mixing text, math and code.  Jupyter notebooks that are posted to sites such as github are automatically rendered by those sites in human readable form (see, for example, [Edgeworth.ipynb](https://github.com/jhconning/Econ-Teach/blob/master/notebooks/trade/Edgeworth.ipynb)).  This however allows one to only display one notebook at a time and for a larger project one would want to organize several notebooks and markdown files into a clearly navigable book or website.
 
Jupyterbook was created for this purpose as part of [The Executable Book Project](https://executablebooks.org/en/latest/).  Many Executable Books and Courses are being written using Jupyterbook. See the [Gallery of Jupyter Books](https://executablebooks.org/en/latest/gallery.html).  Some of the peopl behind the [Quantecon](https://quantecon.org/) project were important to the development of Jupyter Book.

Jupyterbook extends the simple markdown syntax typically used for jupyter notebooks by adding extra [MyST Markdown](https://jupyterbook.org/content/myst.html) 'directives' and 'roles' to allow us several 'book writing' tasks including adding bibliographic citations and bibliographies, numberering equations, adding cross-references, creating tabs and dropdowns, etc. MyST also gives us more fine control over things such as image size and positioning on a page, figure captioning, hiding code, etc.

## Setup and Build

See installation instructions on the [jupyter book](https://jupyterbook.org/) page.  We need a `_config.yml` with basic configuration settings and a `_toc.yml` file that establishes which files will be included in the navigation structure that you'll to the left of the site.

Suppose you have [cloned](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the [Econ-Teach](https://github.com/jhconning/Econ-Teach)repository that builds this site to a folder on your machine labeled `Econ-Teach` and have already installed jupyterbook.  If you then open up an Anaconda command terminal on your machine and navigate to that folder, you can then type

`jb build .`

Then jupyterbook will build a local HTML website which you can view from a browser (at the end of the build process it will tell you how to open it).  


## Github Actions and webpage

In order to build and share a website that can be reached from anywhere on the internet I use the free github pages servive. 

I've [setup a github action](https://jupyterbook.org/publish/gh-pages.html#automatically-host-your-book-with-github-actions) so that any new push of new content to the Github repository at [github.com/jhconning/Econ-Teach](https://github.com/jhconning/Econ-Teach) will trigger the creation of a virtual cloud machine that will then produce the jupyterbook site using the build process just described such that the rendered site then displays at [jhconning.github.io/Econ-Teach](https://jhconning.github.io/Econ-Teach).  It's a neat process and it's fun to see github actions do all this work for you.  There may be a few minutes delay between a new build and the changes appearing on the site.[^1]



[^1]: If setting up your own page, make sure you've enabled Github pages in the settings.  Also make sure that your version of the [book.yml](https://github.com/jhconning/Econ-Teach/blob/master/.github/workflows/book.yml) file points to the right branch (e.g. 'main' or 'master').