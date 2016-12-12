[![Build Status](https://travis-ci.org/mathuin/pyment.svg?branch=master)](https://travis-ci.org/mathuin/pyment)
[![Code Health](https://landscape.io/github/mathuin/pyment/master/landscape.svg?style=flat)](https://landscape.io/github/mathuin/pyment/master)
# Welcome to Pyment!

Pyment is a website that tracks the production, storage, and distribution of my home-brewed mead.

Pyment was written in Python using the Django framework. The distribution portion of the website (the original catalog, the color scheme, the shopping cart, and other associated code) is based heavily upon the example site from "Beginning Django E-Commerce" by Jim McGaw.

This code is now in production.  The database schemas and models should now be stable.  There are a number of design decisions that I have made to support my specific environment: many jars of mead stored in multiple locations brewed during regularly-scheduled brewing events with multiple batches per event.  Feel free to modify the code to match your particular needs -- I am especially interested in pull requests that improve the look and feel of the site!

# Major Features

The entire mead life cycle is now supported, from ingredients and recipes through batches and products.  Individual ingredients can be defined as 'natural' or having a particular appellation.  Batches are created from recipes with the recipe template values copied over.  Recipes can in turn be created from batches as well.  Recipes include projected original and final gravities as well as estimated volumes.  Products can be created from batches, and labels can be generated from batches.

An inventory management system has been implemented, including support for multiple warehouses and picklists.  A number of management commands have been added to facilitate capacity management and to aid in adding new product in bulk.  Drill-down capability is now available on the admin site from warehouse to crate as well as a few other places.

# Requirements

Pyment requires Docker Engine 1.10.0+ and Docker Compose 1.6.0+.

# Standard workflow

## Production

The first step is to create or select a recipe.  The recipes all follow the same pattern:

1.  Pour some honey into a bucket.
2.  Pour some warm water into the bucket, and stir until uniform.
3.  Pour some cool water into the bucket, and stir until uniform.
4.  (Optional) Add some flavoring to the bucket.
5.  Take sample, and record observations.
6.  Pitch yeast.

The information stored in the app focuses on the ingredients.  For instance, multiple types of honey could be used for a particular recipe, or perhaps apple juice instead of water, or maybe some spices for flavor in the case of a metheglin.

The next step is to create a batch based on that recipe.  The values for the recipe will be copied into the batch where they can be modified when the mead is actually brewed.  If the batch's ingredients change significantly, a new recipe can be created.  The batch includes space for observations such as temperature, specific gravity, and tasting notes.  These observations will be useful for determining the strength of the mead and the flavor text for the labels among other factors.  As the batch progresses, it will be updated with samples from time to time.

Once the batch is bottled, the final modifications to the batch are made, including the number of jars created.  At this time, the labels can be printed and applied to the jars.  When the jars are labeled, a product can be created from the batch.  The jars can then be placed into the crates, and the database can be updated to reflect the new jars.  That's it!

## Consumption

The site works like a standard e-commerce site, where orders can be placed.  From the checkout admin site, the orders can be examined for errors.  If no errors are found, the orders should be processed into pick lists.  Pick lists identify specific jars in specific locations which must be retrieved to fulfill the order.  Once the entire pick list is completed, it must be marked as processed so the order will be marked delivered.

# Initial Configuration

Copy `pyment/settings.py` to `pyment/settings_local.py` and modify it to suit your environment.

Use the text editor of your choice to create a new file named `pyment/.env`.  The following is an example env file which includes all the required variables:

```
# DEBUG must be false for production
DEBUG=False

# Site-specific parameters
SITE_NAME='My Pyment Site'
META_KEYWORDS='mead, cyser, pyment, melomel, metheglin, braggot'
META_DESCRIPTION='This is my pyment site where I track the production, storage, and distribution of my home-brewed mead.'
BREWER_NAME='My Name'
BREWER_EMAIL='My Email'
BREWER_LOCATION='My Location'

# 1 is example.com 2 is production
SITE_ID=2

# Make this unique, and don't share it with anybody.
SECRET_KEY='NOPE'

# public file root
PUBLIC_ROOT=/web/pyment-site

# mail
EMAIL_URL='smtps://username@domain.org:password@mailhost:port'
EMAIL_SUBJECT_PREFIX='[Pyment] '

# hosts
USE_X_FORWARDED_HOST=True
ALLOWED_HOSTS=.example.org,
```

Modify the file to reflect your site's requirements.  Generate your own secret key for Django and use it in the file.  Sync the database and start the admin site.  Create flatpages for "about" and "contact".  This should be enough for the site itself to look right.

The cornerstone of the inventory model is the warehouse.  Each warehouse should contain at least one row.  Each row should contain at least one shelf.  Each shelf should contain at least one bin (a section of shelf set aside for one or more crates).  Using the admin site, create the warehouse first, then rows, then shelves, then bins.

The next step is to populate the meadery app.  The meadery app stores the ingredients and recipes as well as batches.  At least one recipe must be created as a basis for current and future batches and products.  For batches currently in progress, it may be easiest to create the batch on the meadery admin site and supply the relevant information retroactively.  Similarly, it may be easier to create existing products on the admin site.  However, if the data is available and time permits, it is best to start from recipes and work through products as in the standard workflow.

For each crate in your warehouse, create a crate in the admin site and assign it to a bin.  For each jar in that crate, create a jar in the admin site with the corresponding product data and assign it to that crate.  That's it!

Once all the mead has been entered into the database, take another tour of the site to ensure that everything works as you expect.

## Custom labels

Simple labels are created by default.  Custom labels can be produced by creating a file 'meadery\_local.py' in the meadery app which contains a 'generate\_labels(batch)' function, plus any supporting code.  If images are used on labels, they must be copied into the static directory and 'collectstatic' must be run.

# License

This software is released under the [MIT license](http://opensource.org/licenses/mit-license.php).
