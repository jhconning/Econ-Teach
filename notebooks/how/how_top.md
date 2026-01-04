# MyST built this site

```{contents}
:depth: 3
```

This Econ-Teach site is now built using [MyST Markdown](https://mystmd.org/), a powerful ecosystem for authoring scientific and technical content in markdown. MyST enables you to write content in standard markdown, enhanced with directives and roles for equations, citations, figures, and more. The site is generated and published using [MyST tools](https://mystmd.org/guide/intro), which convert markdown and Jupyter notebooks (`.ipynb`) into a well-structured, interactive website.  Each time new content is pushed to the github site, a github action rebuilds the rendered website. MyST builds on the work of [Executable Books](https://executablebooks.org/) and is designed for reproducible research, making it easy to share text, math, and code in a variety of output formats, including HTML and PDF.

Some pages contain [geogebra applets](https://geogebra.org) that are immediately interactive in any modern browser.   Other pages which have been created as jupyter notebooks with embedded  python code will display as static pages but can be modified and made interactive by running the the jupyter notebook on a server.  This can be accomplished by clicking the Binder or Google Colab button at the top of the page, or by cloning the [Econ-Teach github repository](https://github.com/jhconning/Econ-Teach) to your local computer and then running them on a local jupyter notebook server.  Here is one [guide](https://www.dataquest.io/blog/jupyter-notebook-tutorial/) to getting started. 

 Most users can interact with the content without having to learn how the entire 'book/website' was built. What follows are a few pointers and tips only for those who might be curious about how to build a similar site.


## Concepts

The aim is to create content using easy human-readable [markdown](https://www.markdownguide.org/getting-started/) in combination with python (or other coding languages) to explore ideas and create scientific content with simulations and visualizations and to then convert this via a nice looking rendered website and/or to other intermediary or final formats such as Latex, PDF, etc.  In short, we want to get a nice looking website and 'book' content for sharing reproducible research without having to learn (too much) HTML/CSS, Latex or other technical content.

[Jupyter notebooks](https://jupyter.org/) already accomplish much of this goal by themselves by providing a 'front end' for mixing text, math and code.  Jupyter notebooks that are posted to sites such as github are automatically rendered by those sites in human readable form (see, for example, [Edgeworth.ipynb](https://github.com/jhconning/Econ-Teach/blob/master/notebooks/trade/Edgeworth.ipynb)).  This however allows one to only display one notebook at a time and for a larger project one would want to organize several notebooks and markdown files into a clearly navigable book or website.
 
Some of the people behind the fantastic [Quantecon](https://quantecon.org/) project were important to the development of MyST markdown (and the earlier [Jupyter Book](https://jupyterbook.org/)).

[MyST Markdown](https://jupyterbook.org/content/myst.html) extends the simple markdown syntax typically used for jupyter notebooks by adding 'directives' and 'roles' to allow several 'book writing' tasks including adding bibliographic citations and bibliographies, numberering equations, adding cross-references, creating tabs and dropdowns, etc. MyST also gives us more fine control over things such as image size and positioning on a page, figure captioning, hiding code, etc.

## Setup and Build
To set up and build the site using the MyST workflow, first ensure you have [MyST CLI](https://mystmd.org/guide/intro) installed. 


Once installed, navigate to your project directory (e.g., `Econ-Teach`) in your terminal. To build the site locally, run:

```bash
myst build .
```

This command utilizes configuration instructions from both `myst.yml` and `_toc.yml` files.
- `myst.yml` provides project-wide settings for MyST Markdown parsing and Sphinx integration.
- `_toc.yml` defines the structure and order of the table of contents for the documentation build.
By referencing these files, the command ensures that documentation is built and organized according to the specified configurations and content hierarchy.


This command will generate the static site in the `_build/html` directory. You can preview the site locally by running:

```bash
myst preview
```

This will start a local server and provide a link to view your site in your browser. The MyST workflow supports both markdown (`.md`) and Jupyter notebook (`.ipynb`) files, allowing you to mix narrative content and executable code seamlessly. For more details on configuration and advanced options, see the [MyST documentation](https://mystmd.org/guide/).

See installation instructions on the [MyST markdown site](https://mystmd.org/guide/).


## Github Actions and webpage

In order to build and share a website that can be reached from anywhere on the internet I use the free github pages servive. 

I've [setup a github action](https://mystmd.org/guide/deployment-github-pages) so that any new push of new content to the Github repository at [github.com/jhconning/Econ-Teach](https://github.com/jhconning/Econ-Teach) will trigger the creation of a virtual cloud machine that will then produce the jupyterbook site using the build process just described such that the rendered site then displays at [jhconning.github.io/Econ-Teach](https://jhconning.github.io/Econ-Teach).  It's a neat process and it's fun to see github actions do all this work for you.  There may be a few minutes delay between a new build and the changes appearing on the site.[^1]

## Workflow

I typically develop jupyter notebook and markdown file content using [jupyterlab](https://jupyter.org/) and [Visual Studio Code](https://code.visualstudio.com/) to edit content and move files around, but I sometimes use a markdown editor such as [Typora](https://typora.io/) particularly if I'm going to type a lot of math.  You can have these different tools open at the same time, editing the same files.  VS code allows you to preview how both markdown files and jupyter notebooks will render, plus you can open up a terminal window to run local jupyterbook builds to see how they look in the browser.  

When I'm satisified that new content is ready to be shared I will then push the changes to the github repository (either via the command line, or using either VS code or the github desktop app).  I only push the 'source' files (markdown, jupyter notebooks, and relevant other files) not the locally rendered HTML because, as mentioned, a github action will build the site on a virtual machine (everything needed to make it run is in the [book.yml](https://github.com/jhconning/Econ-Teach/blob/master/.github/workflows/book.yml) configuration file).  



[^1]: If setting up your own page, make sure you've enabled Github pages in the settings.  Also make sure that your version of the [book.yml](https://github.com/jhconning/Econ-Teach/blob/master/.github/workflows/book.yml) file points to the right branch (e.g. 'main' or 'master').
