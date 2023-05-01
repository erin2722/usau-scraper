.. _developer:

developer documentation
===========================================

Getting Started Developing
+++++++++++++++++++++++++++

Prerequisites: Make sure you have Python3.7+ installed.

1. Fork the repository from the main page.

2. Clone your fork to your computer and add the remote ::

        git clone git@github.com:<your GitHub handle>/usau-scraper.git
        cd usau-scraper
        git remote add upstream git@github.com:erin2722/usau-scraper.git
3. Create a branch
4. git checkout -b my-awesome-new-feature
5. Run :code:`make develop` to get ready to develop (strongly recommend in a virtualenv)

6. Make your changes. Make sure to add in tests and documentation changes for all new features.

7. Run the test suite. From the top level usau-scraper directory run::

        make test

8. Run :code:`make format` and :code:`make lint` to autoformat the library.

9. Add and commit changes with descriptive message ::

        git add file1.py tests/test_file1.py docs/file1.md
        git commit -m "My new fancy functionality"
10. Sync with upstream to pull any recent changes ::

        git fetch upstream
        git rebase upstream/master
11. Push your changes ::

        git push origin my-awesome-new-feature
12. Click the link that appears in your terminal to make a pull request, or go to your fork of the repository and click the link. 
    Add a summary of your changes and submit!

Documentation Contributions
++++++++++++++++++++++++++++

The documentation is built using sphinx and read the docs. When writing new public-facing functions, always add in google-style 
docstrings so that the functions can be added to autodocumentation. 

If you want to contribute a new example, edit/add in another google collab notebook to the :code:`examples/` folder.
