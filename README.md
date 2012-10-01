# Welcome to Pyment!

Pyment is a website that tracks the production, storage, and distribution of my home-brewed mead.

Pyment was written in Python using the Django framework. The distribution portion of the website (the catalog, the shopping cart, and other associated code) is based heavily upon the example site from "Beginning Django E-Commerce" by Jim McGaw.

Please note that this code is in the pre-alpha state!  The database schemas and models and views and everything else are subject to change without notice.  When the code settles down, I will modify the documentation to reflect any increase in stability.  Additionally, there are a number of design decisions that I have made to support my specific environment: many jars of mead stored in multiple locations brewed during regularly-scheduled brewing events with multiple batches per event.  Feel free to modify the code to match your particular needs -- I am especially interested in pull requests that improve the look and feel of the site!

# Requirements

Pyment is my first experience with virtualenv.  I have created a requirements.txt file from the output of 'pip freeze' which should be enough to recreate my environment.  Please let me know if anything is missing!

# Initial Configuration

Copy pyment/settings-stock.py to pyment/settings.py and modify it to suit your environment.

Sync the database and start the admin site.  Create flatpages for "about" and "contact".  This should be enough for the site itself to look right.

The cornerstone of the inventory model is the warehouse.  Each warehouse should contain at least one row.  Each row should contain at least one shelf.  Each shelf should contain at least one bin (a section of shelf set aside for one or more crates).  Using the admin site, create the warehouse first, then rows, then shelves, then bins.

The catalog is based on two models: category and product.  The categories are designed around those in the [Beer Judge Certification Program](http://www.bjcp.org/) but need to be populated.  Products have a variety of specific identifying characteristics which may need to be modified to suit your environment.  Again using the admin site, create the categories and then the products.

For each crate in your warehouse, create a crate in the admin site and assign it to a bin.  For each jar in that crate, create a jar in the admin site with the corresponding product data and assign it to that crate.  That's it!

Once all the mead has been entered into the database, take another tour of the site to ensure that everything works as you expect.

# Work still to be done

The checkout app has been added and appears to work well.  Orders are created which are visible in the admin site.  The next step I think is to create picklists.  The order states will be redone -- "Submitted", "Approved", "Picked", "Completed" and "Cancelled".  When an order is changed from "Submitted" to "Approved", a picklist will be created.  The picklist model will be in the inventory app, and will be a list of the exact jars that correspond to the order items, complete with location in the warehouse(s).  When jars are placed on a picklist, their "is_active" flag will be set to False so they do not show up as "in stock" in the catalog.  If the order is set to "Cancelled", the flags will be set back to True.  I'm not yet sure what to do if the order is set to "Completed".  For now, nothing, I guess.

The user profile app has been added and it also appears to work well.  It can track past orders by account, so I will consider using it instead of the picklist jar reassignment bit depending on how the rest of the book turns out.

The inventory app needs to be beefed up.  It will have to support the picklists mentioned above as well as common tasks like crate consolidation, location of all jars of a particular product, and the like.

The meadery app needs to be written.  It will keep track of recipes past and present and document the differences between theory and practice as well as track the buckets and carboys and create jars at bottling time.

# License

This software is released under the [MIT license](http://opensource.org/licenses/mit-license.php).



