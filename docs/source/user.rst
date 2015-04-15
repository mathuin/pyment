User's Guide
============

This document is designed to help the new user get acquainted with the
project.  The first section describes how to use the software, while
the remainder of the document breaks the software down into three
basic parts: production, storage, and distribution.

How to use the software
-----------------------

Throughout this section, there are references to two roles: the
producer and the consumer.  The producer is the person who administers
the software, while the consumer is the person who actually consumes
the mead.  Typically, these people are both the same person who also
made the mead in question.  However, each role performs different
actions in the distribution process.

.. note:: While the distribution software components are based on
          those found in traditional online storefronts, there is one
          key difference: there are no prices, as selling home-brewed
          mead is illegal in many jurisdictions.

Order placement
~~~~~~~~~~~~~~~

The order placement process is similar to that in any other store on
the web.

#. (Optional) Accounts can be created by consumers, including
   information such as email address and phone number.

#. The consumer selects a product, modifies the quantity if
   appropriate, and presses the "Add To Cart" button, repeating as
   necessary.

#. The consumer presses the "Checkout" button, possibly updates
   contact info, then presses the "Place Order" button.

This causes an order to be generated, and emails to be sent to the 
consumer and the producer.

Order fulfillment
~~~~~~~~~~~~~~~~~

#. The producer visits the relevant link in the email.  After
   confirming the validity of the order, the producer then presses the
   "Process order" button.  This marks the order as 'processed',
   generates a pick list and sends another email to the consumer.

#. The producer visits the pick list associated with the order.  After
   retrieving each jar identified in the pick list from the warehouse,
   the producer presses the "Process picklist" button.  This marks the
   picklist as 'processed', marks the order as 'delivered', and sends
   a final email to the consumer.

Individual orders and pick lists can also be modified and/or cancelled by
the producer.

Production
----------

.. warning:: It is essential to remember that there are many ways to
	     brew mead, and that this software was written to suit the
	     particular brewing :doc:`process <brewprocess>` used by
	     its author.  That being said, other brewers will likely
	     find this software useful, and :doc:`pull requests <dev>`
	     are cheerfully encouraged.

The software components associated with mead production are primarily
concentrated in the ``meadery`` app.

Ingredients
~~~~~~~~~~~

Ingredients are the raw components of the mead.  

There are four types of ingredients: 

* sugars (example: wildflower honey)
* solvents (example: spring water)
* flavors (example: bulk cinnamon)
* yeasts (example: Red Star champagne yeast)

Different types of information are stored for each type of ingredient:

* Specific gravity and specific heat (sugars and solvents)
* Cost per unit (all)
* "Natural" or not (all but yeast)
* Appellation (all but yeast)

Cost per unit is recorded per kilogram for sugars, per liter for
solvents, "other" for flavor, and per packet or vial for yeast.
"Natural" is defined as "does not contain added color, artificial
flavors or synthetic substances" for these purposes.  Appellation
describes the region from which the ingredient is sourced.

Recipes
~~~~~~~

Recipes are collections of ingredients, including the ingredient's
amount and (in the case of sugars and solvents) temperature as
appropriate.  The total cost of the batch can be calculated based on
the ingredients and their amounts.

Information for the ingredients is also used to determine the
appropriate BJCP category.  Here are some examples:

* A recipe with apple juice as the only solvent will be classified as
  a cyser.

* A recipe with spices as the only flavor will be classified as a
  metheglin.

* A recipe with apple juice *and* spices will be classified as an open
  category mead.

.. note:: These classifications are just recommendations.  If they are
          incorrect or incomplete, please submit :doc:`bug reports
          <bugfeature>` as appropriate.

Recipes also have titles and descriptions for organizational purposes
as well.

Batches
~~~~~~~

Batches are actual instantiations of recipes.  Sometimes brew day
doesn't go exactly as planned, so ingredient substitutions and other
changes are possible.  Additionally, samples are associated with
batches.

Like recipes, batches have titles and descriptions.  Unlike recipes,
batches also have names.  Batch names are composed of unique strings
representing brewing events and a batch letter indicating the sequence
in which the batch was brewed.  The author uses batch names like "SIP
26 C", where "SIP 26" represents the brewing event and "C" indicates
that this was the third batch brewed during that event.

.. note:: Any non-empty string can be used as an event identifier.

Products
~~~~~~~~

Products are batches which have been bottled.  Once the bottling is
complete, labels can be generated based on the product's ingredients
and other characteristics.  Products that have been labeled can be
entered into the inventory management system.

Product names, titles, and descriptions are all inherited from their
batches.  Product titles and descriptions are currently used for both
labels and distribution.

Samples
~~~~~~~

Samples are taken throughout the lifetime of the batch.  The following
information is collected for each sample:

* Temperature (in degrees Fahrenheit)
* Specific gravity
* Notes (traditionally used for sensory data)

These samples are used to calculate the percent alcohol of the mead,
and are convenient for storing information which can be referenced
when making labels.

Storage
-------

The software components associated with mead storage are primarily
concentrated in the ``inventory`` app.  The components are ordered
from largest to smallest.

Warehouse
~~~~~~~~~

A warehouse is a collection of rows of shelves.  Warehouses are
identified by a sequence number, and optionally a title.  An example
warehouse name would be "Warehouse 1".

Row
~~~

Shelves are ordered in rows.  Rows are identified by a sequence number
indicated on the row of shelves and the identifier of the warehouse
containing that row.  An example row name would be "Warehouse 1 Row
2".

Shelf
~~~~~

Shelves are identified by a sequence number indicated on the row of
shelves.  An example shelf name would be "Warehouse 1 Row 2 Shelf 3".
Shelves can be sections of floor -- in this case, the row would
contain only one shelf.

Bin
~~~

Bins are crate-sized portions of shelves -- if a shelf is long enough
to store three crates, then that shelf has three bins.  Bins are
identified by a sequence number indicated on the shelf, and the
identifier of the particular shelf.  An example bin name would be
"Warehouse 1 Row 2 Shelf 3 Bin 4".  If a shelf is tall enough to
support multiple crates vertically, then those bins can contain
multiple crates.

Crate
~~~~~

Jars are stored in crates.  These crates are identified by a sequence
number and should be included on its label.  An example crate name
would be "Crate 42".

Jar
~~~

The smallest unit of storage is the jar.  Batches become products as
they are bottled into jars.  Each jar is identified by the product it
contains and the sequence number it recieved when bottled.  This
information is traditionally included on its label.  An example jar
name would be "SIP 26 A10", where the product name is "SIP 26 A" and
the sequence number is "10".

Each jar has two flags associated with it:

* "is active", which is True when the jar is still in a warehouse
* "is available", which is True when the jar is available for distribution

.. note:: If the producer wishes to protect a jar from being
          distributed, they should use the admin interface to set that
          jar's "is available" flag to False.

Distribution
------------

The software components associated with mead distribution are found in
both the ``meadery`` app and the ``checkout`` app.

Product review
~~~~~~~~~~~~~~

Each product can have product reviews.  These reviews have the
following attributes:

* Title, describing the review
* Rating, from 1 (fair) to 5 (outstanding)
* Notes

Order
~~~~~

Orders are collections of products with amounts.  They are generated
by consumers using the front end of the project.  They can have
accounts as owners or can be anonymous.

Pick list
~~~~~~~~~

A "pick list" is a collection of jars generated from an order.  The
pick list includes the location (crate and bin) of each jar to
facilitate its retrieval.

