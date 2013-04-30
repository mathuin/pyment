# Welcome to Pyment!

Pyment is a website that tracks the production, storage, and distribution of my home-brewed mead.

Pyment was written in Python using the Django framework. The distribution portion of the website (the catalog, the shopping cart, and other associated code) is based heavily upon the example site from "Beginning Django E-Commerce" by Jim McGaw.

Please note that this code is in the beta state!  The database schemas and models and views and everything else are subject to change without notice.  When the code settles down, I will modify the documentation to reflect any increase in stability.  Additionally, there are a number of design decisions that I have made to support my specific environment: many jars of mead stored in multiple locations brewed during regularly-scheduled brewing events with multiple batches per event.  Feel free to modify the code to match your particular needs -- I am especially interested in pull requests that improve the look and feel of the site!

# Additional Features

Pyment now runs on Django 1.5.1.  This required minimal changes to the codebase, which is now PEP8-compliant except for line length.  

There is a new meadery app which manages ingredients, recipes, and batches.  My standard recipe template is implied here, with specific ingredients or sets of ingredients included as appropriate.  Individual ingredients can be defined as 'natural' or having a particular appellation.  Batches are created from recipes with the recipe template values copied over.  Recipes can in turn be created from batches as well.  Recipes include projected original and final gravities as well as estimated volumes.  Products can be created from batches, but label printing is not yet supported.

An inventory management system has been implemented, including support for multiple warehouses and picklists.  A number of management commands have been added to facilitate capacity management and to aid in adding new product in bulk.  Drill-down capability is now available on the admin site from warehouse to crate as well as a few other places.

# Requirements

Pyment is my first experience with virtualenv.  I have created a requirements.txt file from the output of 'pip freeze' which should be enough to recreate my environment.  Please let me know if anything is missing!

In addition to the packages listed in the requirements file, pyment requires python 2.6 or greater.  Also, there is an issue with label printing if the label includes an image.  The following error message is displayed:

    IOError: decoder zip not available

I am still working on this problem, and will update the documentation when I have a solution.

# Initial Configuration

Copy pyment/settings.py to pyment/settings_local.py and modify it to suit your environment.

Sync the database and start the admin site.  Create flatpages for "about" and "contact".  This should be enough for the site itself to look right.

The cornerstone of the inventory model is the warehouse.  Each warehouse should contain at least one row.  Each row should contain at least one shelf.  Each shelf should contain at least one bin (a section of shelf set aside for one or more crates).  Using the admin site, create the warehouse first, then rows, then shelves, then bins.

The catalog is based on two models: category and product.  The categories are designed around those in the [Beer Judge Certification Program](http://www.bjcp.org/) but need to be populated.  Products have a variety of specific identifying characteristics which may need to be modified to suit your environment.  Again using the admin site, create the categories and then the products.

For each crate in your warehouse, create a crate in the admin site and assign it to a bin.  For each jar in that crate, create a jar in the admin site with the corresponding product data and assign it to that crate.  That's it!

Once all the mead has been entered into the database, take another tour of the site to ensure that everything works as you expect.

# Work still to be done

Picklists have been implemented and work from the admin site.  Minor future changes possibly include emailing admins when new orders are placed and that sort of thing.

# License

This software is released under the [MIT license](http://opensource.org/licenses/mit-license.php).



